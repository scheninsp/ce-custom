# Stacktrace and Registers at Breakpoint 7FF777CED5C9

- Captured at: 2026-10-01T16:27:03.922261+00:00
- CE instance: ce-72480-42f4ba0154dd4fbd8087223e0f808fda
- Process: victoria3 (PID 43884)
- Pointer width: 8 bytes (64 bits)
- Active debugger interface: windows
- Status source: lua&#95;execute&#95;fixed&#95;query
- Final status source: lua&#95;execute&#95;fixed&#95;query
- Status: stopped
- includeExtraRegisters=true
- Stack depth: 128 slots
- residueCheck: unchanged

## Registers

All returned registers are preserved; unavailable FP/XMM registers are not inferred.
FP/XMM byte sequences are in memory order, little-endian (least significant byte first).

| Register | Value |
| --- | --- |
| EFLAGS | 202 |
| FP0 | 00 00 00 00 00 00 00 00 00 00 |
| FP1 | 00 00 00 00 00 00 00 00 00 00 |
| FP2 | 00 00 00 00 00 00 00 00 00 00 |
| FP3 | 00 00 00 00 00 00 00 00 00 00 |
| FP4 | 00 00 00 00 00 00 00 00 00 00 |
| FP5 | 00 00 00 00 00 00 00 00 00 00 |
| FP6 | 00 00 00 00 00 00 00 00 00 00 |
| FP7 | 00 00 00 00 00 00 00 00 00 00 |
| R10 | 36F |
| R11 | B504F333 |
| R12 | 0 |
| R13 | 8C5DE8DC90 |
| R14 | 3A484D9DB60 |
| R15 | 7FF77AF75198 |
| R8 | A |
| R9 | 0 |
| RAX | 7E |
| RBP | 8C5DE8DD30 |
| RBX | 3A57395A770 |
| RCX | FFFFFFEB88C07100 |
| RDI | 3A5FF822A80 |
| RDX | FFFFFFFFFFF29668 |
| RIP | 7FF777CED5C9 |
| RSI | 3A5FF822B30 |
| RSP | 8C5DE8D870 |
| THREADID | 60D0 |
| XMM0 | 08 00 D9 84 A4 03 00 00 6E 98 88 06 00 00 00 00 |
| XMM1 | 2A 00 D9 84 A4 03 00 00 00 00 00 00 00 00 00 00 |
| XMM10 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM11 | 00 00 00 00 00 00 4E 40 00 00 00 00 00 00 00 00 |
| XMM12 | 00 00 00 00 00 00 00 00 0F 00 00 00 00 00 00 00 |
| XMM13 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM14 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM15 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM2 | 56 21 71 33 00 00 00 00 09 DA E3 35 00 00 00 00 |
| XMM3 | DC C7 02 00 00 00 00 00 08 E9 D8 02 00 00 00 00 |
| XMM4 | A5 5B 8C 0E 00 00 00 00 5E B9 ED 02 00 00 00 00 |
| XMM5 | 2C 00 D9 84 A4 03 00 00 00 00 00 00 00 00 00 00 |
| XMM6 | 00 00 C0 3F 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM7 | 76 8F C7 67 0D 39 11 3F 00 00 00 00 00 00 00 00 |
| XMM8 | 00 00 00 00 65 CD CD 41 00 00 00 00 00 00 00 00 |
| XMM9 | 00 00 00 00 00 40 8F 40 00 00 00 00 00 00 00 00 |

## Stacktrace

Stack pointer: 8C5DE8D870
Scanned slots: 128 (maximum 128).

| Index | Stack slot address | Return address | Call instruction | isHeuristic |
| ---: | --- | --- | --- | --- |
| 0 | 8C5DE8DB98 | 7FF777E0D21E | 7FF777E0D219 - E8 5202EEFF - call 7FF777CED470 | true |

## Capture Contract

Captured using read-only debugger queries, with a fixed Lua query for the known status compatibility issue when needed.
Keep CE stopped throughout capture. Original status errors and compatibility query results are preserved below.
The address is the current RIP/EIP, which may differ from a registered breakpoint address.
Stacktrace frames are heuristic candidates, not a symbolicated or confirmed call chain.
Call instructions are optional candidate information; verify against the breakpoint scene and disassembly.
Before/after stopped-state and session checks cannot detect a resume/re-break between calls.
No attach, breakpoint changes, continue, or target memory writes are performed.

## Raw MCP Snapshot

```json
{
  "address": "7FF777CED5C9",
  "capturedAt": "2026-10-01T16:27:03.922261+00:00",
  "context": {
    "includesExtraRegisters": true,
    "is64Bit": true,
    "registers": {
      "EFLAGS": "202",
      "FP0": "00 00 00 00 00 00 00 00 00 00",
      "FP1": "00 00 00 00 00 00 00 00 00 00",
      "FP2": "00 00 00 00 00 00 00 00 00 00",
      "FP3": "00 00 00 00 00 00 00 00 00 00",
      "FP4": "00 00 00 00 00 00 00 00 00 00",
      "FP5": "00 00 00 00 00 00 00 00 00 00",
      "FP6": "00 00 00 00 00 00 00 00 00 00",
      "FP7": "00 00 00 00 00 00 00 00 00 00",
      "R10": "36F",
      "R11": "B504F333",
      "R12": "0",
      "R13": "8C5DE8DC90",
      "R14": "3A484D9DB60",
      "R15": "7FF77AF75198",
      "R8": "A",
      "R9": "0",
      "RAX": "7E",
      "RBP": "8C5DE8DD30",
      "RBX": "3A57395A770",
      "RCX": "FFFFFFEB88C07100",
      "RDI": "3A5FF822A80",
      "RDX": "FFFFFFFFFFF29668",
      "RIP": "7FF777CED5C9",
      "RSI": "3A5FF822B30",
      "RSP": "8C5DE8D870",
      "THREADID": "60D0",
      "XMM0": "08 00 D9 84 A4 03 00 00 6E 98 88 06 00 00 00 00",
      "XMM1": "2A 00 D9 84 A4 03 00 00 00 00 00 00 00 00 00 00",
      "XMM10": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM11": "00 00 00 00 00 00 4E 40 00 00 00 00 00 00 00 00",
      "XMM12": "00 00 00 00 00 00 00 00 0F 00 00 00 00 00 00 00",
      "XMM13": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM14": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM15": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM2": "56 21 71 33 00 00 00 00 09 DA E3 35 00 00 00 00",
      "XMM3": "DC C7 02 00 00 00 00 00 08 E9 D8 02 00 00 00 00",
      "XMM4": "A5 5B 8C 0E 00 00 00 00 5E B9 ED 02 00 00 00 00",
      "XMM5": "2C 00 D9 84 A4 03 00 00 00 00 00 00 00 00 00 00",
      "XMM6": "00 00 C0 3F 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM7": "76 8F C7 67 0D 39 11 3F 00 00 00 00 00 00 00 00",
      "XMM8": "00 00 00 00 65 CD CD 41 00 00 00 00 00 00 00 00",
      "XMM9": "00 00 00 00 00 40 8F 40 00 00 00 00 00 00 00 00"
    }
  },
  "finalFingerprint": {
    "pointerSize": 8,
    "processId": 43884,
    "runtimeEpoch": 1,
    "selectionEpoch": 0
  },
  "finalOverview": {
    "jobCount": 0,
    "process": {
      "isOpen": true,
      "pointerSize": 8,
      "processId": 43884,
      "processName": "victoria3",
      "selectionEpoch": 0
    },
    "resourceCount": 0,
    "runtime": {
      "applicationName": "CheatEngine.Mcp",
      "epoch": 1,
      "gates": {
        "autoAssembler": true,
        "kernelAccess": true,
        "targetCodeExecution": true,
        "unsafeLua": true
      },
      "pluginFileName": "CheatEngine.Mcp.dll",
      "pluginVersion": "2.0.0.0",
      "runtimeFileName": "CheatEngine.Mcp.dll"
    }
  },
  "finalStatus": {
    "activeInterface": "windows",
    "attached": true,
    "broken": true,
    "instructionPointer": "7FF777CED5C9",
    "is64Bit": true,
    "luaResponse": {
      "droppedOpaqueCount": 0,
      "hostEffect": "completed",
      "ok": true,
      "returnValues": [
        {
          "activeInterface": "windows",
          "attached": true,
          "broken": true,
          "instructionPointer": "7FF777CED5C9",
          "is64Bit": true,
          "stackPointer": "8C5DE8D870",
          "stateValid": true
        }
      ]
    },
    "originalStatus": {
      "attached": false,
      "broken": false,
      "canBreak": false,
      "error": "CheatEngine.Mcp/debugger_get_status:4: debug_isBroken did not return a boolean debugger state",
      "reportedBroken": false,
      "stateValid": false,
      "stepping": false
    },
    "stackPointer": "8C5DE8D870",
    "stateValid": true,
    "statusSource": "lua_execute_fixed_query"
  },
  "instanceId": "ce-72480-42f4ba0154dd4fbd8087223e0f808fda",
  "process": {
    "isOpen": true,
    "pointerSize": 8,
    "processId": 43884,
    "processName": "victoria3",
    "selectionEpoch": 0
  },
  "residueCheck": {
    "after": {
      "jobCount": 0,
      "resourceCount": 0
    },
    "before": {
      "jobCount": 0,
      "resourceCount": 0
    },
    "state": "unchanged"
  },
  "runtime": {
    "fingerprint": {
      "pointerSize": 8,
      "processId": 43884,
      "runtimeEpoch": 1,
      "selectionEpoch": 0
    },
    "info": {
      "applicationName": "CheatEngine.Mcp",
      "epoch": 1,
      "gates": {
        "autoAssembler": true,
        "kernelAccess": true,
        "targetCodeExecution": true,
        "unsafeLua": true
      },
      "pluginFileName": "CheatEngine.Mcp.dll",
      "pluginVersion": "2.0.0.0",
      "runtimeFileName": "CheatEngine.Mcp.dll"
    },
    "overview": {
      "jobCount": 0,
      "process": {
        "isOpen": true,
        "pointerSize": 8,
        "processId": 43884,
        "processName": "victoria3",
        "selectionEpoch": 0
      },
      "resourceCount": 0,
      "runtime": {
        "applicationName": "CheatEngine.Mcp",
        "epoch": 1,
        "gates": {
          "autoAssembler": true,
          "kernelAccess": true,
          "targetCodeExecution": true,
          "unsafeLua": true
        },
        "pluginFileName": "CheatEngine.Mcp.dll",
        "pluginVersion": "2.0.0.0",
        "runtimeFileName": "CheatEngine.Mcp.dll"
      }
    },
    "resources": {
      "jobCount": 0,
      "resourceCount": 0
    },
    "statusCompatAvailable": true
  },
  "stacktrace": {
    "frames": [
      {
        "callInstruction": "7FF777E0D219 - E8 5202EEFF - call 7FF777CED470",
        "isHeuristic": true,
        "returnAddress": "7FF777E0D21E",
        "stackAddress": "8C5DE8DB98"
      }
    ],
    "pointerSize": 8,
    "scannedSlots": 128,
    "stackPointer": "8C5DE8D870"
  },
  "status": {
    "activeInterface": "windows",
    "attached": true,
    "broken": true,
    "instructionPointer": "7FF777CED5C9",
    "is64Bit": true,
    "luaResponse": {
      "droppedOpaqueCount": 0,
      "hostEffect": "completed",
      "ok": true,
      "returnValues": [
        {
          "activeInterface": "windows",
          "attached": true,
          "broken": true,
          "instructionPointer": "7FF777CED5C9",
          "is64Bit": true,
          "stackPointer": "8C5DE8D870",
          "stateValid": true
        }
      ]
    },
    "originalStatus": {
      "attached": false,
      "broken": false,
      "canBreak": false,
      "error": "CheatEngine.Mcp/debugger_get_status:4: debug_isBroken did not return a boolean debugger state",
      "reportedBroken": false,
      "stateValid": false,
      "stepping": false
    },
    "stackPointer": "8C5DE8D870",
    "stateValid": true,
    "statusSource": "lua_execute_fixed_query"
  }
}
```
