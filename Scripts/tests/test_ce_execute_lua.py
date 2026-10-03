"""离线验证一次 Lua 请求的输入、合同、失败证据和资源关闭；不连接 CE。"""

import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ce_mcp_client import ToolError, TransportError
from test_stacktrace_register import FakeMcp
import ce_execute_lua as cli
import ce_lua_common as common


class LuaFake(FakeMcp):
    def __init__(self):
        """配置最小 Lua 工具目录；无入参，无返回值。"""
        super().__init__()
        self.catalog = {name: {"inputSchema": {"properties": {key: {} for key in keys}}}
                        for name, keys in common.TOOL_PARAMETERS.items()}
        self.info["gates"] = {"unsafeLua": True}
        self.overview["process"]["processName"] = "victoria3.exe"
        self.context["includesExtraRegisters"] = False
        self.response = {"ok": True, "hostEffect": "completed", "returnValues": [5], "droppedOpaqueCount": 0}
        self.close_count = 0

    def call(self, name, arguments):
        """分离固定查询与业务请求；入参为工具和参数，返回响应副本。"""
        if name == "lua_execute" and arguments["chunkName"] != common.STATUS_COMPAT_CHUNK:
            assert arguments["instanceId"] == "ce-test"
            self.calls.append((name, dict(arguments)))
            self.event("business")
            return copy.deepcopy(self.response)
        return super().call(name, arguments)

    def close(self):
        """记录关闭次数并注入故障；无入参，无返回值。"""
        self.close_count += 1
        super().close()
        self.event("close")


class LuaExecutionTests(unittest.TestCase):
    def setUp(self):
        """准备临时报告目录和网关；无入参，无返回值。"""
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.gateway = self.root / "gateway.exe"
        self.gateway.touch()
        self.output = self.root / "reports"

    def invoke(self, fake=None, extra=(), entry=cli.main, payload=("--source", "return 2 + 3")):
        """调用真实入口与假客户端；入参为假现场和参数，返回退出码、报告及日志。"""
        fake = fake or LuaFake()
        stream = io.StringIO()
        with contextlib.redirect_stderr(stream), contextlib.redirect_stdout(stream):
            code = entry(["--gateway", str(self.gateway), "--output", str(self.output),
                          *payload, *extra], client_factory=Mock(return_value=fake))
        reports = list(self.output.glob("*.json"))
        report = json.loads(reports[-1].read_text(encoding="utf-8")) if reports else None
        self.assertTrue(stream.getvalue().isascii())
        allowed = set(common.TOOL_PARAMETERS) | {"tools/list"}
        self.assertTrue(all(name in allowed for name, _ in fake.calls))
        return code, report, stream.getvalue()

    def test_execute_once_and_quote(self):
        """验证一次请求、返回值和字节转义；无入参，无返回值。"""
        client = Mock()
        client.call.return_value = LuaFake().response
        report = {}
        self.assertEqual(common.execute_once(client, "ce-test", "return 5", "user", report)["returnValues"], [5])
        client.call.assert_called_once_with("lua_execute", {"instanceId": "ce-test", "source": "return 5", "chunkName": "user"})
        self.assertEqual(common.lua_quote('"\\\n木'), '"\\034\\092\\010\\230\\156\\168"')

    def test_success(self):
        """验证独立入口成功并关闭；无入参，无返回值。"""
        fake = LuaFake()
        code, report, _ = self.invoke(fake)
        self.assertEqual(code, 0)
        self.assertEqual(report["result"], [5])
        self.assertEqual(fake.counts["business"], 1)
        self.assertEqual(fake.close_count, 1)

    def test_text_errors_before_start(self):
        """验证非法文本不启动客户端；无入参，无返回值。"""
        for text in ("", " \n", "a\0b", "a" * 65537):
            with self.subTest(text=text[:10]):
                fake = LuaFake()
                self.assertEqual(self.invoke(fake, payload=("--source", text))[0], 2)
                self.assertEqual(fake.calls, [])
        for data in (b"", b"\xff"):
            file = self.root / "input.lua"
            file.write_bytes(data)
            self.assertEqual(self.invoke(payload=("--file", str(file)))[0], 2)
        file.write_bytes(b"\xef\xbb\xbfreturn 5\r\n")
        self.assertEqual(common.read_text(None, file), "return 5\n")

    def test_timeout_validation(self):
        """验证无效超时不启动客户端；无入参，无返回值。"""
        for value in ("0", "-1", "nan", "inf"):
            fake = LuaFake()
            self.assertEqual(self.invoke(fake, ("--timeout", value))[0], 2)
            self.assertEqual(fake.calls, [])

    def test_preflight_failures(self):
        """验证发现、权限及工具错误阻止业务；无入参，无返回值。"""
        for case in ("discovery", "multiple", "closed", "gate", "missing", "schema"):
            fake = LuaFake()
            if case == "discovery": fake.listing["discoveryIncomplete"] = True
            if case == "multiple": fake.listing["instances"].append({"instanceId": "other"})
            if case == "closed": fake.overview["process"]["isOpen"] = False
            if case == "gate": fake.info["gates"]["unsafeLua"] = False
            if case == "missing": del fake.catalog["lua_execute"]
            if case == "schema": fake.catalog["lua_execute"]["inputSchema"] = {}
            with self.subTest(case=case):
                code, report, _ = self.invoke(fake)
                self.assertEqual(code, 2)
                self.assertFalse(report["actionAttempted"])
                self.assertEqual(fake.close_count, 1)

    def test_response_failures(self):
        """验证编译、执行与复制错误保留响应；无入参，无返回值。"""
        for change, expected in (({"ok": False, "phase": "compile", "hostEffect": "not_applied"}, 2),
                                 ({"ok": False, "phase": "runtime", "hostEffect": "unknown"}, 3),
                                 ({"droppedOpaqueCount": 1}, 3), ({"droppedOpaqueCount": True}, 3),
                                 ({"returnValues": None}, 3), ({"hostEffect": "unknown"}, 3)):
            fake = LuaFake()
            fake.response.update(change)
            code, report, _ = self.invoke(fake)
            self.assertEqual(code, expected)
            self.assertEqual(report["luaResponse"], fake.response)
            self.assertEqual(fake.counts["business"], 1)

    def test_transport_interrupt_and_tool_error(self):
        """验证超时无重试、中断及明确未执行；无入参，无返回值。"""
        for error, expected in ((TransportError("timed out"), 3), (KeyboardInterrupt(), 130),
                                (ToolError({"error": {"hostEffect": "not_started"}}), 2)):
            fake = LuaFake()
            fake.failures[("business", 1)] = error
            code, report, _ = self.invoke(fake)
            self.assertEqual(code, expected)
            self.assertEqual(fake.counts["business"], 1)
            self.assertTrue(report["actionAttempted"])
            self.assertEqual(fake.close_count, 1)

    def test_identity_and_close_failure(self):
        """验证目标变化和关闭失败不能成功；无入参，无返回值。"""
        fake = LuaFake()
        fake.final_overview = copy.deepcopy(fake.overview)
        fake.final_overview["process"]["processId"] += 1
        self.assertEqual(self.invoke(fake)[0], 3)
        fake = LuaFake()
        fake.failures[("close", 1)] = OSError("close failed")
        code, report, _ = self.invoke(fake)
        self.assertEqual(code, 3)
        self.assertFalse(report["gatewayClose"]["ok"])

    def test_output_failure(self):
        """验证证据目录或报告写入失败；无入参，无返回值。"""
        fake = LuaFake()
        with patch.object(common, "atomic_text", side_effect=OSError("write failed")):
            self.assertEqual(self.invoke(fake)[0], 2)
        self.assertNotIn("business", fake.counts)

    def test_final_report_failure(self):
        """验证动作后报告写入失败返回不确定；无入参，无返回值。"""
        fake = LuaFake()
        with patch.object(common, "save_report", side_effect=[None, None, OSError("write failed")]):
            self.assertEqual(self.invoke(fake)[0], 3)
        self.assertEqual(fake.counts["business"], 1)
        self.assertEqual(fake.close_count, 1)

    def test_start_and_log_failure(self):
        """验证启动与日志错误关闭客户端；无入参，无返回值。"""
        fake = LuaFake()
        fake.failures[("start", 1)] = OSError("log open failed")
        code, report, _ = self.invoke(fake)
        self.assertEqual(code, 2)
        self.assertFalse(report["actionAttempted"])
        self.assertEqual(fake.close_count, 1)

    def test_postflight_not_started_is_not_business_failure(self):
        """验证后置查询未执行不能掩盖已完成动作；无入参，无返回值。"""
        fake = LuaFake()
        fake.failures[("runtime_get_overview", 2)] = ToolError({"error": {"hostEffect": "not_started"}})
        code, report, _ = self.invoke(fake)
        self.assertEqual(code, 3)
        self.assertEqual(report["hostEffect"], "completed")

    def test_explicit_instance_selection(self):
        """验证精确实例 ID，禁止模糊匹配；无入参，无返回值。"""
        fake = LuaFake()
        fake.listing["instances"].append({"instanceId": "ce-other"})
        self.assertEqual(self.invoke(fake, ("--instance-id", "ce-test"))[0], 0)
        self.assertEqual(self.invoke(LuaFake(), ("--instance-id", "ce"))[0], 2)


if __name__ == "__main__":
    unittest.main()
