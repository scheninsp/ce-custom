# Stacktrace and Registers at Breakpoint 7FF777CED5C9

- Captured at: 2026-10-01T16:29:38.027010+00:00
- CE instance: ce-72480-42f4ba0154dd4fbd8087223e0f808fda
- Process: victoria3 (PID 43884)
- Pointer width: 8 bytes (64 bits)
- Active debugger interface: windows
- Status source: lua&#95;execute&#95;fixed&#95;query
- Final status source: lua&#95;execute&#95;fixed&#95;query
- Status: stopped
- includeExtraRegisters=true
- Stack source: CE View > StackTrace (StackWalk64)
- Stack frames: 17
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
Frames exported: 17 (all rows returned by CE; no 128-slot scan).
Parameters are CE's displayed summaries, not decoded x64 function arguments.
The final frame has a zero return address.

| Index | PC | Stack | Frame | Return | Parameters |
| ---: | --- | --- | --- | --- | --- |
| 0 | victoria3.exe+11FD5C9 | 8C5DE8D870 | 8C5DE8DB90 | victoria3.exe+131D21E | 0000007E,7395A720,7395A770,5DE8DD80,... |
| 1 | victoria3.exe+131D21E | 8C5DE8DBA0 | 8C5DE8EEE0 | victoria3.exe+7B8563 | 47E29B08,FF8302C0,6E0A6930,6E25DCF0,... |
| 2 | victoria3.exe+7B8563 | 8C5DE8EEF0 | 8C5DE8F340 | victoria3.exe+7BE76D | 0000021B,00000000,73A61E78,00000000,... |
| 3 | victoria3.exe+7BE76D | 8C5DE8F350 | 8C5DE8F660 | victoria3.exe+7D65A8 | FE78BD00,6E420C88,0000001C,1AE39FE8,... |
| 4 | victoria3.exe+7D65A8 | 8C5DE8F670 | 8C5DE8F710 | victoria3.exe+137C9E7 | FE76B9B8,00000003,6E420C80,00000000,... |
| 5 | victoria3.exe+137C9E7 | 8C5DE8F720 | 8C5DE8F840 | victoria3.exe+CC0D4D | 00000000,FE76B9B8,00000000,5DE8F930,... |
| 6 | victoria3.exe+CC0D4D | 8C5DE8F850 | 8C5DE8F9A0 | victoria3.exe+34624D9 | 0000000F,00000000,00000001,5DE8FAD0,... |
| 7 | victoria3.exe+34624D9 | 8C5DE8F9B0 | 8C5DE8F9F0 | victoria3.exe+346253C | 5DE8FA30,00000000,00000000,00000000,... |
| 8 | victoria3.exe+346253C | 8C5DE8FA00 | 8C5DE8FA50 | victoria3.exe+332786F | 5DE8FAC0,00000000,7C3D25A0,5DE8003D,... |
| 9 | victoria3.exe+332786F | 8C5DE8FA60 | 8C5DE8FC80 | victoria3.exe+332BCE9 | 7C3D2500,00000001,00000000,00000000,... |
| 10 | victoria3.exe+332BCE9 | 8C5DE8FC90 | 8C5DE8FD40 | victoria3.exe+3ACE43D | 00000005,00000001,7C3D2658,00000000,... |
| 11 | victoria3.exe+3ACE43D | 8C5DE8FD50 | 8C5DE8FD70 | victoria3.exe+3ACD8CE | 61FE81C0,00000000,5DE8FD78,5DE8FD80,... |
| 12 | victoria3.exe+3ACD8CE | 8C5DE8FD80 | 8C5DE8FDA0 | victoria3.exe+3B27992 | 00000000,00000000,00000005,00000005,... |
| 13 | victoria3.exe+3B27992 | 8C5DE8FDB0 | 8C5DE8FDD0 | victoria3.exe+4160DCA | 6E070C40,00000000,00000000,00000000,... |
| 14 | victoria3.exe+4160DCA | 8C5DE8FDE0 | 8C5DE8FE00 | KERNEL32.BaseThreadInitThunk+17 | 00000000,00000000,00000000,00000000,... |
| 15 | KERNEL32.BaseThreadInitThunk+17 | 8C5DE8FE10 | 8C5DE8FE30 | ntdll.RtlUserThreadStart+2C | 00000000,00000000,FFFFFB30,FFFFFB30,... |
| 16 | ntdll.RtlUserThreadStart+2C | 8C5DE8FE40 | 8C5DE8FE80 | 00000000 | 00000000,00000000,00000000,00000000,... |

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
  "address": "7FF777CED5C9",
  "capturedAt": "2026-10-01T16:29:38.027010+00:00",
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
    "stackMode": "native",
    "statusCompatAvailable": true
  },
  "stacktrace": {
    "frameCount": 17,
    "framePointer": "8C5DE8DD30",
    "frames": [
      {
        "frameAddress": "8C5DE8DB90",
        "parameters": "0000007E,7395A720,7395A770,5DE8DD80,...",
        "pc": "victoria3.exe+11FD5C9",
        "pcAddress": "7FF777CED5C9",
        "returnAddress": "7FF777E0D21E",
        "returnSymbol": "victoria3.exe+131D21E",
        "stackAddress": "8C5DE8D870"
      },
      {
        "frameAddress": "8C5DE8EEE0",
        "parameters": "47E29B08,FF8302C0,6E0A6930,6E25DCF0,...",
        "pc": "victoria3.exe+131D21E",
        "pcAddress": "7FF777E0D21E",
        "returnAddress": "7FF7772A8563",
        "returnSymbol": "victoria3.exe+7B8563",
        "stackAddress": "8C5DE8DBA0"
      },
      {
        "frameAddress": "8C5DE8F340",
        "parameters": "0000021B,00000000,73A61E78,00000000,...",
        "pc": "victoria3.exe+7B8563",
        "pcAddress": "7FF7772A8563",
        "returnAddress": "7FF7772AE76D",
        "returnSymbol": "victoria3.exe+7BE76D",
        "stackAddress": "8C5DE8EEF0"
      },
      {
        "frameAddress": "8C5DE8F660",
        "parameters": "FE78BD00,6E420C88,0000001C,1AE39FE8,...",
        "pc": "victoria3.exe+7BE76D",
        "pcAddress": "7FF7772AE76D",
        "returnAddress": "7FF7772C65A8",
        "returnSymbol": "victoria3.exe+7D65A8",
        "stackAddress": "8C5DE8F350"
      },
      {
        "frameAddress": "8C5DE8F710",
        "parameters": "FE76B9B8,00000003,6E420C80,00000000,...",
        "pc": "victoria3.exe+7D65A8",
        "pcAddress": "7FF7772C65A8",
        "returnAddress": "7FF777E6C9E7",
        "returnSymbol": "victoria3.exe+137C9E7",
        "stackAddress": "8C5DE8F670"
      },
      {
        "frameAddress": "8C5DE8F840",
        "parameters": "00000000,FE76B9B8,00000000,5DE8F930,...",
        "pc": "victoria3.exe+137C9E7",
        "pcAddress": "7FF777E6C9E7",
        "returnAddress": "7FF7777B0D4D",
        "returnSymbol": "victoria3.exe+CC0D4D",
        "stackAddress": "8C5DE8F720"
      },
      {
        "frameAddress": "8C5DE8F9A0",
        "parameters": "0000000F,00000000,00000001,5DE8FAD0,...",
        "pc": "victoria3.exe+CC0D4D",
        "pcAddress": "7FF7777B0D4D",
        "returnAddress": "7FF779F524D9",
        "returnSymbol": "victoria3.exe+34624D9",
        "stackAddress": "8C5DE8F850"
      },
      {
        "frameAddress": "8C5DE8F9F0",
        "parameters": "5DE8FA30,00000000,00000000,00000000,...",
        "pc": "victoria3.exe+34624D9",
        "pcAddress": "7FF779F524D9",
        "returnAddress": "7FF779F5253C",
        "returnSymbol": "victoria3.exe+346253C",
        "stackAddress": "8C5DE8F9B0"
      },
      {
        "frameAddress": "8C5DE8FA50",
        "parameters": "5DE8FAC0,00000000,7C3D25A0,5DE8003D,...",
        "pc": "victoria3.exe+346253C",
        "pcAddress": "7FF779F5253C",
        "returnAddress": "7FF779E1786F",
        "returnSymbol": "victoria3.exe+332786F",
        "stackAddress": "8C5DE8FA00"
      },
      {
        "frameAddress": "8C5DE8FC80",
        "parameters": "7C3D2500,00000001,00000000,00000000,...",
        "pc": "victoria3.exe+332786F",
        "pcAddress": "7FF779E1786F",
        "returnAddress": "7FF779E1BCE9",
        "returnSymbol": "victoria3.exe+332BCE9",
        "stackAddress": "8C5DE8FA60"
      },
      {
        "frameAddress": "8C5DE8FD40",
        "parameters": "00000005,00000001,7C3D2658,00000000,...",
        "pc": "victoria3.exe+332BCE9",
        "pcAddress": "7FF779E1BCE9",
        "returnAddress": "7FF77A5BE43D",
        "returnSymbol": "victoria3.exe+3ACE43D",
        "stackAddress": "8C5DE8FC90"
      },
      {
        "frameAddress": "8C5DE8FD70",
        "parameters": "61FE81C0,00000000,5DE8FD78,5DE8FD80,...",
        "pc": "victoria3.exe+3ACE43D",
        "pcAddress": "7FF77A5BE43D",
        "returnAddress": "7FF77A5BD8CE",
        "returnSymbol": "victoria3.exe+3ACD8CE",
        "stackAddress": "8C5DE8FD50"
      },
      {
        "frameAddress": "8C5DE8FDA0",
        "parameters": "00000000,00000000,00000005,00000005,...",
        "pc": "victoria3.exe+3ACD8CE",
        "pcAddress": "7FF77A5BD8CE",
        "returnAddress": "7FF77A617992",
        "returnSymbol": "victoria3.exe+3B27992",
        "stackAddress": "8C5DE8FD80"
      },
      {
        "frameAddress": "8C5DE8FDD0",
        "parameters": "6E070C40,00000000,00000000,00000000,...",
        "pc": "victoria3.exe+3B27992",
        "pcAddress": "7FF77A617992",
        "returnAddress": "7FF77AC50DCA",
        "returnSymbol": "victoria3.exe+4160DCA",
        "stackAddress": "8C5DE8FDB0"
      },
      {
        "frameAddress": "8C5DE8FE00",
        "parameters": "00000000,00000000,00000000,00000000,...",
        "pc": "victoria3.exe+4160DCA",
        "pcAddress": "7FF77AC50DCA",
        "returnAddress": "7FF9E12CCD87",
        "returnSymbol": "KERNEL32.BaseThreadInitThunk+17",
        "stackAddress": "8C5DE8FDE0"
      },
      {
        "frameAddress": "8C5DE8FE30",
        "parameters": "00000000,00000000,FFFFFB30,FFFFFB30,...",
        "pc": "KERNEL32.BaseThreadInitThunk+17",
        "pcAddress": "7FF9E12CCD87",
        "returnAddress": "7FF9E2F4CAEC",
        "returnSymbol": "ntdll.RtlUserThreadStart+2C",
        "stackAddress": "8C5DE8FE10"
      },
      {
        "frameAddress": "8C5DE8FE80",
        "parameters": "00000000,00000000,00000000,00000000,...",
        "pc": "ntdll.RtlUserThreadStart+2C",
        "pcAddress": "7FF9E2F4CAEC",
        "returnAddress": "0",
        "returnSymbol": "00000000",
        "stackAddress": "8C5DE8FE40"
      }
    ],
    "instructionPointer": "7FF777CED5C9",
    "pointerSize": 8,
    "source": "ce_stacktrace_window",
    "stackPointer": "8C5DE8D870",
    "temporaryWindow": false,
    "termination": "zero_return",
    "threadId": "60D0"
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
