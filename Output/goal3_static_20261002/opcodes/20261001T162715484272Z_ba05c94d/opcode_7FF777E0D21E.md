# Opcode window 7FF777E0D21E

- Status: failed
- Run: 20261001T162715484272Z_ba05c94d
- CE instance: ce-72480-42f4ba0154dd4fbd8087223e0f808fda
- Target PID: 43884
- Captured at: 2026-10-01T16:27:16.117843+00:00
- Requested: 1000 before + target + 1000 after
- Boundary method: CE estimated predecessors; continuity checked on success
- Capture mode: live reads, not an atomic process snapshot
- Expected target bytes: 440AE0

## Failure

{"error": {"kind": "limit_exceeded", "message": "count: count plus before accepts at most 1024 instructions.", "hostEffect": "not_started", "retryable": false, "hint": "Lower limit or size, or page with offset.", "details": {"parameter": "count"}}}
