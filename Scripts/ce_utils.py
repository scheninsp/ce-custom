"""提供 Cheat Engine 单步脚本共用功能。"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from ce_mcp_client import McpClient
from opcode_report import atomic_text

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GATEWAY = ROOT / "McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64/CheatEngine.Mcp.Gateway.exe"
DEFAULT_OUTPUT = ROOT / "Output"


class CaptureError(RuntimeError):
    """表示 CE 实例选择或单步工具合同无效。"""


def now():
    """获取 UTC 时间；无参数，返回 ISO 8601 时间文本。"""
    return datetime.now(timezone.utc).isoformat()


def validate_step_tool(catalog, mode):
    """确认单步工具支持指定模式；参数为工具目录和模式，返回工具定义。"""
    tool = catalog.get("debugger_step") if isinstance(catalog, dict) else None
    if not isinstance(tool, dict):
        raise CaptureError("debugger_step tool is unavailable")
    properties = tool.get("inputSchema", {}).get("properties", {})
    modes = properties.get("mode", {}).get("enum", [])
    if "instanceId" not in properties or mode not in modes:
        raise CaptureError(f"debugger_step does not support the required {mode} mode")
    return tool


def select_instance(client, requested_id=None):
    """选择 CE 实例；参数为 MCP 客户端和可选实例 ID，返回唯一实例 ID。"""
    instances = client.call("instance_list", {}).get("instances")
    if not isinstance(instances, list):
        raise CaptureError("invalid CE instance listing")
    instance_ids = [item.get("instanceId") for item in instances
                    if isinstance(item, dict) and isinstance(item.get("instanceId"), str)]
    if requested_id:
        if requested_id not in instance_ids:
            raise CaptureError("requested CE instance was not found")
        return requested_id
    if len(instance_ids) != 1:
        raise CaptureError("select exactly one CE instance or pass --instance-id")
    return instance_ids[0]


def render_report(report):
    """渲染 Markdown/JSON 报告；参数为报告字典，返回完整文本。"""
    title = "Debugger Step " + report["mode"].title()
    return f"# {title}\n\n```json\n" + json.dumps(report, ensure_ascii=False, indent=2) + "\n```\n"


def write_report(path, report):
    """原子写入单步报告；参数为报告路径和报告字典，无返回值。"""
    atomic_text(path, render_report(report))


def run_capture(argv, mode, description, client_factory=McpClient, allow_mode=False):
    """执行一次指定类型的单步；参数为参数列表、模式、描述和客户端工厂，返回进程退出码。"""
    parser = argparse.ArgumentParser(description=description)
    if allow_mode:
        parser.add_argument("--mode", choices=("over", "into"), default=mode)
    parser.add_argument("--gateway", type=Path, default=DEFAULT_GATEWAY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-output", action="store_true", help="Do not write the report or gateway stderr log")
    parser.add_argument("--instance-id")
    parser.add_argument("--timeout", type=float, default=30)
    args = parser.parse_args(argv)
    actual_mode = args.mode if allow_mode else mode
    report = {"startedAt": now(), "mode": actual_mode, "stepCallStarted": False}
    client = None
    exit_code = 2
    try:
        stderr_path = None if args.no_output else args.output / "step_capture_gateway.stderr.log"
        client = client_factory([str(args.gateway)], args.timeout, stderr_path).start()
        validate_step_tool(client.tools(), actual_mode)
        instance_id = select_instance(client, args.instance_id)
        report["instanceId"] = instance_id
        report["stepCallStarted"] = True
        report["stepResponse"] = client.call("debugger_step", {"instanceId": instance_id, "mode": actual_mode})
        report["stepResponseReceived"] = True
        exit_code = 0
    except KeyboardInterrupt:
        report["error"] = "interrupted by user"
        exit_code = 130 if report["stepCallStarted"] else 2
    except BaseException as exc:
        report["error"] = str(exc)
        report["stepResponseReceived"] = False if report["stepCallStarted"] else None
        exit_code = 3 if report["stepCallStarted"] else 2
    finally:
        report["finishedAt"] = now()
        if client is not None:
            try:
                client.close()
                report["gatewayClosed"] = True
            except Exception as exc:
                report["gatewayClosed"] = False
                report["gatewayCloseError"] = str(exc)
                exit_code = 3 if report["stepCallStarted"] else 2
        if not args.no_output:
            try:
                args.output.mkdir(parents=True, exist_ok=True)
                write_report(args.output / "step_capture.md", report)
            except Exception as exc:
                report["reportWriteError"] = str(exc)
                exit_code = 3 if report["stepCallStarted"] else 2
    if exit_code != 0:
        error = report.get("error") or report.get("gatewayCloseError") or report.get("reportWriteError")
        if error:
            print("ERROR: " + str(error), file=sys.stderr)
    return exit_code
