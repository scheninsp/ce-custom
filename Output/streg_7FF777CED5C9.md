# Stacktrace and Registers at Breakpoint 7FF777CED5C9

- Captured at: 2026-10-01T14:46:29.909819+00:00
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
| R10 | 0 |
| R11 | B504F333 |
| R12 | 0 |
| R13 | 8C5DE8DC90 |
| R14 | 3A484D9DB60 |
| R15 | 7FF77AF75198 |
| R8 | 16A09E666 |
| R9 | 0 |
| RAX | 7E |
| RBP | 8C5DE8DD30 |
| RBX | 3A573942770 |
| RCX | 0 |
| RDI | 3A5FF432A80 |
| RDX | 0 |
| RIP | 7FF777CED5C9 |
| RSI | 3A5FF432B30 |
| RSP | 8C5DE8D870 |
| THREADID | 60D0 |
| XMM0 | 08 00 D9 84 A4 03 00 00 E7 C9 41 06 00 00 00 00 |
| XMM1 | 2A 00 D9 84 A4 03 00 00 00 00 00 00 00 00 00 00 |
| XMM10 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM11 | 00 00 00 00 00 00 4E 40 00 00 00 00 00 00 00 00 |
| XMM12 | 00 00 00 00 00 00 00 00 0F 00 00 00 00 00 00 00 |
| XMM13 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM14 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM15 | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM2 | 7B 95 2D 33 00 00 00 00 F6 D3 E3 35 00 00 00 00 |
| XMM3 | D4 C4 02 00 00 00 00 00 E4 E5 D8 02 00 00 00 00 |
| XMM4 | D4 75 67 0E 00 00 00 00 90 94 B8 02 00 00 00 00 |
| XMM5 | 2C 00 D9 84 A4 03 00 00 00 00 00 00 00 00 00 00 |
| XMM6 | 00 00 C0 3F 00 00 00 00 00 00 00 00 00 00 00 00 |
| XMM7 | 05 1F 39 88 8C FD 3B 3F 00 00 00 00 00 00 00 00 |
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
  "capturedAt": "2026-10-01T14:46:29.909819+00:00",
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
      "R10": "0",
      "R11": "B504F333",
      "R12": "0",
      "R13": "8C5DE8DC90",
      "R14": "3A484D9DB60",
      "R15": "7FF77AF75198",
      "R8": "16A09E666",
      "R9": "0",
      "RAX": "7E",
      "RBP": "8C5DE8DD30",
      "RBX": "3A573942770",
      "RCX": "0",
      "RDI": "3A5FF432A80",
      "RDX": "0",
      "RIP": "7FF777CED5C9",
      "RSI": "3A5FF432B30",
      "RSP": "8C5DE8D870",
      "THREADID": "60D0",
      "XMM0": "08 00 D9 84 A4 03 00 00 E7 C9 41 06 00 00 00 00",
      "XMM1": "2A 00 D9 84 A4 03 00 00 00 00 00 00 00 00 00 00",
      "XMM10": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM11": "00 00 00 00 00 00 4E 40 00 00 00 00 00 00 00 00",
      "XMM12": "00 00 00 00 00 00 00 00 0F 00 00 00 00 00 00 00",
      "XMM13": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM14": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM15": "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM2": "7B 95 2D 33 00 00 00 00 F6 D3 E3 35 00 00 00 00",
      "XMM3": "D4 C4 02 00 00 00 00 00 E4 E5 D8 02 00 00 00 00",
      "XMM4": "D4 75 67 0E 00 00 00 00 90 94 B8 02 00 00 00 00",
      "XMM5": "2C 00 D9 84 A4 03 00 00 00 00 00 00 00 00 00 00",
      "XMM6": "00 00 C0 3F 00 00 00 00 00 00 00 00 00 00 00 00",
      "XMM7": "05 1F 39 88 8C FD 3B 3F 00 00 00 00 00 00 00 00",
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
      "capabilities": [
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Satisfied, Reason = CheatEngine.SDK observed the selected-process primitive (Process.Current) in this snapshot., IsSatisfied = True }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., EffectiveReasonCode = LiveQualification }",
          "isAvailable": false,
          "name": "Client.ProcessSelection",
          "reason": "No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.TypedMemory",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.PatternScanning",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5001) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.ValueScanning",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.Inspection",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.Tables",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.ProtectedLua",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = Client.UnsafeLuaExecution is never host-qualified: no live scenario covers it., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = Unsafe Lua execution was explicitly enabled for this activation., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.UnsafeLuaExecution",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5002) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.Allocations",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5003) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.Assembly",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5004) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = Auto Assembler patches were explicitly enabled for this activation., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.AutoAssemblerPatches",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        }
      ],
      "epoch": 1,
      "gates": {
        "autoAssembler": true,
        "kernelAccess": true,
        "targetCodeExecution": true,
        "unsafeLua": true
      },
      "hostVersion": "CheatEngineRuntimeVersionInfo { CheatEngineVersion = 7.7.0.10621, QualifiedCheatEngineBaseline = 7.7.0.10621, ClientAssemblyVersion = 1.0.0.0, SdkAssemblyVersion = 2.0.0.0, SdkPackageVersion = 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696, IsReviewedSdkPackage = True, IsOnQualifiedCheatEngineLine = True }",
      "platform": "CheatEngineRuntimePlatformInfo { HostOperatingSystem = Windows, HostArchitecture = X64, CheatEngineBitness = CheatEngine.SDK.Engine.Runtime.PointerSize, TargetBackend = LocalProcess, TargetArchitecture = X64, TargetBitness = CheatEngine.SDK.Engine.Runtime.PointerSize, TargetAbi = Windows, TargetIsAndroid = False, ConfiguredPointerSizeBytes = 8, ConfiguredPointerSize = CheatEngine.SDK.Engine.Runtime.PointerSize, ConfiguredPointerSizeDiffersFromBitness = False }",
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
      "capabilities": [
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Satisfied, Reason = CheatEngine.SDK observed the selected-process primitive (Process.Current) in this snapshot., IsSatisfied = True }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., EffectiveReasonCode = LiveQualification }",
          "isAvailable": false,
          "name": "Client.ProcessSelection",
          "reason": "No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.TypedMemory",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.PatternScanning",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5001) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.ValueScanning",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.Inspection",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.Tables",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.ProtectedLua",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = Client.UnsafeLuaExecution is never host-qualified: no live scenario covers it., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = Unsafe Lua execution was explicitly enabled for this activation., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.UnsafeLuaExecution",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5002) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.Allocations",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5003) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.Assembly",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        },
        {
          "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5004) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = Auto Assembler patches were explicitly enabled for this activation., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
          "isAvailable": false,
          "name": "Client.AutoAssemblerPatches",
          "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
          "state": "Unknown"
        }
      ],
      "epoch": 1,
      "gates": {
        "autoAssembler": true,
        "kernelAccess": true,
        "targetCodeExecution": true,
        "unsafeLua": true
      },
      "hostVersion": "CheatEngineRuntimeVersionInfo { CheatEngineVersion = 7.7.0.10621, QualifiedCheatEngineBaseline = 7.7.0.10621, ClientAssemblyVersion = 1.0.0.0, SdkAssemblyVersion = 2.0.0.0, SdkPackageVersion = 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696, IsReviewedSdkPackage = True, IsOnQualifiedCheatEngineLine = True }",
      "platform": "CheatEngineRuntimePlatformInfo { HostOperatingSystem = Windows, HostArchitecture = X64, CheatEngineBitness = CheatEngine.SDK.Engine.Runtime.PointerSize, TargetBackend = LocalProcess, TargetArchitecture = X64, TargetBitness = CheatEngine.SDK.Engine.Runtime.PointerSize, TargetAbi = Windows, TargetIsAndroid = False, ConfiguredPointerSizeBytes = 8, ConfiguredPointerSize = CheatEngine.SDK.Engine.Runtime.PointerSize, ConfiguredPointerSizeDiffersFromBitness = False }",
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
        "capabilities": [
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Satisfied, Reason = CheatEngine.SDK observed the selected-process primitive (Process.Current) in this snapshot., IsSatisfied = True }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., EffectiveReasonCode = LiveQualification }",
            "isAvailable": false,
            "name": "Client.ProcessSelection",
            "reason": "No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.TypedMemory",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.PatternScanning",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5001) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.ValueScanning",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.Inspection",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.Tables",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.ProtectedLua",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = Client.UnsafeLuaExecution is never host-qualified: no live scenario covers it., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = Unsafe Lua execution was explicitly enabled for this activation., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.UnsafeLuaExecution",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5002) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.Allocations",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5003) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = This capability has no additional activation policy opt-in., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.Assembly",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          },
          {
            "evidence": "ClientCapabilityEvidence { Implementation = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client composes an operational adapter for this capability; its API is experimental (CECLIENT5004) until its live scenarios pass., IsSatisfied = True }, Package = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The loaded CheatEngine.SDK.Engine 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is exactly the reviewed package this Client build consumed (NuGet content hash NLEdZYJ9LKW3EFNB4X5snKCQf7ZS86GkCQ+El7o+S1XQcxHQGjS45Q1ap8lfjQuIwm004mQ3TPxo+ph1yvRrlQ==, read from the lock file at build time)., IsSatisfied = True }, Host = ClientCapabilityEvidenceGate { State = Unknown, Reason = The runtime snapshot does not probe every host primitive required by this capability., IsSatisfied = False }, LiveQualification = ClientCapabilityEvidenceGate { State = Unknown, Reason = No Client qualification receipt for profile ce-7.7.0.10621-x64-managed-hostfxr with CheatEngine.SDK 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696 is embedded in this build; SDK-branch receipts never qualify the Client tuple., IsSatisfied = False }, Policy = ClientCapabilityEvidenceGate { State = Satisfied, Reason = Auto Assembler patches were explicitly enabled for this activation., IsSatisfied = True }, Lifetime = ClientCapabilityEvidenceGate { State = Satisfied, Reason = The Client activation is current., IsSatisfied = True }, AvailabilityState = Unknown, EffectiveReason = The runtime snapshot does not probe every host primitive required by this capability., EffectiveReasonCode = Host }",
            "isAvailable": false,
            "name": "Client.AutoAssemblerPatches",
            "reason": "The runtime snapshot does not probe every host primitive required by this capability.",
            "state": "Unknown"
          }
        ],
        "epoch": 1,
        "gates": {
          "autoAssembler": true,
          "kernelAccess": true,
          "targetCodeExecution": true,
          "unsafeLua": true
        },
        "hostVersion": "CheatEngineRuntimeVersionInfo { CheatEngineVersion = 7.7.0.10621, QualifiedCheatEngineBaseline = 7.7.0.10621, ClientAssemblyVersion = 1.0.0.0, SdkAssemblyVersion = 2.0.0.0, SdkPackageVersion = 2.0.0+325c47b573f8bd39a247f1d0101f110fa36c1696, IsReviewedSdkPackage = True, IsOnQualifiedCheatEngineLine = True }",
        "platform": "CheatEngineRuntimePlatformInfo { HostOperatingSystem = Windows, HostArchitecture = X64, CheatEngineBitness = CheatEngine.SDK.Engine.Runtime.PointerSize, TargetBackend = LocalProcess, TargetArchitecture = X64, TargetBitness = CheatEngine.SDK.Engine.Runtime.PointerSize, TargetAbi = Windows, TargetIsAndroid = False, ConfiguredPointerSizeBytes = 8, ConfiguredPointerSize = CheatEngine.SDK.Engine.Runtime.PointerSize, ConfiguredPointerSizeDiffersFromBitness = False }",
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
