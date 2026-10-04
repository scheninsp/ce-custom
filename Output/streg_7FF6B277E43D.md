# Stacktrace and Registers at Breakpoint 7FF6B277E43D

- Captured at: 2026-10-04T12:06:44.309038+00:00
- CE instance: ce-27656-feb613268bc942f3b77a51a1385c8c93
- Process: victoria3 (PID 12472)
- Pointer width: 8 bytes (64 bits)
- Active debugger interface: windows
- Status source: lua&#95;execute&#95;fixed&#95;query
- Final status source: lua&#95;execute&#95;fixed&#95;query
- Status: stopped
- includeExtraRegisters=true
- Stack source: CE View > StackTrace (StackWalk64)
- Stack frames: 6
- Unwind termination: zero_return
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
| R10 | 546C6148 |
| R11 | 5F6C7D6CB8A |
| R12 | 0 |
| R13 | 0 |
| R14 | 0 |
| R15 | 0 |
| R8 | 83 |
| R9 | 7FFED000 |
| RAX | 4B33404ED3E01 |
| RBP | 0 |
| RBX | 7FF6B4592658 |
| RCX | C08333FCFFD |
| RDI | 0 |
| RDX | 6116B690473 |
| RIP | 7FF6B277E43D |
| RSI | 0 |
| RSP | 9E6BCFB80 |
| THREADID | 14120 |
| XMM0 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM1 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM10 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM11 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM12 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM13 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM14 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM15 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM2 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM3 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM4 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM5 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM6 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM7 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM8 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM9 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |

## Stacktrace

Stack pointer: 9E6BCFB80
Frames exported: 6 (all rows returned by CE; no 128-slot scan).
Parameters are CE's displayed summaries, not decoded x64 function arguments.
The final frame has a zero return address.

| Index | PC | Stack | Frame | Return | Parameters |
| ---: | --- | --- | --- | --- | --- |
| 0 | victoria3.exe+3ACE43D | 9E6BCFB80 | 9E6BCFBA0 | victoria3.exe+3ACD8CE | 7BFE81C0,00000000,E6BCFBA8,E6BCFBB0,... |
| 1 | victoria3.exe+3ACD8CE | 9E6BCFBB0 | 9E6BCFBD0 | victoria3.exe+3B27992 | 00000000,00000000,00000005,00000005,... |
| 2 | victoria3.exe+3B27992 | 9E6BCFBE0 | 9E6BCFC00 | victoria3.exe+4160DCA | 356B6DC0,00000000,00000000,00000000,... |
| 3 | victoria3.exe+4160DCA | 9E6BCFC10 | 9E6BCFC30 | KERNEL32.BaseThreadInitThunk+17 | 00000000,00000000,00000000,00000000,... |
| 4 | KERNEL32.BaseThreadInitThunk+17 | 9E6BCFC40 | 9E6BCFC60 | ntdll.RtlUserThreadStart+2C | 00000000,00000000,FFFFFB30,FFFFFB30,... |
| 5 | ntdll.RtlUserThreadStart+2C | 9E6BCFC70 | 9E6BCFCB0 | 00000000 | 00000000,00000000,00000000,00000000,... |

## Capture Contract

Captured using debugger reads and fixed Lua queries; native stack mode also refreshes CE's StackTrace UI.
Keep CE stopped throughout capture. Original status errors and compatibility query results are preserved below.
The address is the current RIP/EIP, which may differ from a registered breakpoint address.
The native StackTrace window is refreshed; a window opened by this query is closed after copying.
Every row returned by CE is exported. Unwind results depend on CE, target unwind metadata and readable memory.
PC/SP/BP/thread identity is checked against the stopped context before and after capture.
Before/after stopped-state and session checks cannot detect a resume/re-break between calls.
No attach, breakpoint changes, continue, or target memory writes are performed.

## Raw MCP Snapshot

```json
{
  "address": "7FF6B277E43D",
  "capturedAt": "2026-10-04T12:06:44.309038+00:00",
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
      "R10": "546C6148",
      "R11": "5F6C7D6CB8A",
      "R12": "0",
      "R13": "0",
      "R14": "0",
      "R15": "0",
      "R8": "83",
      "R9": "7FFED000",
      "RAX": "4B33404ED3E01",
      "RBP": "0",
      "RBX": "7FF6B4592658",
      "RCX": "C08333FCFFD",
      "RDI": "0",
      "RDX": "6116B690473",
      "RIP": "7FF6B277E43D",
      "RSI": "0",
      "RSP": "9E6BCFB80",
      "THREADID": "14120",
      "XMM0": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM1": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM10": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM11": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM12": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM13": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM14": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM15": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM2": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM3": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM4": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM5": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM6": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM7": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM8": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM9": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
    }
  },
  "finalFingerprint": {
    "pointerSize": 8,
    "processId": 12472,
    "runtimeEpoch": 1,
    "selectionEpoch": 0
  },
  "finalOverview": {
    "jobCount": 0,
    "process": {
      "isOpen": true,
      "pointerSize": 8,
      "processId": 12472,
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
    "instructionPointer": "7FF6B277E43D",
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
          "instructionPointer": "7FF6B277E43D",
          "is64Bit": true,
          "stackPointer": "9E6BCFB80",
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
    "stackPointer": "9E6BCFB80",
    "stateValid": true,
    "statusSource": "lua_execute_fixed_query"
  },
  "instanceId": "ce-27656-feb613268bc942f3b77a51a1385c8c93",
  "process": {
    "isOpen": true,
    "pointerSize": 8,
    "processId": 12472,
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
      "processId": 12472,
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
        "processId": 12472,
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
    "stackMode": "native",
    "statusCompatAvailable": true
  },
  "stacktrace": {
    "frameCount": 6,
    "framePointer": "0",
    "frames": [
      {
        "frameAddress": "9E6BCFBA0",
        "parameters": "7BFE81C0,00000000,E6BCFBA8,E6BCFBB0,...",
        "pc": "victoria3.exe+3ACE43D",
        "pcAddress": "7FF6B277E43D",
        "returnAddress": "7FF6B277D8CE",
        "returnSymbol": "victoria3.exe+3ACD8CE",
        "stackAddress": "9E6BCFB80"
      },
      {
        "frameAddress": "9E6BCFBD0",
        "parameters": "00000000,00000000,00000005,00000005,...",
        "pc": "victoria3.exe+3ACD8CE",
        "pcAddress": "7FF6B277D8CE",
        "returnAddress": "7FF6B27D7992",
        "returnSymbol": "victoria3.exe+3B27992",
        "stackAddress": "9E6BCFBB0"
      },
      {
        "frameAddress": "9E6BCFC00",
        "parameters": "356B6DC0,00000000,00000000,00000000,...",
        "pc": "victoria3.exe+3B27992",
        "pcAddress": "7FF6B27D7992",
        "returnAddress": "7FF6B2E10DCA",
        "returnSymbol": "victoria3.exe+4160DCA",
        "stackAddress": "9E6BCFBE0"
      },
      {
        "frameAddress": "9E6BCFC30",
        "parameters": "00000000,00000000,00000000,00000000,...",
        "pc": "victoria3.exe+4160DCA",
        "pcAddress": "7FF6B2E10DCA",
        "returnAddress": "7FF9E12CCD87",
        "returnSymbol": "KERNEL32.BaseThreadInitThunk+17",
        "stackAddress": "9E6BCFC10"
      },
      {
        "frameAddress": "9E6BCFC60",
        "parameters": "00000000,00000000,FFFFFB30,FFFFFB30,...",
        "pc": "KERNEL32.BaseThreadInitThunk+17",
        "pcAddress": "7FF9E12CCD87",
        "returnAddress": "7FF9E2F4CAEC",
        "returnSymbol": "ntdll.RtlUserThreadStart+2C",
        "stackAddress": "9E6BCFC40"
      },
      {
        "frameAddress": "9E6BCFCB0",
        "parameters": "00000000,00000000,00000000,00000000,...",
        "pc": "ntdll.RtlUserThreadStart+2C",
        "pcAddress": "7FF9E2F4CAEC",
        "returnAddress": "0",
        "returnSymbol": "00000000",
        "stackAddress": "9E6BCFC70"
      }
    ],
    "instructionPointer": "7FF6B277E43D",
    "pointerSize": 8,
    "source": "ce_stacktrace_window",
    "stackPointer": "9E6BCFB80",
    "temporaryWindow": false,
    "termination": "zero_return",
    "threadId": "14120"
  },
  "status": {
    "activeInterface": "windows",
    "attached": true,
    "broken": true,
    "instructionPointer": "7FF6B277E43D",
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
          "instructionPointer": "7FF6B277E43D",
          "is64Bit": true,
          "stackPointer": "9E6BCFB80",
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
    "stackPointer": "9E6BCFB80",
    "stateValid": true,
    "statusSource": "lua_execute_fixed_query"
  }
}
```
