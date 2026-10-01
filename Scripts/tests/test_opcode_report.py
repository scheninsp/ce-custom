"""opcode 报告校验、渲染和原子写入功能测试。"""

import copy
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from opcode_report import Target, atomic_text, validate_anchor, validate_window


def window(address="1064"):
    """生成指定地址的模拟连续指令窗口；参数为目标地址，返回响应字典。"""
    center = int(address, 16)
    return {
        "address": address,
        "instructions": [
            {"address": f"{center - 100 + i:X}", "addressText": f"test.exe+{i:X}",
             "opcode": "nop", "extra": "", "text": "nop", "bytes": "90", "size": 1}
            for i in range(201)
        ],
    }


class WindowTests(unittest.TestCase):
    def test_valid_window(self):
        """验证合法指令窗口可以通过校验；无参数和返回值。"""
        self.assertEqual(len(validate_window(Target("1064", "90"), window())), 201)

    def test_bad_windows(self):
        """验证缺失、断裂和重复目标窗口会被拒绝；无参数和返回值。"""
        base = window()
        variants = []
        short = copy.deepcopy(base)
        short["instructions"].pop()
        variants.append(short)
        for field, value in (("size", 0), ("bytes", "9090"), ("opcode", "db 90"),
                             ("address", "1064")):
            bad = copy.deepcopy(base)
            bad["instructions"][0][field] = value
            variants.append(bad)
        changed = copy.deepcopy(base)
        changed["instructions"][100]["bytes"] = "CC"
        variants.append(changed)
        shifted = window("1065")
        shifted["address"] = "1064"
        variants.append(shifted)
        for bad in variants:
            with self.subTest(bad=bad["instructions"][0]), self.assertRaises(ValueError):
                validate_window(Target("1064", "90"), bad)

    def test_anchor_validation(self):
        """验证锚点地址、长度和机器码校验；无参数和返回值。"""
        row = window()["instructions"][100]
        validate_anchor(Target("1064", "90"), {"instruction": row, "length": 1})
        cases = (
            {"instruction": {**row, "address": "1065"}, "length": 1},
            {"instruction": {**row, "bytes": "CC"}, "length": 1},
            {"instruction": {**row, "size": 2}, "length": 2},
            {"instruction": row, "length": 2},
        )
        for payload in cases:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                validate_anchor(Target("1064", "90"), payload)

    def test_atomic_write_failure_keeps_old_file(self):
        """验证原子写入失败时保留旧文件并清理临时文件；无参数和返回值。"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "opcode_1064.md"
            atomic_text(path, "old")
            with patch("opcode_report.os.replace", side_effect=PermissionError):
                with self.assertRaises(PermissionError):
                    atomic_text(path, "new")
            self.assertEqual(path.read_text(encoding="utf-8"), "old")
            self.assertEqual(list(Path(directory).glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
