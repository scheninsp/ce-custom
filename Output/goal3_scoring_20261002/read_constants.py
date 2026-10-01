"""只读记录评分常量与候选，并核对采集前后的暂停现场；不执行目标代码。"""
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parents[1] / "Scripts"))
from ce_mcp_client import McpClient
from get_stacktrace_register_at_breakpoint import DEFAULT_GATEWAY, select_instance, read_status, require_stopped


def main():
    """采集常量及候选；无入参，向本目录写入证据 JSON，无返回值。"""
    addresses = {
        "tariff_weight": "7FF77C37A8C8", "subvention_weight": "7FF77C37A8A8",
        "new_goods_multiplier": "7FF77C37A8D0", "opposite_share_weight": "7FF77C37A8C0",
        "shortage_weight": "7FF77C37A8E0", "random_factor": "7FF77C37A918",
        "world_demand_buffer": "7FF77C379E20", "quantity_limit_factor": "7FF77C379D10",
        "shortage_threshold": "7FF77C379D08", "shortage_max": "7FF77C379CF0",
    }
    client = McpClient([str(DEFAULT_GATEWAY)], 30, OUT / "constants.stderr.log").start()
    evidence = {}
    try:
        iid = select_instance(client, None)
        before = read_status(client, iid, compat_available=True)
        require_stopped(before)
        assert before["instructionPointer"] == "7FF777CED5C9"
        assert before["stackPointer"] == "8C5DE8D870"
        evidence["before"] = before
        evidence["registersBefore"] = client.call("debugger_get_context", {"instanceId": iid, "includeExtraRegisters": True})
        evidence["names"] = addresses
        items = [{"address": address, "valueType": "int64"} for address in addresses.values()]
        items += [{"address": "3A5FF822A80", "valueType": "bytes", "size": 320}]
        evidence["reads"] = client.call("memory_read_batch", {"instanceId": iid, "items": items})
        assert evidence["reads"]["failed"] == 0
        evidence["registersAfter"] = client.call("debugger_get_context", {"instanceId": iid, "includeExtraRegisters": True})
        evidence["after"] = read_status(client, iid, compat_available=True)
        require_stopped(evidence["after"])
        assert evidence["after"]["instructionPointer"] == before["instructionPointer"]
        assert evidence["after"]["stackPointer"] == before["stackPointer"]
        evidence["registersUnchanged"] = evidence["registersBefore"] == evidence["registersAfter"]
        assert evidence["registersUnchanged"]
        print(json.dumps(evidence["reads"]["items"][:len(addresses)]))
    finally:
        (OUT / "constants_snapshot.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
        client.close()


if __name__ == "__main__":
    main()
