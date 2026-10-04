# Opcode window 7FF6B277D8CE

- Status: success
- Run: 20261004T121013357957Z_fba0b1f4
- CE instance: ce-27656-feb613268bc942f3b77a51a1385c8c93
- Target PID: 12472
- Captured at: 2026-10-04T12:10:14.082270+00:00
- Requested: 32 before + target + 32 after
- Boundary method: CE estimated predecessors; continuity checked on success
- Capture mode: live reads, not an atomic process snapshot
- Expected target bytes: 90

## Instructions

| Offset | Address | CE address | Bytes | Opcode | Extra | Marker |
| ---: | --- | --- | --- | --- | --- | --- |
| -32 | 7FF6B277D86A | 7FF6B277D86A | 41 8B 04 08 | mov eax,[r8+rcx] |  |  |
| -31 | 7FF6B277D86E | 7FF6B277D86E | A8 01 | test al,01 |  |  |
| -30 | 7FF6B277D870 | 7FF6B277D870 | 75 26 | jne 7FF6B277D898 |  |  |
| -29 | 7FF6B277D872 | 7FF6B277D872 | 83 C8 01 | or eax,01 |  |  |
| -28 | 7FF6B277D875 | 7FF6B277D875 | C6 42 0C 01 | mov byte ptr [rdx+0C],01 |  |  |
| -27 | 7FF6B277D879 | 7FF6B277D879 | 41 89 04 08 | mov [r8+rcx],eax |  |  |
| -26 | 7FF6B277D87D | 7FF6B277D87D | 33 C0 | xor eax,eax |  |  |
| -25 | 7FF6B277D87F | 7FF6B277D87F | 48 89 02 | mov [rdx],rax |  |  |
| -24 | 7FF6B277D882 | 7FF6B277D882 | 89 42 08 | mov [rdx+08],eax |  |  |
| -23 | 7FF6B277D885 | 7FF6B277D885 | 88 42 10 | mov [rdx+10],al |  |  |
| -22 | 7FF6B277D888 | 7FF6B277D888 | B8 01 00 00 00 | mov eax,00000001 |  |  |
| -21 | 7FF6B277D88D | 7FF6B277D88D | F0 0F C1 05 FB 0A E7 01 | lock xadd [7FF6B45EE390],eax |  |  |
| -20 | 7FF6B277D895 | 7FF6B277D895 | 89 42 14 | mov [rdx+14],eax |  |  |
| -19 | 7FF6B277D898 | 7FF6B277D898 | 8B 42 14 | mov eax,[rdx+14] |  |  |
| -18 | 7FF6B277D89B | 7FF6B277D89B | C3 | ret  |  |  |
| -17 | 7FF6B277D89C | 7FF6B277D89C | CC | int 3  |  |  |
| -16 | 7FF6B277D89D | 7FF6B277D89D | CC | int 3  |  |  |
| -15 | 7FF6B277D89E | 7FF6B277D89E | CC | int 3  |  |  |
| -14 | 7FF6B277D89F | 7FF6B277D89F | CC | int 3  |  |  |
| -13 | 7FF6B277D8A0 | 7FF6B277D8A0 | 40 53 | push rbx |  |  |
| -12 | 7FF6B277D8A2 | 7FF6B277D8A2 | 48 83 EC 20 | sub rsp,20 |  |  |
| -11 | 7FF6B277D8A6 | 7FF6B277D8A6 | 48 8B D9 | mov rbx,rcx |  |  |
| -10 | 7FF6B277D8A9 | 7FF6B277D8A9 | 48 83 C1 10 | add rcx,10 |  |  |
| -9 | 7FF6B277D8AD | 7FF6B277D8AD | 83 79 08 00 | cmp dword ptr [rcx+08],00 |  |  |
| -8 | 7FF6B277D8B1 | 7FF6B277D8B1 | 74 05 | je 7FF6B277D8B8 |  |  |
| -7 | 7FF6B277D8B3 | 7FF6B277D8B3 | E8 C8 FE FF FF | call 7FF6B277D780 |  |  |
| -6 | 7FF6B277D8B8 | 7FF6B277D8B8 | 48 8B 05 39 CC DE 01 | mov rax,[7FF6B456A4F8] | [B1D02780] |  |
| -5 | 7FF6B277D8BF | 7FF6B277D8BF | 48 85 C0 | test rax,rax |  |  |
| -4 | 7FF6B277D8C2 | 7FF6B277D8C2 | 74 11 | je 7FF6B277D8D5 |  |  |
| -3 | 7FF6B277D8C4 | 7FF6B277D8C4 | 48 8B 53 28 | mov rdx,[rbx+28] |  |  |
| -2 | 7FF6B277D8C8 | 7FF6B277D8C8 | 48 8B 4B 20 | mov rcx,[rbx+20] |  |  |
| -1 | 7FF6B277D8CC | 7FF6B277D8CC | FF D0 | call rax |  |  |
| 0 | 7FF6B277D8CE | 7FF6B277D8CE | 90 | nop  |  | TARGET |
| 1 | 7FF6B277D8CF | 7FF6B277D8CF | 48 83 C4 20 | add rsp,20 |  |  |
| 2 | 7FF6B277D8D3 | 7FF6B277D8D3 | 5B | pop rbx |  |  |
| 3 | 7FF6B277D8D4 | 7FF6B277D8D4 | C3 | ret  |  |  |
| 4 | 7FF6B277D8D5 | 7FF6B277D8D5 | 48 8B 43 20 | mov rax,[rbx+20] |  |  |
| 5 | 7FF6B277D8D9 | 7FF6B277D8D9 | 48 8B 4B 28 | mov rcx,[rbx+28] |  |  |
| 6 | 7FF6B277D8DD | 7FF6B277D8DD | FF D0 | call rax |  |  |
| 7 | 7FF6B277D8DF | 7FF6B277D8DF | 90 | nop  |  |  |
| 8 | 7FF6B277D8E0 | 7FF6B277D8E0 | 48 83 C4 20 | add rsp,20 |  |  |
| 9 | 7FF6B277D8E4 | 7FF6B277D8E4 | 5B | pop rbx |  |  |
| 10 | 7FF6B277D8E5 | 7FF6B277D8E5 | C3 | ret  |  |  |
| 11 | 7FF6B277D8E6 | 7FF6B277D8E6 | CC | int 3  |  |  |
| 12 | 7FF6B277D8E7 | 7FF6B277D8E7 | CC | int 3  |  |  |
| 13 | 7FF6B277D8E8 | 7FF6B277D8E8 | CC | int 3  |  |  |
| 14 | 7FF6B277D8E9 | 7FF6B277D8E9 | CC | int 3  |  |  |
| 15 | 7FF6B277D8EA | 7FF6B277D8EA | CC | int 3  |  |  |
| 16 | 7FF6B277D8EB | 7FF6B277D8EB | CC | int 3  |  |  |
| 17 | 7FF6B277D8EC | 7FF6B277D8EC | CC | int 3  |  |  |
| 18 | 7FF6B277D8ED | 7FF6B277D8ED | CC | int 3  |  |  |
| 19 | 7FF6B277D8EE | 7FF6B277D8EE | CC | int 3  |  |  |
| 20 | 7FF6B277D8EF | 7FF6B277D8EF | CC | int 3  |  |  |
| 21 | 7FF6B277D8F0 | 7FF6B277D8F0 | 48 83 EC 28 | sub rsp,28 |  |  |
| 22 | 7FF6B277D8F4 | 7FF6B277D8F4 | 85 C9 | test ecx,ecx |  |  |
| 23 | 7FF6B277D8F6 | 7FF6B277D8F6 | 74 39 | je 7FF6B277D931 |  |  |
| 24 | 7FF6B277D8F8 | 7FF6B277D8F8 | 83 E9 01 | sub ecx,01 |  |  |
| 25 | 7FF6B277D8FB | 7FF6B277D8FB | 74 1E | je 7FF6B277D91B |  |  |
| 26 | 7FF6B277D8FD | 7FF6B277D8FD | 83 F9 01 | cmp ecx,01 |  |  |
| 27 | 7FF6B277D900 | 7FF6B277D900 | 75 48 | jne 7FF6B277D94A |  |  |
| 28 | 7FF6B277D902 | 7FF6B277D902 | FF 15 88 69 7B 00 | call qword ptr [7FF6B2F34290] |  |  |
| 29 | 7FF6B277D908 | 7FF6B277D908 | 48 8B C8 | mov rcx,rax |  |  |
| 30 | 7FF6B277D90B | 7FF6B277D90B | BA 01 00 00 00 | mov edx,00000001 |  |  |
| 31 | 7FF6B277D910 | 7FF6B277D910 | 48 83 C4 28 | add rsp,28 |  |  |
| 32 | 7FF6B277D914 | 7FF6B277D914 | 48 FF 25 35 6E 7B 00 | jmp qword ptr [7FF6B2F34750] |  |  |
