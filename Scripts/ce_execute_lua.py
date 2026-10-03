"""从命令行文本或 UTF-8 文件执行一次 CE Lua，并保存原始回执；不隐式控制目标。"""

import sys
from pathlib import Path
from ce_mcp_client import McpClient
from ce_lua_common import make_parser, read_text, run_cli


def main(argv=None, client_factory=McpClient):
    """执行一次用户 Lua；入参为命令参数和客户端工厂，返回退出码。"""
    parser = make_parser("Execute one Cheat Engine Lua request")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source")
    group.add_argument("--file", type=Path)
    args = parser.parse_args(argv)
    try:
        source = read_text(args.source, args.file)
    except KeyboardInterrupt:
        return 130
    except (OSError, UnicodeError, ValueError) as error:
        print("ERROR: " + ascii(str(error)), file=sys.stderr)
        return 2
    request = {"source": source, "sourceFile": str(args.file) if args.file else None}
    return run_cli(args, "lua", request, source, client_factory=client_factory)


if __name__ == "__main__":
    sys.exit(main())
