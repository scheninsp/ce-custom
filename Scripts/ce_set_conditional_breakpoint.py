"""在指定地址添加一个原生条件执行断点，保存并读回；不继续目标或清理断点。"""

import re
import sys
from pathlib import Path
from ce_mcp_client import McpClient
from ce_lua_common import lua_quote, make_parser, read_text, run_cli


def build_condition_source(address, condition_type, condition):
    """构造固定后端请求；入参为地址、条件类型和文本，返回安全编码的 Lua 源码。"""
    absolute = re.fullmatch(r"(?:0[xX])?([0-9a-fA-F]{1,16})", address)
    relative = re.fullmatch(r"victoria3\.exe\+([0-9a-fA-F]{1,16})", address)
    if not (absolute or relative) or (absolute and int(absolute[1], 16) == 0):
        raise ValueError("invalid breakpoint address")
    if condition_type not in {"simple", "complex"}:
        raise ValueError("invalid condition type")
    if condition_type == "simple" and "\n" in condition:
        raise ValueError("simple condition must be a single expression")
    normalized = f"{int(absolute[1], 16):X}" if absolute else address
    prefix = (
        "local request = {address=" + lua_quote(normalized)
        + ",conditionType=" + lua_quote(condition_type)
        + ",condition=" + lua_quote(condition) + "}\n"
    )
    backend = Path(__file__).with_name("ce_native_condition.lua").read_text(encoding="utf-8")
    source = prefix + backend
    if len(source.encode("utf-8")) > 65536:
        raise ValueError("assembled Lua source exceeds the local limit")
    return source


def validate_condition_result(response, request):
    """验证条件业务回执；入参为 Lua 响应和请求，返回成功业务对象，否则抛出异常。"""
    values = response["returnValues"]
    if len(values) != 1 or not isinstance(values[0], dict):
        raise ValueError("expected one native condition result")
    result = values[0]
    if any(result.get(key) is not True for key in ("ok", "created", "conditionReadbackMatched")):
        raise ValueError("native condition setup is incomplete")
    if result.get("backend") != "native-ui" or result.get("phase") != "completed":
        raise ValueError("unexpected condition backend or phase")
    if result.get("conditionType") != request["conditionType"] or result.get("condition") != request["source"]:
        raise ValueError("condition receipt differs from request")
    address = result.get("address")
    if not isinstance(address, str) or not re.fullmatch(r"[0-9A-F]{1,16}", address) or int(address, 16) == 0:
        raise ValueError("invalid resolved breakpoint address")
    absolute = re.fullmatch(r"(?:0[xX])?([0-9a-fA-F]{1,16})", request.get("address", ""))
    if absolute and int(address, 16) != int(absolute[1], 16):
        raise ValueError("resolved absolute address differs from request")
    thread_before = result.get("threadIdBefore")
    if not isinstance(thread_before, str) or not re.fullmatch(r"[0-9A-F]{1,16}", thread_before) or int(thread_before, 16) == 0:
        raise ValueError("invalid stopped thread receipt")
    if result.get("threadIdAfter") != thread_before:
        raise ValueError("stopped thread changed")
    return result


def main(argv=None, client_factory=McpClient):
    """添加一个原生条件断点；入参为命令参数和客户端工厂，返回退出码。"""
    parser = make_parser("Add one native conditional execute breakpoint")
    parser.add_argument("--address", required=True)
    parser.add_argument("--condition-type", choices=("simple", "complex"), required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--condition")
    group.add_argument("--condition-file", type=Path)
    args = parser.parse_args(argv)
    try:
        condition = read_text(args.condition, args.condition_file)
        source = build_condition_source(args.address, args.condition_type, condition)
    except KeyboardInterrupt:
        return 130
    except (OSError, UnicodeError, ValueError) as error:
        print("ERROR: " + ascii(str(error)), file=sys.stderr)
        return 2
    request = {"address": args.address, "conditionType": args.condition_type, "source": condition,
               "sourceFile": str(args.condition_file) if args.condition_file else None}
    return run_cli(args, "condition", request, source, client_factory=client_factory,
                   result_validator=validate_condition_result)


if __name__ == "__main__":
    sys.exit(main())
