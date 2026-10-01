"""校验 Cheat Engine 指令数据并渲染 opcode 报告文件。"""

import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Target:
    address: str
    expected_bytes: str


def hex_address(value: str) -> str:
    """规范化十六进制地址；参数为地址文本，返回无前缀的大写地址。"""
    if not isinstance(value, str) or not re.fullmatch(r"(?:0x)?[0-9A-Fa-f]+", value):
        raise ValueError("invalid hexadecimal address")
    number = int(value, 16)
    if not 0 < number < 2**64:
        raise ValueError("address outside uint64 range")
    return f"{number:X}"


def hex_bytes(value: str) -> str:
    """规范化机器码字节；参数为字节文本，返回连续的大写十六进制字符串。"""
    value = re.sub(r"\s+", "", value).upper()
    if not re.fullmatch(r"(?:[0-9A-F]{2}){1,15}", value):
        raise ValueError("invalid x86 instruction bytes")
    return value


def checked_instruction(row: dict) -> tuple[int, int]:
    """校验单条指令字段；参数为指令字典，返回整数地址和指令长度。"""
    address = int(hex_address(row["address"]), 16)
    size = row["size"]
    if type(size) is not int or not 1 <= size <= 15:
        raise ValueError("invalid instruction size")
    if len(hex_bytes(row["bytes"])) != size * 2:
        raise ValueError("instruction bytes and size disagree")
    for key in ("addressText", "opcode", "extra", "text"):
        if not isinstance(row[key], str):
            raise ValueError(f"invalid instruction field: {key}")
    opcode = row["opcode"].strip().lower()
    if not opcode or opcode.split()[0] in {"db", "??", "???", "invalid", "(bad)"}:
        raise ValueError("undecodable instruction")
    if address + size >= 2**64:
        raise ValueError("instruction address overflow")
    return address, size


def validate_anchor(target: Target, payload: dict) -> None:
    """校验目标锚点指令；参数为目标和 CE 响应，成功时无返回值，失败抛出异常。"""
    row = payload["instruction"]
    address, size = checked_instruction(row)
    if address != int(target.address, 16) or payload["length"] != size:
        raise ValueError("anchor address or length mismatch")
    if hex_bytes(row["bytes"]) != target.expected_bytes:
        raise ValueError("source bytes mismatch; refresh the source report")


def validate_window(target: Target, payload: dict, before: int = 100,
                    after: int = 100) -> list[dict]:
    """校验目标居中的连续指令窗口；参数为目标、响应及前后条数，返回指令列表。"""
    if hex_address(payload["address"]) != target.address:
        raise ValueError("response address mismatch")
    rows = payload["instructions"]
    expected_count = before + after + 1
    if not isinstance(rows, list) or len(rows) != expected_count:
        raise ValueError(f"expected exactly {expected_count} instructions")
    positions, previous_end = [], None
    for index, row in enumerate(rows):
        address, size = checked_instruction(row)
        if previous_end is not None and address != previous_end:
            raise ValueError("instruction window is not contiguous")
        previous_end = address + size
        if address == int(target.address, 16):
            positions.append(index)
    if positions != [before]:
        raise ValueError(f"target must occur exactly once at index {before}")
    if hex_bytes(rows[before]["bytes"]) != target.expected_bytes:
        raise ValueError("target bytes changed or source report is stale")
    return rows


def md(value) -> str:
    """转义 Markdown 表格文本；参数为任意值，返回单行安全字符串。"""
    return str(value).replace("\r", " ").replace("\n", " ").replace("|", r"\|")


def render_target(target: Target, record: dict, rows: list[dict], metadata: dict) -> str:
    """渲染单个目标的 Markdown 报告；参数为目标、记录、指令和元数据，返回文本。"""
    lines = [
        f"# Opcode window {target.address}", "",
        f"- Status: {record['status']}",
        f"- Run: {metadata['runId']}",
        f"- CE instance: {metadata['instanceId']}",
        f"- Target PID: {metadata['processId']}",
        f"- Captured at: {record['capturedAt']}",
        f"- Requested: {metadata.get('before', 100)} before + target + {metadata.get('after', 100)} after",
        "- Boundary method: CE estimated predecessors; continuity checked on success",
        "- Capture mode: live reads, not an atomic process snapshot",
        "- Expected target bytes: " + target.expected_bytes, "",
    ]
    if record["status"] != "success":
        return "\n".join(lines + ["## Failure", "", md(record["error"]), ""])
    before = metadata.get("before", 100)
    after = metadata.get("after", 100)
    if len(rows) != before + after + 1:
        raise ValueError("refusing to render an incomplete successful window")
    lines += ["## Instructions", "",
              "| Offset | Address | CE address | Bytes | Opcode | Extra | Marker |",
              "| ---: | --- | --- | --- | --- | --- | --- |"]
    for index, row in enumerate(rows):
        byte_text = " ".join(f"{b:02X}" for b in bytes.fromhex(row["bytes"]))
        marker = "TARGET" if index == before else ""
        values = [index - before, row["address"], row["addressText"],
                  byte_text, row["opcode"], row["extra"], marker]
        lines.append("| " + " | ".join(md(value) for value in values) + " |")
    return "\n".join(lines) + "\n"


def atomic_text(path: Path, text: str) -> None:
    """以临时文件替换方式原子写入文本；参数为目标路径和内容，无返回值。"""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n",
            dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False,
        ) as handle:
            temporary = Path(handle.name)
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
