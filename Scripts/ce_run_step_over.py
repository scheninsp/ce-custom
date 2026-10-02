"""通过 Cheat Engine MCP 对当前调试现场执行一次 Step over。"""
"""
exp.
cd D:\cebuild\ce-custom
python Scripts\ce_run_step_over.py
结果默认保存到项目根目录下的 `Output/step_capture.md`。网关的标准错误日志也写在 `Output/step_capture_gateway.stderr.log`。
使用 `--output` 可以指定其他目录，例如 `--output D:\temp\capture`。
如果不需要采集文件，则使用：`python Scripts/ce_run_step_over.py --no-output`
"""

import sys

from ce_mcp_client import McpClient
from ce_utils import run_capture as _run_capture


def main(argv=None):
    """执行 Step over 入口；参数为命令行参数，返回进程退出码。"""
    return run_capture(argv)


def run_capture(argv=None):
    """执行 Step over；参数为命令行参数，返回进程退出码。"""
    return _run_capture(argv, "over", "Execute one Cheat Engine debugger Step over",
                        client_factory=McpClient, allow_mode=True)


if __name__ == "__main__":
    sys.exit(main())
