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
    if not isinstance(value, str) or not re.fullmatch(r"(?:0x)?[0-9A-Fa-f]+", value):
        raise ValueError("invalid hexadecimal address")
    number = int(value, 16)
    if not 0 < number < 2**64:
        raise ValueError("address outside uint64 range")
    return f"{number:X}"


def hex_bytes(value: str) -> str:
    value = re.sub(r"\s+", "", value).upper()
    if not re.fullmatch(r"(?:[0-9A-F]{2}){1,15}", value):
        raise ValueError("invalid x86 instruction bytes")
    return value


def checked_instruction(row: dict) -> tuple[int, int]:
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
    row = payload["instruction"]
    address, size = checked_instruction(row)
    if address != int(target.address, 16) or payload["length"] != size:
        raise ValueError("anchor address or length mismatch")
    if hex_bytes(row["bytes"]) != target.expected_bytes:
        raise ValueError("source bytes mismatch; refresh the source report")


def validate_window(target: Target, payload: dict) -> list[dict]:
    if hex_address(payload["address"]) != target.address:
        raise ValueError("response address mismatch")
    rows = payload["instructions"]
    if not isinstance(rows, list) or len(rows) != 201:
        raise ValueError("expected exactly 201 instructions")
    positions, previous_end = [], None
    for index, row in enumerate(rows):
        address, size = checked_instruction(row)
        if previous_end is not None and address != previous_end:
            raise ValueError("instruction window is not contiguous")
        previous_end = address + size
        if address == int(target.address, 16):
            positions.append(index)
    if positions != [100]:
        raise ValueError("target must occur exactly once at index 100")
    if hex_bytes(rows[100]["bytes"]) != target.expected_bytes:
        raise ValueError("target bytes changed or source report is stale")
    return rows


def md(value) -> str:
    return str(value).replace("\r", " ").replace("\n", " ").replace("|", r"\|")


def render_target(target: Target, record: dict, rows: list[dict], metadata: dict) -> str:
    lines = [
        f"# Opcode window {target.address}", "",
        f"- Status: {record['status']}",
        f"- Run: {metadata['runId']}",
        f"- CE instance: {metadata['instanceId']}",
        f"- Target PID: {metadata['processId']}",
        f"- Captured at: {record['capturedAt']}",
        "- Requested: 100 before + target + 100 after",
        "- Boundary method: CE estimated predecessors; continuity checked on success",
        "- Capture mode: live reads, not an atomic process snapshot",
        "- Expected target bytes: " + target.expected_bytes, "",
    ]
    if record["status"] != "success":
        return "\n".join(lines + ["## Failure", "", md(record["error"]), ""])
    if len(rows) != 201:
        raise ValueError("refusing to render an incomplete successful window")
    lines += ["## Instructions", "",
              "| Offset | Address | CE address | Bytes | Opcode | Extra | Marker |",
              "| ---: | --- | --- | --- | --- | --- | --- |"]
    for index, row in enumerate(rows):
        byte_text = " ".join(f"{b:02X}" for b in bytes.fromhex(row["bytes"]))
        marker = "TARGET" if index == 100 else ""
        values = [index - 100, row["address"], row["addressText"],
                  byte_text, row["opcode"], row["extra"], marker]
        lines.append("| " + " | ".join(md(value) for value in values) + " |")
    return "\n".join(lines) + "\n"


def atomic_text(path: Path, text: str) -> None:
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
