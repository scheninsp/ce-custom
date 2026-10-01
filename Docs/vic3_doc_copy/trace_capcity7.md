# victoria3.exe+122A470 断点
# 调用栈
Stacktrace
PC                      Stack       Frame       Return                      Parameters
victoria3.exe+122A470   AE769CD118  AE769CD110  victoria3.exe+122B9D7       2DDFD7FD,769CDE20,00000000,04550021,...
victoria3.exe+122B9D7   AE769CD120  AE769CD400  victoria3.exe+1335C89       00000000,2DDFD7FD,00000000,0000007E,...
victoria3.exe+1335C89   AE769CD410  AE769CD430  victoria3.exe+3A8D16D       FFFFFFFF,00000000,769CD702,FFFFFFFF,...
victoria3.exe+3A8D16D   AE769CD440  AE769CD4A0  victoria3.exe+3ACBB7A       FFFFFFFF,AB8C1440,769CD700,000003C3,...
victoria3.exe+3ACBB7A   AE769CD4B0  AE769CD4D0  victoria3.exe+13261FD       00000000,000003C3,769CD640,769CD6E8,...
victoria3.exe+13261FD   AE769CD4E0  AE769CD680  victoria3.exe+131C3D4       E6AE3C00,769CD790,00000000,E6AE3CF0,...
victoria3.exe+131C3D4   AE769CD690  AE769CE9D0  victoria3.exe+7B8563        2DDFD7FD,00000000,00000000,E6AE3CF0,...
victoria3.exe+7B8563    AE769CE9E0  AE769CEE30  victoria3.exe+7BE76D        000021B,00000000,BB569678,00000000,...
victoria3.exe+7BE76D    AE769CEE40  AE769CF150  victoria3.exe+7D65A8        BA032400,7C057308,00000054,2816D278,...
victoria3.exe+7D65A8    AE769CF160  AE769CF200  victoria3.exe+137C9E7       BA06F228,00000003,7C057300,00000000,...
victoria3.exe+137C9E7   AE769CF210  AE769CF330  victoria3.exe+CC0D4D        00000000,BA06F228,00000000,769CF420,...
victoria3.exe+CC0D4D    AE769CF340  AE769CF490  victoria3.exe+34624D9       0000000F,00000000,00000001,769CF5C0,...
victoria3.exe+34624D9   AE769CF4A0  AE769CF4E0  victoria3.exe+346253C       769CF520,00000000,00000000,00000000,...
victoria3.exe+346253C   AE769CF4F0  AE769CF540  victoria3.exe+332786F       769CF5B0,00000000,EF7625A0,769C003D,...
victoria3.exe+332786F   AE769CF550  AE769CF770  victoria3.exe+332BCE9       EF762500,00000001,00000000,00000000,...
victoria3.exe+332BCE9   AE769CF780  AE769CF830  victoria3.exe+3ACE43D       00000000,00000001,EF762658,00000000,...
victoria3.exe+3ACE43D   AE769CF840  AE769CF860  victoria3.exe+3ACD8CE       B1FE81C0,00000000,769CF868,769CF870,...
victoria3.exe+3ACD8CE   AE769CF870  AE769CF890  victoria3.exe+3B27992       00000000,00000000,00000005,00000005,...
victoria3.exe+3B27992   AE769CF8A0  AE769CF8C0  victoria3.exe+4160DCA       502C9D30,00000000,00000000,00000000,...
victoria3.exe+4160DCA   AE769CF8D0  AE769CF8F0  KERNEL32.BaseThreadInitThun... 00000000,00000000,00000000,...
KERNEL32.BaseThreadInitThunk+17 AE769CF900 AE769CF920 ntdll.RtlUserThreadStart+2C 00000000,00000000,FFFFFB30,FFFFFB30,...
ntdll.RtlUserThreadStart+2C AE769CF930 AE769CF970 00000000                    00000000,00000000,00000000,00000000,...

第一次记录
The following opcodes accessed 32FDB11F8B8
Count	Instruction
1	7FF7EB0AB9C7 - 89 86 58 1D 00 00 - mov [rsi+00001D58],eax
1	7FF7EB0ABA8E - 44 2B BE 58 1D 00 00 - sub r15d,[rsi+00001D58]
98	7FF7EB0A9218 - 49 63 85 58 1D 00 00 - movsxd rax,dword ptr [r13+00001D58]
13	7FF7EB07D5C9 - 41 8B 86 58 1D 00 00 - mov eax,[r14+00001D58]
12	7FF7EB0ABF62 - 89 83 58 1D 00 00 - mov [rbx+00001D58],eax
1	7FF7EB091346 - 48 63 87 58 1D 00 00 - movsxd rax,dword ptr [rdi+00001D58]

The following opcodes accessed 32FDB11F8BC
Count	Instruction
1	7FF7EB0AB9DA - 89 86 5C 1D 00 00 - mov [rsi+00001D5C],eax
13	7FF7EB07D5BB - 41 8B 86 5C 1D 00 00 - mov eax,[r14+00001D5C]
12	7FF7EB0ABF70 - 89 83 5C 1D 00 00 - mov [rbx+00001D5C],eax

第二次记录
The following opcodes accessed 32FDB11F8B8
Count	Instruction
3	7FF7EACB7334 - 48 63 90 58 1D 00 00 - movsxd rdx,dword ptr [ra...
3	7FF7EB091346 - 48 63 87 58 1D 00 00 - movsxd rax,dword ptr [rdi...
279	7FF7EB0A9218 - 49 63 85 58 1D 00 00 - movsxd rax,dword ptr [r1...
2	7FF7EB0AB9C7 - 89 86 58 1D 00 00 - mov [rsi+00001D58],eax
2	7FF7EB0ABA8E - 44 2B BE 58 1D 00 00 - sub r15d,[rsi+00001D58]
2	7FF7EB07D5C9 - 41 8B 86 58 1D 00 00 - mov eax,[r14+00001D58]

The following opcodes accessed 32FDB11F8BC
Count	Instruction
3	7FF7EACB7358 - 2B 90 5C 1D 00 00 - sub edx,[rax+00001D5C]
2	7FF7EB0AB9DA - 89 86 5C 1D 00 00 - mov [rsi+00001D5C],eax
2	7FF7EB07D5BB - 41 8B 86 5C 1D 00 00 - mov eax,[r14+00001D5C]






当前最强的调用链已经变成：
+122BF50
    ├─ +1229C50 → 计算总容量 → 写入 +1D58
    ├─ +122A470 → 遍历条目并计算分配容量
    │      └─ +122AB50 → 单项容量分配
    └─ 写入 +1D5C

victoria3.exe+122BF50


victoria3.exe+122BF62 - 89 83 581D0000        - mov [rbx+00001D58],eax
断点时 RAX，RBX 的值：
0000041B，32FDAB67220
00000386，32FDAA94D70
00000265，32FDAF0B3E0
000001F0，32FDB152C20
0000002E，32FDB08BD50

# 条件断点
7FF7EB0A9218:
R13 == 0x32FDB11DB60

7FF7EACB7334:
RAX == 0x32FDB11DB60

7FF7EB07D5C9:
R14 == 0x32FDB11DB60

7FF7EB091346:
RDI == 0x32FDB11DB60

# 命中断点，且条件 
7FF7EB0A9218:
R13 == 0x32FDB11DB60
victoria3.exe+1229218 - 49 63 85 581D0000     - movsxd  rax,dword ptr [r13+00001D58]

[R13+1D58] = 184 已确认

# 补充 victoria3.exe+1229218 附近反编译 opcode
victoria3.exe+1228B8D - CC                    - int 3 
victoria3.exe+1228B8E - CC                    - int 3 
victoria3.exe+1228B8F - CC                    - int 3 
victoria3.exe+1228B90 - 48 89 5C 24 10        - mov [rsp+10],rbx
victoria3.exe+1228B95 - 55                    - push rbp
victoria3.exe+1228B96 - 56                    - push rsi
victoria3.exe+1228B97 - 57                    - push rdi
victoria3.exe+1228B98 - 41 54                 - push r12
victoria3.exe+1228B9A - 41 55                 - push r13
victoria3.exe+1228B9C - 41 56                 - push r14
victoria3.exe+1228B9E - 41 57                 - push r15
victoria3.exe+1228BA0 - 48 8D AC 24 80FEFFFF  - lea rbp,[rsp-00000180]
victoria3.exe+1228BA8 - 48 81 EC 80020000     - sub rsp,00000280
victoria3.exe+1228BAF - C5F829B4 24 70 020000 - vmovaps [rsp+00000270],xmm6
victoria3.exe+1228BB8 - 4C 8B FA              - mov r15,rdx
victoria3.exe+1228BBB - 4C 8B E9              - mov r13,rcx
victoria3.exe+1228BBE - 45 33 E4              - xor r12d,r12d
victoria3.exe+1228BC1 - 44 89 A5 C0010000     - mov [rbp+000001C0],r12d
victoria3.exe+1228BC8 - 48 8B 99 B0180000     - mov rbx,[rcx+000018B0]
victoria3.exe+1228BCF - 48 89 5D 50           - mov [rbp+50],rbx
victoria3.exe+1228BD3 - 48 85 DB              - test rbx,rbx
victoria3.exe+1228BD6 - 74 04                 - je victoria3.exe+1228BDC
victoria3.exe+1228BD8 - F0 FF 43 08           - lock inc [rbx+08]
victoria3.exe+1228BDC - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+1228BE0 - C5F81144 24 40        - vmovups [rsp+40],xmm0
victoria3.exe+1228BE6 - C5FA6F35 D2 D35D03    - vmovdqu xmm6,xmm0,[victoria3.exe+4805FC0]
victoria3.exe+1228BEE - C5FA7F74 24 50        - vmovdqu [rsp+50],xmm6
victoria3.exe+1228BF4 - C6 44 24 40 00        - mov byte ptr [rsp+40],00
victoria3.exe+1228BF9 - 48 8D 44 24 40        - lea rax,[rsp+40]
victoria3.exe+1228BFE - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+1228C03 - 44 0FB7 0D 85E3EA03   - movzx r9d,word ptr [victoria3.exe+50D6F90]
victoria3.exe+1228C0B - 4C 8D 45 50           - lea r8,[rbp+50]
victoria3.exe+1228C0F - BA 02000000           - mov edx,00000002
victoria3.exe+1228C14 - 49 8B CF              - mov rcx,r15
victoria3.exe+1228C17 - E8 94539CFF           - call victoria3.exe+BEDFB0
victoria3.exe+1228C1C - 90                    - nop 
victoria3.exe+1228C1D - 48 8B 44 24 58        - mov rax,[rsp+58]
victoria3.exe+1228C22 - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+1228C26 - 76 35                 - jna victoria3.exe+1228C5D
victoria3.exe+1228C28 - 48 8B 54 24 40        - mov rdx,[rsp+40]
victoria3.exe+1228C2D - 48 8B CA              - mov rcx,rdx
victoria3.exe+1228C30 - 48 FF C0              - inc rax
victoria3.exe+1228C33 - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+1228C39 - 72 15                 - jb victoria3.exe+1228C50
victoria3.exe+1228C3B - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+1228C3F - 48 2B CA              - sub rcx,rdx
victoria3.exe+1228C42 - 48 83 E9 08           - sub rcx,08
victoria3.exe+1228C46 - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+1228C4A - 0F87 98080000         - ja victoria3.exe+12294E8
victoria3.exe+1228C50 - 48 85 D2              - test rdx,rdx
victoria3.exe+1228C53 - 74 08                 - je victoria3.exe+1228C5D
victoria3.exe+1228C55 - 48 8B CA              - mov rcx,rdx
victoria3.exe+1228C58 - E8 D376EF02           - call victoria3.exe+4120330
victoria3.exe+1228C5D - 49 8B CD              - mov rcx,r13
victoria3.exe+1228C60 - E8 AB8E0000           - call victoria3.exe+1231B10
victoria3.exe+1228C65 - 48 8B F0              - mov rsi,rax
victoria3.exe+1228C68 - 48 8D 48 08           - lea rcx,[rax+08]
victoria3.exe+1228C6C - 48 8B 11              - mov rdx,[rcx]
victoria3.exe+1228C6F - FF 52 08              - call qword ptr [rdx+08]
victoria3.exe+1228C72 - 41 BE 33F304B5        - mov r14d,B504F333
victoria3.exe+1228C78 - 84 C0                 - test al,al
victoria3.exe+1228C7A - 0F84 98050000         - je victoria3.exe+1229218
victoria3.exe+1228C80 - 83 BE E8000000 00     - cmp dword ptr [rsi+000000E8],00
victoria3.exe+1228C87 - 0F8E 8B050000         - jng victoria3.exe+1229218
victoria3.exe+1228C8D - E8 DE3B58FF           - call victoria3.exe+7AC870
victoria3.exe+1228C92 - 48 8B B8 600F0000     - mov rdi,[rax+00000F60]
victoria3.exe+1228C99 - 48 8B CE              - mov rcx,rsi
victoria3.exe+1228C9C - E8 9F6FC1FF           - call victoria3.exe+E3FC40
victoria3.exe+1228CA1 - 4C 8B C7              - mov r8,rdi
victoria3.exe+1228CA4 - 48 8D 95 D8010000     - lea rdx,[rbp+000001D8]
victoria3.exe+1228CAB - 48 8B C8              - mov rcx,rax
victoria3.exe+1228CAE - E8 5DE7DFFF           - call victoria3.exe+1027410
victoria3.exe+1228CB3 - 48 8B 85 D8010000     - mov rax,[rbp+000001D8]
victoria3.exe+1228CBA - 48 85 C0              - test rax,rax
victoria3.exe+1228CBD - 0F8E 55050000         - jng victoria3.exe+1229218
victoria3.exe+1228CC3 - 4C 8B 0D D6106604     - mov r9,[victoria3.exe+5889DA0]
victoria3.exe+1228CCA - 49 3B C6              - cmp rax,r14
victoria3.exe+1228CCD - 7F 37                 - jg victoria3.exe+1228D06
victoria3.exe+1228CCF - 4B 8D 0C 31           - lea rcx,[r9+r14]
victoria3.exe+1228CD3 - 48 BA 66E6096A01000000 - mov rdx,000000016A09E666
victoria3.exe+1228CDD - 48 3B CA              - cmp rcx,rdx
victoria3.exe+1228CE0 - 77 24                 - ja victoria3.exe+1228D06
victoria3.exe+1228CE2 - 4C 0FAF C8            - imul r9,rax
victoria3.exe+1228CE6 - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+1228CF0 - 49 F7 E9              - imul r9
victoria3.exe+1228CF3 - 48 8B FA              - mov rdi,rdx
victoria3.exe+1228CF6 - 48 C1 FF 0E           - sar rdi,0E
victoria3.exe+1228CFA - 48 8B C7              - mov rax,rdi
victoria3.exe+1228CFD - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+1228D01 - 48 03 F8              - add rdi,rax
victoria3.exe+1228D04 - EB 5B                 - jmp victoria3.exe+1228D61
victoria3.exe+1228D06 - 4D 8B C1              - mov r8,r9
victoria3.exe+1228D09 - 4C 3B C8              - cmp r9,rax
victoria3.exe+1228D0C - 4C 0F4C C0            - cmovl r8,rax
victoria3.exe+1228D10 - 4C 0F4F C8            - cmovg r9,rax
victoria3.exe+1228D14 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+1228D1E - 49 8B C2              - mov rax,r10
victoria3.exe+1228D21 - 49 F7 E8              - imul r8
victoria3.exe+1228D24 - 48 8B CA              - mov rcx,rdx
victoria3.exe+1228D27 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+1228D2B - 48 8B C1              - mov rax,rcx
victoria3.exe+1228D2E - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+1228D32 - 48 03 C8              - add rcx,rax
victoria3.exe+1228D35 - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+1228D3C - 4C 2B C0              - sub r8,rax
victoria3.exe+1228D3F - 4D 0FAF C1            - imul r8,r9
victoria3.exe+1228D43 - 49 8B C2              - mov rax,r10
victoria3.exe+1228D46 - 49 F7 E8              - imul r8
victoria3.exe+1228D49 - 48 8B FA              - mov rdi,rdx
victoria3.exe+1228D4C - 48 C1 FF 0E           - sar rdi,0E
victoria3.exe+1228D50 - 48 8B C7              - mov rax,rdi
victoria3.exe+1228D53 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+1228D57 - 48 03 F8              - add rdi,rax
victoria3.exe+1228D5A - 49 0FAF C9            - imul rcx,r9
victoria3.exe+1228D5E - 48 03 F9              - add rdi,rcx
victoria3.exe+1228D61 - 48 89 7D 58           - mov [rbp+58],rdi
victoria3.exe+1228D65 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+1228D69 - C5F81145 B0           - vmovups [rbp-50],xmm0
victoria3.exe+1228D6E - C5FA7F75 C0           - vmovdqu [rbp-40],xmm6
victoria3.exe+1228D73 - C6 45 B0 00           - mov byte ptr [rbp-50],00
victoria3.exe+1228D77 - 48 8D 05 AA4B2503     - lea rax,[victoria3.exe+447D928]
victoria3.exe+1228D7E - 48 89 45 70           - mov [rbp+70],rax
victoria3.exe+1228D82 - 48 8D 45 58           - lea rax,[rbp+58]
victoria3.exe+1228D86 - 48 89 45 78           - mov [rbp+78],rax
victoria3.exe+1228D8A - 48 8D 85 D8010000     - lea rax,[rbp+000001D8]
victoria3.exe+1228D91 - 48 89 85 80000000     - mov [rbp+00000080],rax
victoria3.exe+1228D98 - 48 8D 4D 70           - lea rcx,[rbp+70]
victoria3.exe+1228D9C - 48 89 8D A8000000     - mov [rbp+000000A8],rcx
victoria3.exe+1228DA3 - 48 8D 05 86B12003     - lea rax,[victoria3.exe+4433F30]
victoria3.exe+1228DAA - 48 89 85 F0000000     - mov [rbp+000000F0],rax
victoria3.exe+1228DB1 - 48 8D 45 B0           - lea rax,[rbp-50]
victoria3.exe+1228DB5 - 48 89 85 F8000000     - mov [rbp+000000F8],rax
victoria3.exe+1228DBC - 4C 8D 85 F0000000     - lea r8,[rbp+000000F0]
victoria3.exe+1228DC3 - 4C 89 85 28010000     - mov [rbp+00000128],r8
victoria3.exe+1228DCA - 48 89 7D 80           - mov [rbp-80],rdi
victoria3.exe+1228DCE - 49 01 7F 10           - add [r15+10],rdi
victoria3.exe+1228DD2 - 41 80 7F 31 01        - cmp byte ptr [r15+31],01
victoria3.exe+1228DD7 - 0F85 BF030000         - jne victoria3.exe+122919C
victoria3.exe+1228DDD - 4D 8B 77 38           - mov r14,[r15+38]
victoria3.exe+1228DE1 - 41 80 BE AC010000 00  - cmp byte ptr [r14+000001AC],00
victoria3.exe+1228DE9 - 74 09                 - je victoria3.exe+1228DF4
victoria3.exe+1228DEB - 48 85 FF              - test rdi,rdi
victoria3.exe+1228DEE - 0F84 A2030000         - je victoria3.exe+1229196
victoria3.exe+1228DF4 - 48 8D 55 F0           - lea rdx,[rbp-10]
victoria3.exe+1228DF8 - 48 8D 4D 70           - lea rcx,[rbp+70]
victoria3.exe+1228DFC - E8 EF570100           - call victoria3.exe+123E5F0
victoria3.exe+1228E01 - 90                    - nop 
victoria3.exe+1228E02 - 48 83 7D 00 00        - cmp qword ptr [rbp+00],00
victoria3.exe+1228E07 - 75 09                 - jne victoria3.exe+1228E12
victoria3.exe+1228E09 - 48 85 FF              - test rdi,rdi
victoria3.exe+1228E0C - 0F84 6D030000         - je victoria3.exe+122917F
victoria3.exe+1228E12 - 49 8D 8E 50010000     - lea rcx,[r14+00000150]
victoria3.exe+1228E19 - E8 0240A2FF           - call victoria3.exe+C4CE20
victoria3.exe+1228E1E - 48 8B F0              - mov rsi,rax
victoria3.exe+1228E21 - C7 40 28 02000000     - mov [rax+28],00000002
victoria3.exe+1228E28 - 48 89 78 20           - mov [rax+20],rdi
victoria3.exe+1228E2C - 48 8B 8D 28010000     - mov rcx,[rbp+00000128]
victoria3.exe+1228E33 - 48 85 C9              - test rcx,rcx
victoria3.exe+1228E36 - 0F84 C1060000         - je victoria3.exe+12294FD
victoria3.exe+1228E3C - 48 8B 01              - mov rax,[rcx]
victoria3.exe+1228E3F - 48 8D 55 30           - lea rdx,[rbp+30]
victoria3.exe+1228E43 - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+1228E46 - C7 85 C0010000 03000000 - mov [rbp+000001C0],00000003
victoria3.exe+1228E50 - 48 83 7D 40 00        - cmp qword ptr [rbp+40],00
victoria3.exe+1228E55 - 0F84 E5020000         - je victoria3.exe+1229140
victoria3.exe+1228E5B - 41 8B BE B0010000     - mov edi,[r14+000001B0]
victoria3.exe+1228E62 - 48 8B CE              - mov rcx,rsi
victoria3.exe+1228E65 - 48 83 7D 00 00        - cmp qword ptr [rbp+00],00
victoria3.exe+1228E6A - 0F85 A4000000         - jne victoria3.exe+1228F14
victoria3.exe+1228E70 - E8 8B383FFF           - call victoria3.exe+61C700
victoria3.exe+1228E75 - 49 8B D6              - mov rdx,r14
victoria3.exe+1228E78 - 48 8B CE              - mov rcx,rsi
victoria3.exe+1228E7B - E8 209A1900           - call victoria3.exe+13C28A0
victoria3.exe+1228E80 - 89 7C 24 20           - mov [rsp+20],edi
victoria3.exe+1228E84 - 45 33 C9              - xor r9d,r9d
victoria3.exe+1228E87 - 41 B8 02000000        - mov r8d,00000002
victoria3.exe+1228E8D - 48 8D 54 24 40        - lea rdx,[rsp+40]
victoria3.exe+1228E92 - 49 8B CF              - mov rcx,r15
victoria3.exe+1228E95 - E8 06649CFF           - call victoria3.exe+BEF2A0
victoria3.exe+1228E9A - 90                    - nop 
victoria3.exe+1228E9B - 48 8D 44 24 40        - lea rax,[rsp+40]
victoria3.exe+1228EA0 - 48 83 7C 24 58 0F     - cmp qword ptr [rsp+58],0F
victoria3.exe+1228EA6 - 48 0F47 44 24 40      - cmova rax,[rsp+40]
victoria3.exe+1228EAC - 48 89 44 24 60        - mov [rsp+60],rax
victoria3.exe+1228EB1 - 8B 44 24 50           - mov eax,[rsp+50]
victoria3.exe+1228EB5 - 89 44 24 68           - mov [rsp+68],eax
victoria3.exe+1228EB9 - C6 44 24 6C 00        - mov byte ptr [rsp+6C],00
victoria3.exe+1228EBE - 48 8D 45 30           - lea rax,[rbp+30]
victoria3.exe+1228EC2 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+1228EC7 - 4C 8D 4D 80           - lea r9,[rbp-80]
victoria3.exe+1228ECB - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+1228ED0 - 48 8D 4D 90           - lea rcx,[rbp-70]
victoria3.exe+1228ED4 - E8 D71BA2FF           - call victoria3.exe+C4AAB0
victoria3.exe+1228ED9 - 90                    - nop 
victoria3.exe+1228EDA - 4C 8B 40 10           - mov r8,[rax+10]
victoria3.exe+1228EDE - 48 83 78 18 0F        - cmp qword ptr [rax+18],0F
victoria3.exe+1228EE3 - 76 03                 - jna victoria3.exe+1228EE8
victoria3.exe+1228EE5 - 48 8B 00              - mov rax,[rax]
victoria3.exe+1228EE8 - 48 8B D0              - mov rdx,rax
victoria3.exe+1228EEB - 48 8B CE              - mov rcx,rsi
victoria3.exe+1228EEE - E8 FDAF7001           - call victoria3.exe+2933EF0
victoria3.exe+1228EF3 - 90                    - nop 
victoria3.exe+1228EF4 - 48 8D 4D 90           - lea rcx,[rbp-70]
victoria3.exe+1228EF8 - E8 E3C83EFF           - call victoria3.exe+6157E0
victoria3.exe+1228EFD - 90                    - nop 
victoria3.exe+1228EFE - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+1228F03 - E8 D8C83EFF           - call victoria3.exe+6157E0
victoria3.exe+1228F08 - 45 89 A6 B0010000     - mov [r14+000001B0],r12d
victoria3.exe+1228F0F - E9 61020000           - jmp victoria3.exe+1229175
victoria3.exe+1228F14 - E8 E7373FFF           - call victoria3.exe+61C700
victoria3.exe+1228F19 - 49 8B D6              - mov rdx,r14
victoria3.exe+1228F1C - 48 8B CE              - mov rcx,rsi
victoria3.exe+1228F1F - E8 7C991900           - call victoria3.exe+13C28A0
victoria3.exe+1228F24 - 41 80 7F 31 01        - cmp byte ptr [r15+31],01
victoria3.exe+1228F29 - 74 17                 - je victoria3.exe+1228F42
victoria3.exe+1228F2B - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+1228F2F - C5F81145 D0           - vmovups [rbp-30],xmm0
victoria3.exe+1228F34 - C5FA7F75 E0           - vmovdqu [rbp-20],xmm6
victoria3.exe+1228F39 - C6 45 D0 00           - mov byte ptr [rbp-30],00
victoria3.exe+1228F3D - E9 6B010000           - jmp victoria3.exe+12290AD
victoria3.exe+1228F42 - C5F1EFC9              - vpxor xmm1,xmm1,xmm1
victoria3.exe+1228F46 - C5F8114C 24 60        - vmovups [rsp+60],xmm1
victoria3.exe+1228F4C - C5FA7F74 24 70        - vmovdqu [rsp+70],xmm6
victoria3.exe+1228F52 - C6 44 24 60 00        - mov byte ptr [rsp+60],00
victoria3.exe+1228F57 - 41 B8 04000000        - mov r8d,00000004
victoria3.exe+1228F5D - 48 8D 15 308C2003     - lea rdx,[victoria3.exe+4431B94]
victoria3.exe+1228F64 - 48 8D 4C 24 60        - lea rcx,[rsp+60]
victoria3.exe+1228F69 - E8 A2C23EFF           - call victoria3.exe+615210
victoria3.exe+1228F6E - 49 8B 57 38           - mov rdx,[r15+38]
victoria3.exe+1228F72 - 48 81 C2 88010000     - add rdx,00000188
victoria3.exe+1228F79 - 48 8D 4D 10           - lea rcx,[rbp+10]
victoria3.exe+1228F7D - E8 9E963EFF           - call victoria3.exe+612620
victoria3.exe+1228F82 - C7 85 C0010000 0B000000 - mov [rbp+000001C0],0000000B
victoria3.exe+1228F8C - 41 B8 11000000        - mov r8d,00000011
victoria3.exe+1228F92 - 48 8D 15 278C2003     - lea rdx,[victoria3.exe+4431BC0]
victoria3.exe+1228F99 - 48 8D 4D 10           - lea rcx,[rbp+10]
victoria3.exe+1228F9D - E8 4EAF7001           - call victoria3.exe+2933EF0
victoria3.exe+1228FA2 - 90                    - nop 
victoria3.exe+1228FA3 - C5FC1045 10           - vmovups ymm0,[rbp+10]
victoria3.exe+1228FA8 - C5FC1145 90           - vmovups [rbp-70],ymm0
victoria3.exe+1228FAD - C5FA7F75 20           - vmovdqu [rbp+20],xmm6
victoria3.exe+1228FB2 - C6 45 10 00           - mov byte ptr [rbp+10],00
victoria3.exe+1228FB6 - C7 85 C0010000 1B000000 - mov [rbp+000001C0],0000001B
victoria3.exe+1228FC0 - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+1228FC5 - 48 83 7C 24 78 0F     - cmp qword ptr [rsp+78],0F
victoria3.exe+1228FCB - 48 0F47 54 24 60      - cmova rdx,[rsp+60]
victoria3.exe+1228FD1 - 4C 8B 44 24 70        - mov r8,[rsp+70]
victoria3.exe+1228FD6 - 48 8D 4D 90           - lea rcx,[rbp-70]
victoria3.exe+1228FDA - C5F877                - vzeroupper 
victoria3.exe+1228FDD - E8 0EAF7001           - call victoria3.exe+2933EF0
victoria3.exe+1228FE2 - 4C 8D 05 EB8B2003     - lea r8,[victoria3.exe+4431BD4]
victoria3.exe+1228FE9 - 48 8D 55 90           - lea rdx,[rbp-70]
victoria3.exe+1228FED - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+1228FF2 - E8 097E58FF           - call victoria3.exe+7B0E00
victoria3.exe+1228FF7 - 90                    - nop 
victoria3.exe+1228FF8 - 4C 8B 45 A8           - mov r8,[rbp-58]
victoria3.exe+1228FFC - 49 83 F8 0F           - cmp r8,0F
victoria3.exe+1229000 - 76 0D                 - jna victoria3.exe+122900F
victoria3.exe+1229002 - 48 8B 55 90           - mov rdx,[rbp-70]
victoria3.exe+1229006 - 48 8D 4D 90           - lea rcx,[rbp-70]
victoria3.exe+122900A - E8 51CC3EFF           - call victoria3.exe+615C60
victoria3.exe+122900F - C5FA7F75 A0           - vmovdqu [rbp-60],xmm6
victoria3.exe+1229014 - C6 45 90 00           - mov byte ptr [rbp-70],00
victoria3.exe+1229018 - 4C 8B 45 28           - mov r8,[rbp+28]
victoria3.exe+122901C - 49 83 F8 0F           - cmp r8,0F
victoria3.exe+1229020 - 76 0D                 - jna victoria3.exe+122902F
victoria3.exe+1229022 - 48 8B 55 10           - mov rdx,[rbp+10]
victoria3.exe+1229026 - 48 8D 4D 10           - lea rcx,[rbp+10]
victoria3.exe+122902A - E8 31CC3EFF           - call victoria3.exe+615C60
victoria3.exe+122902F - C5FA7F75 20           - vmovdqu [rbp+20],xmm6
victoria3.exe+1229034 - C6 45 10 00           - mov byte ptr [rbp+10],00
victoria3.exe+1229038 - 41 B8 11000000        - mov r8d,00000011
victoria3.exe+122903E - 48 8D 15 AB8B2003     - lea rdx,[victoria3.exe+4431BF0]
victoria3.exe+1229045 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122904A - E8 A1AE7001           - call victoria3.exe+2933EF0
victoria3.exe+122904F - 83 FF 01              - cmp edi,01
victoria3.exe+1229052 - 75 09                 - jne victoria3.exe+122905D
victoria3.exe+1229054 - 48 8D 15 858B2003     - lea rdx,[victoria3.exe+4431BE0]
victoria3.exe+122905B - EB 0C                 - jmp victoria3.exe+1229069
victoria3.exe+122905D - 83 FF 02              - cmp edi,02
victoria3.exe+1229060 - 75 17                 - jne victoria3.exe+1229079
victoria3.exe+1229062 - 48 8D 15 BF8C2003     - lea rdx,[victoria3.exe+4431D28]
victoria3.exe+1229069 - 41 B8 09000000        - mov r8d,00000009
victoria3.exe+122906F - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+1229074 - E8 77AE7001           - call victoria3.exe+2933EF0
victoria3.exe+1229079 - C5FC1044 24 40        - vmovups ymm0,[rsp+40]
victoria3.exe+122907F - C5FC1145 D0           - vmovups [rbp-30],ymm0
victoria3.exe+1229084 - C5FA7F74 24 50        - vmovdqu [rsp+50],xmm6
victoria3.exe+122908A - C6 44 24 40 00        - mov byte ptr [rsp+40],00
victoria3.exe+122908F - 4C 8B 44 24 78        - mov r8,[rsp+78]
victoria3.exe+1229094 - 49 83 F8 0F           - cmp r8,0F
victoria3.exe+1229098 - 76 13                 - jna victoria3.exe+12290AD
victoria3.exe+122909A - 48 8B 54 24 60        - mov rdx,[rsp+60]
victoria3.exe+122909F - 48 8D 4C 24 60        - lea rcx,[rsp+60]
victoria3.exe+12290A4 - C5F877                - vzeroupper 
victoria3.exe+12290A7 - E8 B4CB3EFF           - call victoria3.exe+615C60
victoria3.exe+12290AC - 90                    - nop 
victoria3.exe+12290AD - 48 8D 55 F0           - lea rdx,[rbp-10]
victoria3.exe+12290B1 - 48 8D 4D 90           - lea rcx,[rbp-70]
victoria3.exe+12290B5 - C5F877                - vzeroupper 
victoria3.exe+12290B8 - E8 F307A901           - call victoria3.exe+2CB98B0
victoria3.exe+12290BD - 90                    - nop 
victoria3.exe+12290BE - 48 8D 4D D0           - lea rcx,[rbp-30]
victoria3.exe+12290C2 - 48 83 7D E8 0F        - cmp qword ptr [rbp-18],0F
victoria3.exe+12290C7 - 48 0F47 4D D0         - cmova rcx,[rbp-30]
victoria3.exe+12290CC - 48 89 4C 24 60        - mov [rsp+60],rcx
victoria3.exe+12290D1 - 8B 4D E0              - mov ecx,[rbp-20]
victoria3.exe+12290D4 - 89 4C 24 68           - mov [rsp+68],ecx
victoria3.exe+12290D8 - C6 44 24 6C 00        - mov byte ptr [rsp+6C],00
victoria3.exe+12290DD - 48 89 44 24 38        - mov [rsp+38],rax
victoria3.exe+12290E2 - 48 8D 45 30           - lea rax,[rbp+30]
victoria3.exe+12290E6 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+12290EB - 4C 8D 4D 80           - lea r9,[rbp-80]
victoria3.exe+12290EF - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+12290F4 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+12290F9 - E8 723EA2FF           - call victoria3.exe+C4CF70
victoria3.exe+12290FE - 90                    - nop 
victoria3.exe+12290FF - 48 8B D0              - mov rdx,rax
victoria3.exe+1229102 - 48 8B CE              - mov rcx,rsi
victoria3.exe+1229105 - E8 86A98802           - call victoria3.exe+3AB3A90
victoria3.exe+122910A - 90                    - nop 
victoria3.exe+122910B - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+1229110 - E8 CBC63EFF           - call victoria3.exe+6157E0
victoria3.exe+1229115 - 90                    - nop 
victoria3.exe+1229116 - 48 8D 4D 90           - lea rcx,[rbp-70]
victoria3.exe+122911A - E8 C1C63EFF           - call victoria3.exe+6157E0
victoria3.exe+122911F - 90                    - nop 
victoria3.exe+1229120 - 4C 8B 45 E8           - mov r8,[rbp-18]
victoria3.exe+1229124 - 49 83 F8 0F           - cmp r8,0F
victoria3.exe+1229128 - 76 0D                 - jna victoria3.exe+1229137
victoria3.exe+122912A - 48 8B 55 D0           - mov rdx,[rbp-30]
victoria3.exe+122912E - 48 8D 4D D0           - lea rcx,[rbp-30]
victoria3.exe+1229132 - E8 29CB3EFF           - call victoria3.exe+615C60
victoria3.exe+1229137 - 45 89 A6 B0010000     - mov [r14+000001B0],r12d
victoria3.exe+122913E - EB 35                 - jmp victoria3.exe+1229175
victoria3.exe+1229140 - 48 83 7D 00 00        - cmp qword ptr [rbp+00],00
victoria3.exe+1229145 - 74 2E                 - je victoria3.exe+1229175
victoria3.exe+1229147 - 48 8B CE              - mov rcx,rsi
victoria3.exe+122914A - E8 B1353FFF           - call victoria3.exe+61C700
victoria3.exe+122914F - 49 8B D6              - mov rdx,r14
victoria3.exe+1229152 - 48 8B CE              - mov rcx,rsi
victoria3.exe+1229155 - E8 46971900           - call victoria3.exe+13C28A0
victoria3.exe+122915A - 48 8D 55 F0           - lea rdx,[rbp-10]
victoria3.exe+122915E - 48 83 7D 08 0F        - cmp qword ptr [rbp+08],0F
victoria3.exe+1229163 - 48 0F47 55 F0         - cmova rdx,[rbp-10]
victoria3.exe+1229168 - 4C 8B 45 00           - mov r8,[rbp+00]
victoria3.exe+122916C - 48 8B CE              - mov rcx,rsi
victoria3.exe+122916F - E8 7CAD7001           - call victoria3.exe+2933EF0
victoria3.exe+1229174 - 90                    - nop 
victoria3.exe+1229175 - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+1229179 - E8 62C63EFF           - call victoria3.exe+6157E0
victoria3.exe+122917E - 90                    - nop 
victoria3.exe+122917F - 48 8D 4D F0           - lea rcx,[rbp-10]
victoria3.exe+1229183 - E8 58C63EFF           - call victoria3.exe+6157E0
victoria3.exe+1229188 - 4C 8B 85 28010000     - mov r8,[rbp+00000128]
victoria3.exe+122918F - 48 8B 8D A8000000     - mov rcx,[rbp+000000A8]
victoria3.exe+1229196 - 41 BE 33F304B5        - mov r14d,B504F333
victoria3.exe+122919C - 4D 85 C0              - test r8,r8
victoria3.exe+122919F - 74 1D                 - je victoria3.exe+12291BE
victoria3.exe+12291A1 - 48 8D 85 F0000000     - lea rax,[rbp+000000F0]
victoria3.exe+12291A8 - 4C 3B C0              - cmp r8,rax
victoria3.exe+12291AB - 0F95 C2               - setne dl
victoria3.exe+12291AE - 49 8B 00              - mov rax,[r8]
victoria3.exe+12291B1 - 49 8B C8              - mov rcx,r8
victoria3.exe+12291B4 - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+12291B7 - 48 8B 8D A8000000     - mov rcx,[rbp+000000A8]
victoria3.exe+12291BE - 48 85 C9              - test rcx,rcx
victoria3.exe+12291C1 - 74 17                 - je victoria3.exe+12291DA
victoria3.exe+12291C3 - 48 8D 45 70           - lea rax,[rbp+70]
victoria3.exe+12291C7 - 48 3B C8              - cmp rcx,rax
victoria3.exe+12291CA - 0F95 C2               - setne dl
victoria3.exe+12291CD - 48 8B 01              - mov rax,[rcx]
victoria3.exe+12291D0 - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+12291D3 - 4C 89 A5 A8000000     - mov [rbp+000000A8],r12
victoria3.exe+12291DA - 48 8B 45 C8           - mov rax,[rbp-38]
victoria3.exe+12291DE - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+12291E2 - 76 34                 - jna victoria3.exe+1229218
victoria3.exe+12291E4 - 48 8B 55 B0           - mov rdx,[rbp-50]
victoria3.exe+12291E8 - 48 8B CA              - mov rcx,rdx
victoria3.exe+12291EB - 48 FF C0              - inc rax
victoria3.exe+12291EE - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+12291F4 - 72 15                 - jb victoria3.exe+122920B
victoria3.exe+12291F6 - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+12291FA - 48 2B CA              - sub rcx,rdx
victoria3.exe+12291FD - 48 83 E9 08           - sub rcx,08
victoria3.exe+1229201 - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+1229205 - 0F87 F8020000         - ja victoria3.exe+1229503
victoria3.exe+122920B - 48 85 D2              - test rdx,rdx
victoria3.exe+122920E - 74 08                 - je victoria3.exe+1229218
victoria3.exe+1229210 - 48 8B CA              - mov rcx,rdx
victoria3.exe+1229213 - E8 1871EF02           - call victoria3.exe+4120330
victoria3.exe+1229218 - 49 63 85 581D0000     - movsxd  rax,dword ptr [r13+00001D58]
victoria3.exe+122921F - 48 69 F8 A0860100     - imul rdi,rax,000186A0
victoria3.exe+1229226 - 48 89 7D 60           - mov [rbp+60],rdi
victoria3.exe+122922A - 44 0FB7 05 62DDEA03   - movzx r8d,word ptr [victoria3.exe+50D6F94]
victoria3.exe+1229232 - 48 8D 95 C0010000     - lea rdx,[rbp+000001C0]
victoria3.exe+1229239 - 48 8D 4B 10           - lea rcx,[rbx+10]
victoria3.exe+122923D - E8 0EAF61FF           - call victoria3.exe+844150
victoria3.exe+1229242 - 4C 8B 8D C0010000     - mov r9,[rbp+000001C0]
victoria3.exe+1229249 - 4A 8D 0C 37           - lea rcx,[rdi+r14]
victoria3.exe+122924D - 48 B8 66E6096A01000000 - mov rax,000000016A09E666
victoria3.exe+1229257 - 48 3B C8              - cmp rcx,rax
victoria3.exe+122925A - 77 2D                 - ja victoria3.exe+1229289
victoria3.exe+122925C - 4B 8D 0C 31           - lea rcx,[r9+r14]
victoria3.exe+1229260 - 48 3B C8              - cmp rcx,rax
victoria3.exe+1229263 - 77 24                 - ja victoria3.exe+1229289
victoria3.exe+1229265 - 4C 0FAF CF            - imul r9,rdi
victoria3.exe+1229269 - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+1229273 - 49 F7 E9              - imul r9
victoria3.exe+1229276 - 48 8B FA              - mov rdi,rdx
victoria3.exe+1229279 - 48 C1 FF 0E           - sar rdi,0E
victoria3.exe+122927D - 48 8B C7              - mov rax,rdi
victoria3.exe+1229280 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+1229284 - 48 03 F8              - add rdi,rax
victoria3.exe+1229287 - EB 5B                 - jmp victoria3.exe+12292E4
victoria3.exe+1229289 - 49 8B C9              - mov rcx,r9
victoria3.exe+122928C - 4C 3B CF              - cmp r9,rdi
victoria3.exe+122928F - 48 0F4C CF            - cmovl rcx,rdi
victoria3.exe+1229293 - 4C 0F4F CF            - cmovg r9,rdi
victoria3.exe+1229297 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+12292A1 - 49 8B C2              - mov rax,r10
victoria3.exe+12292A4 - 48 F7 E9              - imul rcx
victoria3.exe+12292A7 - 4C 8B C2              - mov r8,rdx
victoria3.exe+12292AA - 49 C1 F8 0E           - sar r8,0E
victoria3.exe+12292AE - 49 8B C0              - mov rax,r8
victoria3.exe+12292B1 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+12292B5 - 4C 03 C0              - add r8,rax
victoria3.exe+12292B8 - 49 69 C0 A0860100     - imul rax,r8,000186A0
victoria3.exe+12292BF - 48 2B C8              - sub rcx,rax
victoria3.exe+12292C2 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+12292C6 - 49 8B C2              - mov rax,r10
victoria3.exe+12292C9 - 48 F7 E9              - imul rcx
victoria3.exe+12292CC - 48 8B FA              - mov rdi,rdx
victoria3.exe+12292CF - 48 C1 FF 0E           - sar rdi,0E
victoria3.exe+12292D3 - 48 8B C7              - mov rax,rdi
victoria3.exe+12292D6 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+12292DA - 48 03 F8              - add rdi,rax
victoria3.exe+12292DD - 4D 0FAF C1            - imul r8,r9
victoria3.exe+12292E1 - 49 03 F8              - add rdi,r8
victoria3.exe+12292E4 - 48 89 7D 88           - mov [rbp-78],rdi
victoria3.exe+12292E8 - 44 0FB7 05 A8DCEA03   - movzx r8d,word ptr [victoria3.exe+50D6F98]
victoria3.exe+12292F0 - 48 8D 95 D0010000     - lea rdx,[rbp+000001D0]
victoria3.exe+12292F7 - 48 8D 4B 10           - lea rcx,[rbx+10]
victoria3.exe+12292FB - E8 50AE61FF           - call victoria3.exe+844150
victoria3.exe+1229300 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+1229304 - C5F81145 30           - vmovups [rbp+30],xmm0
victoria3.exe+1229309 - C5FA7F75 40           - vmovdqu [rbp+40],xmm6
victoria3.exe+122930E - C6 45 30 00           - mov byte ptr [rbp+30],00
victoria3.exe+1229312 - 48 8D 05 47462503     - lea rax,[victoria3.exe+447D960]
victoria3.exe+1229319 - 48 89 85 B0000000     - mov [rbp+000000B0],rax
victoria3.exe+1229320 - 48 8D 45 88           - lea rax,[rbp-78]
victoria3.exe+1229324 - 48 89 85 B8000000     - mov [rbp+000000B8],rax
victoria3.exe+122932B - 48 8D 85 D0010000     - lea rax,[rbp+000001D0]
victoria3.exe+1229332 - 48 89 85 C0000000     - mov [rbp+000000C0],rax
victoria3.exe+1229339 - 48 8D 45 60           - lea rax,[rbp+60]
victoria3.exe+122933D - 48 89 85 C8000000     - mov [rbp+000000C8],rax
victoria3.exe+1229344 - 48 8D 85 B0000000     - lea rax,[rbp+000000B0]
victoria3.exe+122934B - 48 89 85 E8000000     - mov [rbp+000000E8],rax
victoria3.exe+1229352 - 48 8D 55 88           - lea rdx,[rbp-78]
victoria3.exe+1229356 - 48 8D 85 D0010000     - lea rax,[rbp+000001D0]
victoria3.exe+122935D - 48 3B BD D0010000     - cmp rdi,[rbp+000001D0]
victoria3.exe+1229364 - 48 0F4D D0            - cmovge rdx,rax
victoria3.exe+1229368 - 4C 8D 4D 30           - lea r9,[rbp+30]
victoria3.exe+122936C - 4C 8D 85 B0000000     - lea r8,[rbp+000000B0]
victoria3.exe+1229373 - 48 8B 12              - mov rdx,[rdx]
victoria3.exe+1229376 - 49 8B CF              - mov rcx,r15
victoria3.exe+1229379 - E8 F250AEFF           - call victoria3.exe+D0E470
victoria3.exe+122937E - 90                    - nop 
victoria3.exe+122937F - 48 8B 8D E8000000     - mov rcx,[rbp+000000E8]
victoria3.exe+1229386 - 48 85 C9              - test rcx,rcx
victoria3.exe+1229389 - 74 1A                 - je victoria3.exe+12293A5
victoria3.exe+122938B - 48 8D 85 B0000000     - lea rax,[rbp+000000B0]
victoria3.exe+1229392 - 48 3B C8              - cmp rcx,rax
victoria3.exe+1229395 - 0F95 C2               - setne dl
victoria3.exe+1229398 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+122939B - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+122939E - 4C 89 A5 E8000000     - mov [rbp+000000E8],r12
victoria3.exe+12293A5 - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+12293A9 - E8 32C43EFF           - call victoria3.exe+6157E0
victoria3.exe+12293AE - 49 8B 55 68           - mov rdx,[r13+68]
victoria3.exe+12293B2 - 48 89 55 68           - mov [rbp+68],rdx
victoria3.exe+12293B6 - 48 81 FA A0860100     - cmp rdx,000186A0
victoria3.exe+12293BD - 0F8D AE000000         - jnl victoria3.exe+1229471
victoria3.exe+12293C3 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+12293C7 - C5F81145 B0           - vmovups [rbp-50],xmm0
victoria3.exe+12293CC - C5FA7F75 C0           - vmovdqu [rbp-40],xmm6
victoria3.exe+12293D1 - C6 45 B0 00           - mov byte ptr [rbp-50],00
victoria3.exe+12293D5 - 48 8D 05 D4462503     - lea rax,[victoria3.exe+447DAB0]
victoria3.exe+12293DC - 48 89 85 30010000     - mov [rbp+00000130],rax
victoria3.exe+12293E3 - 48 8D 45 68           - lea rax,[rbp+68]
victoria3.exe+12293E7 - 48 89 85 38010000     - mov [rbp+00000138],rax
victoria3.exe+12293EE - 48 8D 85 30010000     - lea rax,[rbp+00000130]
victoria3.exe+12293F5 - 48 89 85 68010000     - mov [rbp+00000168],rax
victoria3.exe+12293FC - 4C 8D 4D B0           - lea r9,[rbp-50]
victoria3.exe+1229400 - 4C 8D 85 30010000     - lea r8,[rbp+00000130]
victoria3.exe+1229407 - 49 8B CF              - mov rcx,r15
victoria3.exe+122940A - E8 A1589CFF           - call victoria3.exe+BEECB0
victoria3.exe+122940F - 90                    - nop 
victoria3.exe+1229410 - 48 8B 8D 68010000     - mov rcx,[rbp+00000168]
victoria3.exe+1229417 - 48 85 C9              - test rcx,rcx
victoria3.exe+122941A - 74 1A                 - je victoria3.exe+1229436
victoria3.exe+122941C - 48 8D 85 30010000     - lea rax,[rbp+00000130]
victoria3.exe+1229423 - 48 3B C8              - cmp rcx,rax
victoria3.exe+1229426 - 0F95 C2               - setne dl
victoria3.exe+1229429 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+122942C - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+122942F - 4C 89 A5 68010000     - mov [rbp+00000168],r12
victoria3.exe+1229436 - 48 8B 45 C8           - mov rax,[rbp-38]
victoria3.exe+122943A - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+122943E - 76 31                 - jna victoria3.exe+1229471
victoria3.exe+1229440 - 48 8B 55 B0           - mov rdx,[rbp-50]
victoria3.exe+1229444 - 48 8B CA              - mov rcx,rdx
victoria3.exe+1229447 - 48 FF C0              - inc rax
victoria3.exe+122944A - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+1229450 - 72 11                 - jb victoria3.exe+1229463
victoria3.exe+1229452 - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+1229456 - 48 2B CA              - sub rcx,rdx
victoria3.exe+1229459 - 48 83 E9 08           - sub rcx,08
victoria3.exe+122945D - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+1229461 - 77 70                 - ja victoria3.exe+12294D3
victoria3.exe+1229463 - 48 85 D2              - test rdx,rdx
victoria3.exe+1229466 - 74 09                 - je victoria3.exe+1229471
victoria3.exe+1229468 - 48 8B CA              - mov rcx,rdx
victoria3.exe+122946B - E8 C06EEF02           - call victoria3.exe+4120330
victoria3.exe+1229470 - 90                    - nop 
victoria3.exe+1229471 - 48 85 DB              - test rbx,rbx
victoria3.exe+1229474 - 74 39                 - je victoria3.exe+12294AF
victoria3.exe+1229476 - B8 FFFFFFFF           - mov eax,FFFFFFFF
victoria3.exe+122947B - F0 0FC1 43 08         - lock xadd [rbx+08],eax
victoria3.exe+1229480 - 83 F8 01              - cmp eax,01
victoria3.exe+1229483 - 75 2A                 - jne victoria3.exe+12294AF
victoria3.exe+1229485 - 33 D2                 - xor edx,edx
victoria3.exe+1229487 - 48 8B CB              - mov rcx,rbx
victoria3.exe+122948A - E8 C18D58FF           - call victoria3.exe+7B2250
victoria3.exe+122948F - 48 8B 05 0A5DEB03     - mov rax,[victoria3.exe+50DF1A0]
victoria3.exe+1229496 - 48 8B 78 10           - mov rdi,[rax+10]
victoria3.exe+122949A - 48 8B CB              - mov rcx,rbx
victoria3.exe+122949D - E8 E6E5F002           - call victoria3.exe+4137A88
victoria3.exe+12294A2 - 48 8B D0              - mov rdx,rax
victoria3.exe+12294A5 - 48 8D 0D F45CEB03     - lea rcx,[victoria3.exe+50DF1A0]
victoria3.exe+12294AC - FF D7                 - call rdi
victoria3.exe+12294AE - 90                    - nop 
victoria3.exe+12294AF - 48 8B 9C 24 C8020000  - mov rbx,[rsp+000002C8]
victoria3.exe+12294B7 - C5F828B4 24 70 020000 - vmovaps xmm6,[rsp+00000270]
victoria3.exe+12294C0 - 48 81 C4 80020000     - add rsp,00000280
victoria3.exe+12294C7 - 41 5F                 - pop r15
victoria3.exe+12294C9 - 41 5E                 - pop r14
victoria3.exe+12294CB - 41 5D                 - pop r13
victoria3.exe+12294CD - 41 5C                 - pop r12
victoria3.exe+12294CF - 5F                    - pop rdi
victoria3.exe+12294D0 - 5E                    - pop rsi
victoria3.exe+12294D1 - 5D                    - pop rbp
victoria3.exe+12294D2 - C3                    - ret 


# 补充命中断点 7FF7EB0A9218: 条件 R13 == 0x32FDB11DB60 时的寄存器情况
Registers:                Flags
RAX 0000000000000000    CF 0
RBX 00000332B01ECD60    PF 1
RCX 0000000000000000    AF 0
RDX 0000000000000000    ZF 1
RSI 00000330FF363770    SF 0
RDI 0000032F518431E0    DF 0
RBP 000000AE6DDFEFC0    OF 0
RSP 000000AE6DDFEEC0
R8  0000032F518431E0
R9  0000000000003FFF
R10 0000000000000000
R11 0000000000000000
R12 0000000000000000
R13 0000032FDB11DB60
R14 0000000B504F333
R15 000000AE6DDF FF1C0
RIP 00007FF7EB0A9218

Special
CS 0033
SS 002B
DS 002B
ES 002B
FS 0053
GS 002B


# 暂时对 1228B90 的结论

从 `Docs\trace_capcity7.md` 的完整代码看，`+1228B90` 虽然读取了九州对象的 `[R13+1D58] = 184`，但它更像“对象状态/属性更新函数”，目前没有证据表明它正在遍历商品并分配贸易容量。

关键原因是 `+1229218` 位于一个失败分支的尾部：

```asm
+1228C72  mov r14d,B504F333
+1228C78  test al,al
+1228C7A  je   +1229218

+1228C80  cmp dword ptr [rsi+E8],0
+1228C87  jng  +1229218
```

也就是说，只有前面的虚函数检查失败，或者 `[RSI+E8] <= 0` 时，才跳到 `+1229218`。它不是主循环中“每个商品都计算一次”的正常路径。

`+1229218` 后面的实际流程如下：

```asm
movsxd rax,[r13+1D58]       ; 读取容量 184
imul   rdi,rax,186A0        ; 184 * 100000
mov    [rbp+60],rdi
```

因此：

```text
[RBP+60] = 18,400,000
```

这里的 `0x186A0` 是 `100000`，说明游戏使用固定精度整数。

随后：

```asm
movzx r8d,word ptr [victoria3.exe+50D6F94]
lea   rdx,[rbp+1C0]
lea   rcx,[rbx+10]
call  victoria3.exe+844150
```

`+844150` 根据 `RCX = RBX+10` 和 `R8D` 指定的类型或字段，向 `[RBP+1C0]` 输出另一个固定精度数值。返回后：

```asm
mov r9,[rbp+1C0]
```

接着代码使用容量值 `RDI` 和这个输出值 `R9` 做带边界保护的定点插值/比例运算。常量：

```text
0x186A0       = 100000
0x16A09E666   = 溢出保护上限
0x29F16B11C6D1E109
```

属于定点乘法和除法的实现，不像商品遍历索引或订单数量求和。

然后第二次调用：

```asm
movzx r8d,word ptr [victoria3.exe+50D6F98]
lea   rdx,[rbp+1D0]
lea   rcx,[rbx+10]
call  victoria3.exe+844150
```

会把另一个属性写到 `[RBP+1D0]`。随后：

```asm
cmp    rdi,[rbp+1D0]
cmovge rdx,rax
mov    rdx,[rdx]
mov    rcx,r15
call   victoria3.exe+D0E470
```

这表示它最终在两个计算结果之间选择一个，再交给 `+D0E470`。更像是“取限制值/更新对象属性”，而不是把 184 分配给商品。

另外：

```asm
+12293AE mov rdx,[r13+68]
+12293B6 cmp rdx,186A0
```

这里读取的是对象偏移 `+68`，不是贸易容量字段 `+1D58`。如果 `[R13+68] < 100000`，还会构造另一组临时对象并调用 `+BEECB0`。这进一步说明函数在处理多个属性状态。

建议你在 CE 中这样验证：

1. 保留条件断点：

   ```text
   7FF7EB0A9218
   R13 == 32FDB11DB60
   ```

2. 命中后单步到 `+122923D`，记录：

   ```text
   RCX
   RDX
   R8D
   RBX
   [RBX+10]
   [RBP+1C0]
   ```

3. 越过 `call +844150` 后记录：

   ```text
   RAX
   [RBP+1C0]
   R9
   ```

4. 再在第二次调用前后记录：

   ```text
   [RBP+1D0]
   R8D
   RAX
   ```

5. 同时记录：

   ```text
   [R13+68]
   [RBP+60]
   [RBP-78]
   ```

如果这些值只是在固定精度范围内做限制、插值、取最小值，并且没有出现商品 ID、商品数组指针、供给订单数或需求订单数，那么就可以基本排除该函数是贸易容量分配函数。

下一步更有价值的是观察 `+122A470` 或其内部的 `+122AB50`，尤其记录：

```text
当前商品对象指针
商品索引或类型 ID
容量剩余值
计算前后的订单数量
调用返回值
```

而 `+1228B90` 建议暂时定位为“读取贸易中心容量并更新某个固定精度属性”的辅助函数。