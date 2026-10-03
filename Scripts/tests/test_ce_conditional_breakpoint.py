"""离线验证原生条件断点源码合同、回执、现场稳定及失败边界；不连接 CE。"""

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import test_ce_execute_lua as lua_tests
from test_ce_execute_lua import LuaFake
from ce_mcp_client import TransportError
import ce_set_conditional_breakpoint as cli


def condition_fake():
    """创建原生条件成功回执；无入参，返回假客户端。"""
    fake = LuaFake()
    fake.response["returnValues"] = [{
        "ok": True, "created": True, "conditionReadbackMatched": True,
        "backend": "native-ui", "phase": "completed", "address": "7FF777CED93B",
        "conditionType": "complex", "condition": "return true",
        "threadIdBefore": "1234", "threadIdAfter": "1234",
    }]
    return fake


class ConditionTests(unittest.TestCase):
    setUp = lua_tests.LuaExecutionTests.setUp
    invoke = lua_tests.LuaExecutionTests.invoke

    def invoke_condition(self, fake=None, extra=()):
        """调用条件入口；入参为假现场和参数，返回退出码、报告与日志。"""
        return self.invoke(fake or condition_fake(), extra, entry=cli.main, payload=(
            "--address", "victoria3.exe+11FD93B", "--condition-type", "complex", "--condition", "return true"))

    def test_condition_success_and_compat(self):
        """验证正常及已知兼容路径均可完成；无入参，无返回值。"""
        for compat in (False, True):
            fake = condition_fake()
            if compat:
                fake.status = {"stateValid": False, "error": "CheatEngine.Mcp/debugger_get_status:4: debug_isBroken did not return a boolean debugger state"}
            code, report, _ = self.invoke_condition(fake)
            self.assertEqual(code, 0)
            self.assertTrue(report["result"]["conditionReadbackMatched"])
            self.assertEqual(fake.counts["business"], 1)
            self.assertEqual(fake.close_count, 1)
            self.assertTrue(report["manualVerificationRequired"])

    def test_condition_preflight_and_partial_failures(self):
        """验证冲突、语法和部分配置失败分类；无入参，无返回值。"""
        for phase, expected in (("preflight", 2), ("create-attempted", 3),
                                ("condition-write-attempted", 3), ("condition-readback", 3)):
            fake = condition_fake()
            fake.response["returnValues"][0].update(ok=False, phase=phase, created=False,
                                                   conditionReadbackMatched=False, error="setup failed")
            code, report, _ = self.invoke_condition(fake)
            self.assertEqual(code, expected)
            self.assertEqual(report["result"]["phase"], phase)
            self.assertEqual(fake.counts["business"], 1)

    def test_target_process_name_variants(self):
        """验证进程名兼容扩展名与大小写；无入参，无返回值。"""
        for name in ("victoria3", "victoria3.exe", "Victoria3", "VICTORIA3.EXE"):
            with self.subTest(name=name):
                fake = condition_fake()
                fake.overview["process"]["processName"] = name
                self.assertEqual(self.invoke_condition(fake)[0], 0)
                self.assertEqual(fake.counts["business"], 1)

    def test_target_process_name_rejects_non_exact_matches(self):
        """验证非精确目标名称不执行配置；无入参，无返回值。"""
        for name in (None, "", "other.exe", "victoria3.exe.bak", "victoria3_test",
                     " victoria3", "victoria3 ", "C:\\Games\\victoria3.exe"):
            with self.subTest(name=name):
                fake = condition_fake()
                fake.overview["process"]["processName"] = name
                self.assertEqual(self.invoke_condition(fake)[0], 2)
                self.assertNotIn("business", fake.counts)

    def test_malformed_preflight_is_uncertain(self):
        """验证缺字段的失败回执不能证明未创建；无入参，无返回值。"""
        fake = condition_fake()
        fake.response["returnValues"] = [{"ok": False, "phase": "preflight", "created": False, "backend": "native-ui"}]
        self.assertEqual(self.invoke_condition(fake)[0], 3)

    def test_receipt_rejects_incomplete_or_changed(self):
        """验证读回、线程和响应字段缺失不能成功；无入参，无返回值。"""
        good = condition_fake().response
        request = {"conditionType": "complex", "source": "return true", "address": "victoria3.exe+11FD93B"}
        self.assertEqual(cli.validate_condition_result(good, request), good["returnValues"][0])
        for key, value in (("ok", False), ("created", False), ("conditionReadbackMatched", False),
                           ("condition", "return false"), ("backend", "callback"), ("address", "0"),
                           ("threadIdAfter", "5678"), ("threadIdBefore", None)):
            bad = copy.deepcopy(good)
            bad["returnValues"][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                cli.validate_condition_result(bad, request)
            fake = condition_fake()
            fake.response = bad
            self.assertEqual(self.invoke_condition(fake)[0], 3)

    def test_unknown_status_and_target(self):
        """验证未知状态错误及错误进程不执行配置；无入参，无返回值。"""
        for case in ("error", "running", "process", "architecture"):
            fake = condition_fake()
            if case == "error": fake.status = {"stateValid": False, "error": "unexpected status error"}
            if case == "running": fake.status["broken"] = False
            if case == "process": fake.overview["process"]["processName"] = "other.exe"
            if case == "architecture": fake.overview["process"]["pointerSize"] = 4
            self.assertEqual(self.invoke_condition(fake)[0], 2)
            self.assertNotIn("business", fake.counts)

    def test_stopped_context_changes(self):
        """验证后置 RIP/RSP 变化保留失败；无入参，无返回值。"""
        for register in ("RIP", "RSP"):
            fake = condition_fake()
            fake.final_context = copy.deepcopy(fake.context)
            fake.final_context["registers"][register] = "2000"
            self.assertEqual(self.invoke_condition(fake)[0], 3)

    def test_condition_timeout_and_interrupt(self):
        """验证条件超时与中断只发送一次；无入参，无返回值。"""
        for error, expected in ((TransportError("timed out"), 3), (KeyboardInterrupt(), 130)):
            fake = condition_fake()
            fake.failures[("business", 1)] = error
            code, report, _ = self.invoke_condition(fake)
            self.assertEqual(code, expected)
            self.assertEqual(fake.counts["business"], 1)
            self.assertTrue(report["actionAttempted"])
        fake = condition_fake()
        self.assertEqual(self.invoke_condition(fake, ("--timeout", "9"))[0], 2)
        self.assertEqual(fake.calls, [])

    def test_compat_failure_evidence(self):
        """验证异常兼容响应保留原始状态；无入参，无返回值。"""
        fake = condition_fake()
        fake.status = {"stateValid": False, "error": "CheatEngine.Mcp/debugger_get_status:4: debug_isBroken did not return a boolean debugger state"}
        fake.compat_response["ok"] = False
        code, report, _ = self.invoke_condition(fake)
        self.assertEqual(code, 3)
        self.assertEqual(report["status"]["debugger_get_status"], fake.status)
        self.assertEqual(report["status"]["lua_execute"], fake.compat_response)
        self.assertNotIn("business", fake.counts)

    def test_address_and_source_contract(self):
        """验证地址注入与禁止动作以及后端步骤；无入参，无返回值。"""
        for address in ("0", "victoria3.exe+11FD93B;return true", "other.exe+10", " 123", "1" * 17):
            with self.subTest(address=address), self.assertRaises(ValueError):
                cli.build_condition_source(address, "complex", "return true")
        source = cli.build_condition_source("0x1234", "complex", 'return "木"')
        self.assertIn('address="\\049\\050\\051\\052"', source)
        for required in ("debug_setBreakpoint(address)", "debug_getBreakpointList", "visitCondition(menu, true)",
                         "visitCondition(menu, false)", "conditionReadbackMatched", "timer.destroy()"):
            self.assertIn(required, source)
        for forbidden in ("debug_continueFromBreakpoint", "debugger_onBreakpoint", "debug_removeBreakpoint", "writeInteger"):
            self.assertNotIn(forbidden, source)
        with self.assertRaises(ValueError):
            cli.build_condition_source("1234", "simple", "true\nfalse")

    def test_native_text_binding_and_write_verification_contract(self):
        """验证后端使用真实控件文本接口并在确认前校验；无入参，无返回值。"""
        source = cli.build_condition_source("1234", "complex", "return true")
        for required in ("script.setCaption(request.condition)", "script.getCaption()",
                         "expression.setCaption(request.condition)", "expression.getCaption()",
                         "type(text) == 'string'", "result.readbackCondition = readback.condition"):
            self.assertIn(required, source)
        self.assertNotIn("script.Text", source)
        self.assertNotIn("expression.Text", source)
        self.assertLess(source.index("'Condition text write mismatch'"),
                        source.index("dialog.ModalResult = write and 1 or 2"))


if __name__ == "__main__":
    unittest.main()
