import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ce_mcp_client import McpClient, ToolError, TransportError

SERVER = r'''
import json, sys, time
for line in sys.stdin:
    request = json.loads(line)
    if "id" not in request:
        continue
    method, params = request["method"], request["params"]
    if method == "initialize":
        result = {"protocolVersion": "2025-06-18"}
    elif method == "tools/list":
        result = {"tools": [{"name": "b"}]} if params else {
            "tools": [{"name": "a"}], "nextCursor": "page2"}
    else:
        name = params["name"]
        if name == "slow":
            time.sleep(3)
        if name == "eof":
            sys.exit(0)
        if name == "error":
            result = {"isError": True, "structuredContent": {
                "error": {"kind": "memory_read_failed", "message": "unreadable"}}}
        elif name == "text":
            result = {"content": [{"type": "text", "text": "{\"ok\":true}"}]}
        else:
            result = {"structuredContent": {"ok": True}}
        if name == "wrong_id":
            request["id"] += 1
    print(json.dumps({"jsonrpc": "2.0", "method": "notifications/message"}), flush=True)
    print(json.dumps({"jsonrpc": "2.0", "id": request["id"], "result": result}), flush=True)
'''


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        server = root / "server.py"
        server.write_text(SERVER, encoding="utf-8")
        self.client = McpClient([sys.executable, str(server)], 2, root / "stderr.log")
        self.addCleanup(self.client.close)
        self.client.start()

    def test_handshake_pagination_and_results(self):
        self.assertEqual(set(self.client.tools()), {"a", "b"})
        self.assertEqual(self.client.call("ok", {}), {"ok": True})
        self.assertEqual(self.client.call("text", {}), {"ok": True})

    def test_tool_failure(self):
        with self.assertRaises(ToolError) as caught:
            self.client.call("error", {})
        self.assertEqual(caught.exception.kind, "memory_read_failed")
        self.assertEqual(self.client.call("ok", {}), {"ok": True})

    def test_timeout_invalidates_connection(self):
        self.client.timeout = 0.05
        with self.assertRaisesRegex(TransportError, "timed out"):
            self.client.call("slow", {})
        with self.assertRaises(TransportError):
            self.client.call("ok", {})

    def test_eof(self):
        with self.assertRaises(TransportError):
            self.client.call("eof", {})

    def test_wrong_id(self):
        with self.assertRaisesRegex(TransportError, "response id"):
            self.client.call("wrong_id", {})


if __name__ == "__main__":
    unittest.main()
