"""离线验证断点寄存器采集的只读合同、结构校验、退出码与原子写入清理。"""

import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import get_stacktrace_register_at_breakpoint as capture
from ce_mcp_client import ToolError, TransportError


class FakeMcp:
    def __init__(self):
        """初始化独立假现场；无参数和返回值，不连接真实 CE。"""
        self.calls = []
        self.closed = False
        self.broken = False
        self.failures = {}
        self.counts = {}
        self.catalog = {
            name: {"inputSchema": {"properties": {
                "instanceId": {"type": "string"},
                "includeExtraRegisters": {"type": "boolean"}, "depth": {"type": "integer"},
            }}} for name in capture.READ_ONLY_TOOLS
        }
        self.listing = {"discoveryIncomplete": False, "instances": [{"instanceId": "ce-test"}]}
        self.info = {"epoch": 9, "pluginVersion": "2.0.0-beta.2"}
        self.overview = {
            "runtime": dict(self.info),
            "process": {"isOpen": True, "processId": 123, "processName": "test.exe",
                        "pointerSize": 8, "selectionEpoch": 1},
            "resourceCount": 0, "jobCount": 0,
        }
        self.status = {"stateValid": True, "attached": True, "broken": True,
                       "activeInterface": "veh", "canBreak": False,
                       "reportedBroken": True, "stepping": False}
        self.context = {
            "is64Bit": True, "includesExtraRegisters": True,
            "registers": {"RIP": "00007FF012345678", "RSP": "1000", "RBP": "1100",
                          "RAX": "AB", "EFLAGS": "202", "FP0": "00 01 02 03 04 05 06 07 08 09",
                          "XMM0": "00 11 22 33 44 55 66 77 88 99 AA BB CC DD EE FF"},
        }
        self.stack = {"stackPointer": "1000", "pointerSize": 8, "scannedSlots": 128,
                      "frames": [{"stackAddress": "1000", "returnAddress": "7FF011112222",
                                  "callInstruction": "call test.exe+1234", "isHeuristic": True},
                                 {"stackAddress": "1020", "returnAddress": "7FF022223333",
                                  "callInstruction": "call rax", "isHeuristic": True}]}
        self.final_status = None
        self.final_overview = None
        self.final_context = None
        self.native_response = None
        self.compat_response = {"ok": True, "hostEffect": "completed", "droppedOpaqueCount": 0,
                                "returnValues": [{"stateValid": True, "attached": True, "broken": True,
                                                  "activeInterface": "windows", "is64Bit": True,
                                                  "instructionPointer": "7FF012345678", "stackPointer": "1000"}]}
        self.final_compat_response = None

    def event(self, name):
        """注入指定调用故障；参数为事件名，无返回值。"""
        self.counts[name] = self.counts.get(name, 0) + 1
        failure = self.failures.get((name, self.counts[name]))
        if failure is not None:
            if isinstance(failure, TransportError):
                self.broken = True
            raise failure

    def start(self):
        """模拟网关初始化；无参数，返回自身。"""
        self.event("start")
        return self

    def tools(self):
        """模拟一次工具目录请求；无参数，返回目录副本。"""
        self.calls.append(("tools/list", {}))
        self.event("tools/list")
        return copy.deepcopy(self.catalog)

    def call(self, name, arguments):
        """模拟只读业务工具；参数为工具名和参数，返回响应副本。"""
        if name == "lua_execute":
            native = arguments.get("chunkName") == capture.NATIVE_STACK_CHUNK
            assert arguments == {"instanceId": "ce-test",
                                 "source": capture.NATIVE_STACK_SOURCE if native else capture.STATUS_COMPAT_SOURCE,
                                 "chunkName": capture.NATIVE_STACK_CHUNK if native else capture.STATUS_COMPAT_CHUNK}
        elif name not in capture.READ_ONLY_TOOLS:
            raise AssertionError("unexpected mutating tool: " + name)
        self.calls.append((name, dict(arguments)))
        self.event(name)
        if name == "lua_execute":
            self.event(arguments["chunkName"])
            if native:
                return copy.deepcopy(self.native_response)
        payloads = {
            "instance_list": self.listing, "runtime_get_info": self.info,
            "runtime_get_overview": self.overview, "debugger_get_status": self.status,
            "debugger_get_context": self.context, "debugger_get_stack_trace": self.stack,
            "lua_execute": self.compat_response,
        }
        if name == "lua_execute" and self.counts[capture.STATUS_COMPAT_CHUNK] == 2 and self.final_compat_response is not None:
            return copy.deepcopy(self.final_compat_response)
        if name == "debugger_get_context" and self.counts[name] == 2 and self.final_context is not None:
            return copy.deepcopy(self.final_context)
        if name == "runtime_get_overview" and self.counts[name] == 2 and self.final_overview is not None:
            return copy.deepcopy(self.final_overview)
        if name == "debugger_get_status" and self.counts[name] == 2 and self.final_status is not None:
            return copy.deepcopy(self.final_status)
        return copy.deepcopy(payloads[name])

    def close(self):
        """标记本次网关已清理；无参数和返回值。"""
        self.closed = True


class CaptureTests(unittest.TestCase):
    def setUp(self):
        """为测试创建临时目录及假网关路径；无参数和返回值。"""
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.gateway = self.root / "Gateway.exe"
        self.gateway.touch()
        self.output = self.root / "reports"

    def execute(self, fake=None, extra=(), output=None, stack_mode="heuristic"):
        """在临时目录运行入口；参数为假客户端、附加参数、输出路径和模式，返回退出码与输出。"""
        fake = fake or FakeMcp()
        stream = io.StringIO()
        with patch.object(capture, "McpClient", return_value=fake) as constructor, \
                patch.object(capture, "now", return_value="2026-10-01T08:00:00+00:00"), \
                contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            mode_args = [] if stack_mode is None else ["--stack-mode", stack_mode]
            code = capture.main(["--gateway", str(self.gateway), "--output", str(output or self.output), *mode_args, *extra])
        return code, stream.getvalue(), constructor

    def assert_failure(self, fake, code, extra=(), stack_mode="heuristic"):
        """断言失败未生成报告且网关关闭；参数为假客户端、预期码、附加参数和模式，返回诊断。"""
        result, diagnostic, _ = self.execute(fake, extra, stack_mode=stack_mode)
        self.assertEqual(result, code, diagnostic)
        self.assertTrue(fake.closed)
        self.assertEqual(list(self.output.glob("streg_*.md")), [])
        self.assertTrue({name for name, _ in fake.calls} <= capture.READ_ONLY_TOOLS | {"tools/list", "lua_execute"})
        return diagnostic

    def compat_fake(self):
        """构造已知状态缺陷与可用 Lua 目录；无参数，返回假客户端。"""
        fake = FakeMcp()
        fake.status = {"stateValid": False, "attached": False, "broken": False,
                       "error": "CheatEngine.Mcp/debugger_get_status:4: debug_isBroken did not return a boolean debugger state"}
        fake.catalog["lua_execute"] = {"inputSchema": {"properties": {"instanceId": {}, "source": {}, "chunkName": {}}}}
        return fake

    def native_fake(self, count=17, wide=True):
        """构造原生栈及 Lua 响应；参数为帧数和六十四位标志，返回独立假客户端。"""
        fake = FakeMcp()
        fake.catalog["lua_execute"] = {"inputSchema": {"properties": {"instanceId": {}, "source": {}, "chunkName": {}}}}
        if not wide:
            fake.overview["process"]["pointerSize"] = 4
            fake.context = {"is64Bit": False, "includesExtraRegisters": True,
                            "registers": {"EIP": "401000", "ESP": "1000", "EBP": "0"}}
        fake.context["registers"]["THREADID"] = "1234"
        regs = fake.context["registers"]
        ip, sp, bp = ("RIP", "RSP", "RBP") if wide else ("EIP", "ESP", "EBP")
        base = int(regs[ip], 16)
        frames = [{"pc": f"test.exe+{0x1000 + index * 256:X}", "pcAddress": f"{base + index * 256:X}",
                   "stackAddress": f"{0x1000 + index * 2048:X}", "frameAddress": f"{0x1700 + index * 2048:X}",
                   "returnSymbol": f"test.exe+{0x1000 + (index + 1) * 256:X}",
                   "returnAddress": f"{base + (index + 1) * 256:X}", "parameters": "00000001,00000000,..."}
                  for index in range(count)]
        if frames:
            frames[-1].update(returnAddress="0", returnSymbol="00000000")
        fake.native_response = {"ok": True, "hostEffect": "completed", "droppedOpaqueCount": 0,
                                "returnValues": [{"source": "ce_stacktrace_window", "pointerSize": 8 if wide else 4,
                                                  "instructionPointer": regs[ip], "stackPointer": regs[sp],
                                                  "framePointer": regs[bp], "threadId": regs["THREADID"],
                                                  "frameCount": count, "frames": frames,
                                                  "termination": "zero_return", "temporaryWindow": True}]}
        return fake

    def test_default_native_complete_trace(self):
        """验证默认原生模式导出全部十七帧及五列并复核上下文；无参数和返回值。"""
        fake = self.native_fake()
        del fake.catalog["debugger_get_stack_trace"]
        code, diagnostic, _ = self.execute(fake, stack_mode=None)
        self.assertEqual(code, 0, diagnostic)
        self.assertTrue(fake.closed)
        report = next(self.output.glob("*.md")).read_text(encoding="utf-8")
        raw = json.loads(report.split("```json\n", 1)[1].split("\n```", 1)[0])
        self.assertEqual(raw["stacktrace"], fake.native_response["returnValues"][0])
        self.assertIn("| Index | PC | Stack | Frame | Return | Parameters |", report)
        self.assertIn("Frames exported: 17", report)
        self.assertIn("| 16 | test.exe+2000", report)
        self.assertNotIn("Scanned slots:", report)
        self.assertNotIn("debugger_get_stack_trace", fake.counts)
        self.assertEqual([name for name, _ in fake.calls], [
            "tools/list", "instance_list", "runtime_get_info", "runtime_get_overview",
            "debugger_get_status", "debugger_get_context", "lua_execute",
            "debugger_get_status", "debugger_get_context", "runtime_get_overview",
        ])

    def test_native_more_than_128_frames_and_32_bit(self):
        """验证原生模式不受旧扫描深度限制且兼容三十二位及零帧指针；无参数和返回值。"""
        for wide in (True, False):
            fake = self.native_fake(count=129, wide=wide)
            code, diagnostic, _ = self.execute(fake, stack_mode="native")
            self.assertEqual(code, 0, diagnostic)
            address = "7FF012345678" if wide else "401000"
            report = (self.output / f"streg_{address}.md").read_text(encoding="utf-8")
            self.assertIn("Frames exported: 129", report)
            self.assertIn("| 128 | test.exe+9000", report)

    def test_native_unwind_stopped_warning(self):
        """验证非零返回终止不会冒充完整调用链；无参数和返回值。"""
        fake = self.native_fake()
        stack = fake.native_response["returnValues"][0]
        stack["frames"][-1].update(returnAddress="123456", returnSymbol="123456")
        stack["termination"] = "unwind_stopped"
        code, diagnostic, _ = self.execute(fake, stack_mode="native")
        self.assertEqual(code, 0, diagnostic)
        self.assertIn("WARN: CE native unwinding stopped", diagnostic)
        report = next(self.output.glob("*.md")).read_text(encoding="utf-8")
        self.assertIn("the call chain may be incomplete", report)

    def test_native_missing_lua_does_not_fallback(self):
        """验证原生模式缺少 Lua 时拒绝并且不隐式退回扫描；无参数和返回值。"""
        fake = FakeMcp()
        self.assertIn("requires lua_execute", self.assert_failure(fake, 2, stack_mode=None))
        self.assertNotIn("instance_list", fake.counts)
        self.assertNotIn("debugger_get_stack_trace", fake.counts)
        for key in ("instanceId", "source", "chunkName"):
            fake = self.native_fake()
            del fake.catalog["lua_execute"]["inputSchema"]["properties"][key]
            self.assert_failure(fake, 2, stack_mode="native")

    def test_native_malformed_lua_responses(self):
        """验证原生 Lua 响应失败、丢弃内容和返回对象数量；无参数和返回值。"""
        for key, value, code in [("ok", False, 3), ("hostEffect", "unknown", 3),
                                 ("droppedOpaqueCount", 1, 2), ("returnValues", [], 2),
                                 ("returnValues", [True], 2), ("returnValues", [{}, {}], 2)]:
            with self.subTest(key=key):
                fake = self.native_fake()
                fake.native_response[key] = value
                self.assert_failure(fake, code, stack_mode="native")
                self.assertNotIn("debugger_get_stack_trace", fake.counts)

    def test_native_malformed_frames_and_context(self):
        """验证帧结构、地址范围、计数上限和上下文漂移；无参数和返回值。"""
        cases = [("source", "heuristic", 2), ("pointerSize", 4, 2), ("frameCount", 16, 2),
                 ("frameCount", 2049, 2), ("frames", [], 2), ("frames", [{}], 2),
                 ("temporaryWindow", 1, 2), ("termination", "unwind_stopped", 2)]
        cases += [(key, "123", 3) for key in ("instructionPointer", "stackPointer", "framePointer", "threadId")]
        for key, value, code in cases:
            with self.subTest(key=key):
                fake = self.native_fake()
                fake.native_response["returnValues"][0][key] = value
                self.assert_failure(fake, code, stack_mode="native")
        for key in ("pc", "pcAddress", "stackAddress", "frameAddress", "returnSymbol", "returnAddress", "parameters"):
            fake = self.native_fake()
            del fake.native_response["returnValues"][0]["frames"][0][key]
            self.assert_failure(fake, 2, stack_mode="native")
        for key, value, code in [("pcAddress", "1234", 3), ("stackAddress", "2000", 3),
                                 ("returnAddress", "10000000000000000", 2), ("frameAddress", "xyz", 2),
                                 ("pcAddress", "0", 2)]:
            fake = self.native_fake()
            fake.native_response["returnValues"][0]["frames"][0][key] = value
            self.assert_failure(fake, code, stack_mode="native")
        fake = self.native_fake(wide=False)
        fake.native_response["returnValues"][0]["frames"][0]["returnAddress"] = "100000000"
        self.assert_failure(fake, 2, stack_mode="native")

    def test_native_final_context_and_status_compatibility(self):
        """验证原生采集后的线程身份复核及状态兼容查询可共存；无参数和返回值。"""
        for register in ("RIP", "RSP", "RBP", "THREADID"):
            fake = self.native_fake()
            fake.final_context = copy.deepcopy(fake.context)
            fake.final_context["registers"][register] = "123"
            self.assert_failure(fake, 3, stack_mode="native")
        fake = self.native_fake()
        fake.status = self.compat_fake().status
        code, diagnostic, _ = self.execute(fake, stack_mode="native")
        self.assertEqual(code, 0, diagnostic)
        self.assertEqual(fake.counts[capture.STATUS_COMPAT_CHUNK], 2)
        self.assertEqual(fake.counts[capture.NATIVE_STACK_CHUNK], 1)

    def test_native_failures_preserve_existing_report(self):
        """验证查询失败、中断或漂移不会覆盖旧报告且网关关闭；无参数和返回值。"""
        self.assertEqual(self.execute(self.native_fake(), stack_mode="native")[0], 0)
        report = next(self.output.glob("*.md"))
        previous = report.read_bytes()
        for failure, expected in [(TransportError("connection lost"), 3), (KeyboardInterrupt(), 130),
                                  (ToolError({"kind": "capability_disabled", "hostEffect": "not_started"}), 2)]:
            fake = self.native_fake()
            fake.failures[(capture.NATIVE_STACK_CHUNK, 1)] = failure
            code, diagnostic, _ = self.execute(fake, stack_mode="native")
            self.assertEqual(code, expected, diagnostic)
            self.assertTrue(fake.closed)
            self.assertEqual(report.read_bytes(), previous)
            self.assertNotIn("debugger_get_stack_trace", fake.counts)

    def test_native_report_filter_and_escaping(self):
        """验证原生显示文本转义以及四类字段递归过滤且不改变源数据；无参数和返回值。"""
        fake = self.native_fake()
        stack = fake.native_response["returnValues"][0]
        stack["frames"][0]["pc"] = "test|<script>\n`"
        for key in ("evidence", "capabilities", "hostVersion", "platform"):
            fake.info[key] = [{key: "noisy"}]
            stack["frames"][0][key] = "noisy"
        original = copy.deepcopy(stack)
        self.assertEqual(self.execute(fake, stack_mode="native")[0], 0)
        report = next(self.output.glob("*.md")).read_text(encoding="utf-8")
        raw = json.loads(report.split("```json\n", 1)[1].split("\n```", 1)[0])
        self.assertEqual(raw["stacktrace"]["frames"][0]["pc"], "test|<script>\n`")
        self.assertIn(capture.safe_cell(stack["frames"][0]["pc"]), report)
        self.assertNotIn("noisy", report)
        self.assertEqual(stack, original)
        self.assertEqual(capture.filter_report_snapshot(stack)["frames"][0], raw["stacktrace"]["frames"][0])

    def test_compatibility_query_success_preserves_evidence(self):
        """验证兼容采集保留原始失败及查询证据；无参数和返回值。"""
        fake = self.compat_fake()
        code, diagnostic, _ = self.execute(fake)
        self.assertEqual(code, 0, diagnostic)
        self.assertTrue(fake.closed)
        self.assertEqual(fake.counts["lua_execute"], 2)
        report = next(self.output.glob("*.md")).read_text(encoding="utf-8")
        raw = json.loads(report.split("```json\n")[1].split("\n```")[0])
        self.assertEqual(raw["status"]["originalStatus"], fake.status)
        self.assertEqual(raw["status"]["luaResponse"], fake.compat_response)
        self.assertNotIn("reportedBroken", raw["status"])
        self.assertEqual(raw["finalStatus"]["instructionPointer"], raw["address"])
        self.assertNotIn("debug_isBroken", capture.STATUS_COMPAT_SOURCE)
        with self.assertRaises(capture.CaptureError):
            capture.read_tool(fake, "lua_execute", "ce-test")

    def test_compatibility_is_limited_to_known_error(self):
        """验证非特定错误和缺失能力不会绕过前置检查；无参数和返回值。"""
        for error in ("host error", "debug_isBroken did not return a boolean debugger state", None):
            fake = self.compat_fake()
            fake.status["error"] = error
            self.assert_failure(fake, 2)
            self.assertNotIn("lua_execute", fake.counts)
        fake = self.compat_fake()
        del fake.catalog["lua_execute"]
        self.assertIn("unavailable", self.assert_failure(fake, 2))
        self.assertNotIn("lua_execute", fake.counts)
        fake = self.compat_fake()
        fake.failures[("lua_execute", 1)] = ToolError({"kind": "capability_disabled", "hostEffect": "not_started"})
        self.assert_failure(fake, 2)

    def test_compatibility_malformed_and_failed_responses(self):
        """验证 Lua 执行失败、效果未知和结构错误；无参数和返回值。"""
        for key, value, code in [("ok", False, 3), ("hostEffect", "unknown", 3),
                                 ("hostEffect", "started", 3), ("droppedOpaqueCount", 1, 2),
                                 ("returnValues", [], 2), ("returnValues", [True], 2),
                                 ("returnValues", [{"stateValid": True}], 2)]:
            with self.subTest(key=key, value=value):
                fake = self.compat_fake()
                fake.compat_response[key] = value
                self.assert_failure(fake, code)
        for occurrence in (1, 2):
            fake = self.compat_fake()
            fake.failures[("lua_execute", occurrence)] = KeyboardInterrupt()
            self.assert_failure(fake, 130)

    def test_compatibility_context_changes_are_rejected(self):
        """验证前后停止丢失或指令栈指针变化拒绝报告；无参数和返回值。"""
        for final in (False, True):
            for key, value in [("instructionPointer", "1234"), ("stackPointer", "2000"),
                               ("is64Bit", False), ("broken", False)]:
                fake = self.compat_fake()
                result = copy.deepcopy(fake.compat_response)
                result["returnValues"][0][key] = value
                if final:
                    fake.final_compat_response = result
                else:
                    fake.compat_response = result
                self.assert_failure(fake, 2 if key == "broken" and not final else 3)
        fake = self.compat_fake()
        fake.stack["stackPointer"] = "2000"
        self.assert_failure(fake, 3)

    def test_success_contract_and_raw_snapshot(self):
        """验证六十四位报告与调用参数顺序；无参数和返回值。"""
        fake = FakeMcp()
        code, diagnostic, constructor = self.execute(fake)
        self.assertEqual(code, 0, diagnostic)
        self.assertTrue(fake.closed)
        report = self.output / "streg_7FF012345678.md"
        self.assertEqual(list(self.output.glob("*.md")), [report])
        data = report.read_bytes()
        self.assertNotIn(b"\r", data)
        text = data.decode("utf-8")
        raw = json.loads(text.split("```json\n", 1)[1].split("\n```", 1)[0])
        self.assertEqual(raw["context"], fake.context)
        self.assertEqual(raw["stacktrace"], fake.stack)
        self.assertEqual(raw["status"], fake.status)
        self.assertEqual(raw["finalOverview"], fake.overview)
        self.assertEqual(raw["residueCheck"]["state"], "unchanged")
        self.assertEqual(raw["capturedAt"], "2026-10-01T08:00:00+00:00")
        for key, value in fake.context["registers"].items():
            self.assertIn(f"| {key} | {value} |", text)
        self.assertLess(text.index("| EFLAGS |"), text.index("| RIP |"))
        self.assertLess(text.index("| 0 | 1000 |"), text.index("| 1 | 1020 |"))
        self.assertIn("heuristic candidates", text)
        self.assertEqual([name for name, _ in fake.calls], [
            "tools/list", "instance_list", "runtime_get_info", "runtime_get_overview",
            "debugger_get_status", "debugger_get_context", "debugger_get_stack_trace",
            "debugger_get_status", "runtime_get_overview",
        ])
        for name, arguments in fake.calls:
            if name in {"instance_list", "tools/list"}:
                self.assertEqual(arguments, {})
            else:
                expected = {"instanceId": "ce-test"}
                if name == "debugger_get_context":
                    expected["includeExtraRegisters"] = True
                if name == "debugger_get_stack_trace":
                    expected["depth"] = 128
                self.assertEqual(arguments, expected)
        self.assertEqual(constructor.call_args.args[1:], (30, self.output / "streg_gateway.stderr.log"))

    def test_32_bit_and_optional_fields(self):
        """验证三十二位现场及可选字段缺省；无参数和返回值。"""
        fake = FakeMcp()
        fake.overview["process"]["pointerSize"] = 4
        fake.context = {"is64Bit": False, "registers": {"EIP": "00401000", "ESP": "1000", "EBP": "1100"},
                        "includesExtraRegisters": True, "activeInterface": None}
        fake.stack["pointerSize"] = 4
        fake.stack["frames"] = [{"stackAddress": "1000", "returnAddress": "402000"}]
        fake.status["activeInterface"] = None
        code, diagnostic, _ = self.execute(fake)
        self.assertEqual(code, 0, diagnostic)
        text = (self.output / "streg_401000.md").read_text(encoding="utf-8")
        self.assertIn("Active debugger interface: unavailable", text)
        self.assertIn("| 0 | 1000 | 402000 | unavailable | unavailable |", text)
        self.assertNotIn("| XMM", text)

    def test_empty_frames(self):
        """验证空栈候选仍生成扫描数量说明；无参数和返回值。"""
        fake = FakeMcp()
        fake.stack.update(frames=[], scannedSlots=0)
        self.assertEqual(self.execute(fake)[0], 0)
        text = next(self.output.glob("*.md")).read_text(encoding="utf-8")
        self.assertIn("Scanned slots: 0", text)
        self.assertIn("No heuristic candidate frames", text)

    def test_address_validation(self):
        """验证文件名地址安全边界；无参数和返回值。"""
        for value, expected in [(16, "10"), ("0x000abc", "ABC"), ("0XABC", "ABC"), (2**64 - 1, "FFFFFFFFFFFFFFFF")]:
            self.assertEqual(capture.normalize_address(value), expected)
        for value in [True, False, 0, -1, 2**64, "", None, "../x", "1/2", "1\\2", "1e+12", "1e-2", 1.5,
                      " 123", "0x", "0", "10000000000000000"]:
            with self.subTest(value=value), self.assertRaises(capture.CaptureError):
                capture.normalize_address(value)

    def test_context_structure_failures(self):
        """覆盖上下文字段缺失、错误类型及位宽不符；无参数和返回值。"""
        cases = [(key, None, True) for key in ("is64Bit", "registers", "includesExtraRegisters")]
        cases += [("is64Bit", value, False) for value in (False, "true", 1)]
        cases += [("includesExtraRegisters", value, False) for value in (False, "true", 1)]
        cases += [("registers", value, False) for value in ([], {}, {"RIP": 123}, {"RIP": "../x"}, {"RIP": "0"}, {"RIP": "AB", "RAX": 1})]
        cases += [("activeInterface", 1, False)]
        for key, value, remove in cases:
            with self.subTest(key=key, value=value, remove=remove):
                fake = FakeMcp()
                if remove:
                    del fake.context[key]
                else:
                    fake.context[key] = value
                self.assert_failure(fake, 2)
        fake = FakeMcp()
        fake.overview["process"]["pointerSize"] = 4
        fake.context.update(is64Bit=False, registers={"EIP": "100000000"})
        self.assert_failure(fake, 2)

    def test_stack_structure_failures(self):
        """覆盖栈必填字段、可选类型和扫描深度边界；无参数和返回值。"""
        cases = [(key, None, True) for key in ("stackPointer", "pointerSize", "frames", "scannedSlots")]
        cases += [("scannedSlots", value, False) for value in (-1, 129, True, "128")]
        cases += [("pointerSize", value, False) for value in (4, "8", True)]
        cases += [("stackPointer", 0, False), ("frames", {}, False)]
        for frame in [{}, {"stackAddress": "1000"}, {"returnAddress": "2000"},
                      {"stackAddress": 0, "returnAddress": "2000"},
                      {"stackAddress": "1000", "returnAddress": "2000", "callInstruction": None},
                      {"stackAddress": "1000", "returnAddress": "2000", "isHeuristic": "true"}]:
            cases.append(("frames", [frame], False))
        for key, value, remove in cases:
            with self.subTest(key=key, value=value, remove=remove):
                fake = FakeMcp()
                if remove:
                    del fake.stack[key]
                else:
                    fake.stack[key] = value
                self.assert_failure(fake, 2)

    def test_preconditions_stop_before_context(self):
        """验证未附加或未停止时不采集上下文；无参数和返回值。"""
        for key in ("stateValid", "attached", "broken", "error"):
            fake = FakeMcp()
            fake.status[key] = "host unavailable" if key == "error" else False
            self.assert_failure(fake, 2)
            self.assertNotIn("debugger_get_context", fake.counts)
            self.assertNotIn("debugger_get_stack_trace", fake.counts)
        for key, value in [("isOpen", False), ("selectionEpoch", None), ("processId", None), ("pointerSize", 0)]:
            fake = FakeMcp()
            fake.overview["process"][key] = value
            self.assert_failure(fake, 2)
            self.assertNotIn("debugger_get_context", fake.counts)

    def test_discovery_failures_and_explicit_selection(self):
        """覆盖实例发现及精确选择；无参数和返回值。"""
        for items, incomplete, extra in [([], False, ()), ([{"instanceId": "ce-test"}], True, ()),
                                        ([{"instanceId": "ce-test"}, {"instanceId": "ce-other"}], False, ()),
                                        ([{"instanceId": "ce-test"}], False, ("--instance-id", "missing")),
                                        ([{"instanceId": "ce-test"}] * 2, False, ("--instance-id", "ce-test"))]:
            fake = FakeMcp()
            fake.listing.update(instances=items, discoveryIncomplete=incomplete)
            self.assert_failure(fake, 2, extra)
            self.assertNotIn("debugger_get_context", fake.counts)
        fake = FakeMcp()
        fake.listing["instances"].append({"instanceId": "ce-other"})
        self.assertEqual(self.execute(fake, ("--instance-id", "ce-test"))[0], 0)

    def test_catalog_drift(self):
        """验证目录与参数漂移在发现前失败；无参数和返回值。"""
        for name in capture.READ_ONLY_TOOLS:
            fake = FakeMcp()
            del fake.catalog[name]
            self.assert_failure(fake, 2)
            self.assertNotIn("instance_list", fake.counts)
        for name, key in [("debugger_get_context", "includeExtraRegisters"), ("debugger_get_stack_trace", "depth"),
                          ("runtime_get_info", "instanceId")]:
            fake = FakeMcp()
            del fake.catalog[name]["inputSchema"]["properties"][key]
            self.assert_failure(fake, 2)

    def test_transport_and_json_failure_cleanup(self):
        """验证传输及 JSON 解码错误退出并清理；无参数和返回值。"""
        for stage in ("start", "tools/list", "instance_list", "debugger_get_context", "runtime_get_overview"):
            for failure in (TransportError("connection lost"), json.JSONDecodeError("invalid JSON", "x", 0)):
                fake = FakeMcp()
                fake.failures[(stage, 1)] = failure
                self.assert_failure(fake, 3)

    def test_tool_error_kinds_and_host_effects(self):
        """验证全部工具错误分类及只读主机效果；无参数和返回值。"""
        kinds = [(kind, 2) for kind in capture.ARGUMENT_ERRORS]
        kinds += [(kind, 3) for kind in capture.SESSION_ERRORS]
        kinds += [(kind, 3) for kind in ("memory_read_failed", "memory_write_failed", "memory_allocate_failed",
                                        "partial_effect", "limit_exceeded", "unknown_kind")]
        for stage, occurrence in [("debugger_get_status", 1), ("debugger_get_context", 1),
                                  ("debugger_get_status", 2), ("runtime_get_overview", 2)]:
            for kind, code in kinds + [("host_refused", 2 if stage == "debugger_get_status" and occurrence == 1 else 3)]:
                for effect in ("not_started", "started"):
                    with self.subTest(stage=stage, occurrence=occurrence, kind=kind, effect=effect):
                        fake = FakeMcp()
                        fake.failures[(stage, occurrence)] = ToolError({"error": {"kind": kind, "hostEffect": effect}})
                        diagnostic = self.assert_failure(fake, code)
                        self.assertIn("kind=" + kind, diagnostic)
                        self.assertIn("hostEffect=" + effect, diagnostic)
                        self.assertTrue(diagnostic.isascii())
        for effect in (None, "completed", "partial", "unknown", []):
            fake = FakeMcp()
            fake.failures[("debugger_get_context", 1)] = ToolError({"kind": "invalid_argument", "hostEffect": effect})
            self.assertIn("WARN", self.assert_failure(fake, 3))

    def test_unusable_connection_and_allowlist_guard(self):
        """验证失效连接及无实例工具调用被拦截；无参数和返回值。"""
        fake = FakeMcp()
        with self.assertRaises(capture.CaptureError):
            capture.read_tool(fake, "debugger_continue", "ce-test")
        with self.assertRaises(capture.CaptureError):
            capture.read_tool(fake, "debugger_get_context")
        fake.broken = True
        with self.assertRaises(TransportError):
            capture.read_tool(fake, "debugger_get_status", "ce-test")
        self.assertEqual(fake.calls, [])

    def test_final_overview_transport_is_unavailable(self):
        """验证末次概览传输失败记录无法核对；无参数和返回值。"""
        fake = FakeMcp()
        fake.failures[("runtime_get_overview", 2)] = TransportError("connection lost")
        self.assertIn("residueCheck=unavailable", self.assert_failure(fake, 3))

    def test_final_stopped_and_session_checks(self):
        """验证末次状态、会话指纹与计数变化拒绝报告；无参数和返回值。"""
        fake = FakeMcp()
        fake.final_status = dict(fake.status, broken=False)
        self.assert_failure(fake, 3)
        for section, key, value in [("runtime", "epoch", 10), ("process", "processId", 456),
                                    ("process", "selectionEpoch", 2), ("process", "pointerSize", 4),
                                    ("process", "isOpen", False), (None, "resourceCount", 1),
                                    (None, "jobCount", 1), (None, "jobCount", None)]:
            fake = FakeMcp()
            fake.final_overview = copy.deepcopy(fake.overview)
            target = fake.final_overview if section is None else fake.final_overview[section]
            target[key] = value
            diagnostic = self.assert_failure(fake, 3)
            if key in {"resourceCount", "jobCount"}:
                self.assertIn("residueCheck=", diagnostic)

    def test_keyboard_interrupt_lifecycle(self):
        """验证初始化、采集和写文件前后中断；无参数和返回值。"""
        for stage in ("start", "tools/list", "debugger_get_status", "debugger_get_context", "debugger_get_stack_trace"):
            fake = FakeMcp()
            fake.failures[(stage, 1)] = KeyboardInterrupt()
            self.assert_failure(fake, 130)
        with patch.object(capture, "atomic_text", side_effect=KeyboardInterrupt()):
            self.assert_failure(FakeMcp(), 130)
        original = capture.atomic_text

        def commit_then_interrupt(path, text):
            """模拟原子替换完成后中断；参数为路径和文本，无返回值。"""
            original(path, text)
            raise KeyboardInterrupt()

        fake = FakeMcp()
        with patch.object(capture, "atomic_text", side_effect=commit_then_interrupt):
            code, _, _ = self.execute(fake)
        self.assertEqual(code, 130)
        self.assertTrue(fake.closed)
        self.assertEqual(len(list(self.output.glob("*.md"))), 1)
        self.assertTrue(next(self.output.glob("*.md")).read_text(encoding="utf-8").endswith("```\n"))
        self.assertEqual(list(self.output.glob("*.tmp")), [])

    def test_invalid_cli_and_local_io(self):
        """验证参数和路径错误不启动网关；无参数和返回值。"""
        for extra in [("--timeout", "0"), ("--timeout", "-1"), ("--timeout", "abc"),
                      ("--timeout", "1.5"), ("--gateway", str(self.root / "missing.exe")), ("--unknown",)]:
            code, _, constructor = self.execute(extra=extra)
            self.assertEqual(code, 2)
            constructor.assert_not_called()
        code, _, constructor = self.execute(output=self.gateway)
        self.assertEqual(code, 2)
        constructor.assert_not_called()
        with patch("opcode_report.os.replace", side_effect=PermissionError("file is locked")):
            self.assert_failure(FakeMcp(), 2)
        self.assertEqual(list(self.output.glob("*.tmp")), [])

    def test_markdown_sanitization_and_raw_preservation(self):
        """验证恶意表格文本清洗且原始 JSON 可还原；无参数和返回值。"""
        fake = FakeMcp()
        text = "bad\x00\x1b|line\nnext\r\x85<script>`\\|"
        fake.context["registers"]["CUSTOM"] = text
        fake.stack["frames"][0]["callInstruction"] = text
        self.assertEqual(self.execute(fake)[0], 0)
        report = next(self.output.glob("*.md")).read_text(encoding="utf-8")
        self.assertIn(capture.safe_cell(text), report)
        for char in ("\x00", "\x1b", "\x85", "<script>"):
            self.assertNotIn(char, report.split("## Raw MCP Snapshot")[0])
        raw = json.loads(report.split("```json\n")[1].split("\n```")[0])
        self.assertEqual(raw["context"]["registers"]["CUSTOM"], text)

    def test_repeat_atomic_replacement_and_failed_replacement(self):
        """验证重复采集完整覆盖且替换失败保留旧文件；无参数和返回值。"""
        fake = FakeMcp()
        fake.context["registers"]["OLD_ONLY"] = "DEAD"
        self.assertEqual(self.execute(fake)[0], 0)
        report = next(self.output.glob("*.md"))
        original = report.read_bytes()
        with patch("opcode_report.os.replace", side_effect=OSError("replace failed")):
            self.assertEqual(self.execute()[0], 2)
        self.assertEqual(report.read_bytes(), original)
        self.assertEqual(self.execute()[0], 0)
        self.assertNotIn("OLD_ONLY", report.read_text(encoding="utf-8"))
        self.assertEqual(len(list(self.output.glob("*.md"))), 1)
        self.assertEqual(list(self.output.glob("*.tmp")), [])

    def test_shared_output_requires_serial_runs(self):
        """验证两个采集入口共享日志并明确禁止并发；无参数和返回值。"""
        first = self.execute()[2]
        second = self.execute()[2]
        self.assertEqual(first.call_args.args[2], second.call_args.args[2])
        self.assertEqual(first.call_args.args[2].name, "streg_gateway.stderr.log")
        document = (capture.ROOT / "Docs/stacktrace_register.md").read_text(encoding="utf-8")
        self.assertIn("同一输出目录同一时刻只允许一个采集实例", document)
        self.assertIn("不提供并发锁", document)


if __name__ == "__main__":
    unittest.main()
