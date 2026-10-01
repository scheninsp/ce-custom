import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ce_mcp_client import ToolError, TransportError
from opcode_report import Target, atomic_text
from run_opcode_export import (
    READ_ONLY_TOOLS, TARGETS, bind_target, check_residue, load_targets, main,
    run_exports, select_instance,
)
from test_opcode_report import window

# 固化列表的测试内独立副本：与 run_opcode_export.TARGETS 不一致即视为误改。
EXPECTED = [
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


class FakeMcp:
    def __init__(self):
        self.calls = []
        self.broken = False
        self.open = True
        self.pid = 42
        self.name = "victoria3"
        self.epoch = 1
        self.fail = None
        self.timeout = None
        self.change = None
        self.stale = None
        self.interrupt = None
        self.overview_calls = 0
        self.overview_fail_at = None
        self.resource_change_at = None
        self.instances = [{"instanceId": "ce-test"}]
        self.resources = {"resourceCount": 0, "jobCount": 0}

    def tools(self):
        properties = {"instanceId": {}, "address": {}, "before": {}, "count": {}}
        return {
            name: {"inputSchema": {"properties": dict(properties)}}
            for name in READ_ONLY_TOOLS
        }

    def overview(self):
        self.overview_calls += 1
        if self.overview_fail_at == self.overview_calls:
            self.broken = True  # 模拟真实客户端：传输超时后连接失效。
            raise TransportError("MCP request timed out")
        if self.resource_change_at == self.overview_calls:
            self.resources = {"resourceCount": 1, "jobCount": 0}
        return {
            "runtime": {"epoch": 1},
            "process": {
                "isOpen": self.open, "processId": self.pid, "processName": self.name,
                "pointerSize": 8, "selectionEpoch": self.epoch,
            },
            "resourceCount": self.resources["resourceCount"],
            "jobCount": self.resources["jobCount"],
        }

    def call(self, name, arguments):
        self.calls.append((name, dict(arguments)))
        if name == "instance_list":
            return {"instances": self.instances, "discoveryIncomplete": False}
        if name == "runtime_get_info":
            return {}
        if name == "runtime_get_overview":
            return self.overview()
        if self.interrupt is not None and arguments.get("address") == self.interrupt:
            raise KeyboardInterrupt()
        address = arguments["address"]
        if name == "code_decode":
            row = window(address)["instructions"][100]
            if address == self.stale:
                row["bytes"] = "CC"
            return {"instruction": row, "length": 1}
        if name == "code_disassemble":
            assert arguments["before"] == 100 and arguments["count"] == 101
            if address == self.timeout:
                self.broken = True
                raise TransportError("MCP request timed out")
            if address == self.fail:
                raise ToolError({"error": {"kind": "memory_read_failed", "message": "unreadable"}})
            if address == self.change:
                self.epoch += 1
            return window(address)
        raise AssertionError("unexpected tool: " + name)


class Starter:
    # 替代 run_opcode_export.McpClient：把假客户端接入完整 main 流程，并记录启动/关闭。
    def __init__(self, client):
        self.client = client
        self.started = False
        self.closed = False

    @property
    def broken(self):
        return self.client.broken

    def start(self):
        self.started = True
        return self

    def tools(self):
        return self.client.tools()

    def call(self, name, arguments):
        return self.client.call(name, arguments)

    def close(self):
        self.closed = True


class FakePipe:
    # 仅在启动中断测试中替代真实管道：记录关闭调用，不启动真实进程。
    def __init__(self):
        self.closed = False

    def write(self, text):
        pass

    def flush(self):
        pass

    def close(self):
        self.closed = True

    def __iter__(self):
        return iter(())


class FakeGatewayProcess:
    def __init__(self):
        self.stdin = FakePipe()
        self.stdout = FakePipe()
        self.wait_calls = 0
        self.terminate_calls = 0
        self.kill_calls = 0

    def wait(self, timeout=None):
        self.wait_calls += 1
        return 0

    def terminate(self):
        self.terminate_calls += 1

    def kill(self):
        self.kill_calls += 1
        return None


class ExportTests(unittest.TestCase):
    def export(self, client):
        baseline, resources_before = bind_target(client, "ce-test")
        targets = [Target("1064", "90"), Target("2064", "90")]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            metadata = {
                "runId": "test-run", "instanceId": "ce-test", "processId": 42,
                "expectedCount": 2, "ceResourcesBefore": resources_before,
            }
            code = run_exports(client, "ce-test", baseline, targets, output, metadata)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            files = {p.name: p.read_text(encoding="utf-8") for p in output.glob("opcode_*.md")}
            self.assertEqual(len(files), 2)
            self.assertEqual(list(output.glob("*.tmp")), [])
            return code, manifest, files

    def run_main(self, client, targets=(("1064", "90"),)):
        # 以假客户端走完整 main：统一收尾、manifest 与退出码都在覆盖范围内。
        starter = Starter(client)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            gateway = root / "gateway.exe"
            gateway.write_text("fake", encoding="utf-8")
            with patch("run_opcode_export.McpClient", return_value=starter), \
                    patch("run_opcode_export.TARGETS", list(targets)):
                code = main(["--gateway", str(gateway), "--output", str(root / "out")])
            manifests = list((root / "out").glob("*/manifest.json"))
            self.assertEqual(len(manifests), 1)
            manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
        return code, manifest, starter

    def test_fixed_target_list_matches_report(self):
        self.assertEqual(list(TARGETS), EXPECTED)
        targets = load_targets()
        self.assertEqual(len(targets), 9)
        self.assertEqual({t.address for t in targets}, {a for a, _ in EXPECTED})
        self.assertEqual(
            next(t.expected_bytes for t in targets if t.address == "7FF777D19218"),
            "496385581D0000",
        )

    def test_invalid_fixed_list_rejected_before_ce(self):
        for invalid in ([], [("ZZZZ", "90")], [("1064", "90"), ("1064", "90")]):
            with self.subTest(invalid=invalid), patch("run_opcode_export.TARGETS", invalid):
                with self.assertRaises(ValueError):
                    load_targets()

    def test_success(self):
        code, result, files = self.export(FakeMcp())
        self.assertEqual(code, 0)
        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["instructionCount"], 402)
        self.assertEqual(result["successCount"], 2)
        for text in files.values():
            self.assertEqual(text.count("| TARGET |"), 1)
            self.assertEqual(sum(line.startswith("| ") for line in text.splitlines()), 203)
            self.assertIn("CE estimated predecessors", text)
            self.assertNotIn("## Sources", text)

    def test_one_bad_address_does_not_block_next(self):
        client = FakeMcp()
        client.fail = "1064"
        code, result, files = self.export(client)
        self.assertEqual(code, 1)
        self.assertEqual(result["successCount"], 1)
        self.assertNotIn("## Instructions", files["opcode_1064.md"])
        self.assertIn("## Instructions", files["opcode_2064.md"])

    def test_stale_bytes_skip_window_call(self):
        client = FakeMcp()
        client.stale = "1064"
        code, result, _ = self.export(client)
        self.assertEqual(code, 1)
        self.assertEqual(result["successCount"], 1)
        self.assertFalse(any(
            name == "code_disassemble" and args["address"] == "1064"
            for name, args in client.calls
        ))

    def test_transport_and_session_abort_remaining_reads(self):
        for field in ("timeout", "change"):
            client = FakeMcp()
            setattr(client, field, "1064")
            code, result, _ = self.export(client)
            self.assertEqual(code, 3)
            self.assertEqual(result["status"], "aborted")
            self.assertEqual(result["successCount"], 0)
            self.assertFalse(any(args.get("address") == "2064" for _, args in client.calls))

    def test_manual_attach_is_required(self):
        client = FakeMcp()
        client.open = False
        with self.assertRaises(ValueError) as caught:
            bind_target(client, "ce-test")
        self.assertIn("attach it manually", str(caught.exception))
        self.assertFalse(any(name == "process_attach" for name, _ in client.calls))
        client.open = True
        baseline, resources_before = bind_target(client, "ce-test")
        self.assertEqual(baseline["processId"], 42)
        self.assertEqual(resources_before, {"resourceCount": 0, "jobCount": 0})

    def test_other_target_is_not_switched(self):
        client = FakeMcp()
        client.name = "notepad.exe"
        with self.assertRaises(ValueError):
            bind_target(client, "ce-test")
        client.name = "victoria3.exe"
        self.assertEqual(bind_target(client, "ce-test")[0]["processId"], 42)
        self.assertFalse(any(name in ("process_attach", "process_list") for name, _ in client.calls))

    def test_multiple_instances_require_selection(self):
        client = FakeMcp()
        client.instances.append({"instanceId": "ce-second"})
        with self.assertRaises(ValueError):
            select_instance(client, None)
        self.assertEqual(select_instance(client, "ce-second"), "ce-second")

    def test_success_calls_stay_read_only(self):
        client = FakeMcp()
        code, _, _ = self.export(client)
        self.assertEqual(code, 0)
        self.assertTrue(client.calls)
        self.assertLessEqual({name for name, _ in client.calls}, set(READ_ONLY_TOOLS))

    def test_resource_change_reports_changed_state(self):
        client = FakeMcp()
        client.resources = {"resourceCount": 1, "jobCount": 0}
        check = check_residue(client, "ce-test", {
            "ceResourcesBefore": {"resourceCount": 0, "jobCount": 0},
        }, interrupted=False)
        self.assertEqual(check["state"], "changed")
        self.assertEqual(check["after"], {"resourceCount": 1, "jobCount": 0})

    def test_success_records_unchanged_residue(self):
        client = FakeMcp()
        code, manifest, starter = self.run_main(client)
        self.assertEqual(code, 0)
        self.assertEqual(manifest["status"], "complete")
        check = manifest["residueCheck"]
        self.assertEqual(check["state"], "unchanged")
        self.assertEqual(check["before"], check["after"])
        self.assertEqual(client.overview_calls, 4)
        self.assertTrue(starter.started and starter.closed)

    def test_final_overview_failure_is_unavailable_and_exit_3(self):
        client = FakeMcp()
        client.overview_fail_at = 4
        buffer = io.StringIO()
        with contextlib.redirect_stderr(buffer):
            code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 3)
        self.assertEqual(manifest["status"], "complete")
        self.assertEqual(manifest["residueCheck"]["state"], "unavailable")
        self.assertIsNone(manifest["residueCheck"]["after"])
        self.assertIn("residue check could not be completed", buffer.getvalue())

    def test_write_failure_still_checks_residue(self):
        client = FakeMcp()
        original = atomic_text

        def failing(path, text):
            if path.name.startswith("opcode_"):
                raise PermissionError("denied")
            return original(path, text)

        with patch("run_opcode_export.atomic_text", side_effect=failing):
            code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 2)
        self.assertEqual(manifest["status"], "aborted")
        self.assertEqual(manifest["residueCheck"]["state"], "unchanged")
        self.assertEqual(client.overview_calls, 4)

    def test_interrupt_skips_check_without_extra_rpc(self):
        client = FakeMcp()
        client.interrupt = "1064"
        code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 130)
        self.assertEqual(manifest["status"], "interrupted")
        self.assertEqual(manifest["residueCheck"]["state"], "skipped")
        self.assertEqual(manifest["residueCheck"]["reason"], "interrupted by user")
        self.assertEqual(client.overview_calls, 2)

    def test_transport_failure_records_skipped(self):
        client = FakeMcp()
        client.timeout = "1064"
        code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 3)
        self.assertEqual(manifest["status"], "aborted")
        self.assertEqual(manifest["residueCheck"]["state"], "skipped")
        self.assertEqual(manifest["residueCheck"]["reason"], "MCP connection is unusable")

    def test_missing_baseline_records_skipped(self):
        client = FakeMcp()
        client.open = False
        code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 2)
        self.assertEqual(manifest["residueCheck"]["state"], "skipped")
        self.assertEqual(
            manifest["residueCheck"]["reason"], "no resource baseline was established")

    def test_resource_change_warns_and_still_exits_0(self):
        client = FakeMcp()
        client.resource_change_at = 4
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code, manifest, _ = self.run_main(client)
        self.assertEqual(code, 0)
        check = manifest["residueCheck"]
        self.assertEqual(check["state"], "changed")
        self.assertEqual(check["after"], {"resourceCount": 1, "jobCount": 0})
        self.assertIn("WARN: CE resourceCount/jobCount changed", buffer.getvalue())

    def test_interrupt_during_start_reclaims_gateway(self):
        # 初始化握手期间 Ctrl+C：main 仍须回收本次启动的 Gateway 子进程。
        fake = FakeGatewayProcess()
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
            root = Path(directory)
            gateway = root / "gateway.exe"
            gateway.write_text("fake", encoding="utf-8")
            with patch("ce_mcp_client.subprocess.Popen", return_value=fake), \
                    patch("ce_mcp_client.McpClient.rpc", side_effect=KeyboardInterrupt):
                code = main(["--gateway", str(gateway), "--output", str(root / "out")])
            self.assertEqual(code, 130)
            self.assertTrue(fake.stdin.closed, "gateway stdin pipe was not closed")
            self.assertEqual(fake.kill_calls, 0)
            self.assertGreater(fake.wait_calls + fake.terminate_calls, 0,
                               "gateway child process was never waited for or terminated")
            manifest = json.loads(
                next((root / "out").glob("*/manifest.json")).read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "interrupted")


if __name__ == "__main__":
    unittest.main()
