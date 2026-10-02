"""验证 Step over 脚本仅执行一次 debugger_step 且不读取或改变其他目标状态。"""
import json
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ce_run_step_over as capture


class FakeClient:
    """记录脚本发出的 MCP 工具调用。"""
    def __init__(self):
        """初始化假客户端；无参数，无返回值。"""
        self.calls = []
        self.closed = False
        self.response = {"mode": "over", "continued": True}

    def start(self):
        """模拟 Gateway 启动；无参数，返回客户端自身。"""
        return self

    def tools(self):
        """返回支持 over 模式的最小工具目录；无参数，返回工具目录。"""
        return {"debugger_step": {"inputSchema": {"properties": {
            "instanceId": {"type": "string"}, "mode": {"type": "string", "enum": ["into", "over"]}}}}}

    def call(self, name, arguments):
        """记录并模拟 MCP 工具调用；参数为工具名和参数字典，返回响应。"""
        self.calls.append((name, arguments))
        if name == "instance_list":
            return {"instances": [{"instanceId": "ce-test"}]}
        if name == "debugger_step":
            return self.response
        raise AssertionError("unexpected tool: " + name)

    def close(self):
        """记录客户端关闭；无参数，无返回值。"""
        self.closed = True


class StepOverTests(unittest.TestCase):
    """验证入口默认行为、调用次数和失败路径。"""
    def test_default_mode_is_over_and_calls_step_once(self):
        """验证默认命令直接发出一次 over；无参数，无返回值。"""
        fake = FakeClient()
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(capture, "McpClient", return_value=fake):
                result = capture.run_capture(["--output", directory])
            self.assertEqual(result, 0)
            self.assertEqual(fake.calls, [
                ("instance_list", {}),
                ("debugger_step", {"instanceId": "ce-test", "mode": "over"}),
            ])
            self.assertTrue(fake.closed)
            report = Path(directory, "step_capture.md").read_text(encoding="utf-8")
            payload = json.loads(report.split("```json\n", 1)[1].split("\n```", 1)[0])
            self.assertTrue(payload["stepCallStarted"])
            self.assertEqual(payload["mode"], "over")

    def test_no_output_skips_report_and_stderr_files(self):
        """验证禁用输出时不创建文件；参数为空，返回无。"""
        fake = FakeClient()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory, "not-created")
            with patch.object(capture, "McpClient", return_value=fake) as client_factory:
                result = capture.run_capture(["--output", str(output), "--no-output"])
            self.assertEqual(result, 0)
            self.assertFalse(output.exists())
            self.assertIsNone(client_factory.call_args.args[2])
            self.assertTrue(fake.closed)

    def test_no_output_prints_startup_error_to_console(self):
        """验证禁用文件输出时启动失败仍打印错误；参数为空，返回无。"""
        fake = FakeClient()
        with tempfile.TemporaryDirectory() as directory:
            fake.start = lambda: (_ for _ in ()).throw(RuntimeError("gateway unavailable"))
            output = io.StringIO()
            with patch.object(capture, "McpClient", return_value=fake):
                with contextlib.redirect_stderr(output):
                    result = capture.run_capture(["--output", directory, "--no-output"])
        self.assertEqual(result, 2)
        self.assertIn("ERROR: gateway unavailable", output.getvalue())
    def test_explicit_into_mode_is_supported(self):
        """验证显式 into 模式仅改变 debugger_step 参数；参数为空，返回无。"""
        fake = FakeClient()
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(capture, "McpClient", return_value=fake):
                result = capture.run_capture(["--mode", "into", "--output", directory])
            self.assertEqual(result, 0)
            self.assertEqual(fake.calls[-1][1]["mode"], "into")
            self.assertEqual(sum(name == "debugger_step" for name, _ in fake.calls), 1)

    def test_step_failure_is_not_retried(self):
        """验证进入单步调用后异常不重试；参数为空，返回无。"""
        class FailedClient(FakeClient):
            def call(self, name, arguments):
                self.calls.append((name, arguments))
                if name == "instance_list":
                    return {"instances": [{"instanceId": "ce-test"}]}
                raise TimeoutError("response timeout")
        fake = FailedClient()
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(capture, "McpClient", return_value=fake):
                result = capture.run_capture(["--output", directory])
            self.assertEqual(result, 3)
            self.assertEqual(sum(name == "debugger_step" for name, _ in fake.calls), 1)
            self.assertTrue(fake.closed)

    def test_ambiguous_instances_do_not_step(self):
        """验证实例不唯一时不调用单步；参数为空，返回无。"""
        class MultipleClient(FakeClient):
            def call(self, name, arguments):
                self.calls.append((name, arguments))
                return {"instances": [{"instanceId": "one"}, {"instanceId": "two"}]}
        fake = MultipleClient()
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(capture, "McpClient", return_value=fake):
                result = capture.run_capture(["--output", directory])
            self.assertEqual(result, 2)
            self.assertEqual(fake.calls, [("instance_list", {})])

    def test_address_gate_is_not_part_of_capture(self):
        """验证脚本不再依赖特定模块地址；参数为空，返回无。"""
        self.assertFalse(hasattr(capture, "EXPECTED_OFFSET"))
        self.assertFalse(hasattr(capture, "capture_preflight"))


if __name__ == "__main__":
    unittest.main()


