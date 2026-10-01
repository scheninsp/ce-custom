import argparse
import json
import sys
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from ce_mcp_client import McpClient, ToolError, TransportError
from opcode_report import (
    Target, atomic_text, hex_address, hex_bytes, md, render_target,
    validate_anchor, validate_window,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATEWAY = (
    ROOT / "McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe"
)
# 目标地址与原始机器码（地址, expected_bytes）。由用户手动维护，来源为本次报告
# Docs/testdata-2026-10-1-10-58.md；游戏重启后地址失效时，重新采集报告并手动更新本列表。
TARGETS = [
    ("7FF777D19218", "496385581D0000"),
    ("7FF777D1B9C7", "8986581D0000"),
    ("7FF777D1BA8E", "442BBE581D0000"),
    ("7FF777927334", "486390581D0000"),
    ("7FF777CED5C9", "418B86581D0000"),
    ("7FF777D01346", "486387581D0000"),
    ("7FF777D1B9DA", "89865C1D0000"),
    ("7FF777CED5BB", "418B865C1D0000"),
    ("7FF777927358", "2B905C1D0000"),
]
REQUIRED_TOOLS = {
    "instance_list": set(),
    "runtime_get_info": {"instanceId"},
    "runtime_get_overview": {"instanceId"},
    "code_decode": {"instanceId", "address"},
    "code_disassemble": {"instanceId", "address", "before", "count"},
}
# 只读工具白名单：脚本只允许调用这些工具，集成测试断言真实调用集合是其子集。
READ_ONLY_TOOLS = frozenset({
    "instance_list", "runtime_get_info", "runtime_get_overview",
    "code_decode", "code_disassemble",
})
SESSION_ERRORS = {"target_changed", "not_attached", "stopping", "invalid_state"}


class SessionChanged(RuntimeError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def process_name(value) -> str:
    return (value or "").replace("\\", "/").rsplit("/", 1)[-1].casefold().removesuffix(".exe")


def fingerprint(overview: dict) -> dict:
    process = overview["process"]
    if not process["isOpen"] or process_name(process.get("processName")) != "victoria3":
        raise SessionChanged("victoria3 is not the selected process")
    if process.get("pointerSize") != 8 or process.get("selectionEpoch") is None:
        raise SessionChanged("target bitness or selection identity is unavailable")
    return {
        "runtimeEpoch": overview["runtime"]["epoch"],
        "processId": process["processId"],
        "selectionEpoch": process["selectionEpoch"],
        "pointerSize": process["pointerSize"],
    }


def resources(overview: dict) -> dict:
    # 只读工具不会产生 CE 资源；仅记录计数用于运行期残留核对。
    return {"resourceCount": overview["resourceCount"], "jobCount": overview["jobCount"]}


def load_targets() -> list[Target]:
    # 在连接 CE 前校验固化列表；非法条目以 ValueError 失败，不接触 CE。
    targets = [Target(hex_address(address), hex_bytes(expected)) for address, expected in TARGETS]
    if not targets:
        raise ValueError("TARGETS list is empty")
    if len({target.address for target in targets}) != len(targets):
        raise ValueError("duplicate address in TARGETS list")
    return sorted(targets, key=lambda target: int(target.address, 16))


def select_instance(client, wanted):
    listing = client.call("instance_list", {})
    if listing["discoveryIncomplete"]:
        raise ValueError("instance discovery incomplete; run again")
    items = listing["instances"]
    if wanted is not None:
        items = [item for item in items if item["instanceId"] == wanted]
    if len(items) != 1:
        raise ValueError("select exactly one CE instance with --instance-id")
    return items[0]["instanceId"]


def bind_target(client, instance_id):
    # CE 已由用户手动附加：这里只做健康检查，不附加、不切换、不分离。
    arguments = {"instanceId": instance_id}
    client.call("runtime_get_info", arguments)
    overview = client.call("runtime_get_overview", arguments)
    process = overview["process"]
    if not process["isOpen"]:
        raise ValueError("victoria3.exe is not attached in CE; attach it manually in Cheat Engine first")
    if process_name(process.get("processName")) != "victoria3":
        raise ValueError("CE is attached to a different target; the script does not switch targets")
    return fingerprint(overview), resources(overview)


def check_session(client, instance_id, baseline):
    current = fingerprint(client.call("runtime_get_overview", {"instanceId": instance_id}))
    if current != baseline:
        raise SessionChanged("CE runtime or target selection changed")


def check_residue(client, instance_id, metadata, interrupted):
    # 统一收尾残留核对：至多执行一次 overview 读取，从不重连，恒返回结构化结果供 manifest 落盘。
    # state：unchanged=计数一致；changed=计数变化；unavailable=尝试核对但失败；skipped=未执行（原因见 reason）。
    result = {
        "state": "skipped", "before": metadata.get("ceResourcesBefore"),
        "after": None, "checkedAt": now(), "reason": None,
    }
    if result["before"] is None:
        result["reason"] = "no resource baseline was established"
        return result
    if client is None:
        result["reason"] = "MCP client was not started"
        return result
    if client.broken:
        result["reason"] = "MCP connection is unusable"
        return result
    if interrupted:
        # 中断可能打断在途请求；复用同一连接不安全：不重连、不阻塞，只记录跳过原因。
        result["reason"] = "interrupted by user"
        return result
    try:
        result["after"] = resources(client.call("runtime_get_overview", {"instanceId": instance_id}))
    except (TransportError, ToolError) as exc:
        result.update(state="unavailable", reason=ascii(str(exc)))
        return result
    except KeyboardInterrupt:
        # 核对期间再次中断：记录不可确认后立即交给收尾清理。
        result.update(state="unavailable", reason="interrupted during residue check")
        return result
    if result["after"] == result["before"]:
        result["state"] = "unchanged"
    else:
        result["state"] = "changed"
        result["reason"] = "read-only tools cannot create CE resources; verify manually"
        print("WARN: CE resourceCount/jobCount changed during export")
    return result


def save_progress(output, metadata, records, status):
    success = sum(record["status"] == "success" for record in records)
    document = {
        **metadata, "status": status, "updatedAt": now(),
        "successCount": success, "failedCount": len(records) - success,
        "processedCount": len(records), "instructionCount": success * 201,
        "results": records,
    }
    atomic_text(output / "manifest.json", json.dumps(document, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# Opcode export index", "",
        f"- Run: {metadata['runId']}", f"- Status: {status}",
        f"- Expected: {metadata['expectedCount']}; success: {success}; failed: {len(records) - success}",
        "", "| Target | Status | File | Error |", "| --- | --- | --- | --- |",
    ]
    for record in records:
        filename = record["file"]
        lines.append(
            f"| {record['address']} | {record['status']} | "
            f"[{filename}]({filename}) | {md(record.get('error', ''))} |"
        )
    atomic_text(output / "index.md", "\n".join(lines) + "\n")


def run_exports(client, instance_id, baseline, targets, output, metadata):
    records, aborted = [], None
    for target in targets:
        rows = []
        record = {
            **asdict(target), "file": f"opcode_{target.address}.md",
            "status": "failed", "capturedAt": now(),
            "beforeCount": 0, "afterCount": 0, "instructionCount": 0,
        }
        try:
            if aborted is not None:
                raise SessionChanged("not attempted after abort: " + aborted)
            check_session(client, instance_id, baseline)
            arguments = {"instanceId": instance_id, "address": target.address}
            validate_anchor(target, client.call("code_decode", arguments))
            payload = client.call("code_disassemble", {
                **arguments, "before": 100, "count": 101,
            })
            rows = validate_window(target, payload)
            validate_anchor(target, client.call("code_decode", arguments))
            check_session(client, instance_id, baseline)
            record.update(status="success", beforeCount=100, afterCount=100, instructionCount=201)
        except (TransportError, SessionChanged) as exc:
            if aborted is None:
                aborted = str(exc)
            record["error"] = str(exc)
        except ToolError as exc:
            record["error"] = str(exc)
            if exc.kind in SESSION_ERRORS:
                aborted = str(exc)
        except (ValueError, KeyError, TypeError) as exc:
            record["error"] = "invalid opcode result: " + str(exc)
        record["capturedAt"] = now()
        atomic_text(output / record["file"], render_target(target, record, rows, metadata))
        records.append(record)
        save_progress(output, metadata, records, "running")
        print(f"INFO: {target.address} {record['status']}")
    # 残留核对不在此处执行：统一收尾（main）覆盖成功、失败与中断等全部退出路径，且恰好执行一次。
    failed = any(record["status"] != "success" for record in records)
    status = "aborted" if aborted else ("failed" if failed else "complete")
    save_progress(output, metadata, records, status)
    return 3 if aborted else (1 if failed else 0)


def positive_int(text):
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export CE opcode windows through MCP")
    parser.add_argument("--output", type=Path, default=ROOT / "Output/opcodes")
    parser.add_argument("--gateway", type=Path, default=DEFAULT_GATEWAY)
    parser.add_argument("--instance-id")
    parser.add_argument("--timeout", type=positive_int, default=30)
    args = parser.parse_args(argv)
    client, output, metadata, instance_id = None, None, None, None
    code, reason = 0, None
    try:
        # 先校验固化列表格式；失败时不创建运行目录、不接触 CE。
        targets = load_targets()
        gateway = args.gateway.resolve()
        if not gateway.is_file():
            raise ValueError("gateway executable does not exist")
        run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + "_" + uuid.uuid4().hex[:8]
        output = args.output.resolve() / run_id
        output.mkdir(parents=True, exist_ok=False)
        metadata = {
            "runId": run_id, "startedAt": now(), "expectedCount": len(targets),
            "before": 100, "after": 100,
        }
        save_progress(output, metadata, [], "starting")
        # 先保存客户端对象再启动：启动阶段失败或中断时，finally 仍能回收本次 Gateway。
        client = McpClient([str(gateway)], args.timeout, output / "gateway.stderr.log")
        client.start()
        catalog = client.tools()
        for name, properties in REQUIRED_TOOLS.items():
            if name not in catalog:
                raise ValueError("required MCP tool is missing: " + name)
            available = set(catalog[name]["inputSchema"].get("properties", {}))
            if not properties <= available:
                raise ValueError("incompatible MCP tool schema: " + name)
        instance_id = select_instance(client, args.instance_id)
        baseline, resources_before = bind_target(client, instance_id)
        # 记录 CE 资源基线，供统一收尾中的残留核对使用。
        metadata.update(instanceId=instance_id, ceResourcesBefore=resources_before, **baseline)
        code = run_exports(client, instance_id, baseline, targets, output, metadata)
        print("INFO: output directory " + ascii(str(output)))
    except KeyboardInterrupt:
        code, reason = 130, "interrupted by user"
    except (TransportError, SessionChanged) as exc:
        code, reason = 3, str(exc)
    except (OSError, ValueError, ToolError, KeyError, TypeError) as exc:
        code, reason = 2, str(exc)
    finally:
        # 统一收尾：所有退出路径都在关闭客户端之前执行一次残留核对；核对不得覆盖原始退出码。
        residue = None
        try:
            if metadata is not None:
                residue = check_residue(client, instance_id, metadata, interrupted=(code == 130))
        except BaseException as exc:
            # 收尾自身异常（含再次 Ctrl+C）只记录不可确认状态，不覆盖原始退出原因。
            residue = {
                "state": "unavailable", "before": metadata.get("ceResourcesBefore"),
                "after": None, "checkedAt": now(),
                "reason": "residue check crashed: " + ascii(str(exc)),
            }
            print("ERROR: residue check failed: " + ascii(str(exc)), file=sys.stderr)
        if metadata is not None:
            metadata["residueCheck"] = residue
            if code == 0 and residue["state"] == "unavailable":
                # 数据已完整导出但残留无法确认：不以 0 结束，按传输失效语义返回 3，不重连。
                code = 3
                print("ERROR: residue check could not be completed; CE resources are unverified",
                      file=sys.stderr)
        if client is not None:
            client.close()
    if reason is not None:
        print("ERROR: export stopped: " + ascii(reason), file=sys.stderr)
    if output is not None and metadata is not None:
        try:
            # 保留已有逐地址结果，并入统一收尾的残留核对结果；失败路径同时更新失败状态。
            path = output / "manifest.json"
            saved = json.loads(path.read_text(encoding="utf-8")) if path.exists() else metadata
            saved["residueCheck"] = metadata["residueCheck"]
            if reason is not None:
                saved.update(status="interrupted" if code == 130 else "aborted", error=reason)
            saved["updatedAt"] = now()
            atomic_text(path, json.dumps(saved, ensure_ascii=False, indent=2) + "\n")
            save_progress(output, saved, saved.get("results", []), saved["status"])
        except (OSError, ValueError):
            print("ERROR: unable to persist final run status", file=sys.stderr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
