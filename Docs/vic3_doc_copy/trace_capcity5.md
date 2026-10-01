
这次不再是UI频繁触发的了，真正走时间然后看 access
32FDB11F8B8 和 32FDB11F8BC
这两个是九州贸易中心容量的稳定地址，大概率会被用来计算九州贸易中心硬木的进口数量。

32FDB11F8BC 的 access
7FF7EB0AB9DA - 89 86 5C1D0000  - mov [rsi+00001D5C],eax
7FF7EB07D5BB - 41 8B 86 5C1D0000  - mov eax,[r14+00001D5C]
7FF7EACB7358 - 2B 90 5C1D0000  - sub edx,[rax+00001D5C]

32FDB11F8B8 的 access
7FF7EB0AB9C7 - 89 86 581D0000  - mov [rsi+00001D58],eax
7FF7EB0ABA8E - 44 2B BE 581D0000  - sub r15d,[rsi+00001D58]
7FF7EB0A9218 - 49 63 85 581D0000  - movsxd  rax,dword ptr [r13+00001D58]
7FF7EB07D5C9 - 41 8B 86 581D0000  - mov eax,[r14+00001D58]
7FF7EACB7334 - 48 63 90 581D0000  - movsxd  rdx,dword ptr [rax+00001D58]
7FF7EB091346 - 48 63 87 581D0000  - movsxd  rax,dword ptr [rdi+00001D58]



# 7FF7EB0AB9DA

victoria3.exe+122B99D - CC                    - int 3 
victoria3.exe+122B99E - CC                    - int 3 
victoria3.exe+122B99F - CC                    - int 3 
victoria3.exe+122B9A0 - 48 89 5C 24 20        - mov [rsp+20],rbx
victoria3.exe+122B9A5 - 89 54 24 10           - mov [rsp+10],edx
victoria3.exe+122B9A9 - 55                    - push rbp
victoria3.exe+122B9AA - 56                    - push rsi
victoria3.exe+122B9AB - 57                    - push rdi
victoria3.exe+122B9AC - 41 54                 - push r12
victoria3.exe+122B9AE - 41 55                 - push r13
victoria3.exe+122B9B0 - 41 56                 - push r14
victoria3.exe+122B9B2 - 41 57                 - push r15
victoria3.exe+122B9B4 - 48 81 EC B0020000     - sub rsp,000002B0
victoria3.exe+122B9BB - 8B DA                 - mov ebx,edx
victoria3.exe+122B9BD - 48 8B F1              - mov rsi,rcx
victoria3.exe+122B9C0 - 33 D2                 - xor edx,edx
victoria3.exe+122B9C2 - E8 89E2FFFF           - call victoria3.exe+1229C50
victoria3.exe+122B9C7 - 89 86 581D0000        - mov [rsi+00001D58],eax
victoria3.exe+122B9CD - 33 D2                 - xor edx,edx
victoria3.exe+122B9CF - 48 8B CE              - mov rcx,rsi
victoria3.exe+122B9D2 - E8 99EAFFFF           - call victoria3.exe+122A470
victoria3.exe+122B9D7 - 44 8B F8              - mov r15d,eax
victoria3.exe+122B9DA - 89 86 5C1D0000        - mov [rsi+00001D5C],eax
victoria3.exe+122B9E0 - 85 C0                 - test eax,eax
victoria3.exe+122B9E2 - 0F8E 38030000         - jng victoria3.exe+122BD20
victoria3.exe+122B9E8 - 80 BE B8110000 00     - cmp byte ptr [rsi+000011B8],00
victoria3.exe+122B9EF - 74 24                 - je victoria3.exe+122BA15
victoria3.exe+122B9F1 - 8B 86 480B0000        - mov eax,[rsi+00000B48]
victoria3.exe+122B9F7 - 83 F8 FF              - cmp eax,-01
victoria3.exe+122B9FA - 74 19                 - je victoria3.exe+122BA15
victoria3.exe+122B9FC - 89 84 24 F0020000     - mov [rsp+000002F0],eax
victoria3.exe+122BA03 - 48 8D 8C 24 F0020000  - lea rcx,[rsp+000002F0]
victoria3.exe+122BA0B - E8 A07959FF           - call victoria3.exe+7C33B0
victoria3.exe+122BA10 - 8B 48 10              - mov ecx,[rax+10]
victoria3.exe+122BA13 - EB 20                 - jmp victoria3.exe+122BA35
victoria3.exe+122BA15 - 8B 86 480E0000        - mov eax,[rsi+00000E48]
victoria3.exe+122BA1B - 89 84 24 F0020000     - mov [rsp+000002F0],eax
victoria3.exe+122BA22 - 48 8D 8C 24 F0020000  - lea rcx,[rsp+000002F0]
victoria3.exe+122BA2A - E8 815058FF           - call victoria3.exe+7B0AB0
victoria3.exe+122BA2F - 8B 88 D4090000        - mov ecx,[rax+000009D4]
victoria3.exe+122BA35 - 89 8C 24 F0020000     - mov [rsp+000002F0],ecx
victoria3.exe+122BA3C - 48 8D 8C 24 F0020000  - lea rcx,[rsp+000002F0]
victoria3.exe+122BA44 - E8 374959FF           - call victoria3.exe+7C0380
victoria3.exe+122BA49 - 48 8D 88 48080000     - lea rcx,[rax+00000848]
victoria3.exe+122BA50 - E8 5B5058FF           - call victoria3.exe+7B0AB0
victoria3.exe+122BA55 - 48 8B E8              - mov rbp,rax
victoria3.exe+122BA58 - 83 3D E13AEB03 00     - cmp dword ptr [victoria3.exe+50DF540],00
victoria3.exe+122BA5F - 75 18                 - jne victoria3.exe+122BA79
victoria3.exe+122BA61 - 48 8D 05 1E646C04     - lea rax,[victoria3.exe+58F1E86]
victoria3.exe+122BA68 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122BA6D - 48 8D 0D 5C011B03     - lea rcx,[victoria3.exe+43DBBD0]
victoria3.exe+122BA74 - E8 476D8702           - call victoria3.exe+3AA27C0
victoria3.exe+122BA79 - 48 8B 0D D0CF6804     - mov rcx,[victoria3.exe+58B8A50]
victoria3.exe+122BA80 - 48 8B 91 08060000     - mov rdx,[rcx+00000608]
victoria3.exe+122BA87 - 4C 8B AA 20010000     - mov r13,[rdx+00000120]
victoria3.exe+122BA8E - 44 2B BE 581D0000     - sub r15d,[rsi+00001D58]
victoria3.exe+122BA95 - 45 32 E4              - xor r12b,r12b
victoria3.exe+122BA98 - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+122BA9D - E8 1E77C0FF           - call victoria3.exe+E331C0
victoria3.exe+122BAA2 - 90                    - nop 
victoria3.exe+122BAA3 - 4C 8B B6 D81D0000     - mov r14,[rsi+00001DD8]
victoria3.exe+122BAAA - 48 63 86 E41D0000     - movsxd  rax,dword ptr [rsi+00001DE4]
victoria3.exe+122BAB1 - 49 8D 04 C6           - lea rax,[r14+rax*8]
victoria3.exe+122BAB5 - 48 89 84 24 F0020000  - mov [rsp+000002F0],rax
victoria3.exe+122BABD - 4C 3B F0              - cmp r14,rax
victoria3.exe+122BAC0 - 0F84 F2010000         - je victoria3.exe+122BCB8
victoria3.exe+122BAC6 - 66 66 0F1F 84 00 00000000  - nop word ptr [rax+rax+00000000]
victoria3.exe+122BAD0 - 49 8B 3E              - mov rdi,[r14]
victoria3.exe+122BAD3 - 80 BE B8110000 00     - cmp byte ptr [rsi+000011B8],00
victoria3.exe+122BADA - 75 33                 - jne victoria3.exe+122BB0F
victoria3.exe+122BADC - 33 D2                 - xor edx,edx
victoria3.exe+122BADE - 33 C9                 - xor ecx,ecx
victoria3.exe+122BAE0 - 48 63 85 14240000     - movsxd  rax,dword ptr [rbp+00002414]
victoria3.exe+122BAE7 - 85 C0                 - test eax,eax
victoria3.exe+122BAE9 - 7E 24                 - jle victoria3.exe+122BB0F
victoria3.exe+122BAEB - 4C 8B C0              - mov r8,rax
victoria3.exe+122BAEE - 48 8B 85 08240000     - mov rax,[rbp+00002408]
victoria3.exe+122BAF5 - 48 39 38              - cmp [rax],rdi
victoria3.exe+122BAF8 - 74 10                 - je victoria3.exe+122BB0A
victoria3.exe+122BAFA - FF C2                 - inc edx
victoria3.exe+122BAFC - 48 FF C1              - inc rcx
victoria3.exe+122BAFF - 48 83 C0 08           - add rax,08
victoria3.exe+122BB03 - 49 3B C8              - cmp rcx,r8
victoria3.exe+122BB06 - 7C ED                 - jl victoria3.exe+122BAF5
victoria3.exe+122BB08 - EB 05                 - jmp victoria3.exe+122BB0F
victoria3.exe+122BB0A - 83 FA FF              - cmp edx,-01
victoria3.exe+122BB0D - 75 60                 - jne victoria3.exe+122BB6F
victoria3.exe+122BB0F - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BB12 - 48 8B CD              - mov rcx,rbp
victoria3.exe+122BB15 - E8 668FA0FF           - call victoria3.exe+C34A80
victoria3.exe+122BB1A - 34 01                 - xor al,01
victoria3.exe+122BB1C - 75 51                 - jne victoria3.exe+122BB6F
victoria3.exe+122BB1E - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BB21 - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BB24 - E8 A7EFFFFF           - call victoria3.exe+122AAD0
victoria3.exe+122BB29 - 84 C0                 - test al,al
victoria3.exe+122BB2B - 0F85 6E010000         - jne victoria3.exe+122BC9F
victoria3.exe+122BB31 - 48 63 5F 10           - movsxd  rbx,dword ptr [rdi+10]
victoria3.exe+122BB35 - 8B CB                 - mov ecx,ebx
victoria3.exe+122BB37 - E8 F4AADFFF           - call victoria3.exe+1026630
victoria3.exe+122BB3C - 84 C0                 - test al,al
victoria3.exe+122BB3E - 74 2F                 - je victoria3.exe+122BB6F
victoria3.exe+122BB40 - 0FB6 C3               - movzx eax,bl
victoria3.exe+122BB43 - 24 3F                 - and al,3F
victoria3.exe+122BB45 - 0FB6 C8               - movzx ecx,al
victoria3.exe+122BB48 - 48 8B C3              - mov rax,rbx
victoria3.exe+122BB4B - 48 C1 E8 06           - shr rax,06
victoria3.exe+122BB4F - 49 8B 84 C5 C8050000  - mov rax,[r13+rax*8+000005C8]
victoria3.exe+122BB57 - 48 0FA3 C8            - bt rax,rcx
victoria3.exe+122BB5B - 73 12                 - jae victoria3.exe+122BB6F
victoria3.exe+122BB5D - 49 8B 85 B0050000     - mov rax,[r13+000005B0]
victoria3.exe+122BB64 - 48 83 3C D8  00       - cmp qword ptr [rax+rbx*8],00
victoria3.exe+122BB69 - 0F8F 30010000         - jg victoria3.exe+122BC9F
victoria3.exe+122BB6F - 48 63 5F 10           - movsxd  rbx,dword ptr [rdi+10]
victoria3.exe+122BB73 - 8B CB                 - mov ecx,ebx
victoria3.exe+122BB75 - E8 B6AADFFF           - call victoria3.exe+1026630
victoria3.exe+122BB7A - 84 C0                 - test al,al
victoria3.exe+122BB7C - 74 2A                 - je victoria3.exe+122BBA8
victoria3.exe+122BB7E - 0FB6 C3               - movzx eax,bl
victoria3.exe+122BB81 - 24 3F                 - and al,3F
victoria3.exe+122BB83 - 0FB6 C8               - movzx ecx,al
victoria3.exe+122BB86 - 48 8B C3              - mov rax,rbx
victoria3.exe+122BB89 - 48 C1 E8 06           - shr rax,06
victoria3.exe+122BB8D - 48 8B 84 C6 A81D0000  - mov rax,[rsi+rax*8+00001DA8]
victoria3.exe+122BB95 - 48 0FA3 C8            - bt rax,rcx
victoria3.exe+122BB99 - 73 0D                 - jae victoria3.exe+122BBA8
victoria3.exe+122BB9B - 48 8B 8E 901D0000     - mov rcx,[rsi+00001D90]
victoria3.exe+122BBA2 - 48 8B 0C D9           - mov rcx,[rcx+rbx*8]
victoria3.exe+122BBA6 - EB 02                 - jmp victoria3.exe+122BBAA
victoria3.exe+122BBA8 - 33 C9                 - xor ecx,ecx
victoria3.exe+122BBAA - 49 BC 09E1D1C6116BF129 - mov r12,29F16B11C6D1E109
victoria3.exe+122BBB4 - 49 8B C4              - mov rax,r12
victoria3.exe+122BBB7 - 48 F7 E9              - imul rcx
victoria3.exe+122BBBA - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122BBBE - 48 8B C2              - mov rax,rdx
victoria3.exe+122BBC1 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122BBC5 - 48 03 D0              - add rdx,rax
victoria3.exe+122BBC8 - 8B DA                 - mov ebx,edx
victoria3.exe+122BBCA - F7 DB                 - neg ebx
victoria3.exe+122BBCC - 0F48 DA               - cmovs ebx,edx
victoria3.exe+122BBCF - 44 2B FB              - sub r15d,ebx
victoria3.exe+122BBD2 - 4C 8B C7              - mov r8,rdi
victoria3.exe+122BBD5 - 48 8D 94 24 00030000  - lea rdx,[rsp+00000300]
victoria3.exe+122BBDD - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BBE0 - E8 6BEFFFFF           - call victoria3.exe+122AB50
victoria3.exe+122BBE5 - 4C 8B 08              - mov r9,[rax]
victoria3.exe+122BBE8 - 48 63 DB              - movsxd  rbx,ebx
victoria3.exe+122BBEB - 48 69 CB A0860100     - imul rcx,rbx,000186A0
victoria3.exe+122BBF2 - BA 33F304B5           - mov edx,B504F333
victoria3.exe+122BBF7 - 48 8D 04 11           - lea rax,[rcx+rdx]
victoria3.exe+122BBFB - 49 B8 66E6096A01000000 - mov r8,000000016A09E666
victoria3.exe+122BC05 - 49 3B C0              - cmp rax,r8
victoria3.exe+122BC08 - 77 0F                 - ja victoria3.exe+122BC19
victoria3.exe+122BC0A - 49 8D 04 11           - lea rax,[r9+rdx]
victoria3.exe+122BC0E - 49 3B C0              - cmp rax,r8
victoria3.exe+122BC11 - 77 06                 - ja victoria3.exe+122BC19
victoria3.exe+122BC13 - 49 0FAF D9            - imul rbx,r9
victoria3.exe+122BC17 - EB 4E                 - jmp victoria3.exe+122BC67
victoria3.exe+122BC19 - 4D 8B C1              - mov r8,r9
victoria3.exe+122BC1C - 4C 3B C9              - cmp r9,rcx
victoria3.exe+122BC1F - 4C 0F4C C1            - cmovl r8,rcx
victoria3.exe+122BC23 - 4C 0F4F C9            - cmovg r9,rcx
victoria3.exe+122BC27 - 49 8B C4              - mov rax,r12
victoria3.exe+122BC2A - 49 F7 E8              - imul r8
victoria3.exe+122BC2D - 48 8B CA              - mov rcx,rdx
victoria3.exe+122BC30 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+122BC34 - 48 8B C1              - mov rax,rcx
victoria3.exe+122BC37 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122BC3B - 48 03 C8              - add rcx,rax
victoria3.exe+122BC3E - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+122BC45 - 4C 2B C0              - sub r8,rax
victoria3.exe+122BC48 - 4D 0FAF C1            - imul r8,r9
victoria3.exe+122BC4C - 49 8B C4              - mov rax,r12
victoria3.exe+122BC4F - 49 F7 E8              - imul r8
victoria3.exe+122BC52 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122BC56 - 48 8B DA              - mov rbx,rdx
victoria3.exe+122BC59 - 48 C1 EB 3F           - shr rbx,3F
victoria3.exe+122BC5D - 48 03 DA              - add rbx,rdx
victoria3.exe+122BC60 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+122BC64 - 48 03 D9              - add rbx,rcx
victoria3.exe+122BC67 - 4C 8B C3              - mov r8,rbx
victoria3.exe+122BC6A - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BC6D - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+122BC72 - E8 C9BDDFFF           - call victoria3.exe+1027A40
victoria3.exe+122BC77 - 4C 8B C3              - mov r8,rbx
victoria3.exe+122BC7A - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BC7D - 48 8D 8C 24 70010000  - lea rcx,[rsp+00000170]
victoria3.exe+122BC85 - E8 B6BDDFFF           - call victoria3.exe+1027A40
victoria3.exe+122BC8A - 48 8D 8E 881D0000     - lea rcx,[rsi+00001D88]
victoria3.exe+122BC91 - 45 33 C0              - xor r8d,r8d
victoria3.exe+122BC94 - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BC97 - E8 C4BADFFF           - call victoria3.exe+1027760
victoria3.exe+122BC9C - 41 B4 01              - mov r12b,01
victoria3.exe+122BC9F - 49 83 C6 08           - add r14,08
victoria3.exe+122BCA3 - 4C 3B B4 24 F0020000  - cmp r14,[rsp+000002F0]
victoria3.exe+122BCAB - 0F85 1FFEFFFF         - jne victoria3.exe+122BAD0
victoria3.exe+122BCB1 - 8B 9C 24 F8020000     - mov ebx,[rsp+000002F8]
victoria3.exe+122BCB8 - 45 85 FF              - test r15d,r15d
victoria3.exe+122BCBB - 7E 35                 - jle victoria3.exe+122BCF2
victoria3.exe+122BCBD - 0FAF 5E 08            - imul ebx,[rsi+08]
victoria3.exe+122BCC1 - 89 9C 24 F0020000     - mov [rsp+000002F0],ebx
victoria3.exe+122BCC8 - B8 9FBAA65E           - mov eax,5EA6BA9F
victoria3.exe+122BCCD - 2B C3                 - sub eax,ebx
victoria3.exe+122BCCF - 89 84 24 F4020000     - mov [rsp+000002F4],eax
victoria3.exe+122BCD6 - 4C 8D 8C 24 F0020000  - lea r9,[rsp+000002F0]
victoria3.exe+122BCDE - 4C 8D 44 24 30        - lea r8,[rsp+30]
victoria3.exe+122BCE3 - 41 8B D7              - mov edx,r15d
victoria3.exe+122BCE6 - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BCE9 - E8 52000000           - call victoria3.exe+122BD40
victoria3.exe+122BCEE - 85 C0                 - test eax,eax
victoria3.exe+122BCF0 - 7F 05                 - jg victoria3.exe+122BCF7
victoria3.exe+122BCF2 - 45 84 E4              - test r12b,r12b
victoria3.exe+122BCF5 - 74 1F                 - je victoria3.exe+122BD16
victoria3.exe+122BCF7 - 48 8B 06              - mov rax,[rsi]
victoria3.exe+122BCFA - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BCFD - FF 50 08              - call qword ptr [rax+08]
victoria3.exe+122BD00 - 84 C0                 - test al,al
victoria3.exe+122BD02 - 74 12                 - je victoria3.exe+122BD16
victoria3.exe+122BD04 - 48 8D 8E 701D0000     - lea rcx,[rsi+00001D70]
victoria3.exe+122BD0B - BA 03000000           - mov edx,00000003
victoria3.exe+122BD10 - E8 DB09D8FF           - call victoria3.exe+FAC6F0
victoria3.exe+122BD15 - 90                    - nop 
victoria3.exe+122BD16 - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+122BD1B - E8 907AC0FF           - call victoria3.exe+E337B0
victoria3.exe+122BD20 - 48 8B 9C 24 08030000  - mov rbx,[rsp+00000308]
victoria3.exe+122BD28 - 48 81 C4 B0020000     - add rsp,000002B0
victoria3.exe+122BD2F - 41 5F                 - pop r15
victoria3.exe+122BD31 - 41 5E                 - pop r14
victoria3.exe+122BD33 - 41 5D                 - pop r13
victoria3.exe+122BD35 - 41 5C                 - pop r12
victoria3.exe+122BD37 - 5F                    - pop rdi
victoria3.exe+122BD38 - 5E                    - pop rsi
victoria3.exe+122BD39 - 5D                    - pop rbp
victoria3.exe+122BD3A - C3                    - ret 


# 7FF7EB07D5BB
victoria3.exe+11FD46E - CC                    - int 3 
victoria3.exe+11FD46F - CC                    - int 3 
victoria3.exe+11FD470 - 4C 89 4C 24 20        - mov [rsp+20],r9
victoria3.exe+11FD475 - 4C 89 44 24 18        - mov [rsp+18],r8
victoria3.exe+11FD47A - 48 89 54 24 10        - mov [rsp+10],rdx
victoria3.exe+11FD47F - 53                    - push rbx
victoria3.exe+11FD480 - 55                    - push rbp
victoria3.exe+11FD481 - 56                    - push rsi
victoria3.exe+11FD482 - 57                    - push rdi
victoria3.exe+11FD483 - 41 54                 - push r12
victoria3.exe+11FD485 - 41 55                 - push r13
victoria3.exe+11FD487 - 41 56                 - push r14
victoria3.exe+11FD489 - 41 57                 - push r15
victoria3.exe+11FD48B - 48 81 EC E8020000     - sub rsp,000002E8
victoria3.exe+11FD492 - 49 8B D8              - mov rbx,r8
victoria3.exe+11FD495 - 48 8B F9              - mov rdi,rcx
victoria3.exe+11FD498 - 48 83 C1 08           - add rcx,08
victoria3.exe+11FD49C - E8 BFD1A4FF           - call victoria3.exe+C4A660
victoria3.exe+11FD4A1 - 4C 8B F0              - mov r14,rax
victoria3.exe+11FD4A4 - 4C 8B 00              - mov r8,[rax]
victoria3.exe+11FD4A7 - 48 8B C8              - mov rcx,rax
victoria3.exe+11FD4AA - 41 FF 50 08           - call qword ptr [r8+08]
victoria3.exe+11FD4AE - 84 C0                 - test al,al
victoria3.exe+11FD4B0 - 74 6C                 - je victoria3.exe+11FD51E
victoria3.exe+11FD4B2 - 83 7F 04 00           - cmp dword ptr [rdi+04],00
victoria3.exe+11FD4B6 - 7E 66                 - jle victoria3.exe+11FD51E
victoria3.exe+11FD4B8 - 48 8D 05 C7496F04     - lea rax,[victoria3.exe+58F1E86]
victoria3.exe+11FD4BF - 83 3D 7A20EE03 00     - cmp dword ptr [victoria3.exe+50DF540],00
victoria3.exe+11FD4C6 - 75 11                 - jne victoria3.exe+11FD4D9
victoria3.exe+11FD4C8 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+11FD4CD - 48 8D 0D FCE61D03     - lea rcx,[victoria3.exe+43DBBD0]
victoria3.exe+11FD4D4 - E8 E7528A02           - call victoria3.exe+3AA27C0
victoria3.exe+11FD4D9 - 48 8B 05 70B56B04     - mov rax,[victoria3.exe+58B8A50]
victoria3.exe+11FD4E0 - 48 8B 88 08060000     - mov rcx,[rax+00000608]
victoria3.exe+11FD4E7 - 44 0FB6 A1 48010000   - movzx r12d,byte ptr [rcx+00000148]
victoria3.exe+11FD4EF - 48 8B 8F F8000000     - mov rcx,[rdi+000000F8]
victoria3.exe+11FD4F6 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+11FD4F9 - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD4FB - 48 8D B7 B0000000     - lea rsi,[rdi+000000B0]
victoria3.exe+11FD502 - 84 C0                 - test al,al
victoria3.exe+11FD504 - 75 2E                 - jne victoria3.exe+11FD534
victoria3.exe+11FD506 - 48 8B 0E              - mov rcx,[rsi]
victoria3.exe+11FD509 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+11FD50C - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD50E - 84 C0                 - test al,al
victoria3.exe+11FD510 - 75 22                 - jne victoria3.exe+11FD534
victoria3.exe+11FD512 - 45 84 E4              - test r12b,r12b
victoria3.exe+11FD515 - 75 07                 - jne victoria3.exe+11FD51E
victoria3.exe+11FD517 - C7 47 04 00000000     - mov [rdi+04],00000000
victoria3.exe+11FD51E - 32 C0                 - xor al,al
victoria3.exe+11FD520 - 48 81 C4 E8020000     - add rsp,000002E8
victoria3.exe+11FD527 - 41 5F                 - pop r15
victoria3.exe+11FD529 - 41 5E                 - pop r14
victoria3.exe+11FD52B - 41 5D                 - pop r13
victoria3.exe+11FD52D - 41 5C                 - pop r12
victoria3.exe+11FD52F - 5F                    - pop rdi
victoria3.exe+11FD530 - 5E                    - pop rsi
victoria3.exe+11FD531 - 5D                    - pop rbp
victoria3.exe+11FD532 - 5B                    - pop rbx
victoria3.exe+11FD533 - C3                    - ret 
victoria3.exe+11FD534 - 4C 8B AC 24 60030000  - mov r13,[rsp+00000360]
victoria3.exe+11FD53C - 4C 89 6C 24 38        - mov [rsp+38],r13
victoria3.exe+11FD541 - 48 8B 84 24 58030000  - mov rax,[rsp+00000358]
victoria3.exe+11FD549 - 48 89 44 24 30        - mov [rsp+30],rax
victoria3.exe+11FD54E - 48 8B AC 24 50030000  - mov rbp,[rsp+00000350]
victoria3.exe+11FD556 - 48 89 6C 24 28        - mov [rsp+28],rbp
victoria3.exe+11FD55B - 48 8B 84 24 48030000  - mov rax,[rsp+00000348]
victoria3.exe+11FD563 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+11FD568 - 4C 8B CB              - mov r9,rbx
victoria3.exe+11FD56B - 4C 8B 84 24 38030000  - mov r8,[rsp+00000338]
victoria3.exe+11FD573 - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+11FD578 - 48 8B CF              - mov rcx,rdi
victoria3.exe+11FD57B - E8 F0FDFFFF           - call victoria3.exe+11FD370
victoria3.exe+11FD580 - 90                    - nop 
victoria3.exe+11FD581 - 48 8B 8F F8000000     - mov rcx,[rdi+000000F8]
victoria3.exe+11FD588 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+11FD58B - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD58D - 84 C0                 - test al,al
victoria3.exe+11FD58F - 74 11                 - je victoria3.exe+11FD5A2
victoria3.exe+11FD591 - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+11FD596 - 48 8D 8F F8000000     - lea rcx,[rdi+000000F8]
victoria3.exe+11FD59D - E8 FEE7FFFF           - call victoria3.exe+11FBDA0
victoria3.exe+11FD5A2 - 48 8B 0E              - mov rcx,[rsi]
victoria3.exe+11FD5A5 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+11FD5A8 - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD5AA - 84 C0                 - test al,al
victoria3.exe+11FD5AC - 74 0D                 - je victoria3.exe+11FD5BB
victoria3.exe+11FD5AE - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+11FD5B3 - 48 8B CE              - mov rcx,rsi
victoria3.exe+11FD5B6 - E8 E5E7FFFF           - call victoria3.exe+11FBDA0
victoria3.exe+11FD5BB - 41 8B 86 5C1D0000     - mov eax,[r14+00001D5C]
victoria3.exe+11FD5C2 - 89 84 24 30030000     - mov [rsp+00000330],eax
victoria3.exe+11FD5C9 - 41 8B 86 581D0000     - mov eax,[r14+00001D58]
victoria3.exe+11FD5D0 - 89 44 24 50           - mov [rsp+50],eax
victoria3.exe+11FD5D4 - 48 8B 8F F8000000     - mov rcx,[rdi+000000F8]
victoria3.exe+11FD5DB - 48 8B 01              - mov rax,[rcx]
victoria3.exe+11FD5DE - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD5E0 - BB 60000000           - mov ebx,00000060
victoria3.exe+11FD5E5 - 48 BA 66E6096A01000000 - mov rdx,000000016A09E666
victoria3.exe+11FD5EF - 41 B8 33F304B5        - mov r8d,B504F333
victoria3.exe+11FD5F5 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+11FD5FF - 84 C0                 - test al,al
victoria3.exe+11FD601 - 0F84 53020000         - je victoria3.exe+11FD85A
victoria3.exe+11FD607 - 48 8B 1D 1AD36804     - mov rbx,[victoria3.exe+588A928]
victoria3.exe+11FD60E - 83 3D 2B1FEE03 00     - cmp dword ptr [victoria3.exe+50DF540],00
victoria3.exe+11FD615 - 75 32                 - jne victoria3.exe+11FD649
victoria3.exe+11FD617 - 48 8D 05 68486F04     - lea rax,[victoria3.exe+58F1E86]
victoria3.exe+11FD61E - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+11FD623 - 48 8D 0D A6E51D03     - lea rcx,[victoria3.exe+43DBBD0]
victoria3.exe+11FD62A - E8 91518A02           - call victoria3.exe+3AA27C0
victoria3.exe+11FD62F - 48 BA 66E6096A01000000 - mov rdx,000000016A09E666
victoria3.exe+11FD639 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+11FD643 - 41 B8 33F304B5        - mov r8d,B504F333
victoria3.exe+11FD649 - 48 8B 05 00B46B04     - mov rax,[victoria3.exe+58B8A50]
victoria3.exe+11FD650 - 48 8B 88 08060000     - mov rcx,[rax+00000608]
victoria3.exe+11FD657 - 80 B9 48010000 00     - cmp byte ptr [rcx+00000148],00
victoria3.exe+11FD65E - 0F84 8A000000         - je victoria3.exe+11FD6EE
victoria3.exe+11FD664 - 4C 8B 0D 85D26804     - mov r9,[victoria3.exe+588A8F0]
victoria3.exe+11FD66B - 4A 8D 04 03           - lea rax,[rbx+r8]
victoria3.exe+11FD66F - 48 3B C2              - cmp rax,rdx
victoria3.exe+11FD672 - 77 26                 - ja victoria3.exe+11FD69A
victoria3.exe+11FD674 - 4B 8D 04 01           - lea rax,[r9+r8]
victoria3.exe+11FD678 - 48 3B C2              - cmp rax,rdx
victoria3.exe+11FD67B - 77 1D                 - ja victoria3.exe+11FD69A
victoria3.exe+11FD67D - 49 0FAF D9            - imul rbx,r9
victoria3.exe+11FD681 - 49 8B C2              - mov rax,r10
victoria3.exe+11FD684 - 48 F7 EB              - imul rbx
victoria3.exe+11FD687 - 48 8B DA              - mov rbx,rdx
victoria3.exe+11FD68A - 48 C1 FB 0E           - sar rbx,0E
victoria3.exe+11FD68E - 48 8B C3              - mov rax,rbx
victoria3.exe+11FD691 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD695 - 48 03 D8              - add rbx,rax
victoria3.exe+11FD698 - EB 54                 - jmp victoria3.exe+11FD6EE
victoria3.exe+11FD69A - 4D 8B C1              - mov r8,r9
victoria3.exe+11FD69D - 4C 3B CB              - cmp r9,rbx
victoria3.exe+11FD6A0 - 4C 0F4C C3            - cmovl r8,rbx
victoria3.exe+11FD6A4 - 4C 0F4F CB            - cmovg r9,rbx
victoria3.exe+11FD6A8 - 49 8B C2              - mov rax,r10
victoria3.exe+11FD6AB - 49 F7 E8              - imul r8
victoria3.exe+11FD6AE - 48 8B CA              - mov rcx,rdx
victoria3.exe+11FD6B1 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+11FD6B5 - 48 8B C1              - mov rax,rcx
victoria3.exe+11FD6B8 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD6BC - 48 03 C8              - add rcx,rax
victoria3.exe+11FD6BF - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+11FD6C6 - 4C 2B C0              - sub r8,rax
victoria3.exe+11FD6C9 - 4D 0FAF C1            - imul r8,r9
victoria3.exe+11FD6CD - 49 8B C2              - mov rax,r10
victoria3.exe+11FD6D0 - 49 F7 E8              - imul r8
victoria3.exe+11FD6D3 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FD6D7 - 48 8B DA              - mov rbx,rdx
victoria3.exe+11FD6DA - 48 C1 EB 3F           - shr rbx,3F
victoria3.exe+11FD6DE - 48 03 DA              - add rbx,rdx
victoria3.exe+11FD6E1 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+11FD6E5 - 48 03 D9              - add rbx,rcx
victoria3.exe+11FD6E8 - 41 B8 33F304B5        - mov r8d,B504F333
victoria3.exe+11FD6EE - 4C 8B 8F 18010000     - mov r9,[rdi+00000118]
victoria3.exe+11FD6F5 - 44 8B 9C 24 30030000  - mov r11d,[rsp+00000330]
victoria3.exe+11FD6FD - 44 3B 5C 24 50        - cmp r11d,[rsp+50]
victoria3.exe+11FD702 - 0F8C C0000000         - jl victoria3.exe+11FD7C8
victoria3.exe+11FD708 - 48 8B 87 F8000000     - mov rax,[rdi+000000F8]
victoria3.exe+11FD70F - 48 39 87 B0000000     - cmp [rdi+000000B0],rax
victoria3.exe+11FD716 - 0F84 AC000000         - je victoria3.exe+11FD7C8
victoria3.exe+11FD71C - 4C 8B 15 EDD16804     - mov r10,[victoria3.exe+588A910]
victoria3.exe+11FD723 - 4B 8D 04 01           - lea rax,[r9+r8]
victoria3.exe+11FD727 - 48 B9 66E6096A01000000 - mov rcx,000000016A09E666
victoria3.exe+11FD731 - 48 3B C1              - cmp rax,rcx
victoria3.exe+11FD734 - 77 2D                 - ja victoria3.exe+11FD763
victoria3.exe+11FD736 - 4B 8D 04 02           - lea rax,[r10+r8]
victoria3.exe+11FD73A - 48 3B C1              - cmp rax,rcx
victoria3.exe+11FD73D - 77 24                 - ja victoria3.exe+11FD763
victoria3.exe+11FD73F - 49 8B C9              - mov rcx,r9
victoria3.exe+11FD742 - 49 0FAF CA            - imul rcx,r10
victoria3.exe+11FD746 - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+11FD750 - 48 F7 E9              - imul rcx
victoria3.exe+11FD753 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FD757 - 48 8B C2              - mov rax,rdx
victoria3.exe+11FD75A - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD75E - 48 03 D0              - add rdx,rax
victoria3.exe+11FD761 - EB 5C                 - jmp victoria3.exe+11FD7BF
victoria3.exe+11FD763 - 4D 8B C2              - mov r8,r10
victoria3.exe+11FD766 - 4D 3B D1              - cmp r10,r9
victoria3.exe+11FD769 - 4D 0F4C C1            - cmovl r8,r9
victoria3.exe+11FD76D - 4D 0F4F D1            - cmovg r10,r9
victoria3.exe+11FD771 - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+11FD77B - 49 F7 E8              - imul r8
victoria3.exe+11FD77E - 48 8B CA              - mov rcx,rdx
victoria3.exe+11FD781 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+11FD785 - 48 8B C1              - mov rax,rcx
victoria3.exe+11FD788 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD78C - 48 03 C8              - add rcx,rax
victoria3.exe+11FD78F - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+11FD796 - 4C 2B C0              - sub r8,rax
victoria3.exe+11FD799 - 4D 0FAF C2            - imul r8,r10
victoria3.exe+11FD79D - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+11FD7A7 - 49 F7 E8              - imul r8
victoria3.exe+11FD7AA - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FD7AE - 48 8B C2              - mov rax,rdx
victoria3.exe+11FD7B1 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD7B5 - 48 03 D0              - add rdx,rax
victoria3.exe+11FD7B8 - 49 0FAF CA            - imul rcx,r10
victoria3.exe+11FD7BC - 48 03 D1              - add rdx,rcx
victoria3.exe+11FD7BF - 48 3B 97 D0000000     - cmp rdx,[rdi+000000D0]
victoria3.exe+11FD7C6 - 7C 09                 - jl victoria3.exe+11FD7D1
victoria3.exe+11FD7C8 - 4C 3B CB              - cmp r9,rbx
victoria3.exe+11FD7CB - 0F8D 82000000         - jnl victoria3.exe+11FD853
victoria3.exe+11FD7D1 - 0FB6 97 00010000      - movzx edx,byte ptr [rdi+00000100]
victoria3.exe+11FD7D8 - 4D 8B D5              - mov r10,r13
victoria3.exe+11FD7DB - 84 D2                 - test dl,dl
victoria3.exe+11FD7DD - 4C 0F44 94 24 58030000  - cmove r10,[rsp+00000358]
victoria3.exe+11FD7E6 - 4C 8B CD              - mov r9,rbp
victoria3.exe+11FD7E9 - 4C 0F44 8C 24 48030000  - cmove r9,[rsp+00000348]
victoria3.exe+11FD7F2 - 48 8B 8C 24 40030000  - mov rcx,[rsp+00000340]
victoria3.exe+11FD7FA - 48 0F44 8C 24 38030000  - cmove rcx,[rsp+00000338]
victoria3.exe+11FD803 - BB 60000000           - mov ebx,00000060
victoria3.exe+11FD808 - 8B C3                 - mov eax,ebx
victoria3.exe+11FD80A - 41 B8 10000000        - mov r8d,00000010
victoria3.exe+11FD810 - 41 0F45 C0            - cmovne eax,r8d
victoria3.exe+11FD814 - 48 03 C7              - add rax,rdi
victoria3.exe+11FD817 - 4C 89 54 24 40        - mov [rsp+40],r10
victoria3.exe+11FD81C - 4C 89 4C 24 38        - mov [rsp+38],r9
victoria3.exe+11FD821 - 48 89 4C 24 30        - mov [rsp+30],rcx
victoria3.exe+11FD826 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+11FD82B - 49 8D 86 881D0000     - lea rax,[r14+00001D88]
victoria3.exe+11FD832 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+11FD837 - 4C 8B 4E 40           - mov r9,[rsi+40]
victoria3.exe+11FD83B - 4C 8B 87 30010000     - mov r8,[rdi+00000130]
victoria3.exe+11FD842 - 48 8B 8F F8000000     - mov rcx,[rdi+000000F8]
victoria3.exe+11FD849 - E8 D2D6FFFF           - call victoria3.exe+11FAF20
victoria3.exe+11FD84E - 40 B5 01              - mov bpl,01
victoria3.exe+11FD851 - EB 27                 - jmp victoria3.exe+11FD87A
victoria3.exe+11FD853 - BB 60000000           - mov ebx,00000060
victoria3.exe+11FD858 - EB 08                 - jmp victoria3.exe+11FD862
victoria3.exe+11FD85A - 44 8B 9C 24 30030000  - mov r11d,[rsp+00000330]
victoria3.exe+11FD862 - 44 3B 5C 24 50        - cmp r11d,[rsp+50]
victoria3.exe+11FD867 - 7C 0E                 - jl victoria3.exe+11FD877
victoria3.exe+11FD869 - C7 47 04 00000000     - mov [rdi+04],00000000
victoria3.exe+11FD870 - 32 DB                 - xor bl,bl
victoria3.exe+11FD872 - E9 E7010000           - jmp victoria3.exe+11FDA5E
victoria3.exe+11FD877 - 40 32 ED              - xor bpl,bpl
victoria3.exe+11FD87A - 48 8B CE              - mov rcx,rsi
victoria3.exe+11FD87D - E8 FEE3FFFF           - call victoria3.exe+11FBC80
victoria3.exe+11FD882 - 84 C0                 - test al,al
victoria3.exe+11FD884 - 0F84 E6010000         - je victoria3.exe+11FDA70
victoria3.exe+11FD88A - 0FB6 AF B8000000      - movzx ebp,byte ptr [rdi+000000B8]
victoria3.exe+11FD891 - 40 84 ED              - test bpl,bpl
victoria3.exe+11FD894 - 4C 0F44 AC 24 58030000  - cmove r13,[rsp+00000358]
victoria3.exe+11FD89D - 48 8B 84 24 50030000  - mov rax,[rsp+00000350]
victoria3.exe+11FD8A5 - 48 0F44 84 24 48030000  - cmove rax,[rsp+00000348]
victoria3.exe+11FD8AE - 48 89 84 24 50030000  - mov [rsp+00000350],rax
victoria3.exe+11FD8B6 - 48 8B 84 24 40030000  - mov rax,[rsp+00000340]
victoria3.exe+11FD8BE - 48 0F44 84 24 38030000  - cmove rax,[rsp+00000338]
victoria3.exe+11FD8C7 - 48 89 84 24 40030000  - mov [rsp+00000340],rax
victoria3.exe+11FD8CF - B8 10000000           - mov eax,00000010
victoria3.exe+11FD8D4 - 48 0F45 D8            - cmovne rbx,rax
victoria3.exe+11FD8D8 - 48 03 DF              - add rbx,rdi
victoria3.exe+11FD8DB - 48 89 9C 24 30030000  - mov [rsp+00000330],rbx
victoria3.exe+11FD8E3 - 48 8B B7 F0000000     - mov rsi,[rdi+000000F0]
victoria3.exe+11FD8EA - 48 8B 9F E8000000     - mov rbx,[rdi+000000E8]
victoria3.exe+11FD8F1 - 4C 8B BF B0000000     - mov r15,[rdi+000000B0]
victoria3.exe+11FD8F8 - 49 8B 07              - mov rax,[r15]
victoria3.exe+11FD8FB - 49 8B CF              - mov rcx,r15
victoria3.exe+11FD8FE - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD900 - 84 C0                 - test al,al
victoria3.exe+11FD902 - 0F84 19010000         - je victoria3.exe+11FDA21
victoria3.exe+11FD908 - 41 0FB6 47 40         - movzx eax,byte ptr [r15+40]
victoria3.exe+11FD90D - A8 02                 - test al,02
victoria3.exe+11FD90F - 0F84 0C010000         - je victoria3.exe+11FDA21
victoria3.exe+11FD915 - A8 01                 - test al,01
victoria3.exe+11FD917 - 0F85 04010000         - jne victoria3.exe+11FDA21
victoria3.exe+11FD91D - B8 A0860100           - mov eax,000186A0
victoria3.exe+11FD922 - 49 C7 C0 6079FEFF     - mov r8,FFFFFFFFFFFE7960
victoria3.exe+11FD929 - 40 80 FD 01           - cmp bpl,01
victoria3.exe+11FD92D - 4C 0F44 C0            - cmove r8,rax
victoria3.exe+11FD931 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FD934 - 49 8D 8E 881D0000     - lea rcx,[r14+00001D88]
victoria3.exe+11FD93B - E8 30A0E2FF           - call victoria3.exe+1027970
victoria3.exe+11FD940 - 4C 8B C3              - mov r8,rbx
victoria3.exe+11FD943 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FD946 - 48 8B 8C 24 30030000  - mov rcx,[rsp+00000330]
victoria3.exe+11FD94E - E8 1DA0E2FF           - call victoria3.exe+1027970
victoria3.exe+11FD953 - 4C 8B C3              - mov r8,rbx
victoria3.exe+11FD956 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FD959 - 48 8B 8C 24 40030000  - mov rcx,[rsp+00000340]
victoria3.exe+11FD961 - E8 0AA0E2FF           - call victoria3.exe+1027970
victoria3.exe+11FD966 - 4C 8B C3              - mov r8,rbx
victoria3.exe+11FD969 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FD96C - 48 8B 8C 24 50030000  - mov rcx,[rsp+00000350]
victoria3.exe+11FD974 - E8 F79FE2FF           - call victoria3.exe+1027970
victoria3.exe+11FD979 - BA 33F304B5           - mov edx,B504F333
victoria3.exe+11FD97E - 48 8D 0C 13           - lea rcx,[rbx+rdx]
victoria3.exe+11FD982 - 48 B8 66E6096A01000000 - mov rax,000000016A09E666
victoria3.exe+11FD98C - 48 3B C8              - cmp rcx,rax
victoria3.exe+11FD98F - 77 2A                 - ja victoria3.exe+11FD9BB
victoria3.exe+11FD991 - 48 8D 0C 16           - lea rcx,[rsi+rdx]
victoria3.exe+11FD995 - 48 3B C8              - cmp rcx,rax
victoria3.exe+11FD998 - 77 21                 - ja victoria3.exe+11FD9BB
victoria3.exe+11FD99A - 48 0FAF F3            - imul rsi,rbx
victoria3.exe+11FD99E - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+11FD9A8 - 48 F7 EE              - imul rsi
victoria3.exe+11FD9AB - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FD9AF - 48 8B C2              - mov rax,rdx
victoria3.exe+11FD9B2 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD9B6 - 48 03 D0              - add rdx,rax
victoria3.exe+11FD9B9 - EB 58                 - jmp victoria3.exe+11FDA13
victoria3.exe+11FD9BB - 48 8B CE              - mov rcx,rsi
victoria3.exe+11FD9BE - 48 3B F3              - cmp rsi,rbx
victoria3.exe+11FD9C1 - 48 0F4C CB            - cmovl rcx,rbx
victoria3.exe+11FD9C5 - 48 0F4F F3            - cmovg rsi,rbx
victoria3.exe+11FD9C9 - 49 B9 09E1D1C6116BF129 - mov r9,29F16B11C6D1E109
victoria3.exe+11FD9D3 - 49 8B C1              - mov rax,r9
victoria3.exe+11FD9D6 - 48 F7 E9              - imul rcx
victoria3.exe+11FD9D9 - 4C 8B C2              - mov r8,rdx
victoria3.exe+11FD9DC - 49 C1 F8 0E           - sar r8,0E
victoria3.exe+11FD9E0 - 49 8B C0              - mov rax,r8
victoria3.exe+11FD9E3 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD9E7 - 4C 03 C0              - add r8,rax
victoria3.exe+11FD9EA - 49 69 C0 A0860100     - imul rax,r8,000186A0
victoria3.exe+11FD9F1 - 48 2B C8              - sub rcx,rax
victoria3.exe+11FD9F4 - 48 0FAF CE            - imul rcx,rsi
victoria3.exe+11FD9F8 - 49 8B C1              - mov rax,r9
victoria3.exe+11FD9FB - 48 F7 E9              - imul rcx
victoria3.exe+11FD9FE - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FDA02 - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDA05 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDA09 - 48 03 D0              - add rdx,rax
victoria3.exe+11FDA0C - 4C 0FAF C6            - imul r8,rsi
victoria3.exe+11FDA10 - 49 03 D0              - add rdx,r8
victoria3.exe+11FDA13 - 4C 8B C2              - mov r8,rdx
victoria3.exe+11FDA16 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FDA19 - 49 8B CD              - mov rcx,r13
victoria3.exe+11FDA1C - E8 4F9FE2FF           - call victoria3.exe+1027970
victoria3.exe+11FDA21 - 45 84 E4              - test r12b,r12b
victoria3.exe+11FDA24 - 75 0F                 - jne victoria3.exe+11FDA35
victoria3.exe+11FDA26 - 48 8B 97 B0000000     - mov rdx,[rdi+000000B0]
victoria3.exe+11FDA2D - 49 8B CE              - mov rcx,r14
victoria3.exe+11FDA30 - E8 9BE40200           - call victoria3.exe+122BED0
victoria3.exe+11FDA35 - FF 4F 04              - dec [rdi+04]
victoria3.exe+11FDA38 - 49 8B CE              - mov rcx,r14
victoria3.exe+11FDA3B - E8 10E50200           - call victoria3.exe+122BF50
victoria3.exe+11FDA40 - 48 C7 84 24 30030000 03000000 - mov qword ptr [rsp+00000330],00000003
victoria3.exe+11FDA4C - 49 8B D6              - mov rdx,r14
victoria3.exe+11FDA4F - 48 8D 8C 24 30030000  - lea rcx,[rsp+00000330]
victoria3.exe+11FDA57 - E8 B489A4FF           - call victoria3.exe+C46410
victoria3.exe+11FDA5C - B3 01                 - mov bl,01
victoria3.exe+11FDA5E - 48 8D 4C 24 60        - lea rcx,[rsp+60]
victoria3.exe+11FDA63 - E8 485DC3FF           - call victoria3.exe+E337B0
victoria3.exe+11FDA68 - 0FB6 C3               - movzx eax,bl
victoria3.exe+11FDA6B - E9 B0FAFFFF           - jmp victoria3.exe+11FD520
victoria3.exe+11FDA70 - 40 84 ED              - test bpl,bpl
victoria3.exe+11FDA73 - 75 C0                 - jne victoria3.exe+11FDA35
victoria3.exe+11FDA75 - 45 84 E4              - test r12b,r12b
victoria3.exe+11FDA78 - 74 07                 - je victoria3.exe+11FDA81
victoria3.exe+11FDA7A - FF 4F 04              - dec [rdi+04]
victoria3.exe+11FDA7D - 32 DB                 - xor bl,bl
victoria3.exe+11FDA7F - EB DD                 - jmp victoria3.exe+11FDA5E
victoria3.exe+11FDA81 - 48 63 07              - movsxd  rax,dword ptr [rdi]
victoria3.exe+11FDA84 - 48 69 C8 A0860100     - imul rcx,rax,000186A0
victoria3.exe+11FDA8B - 4C 8B 0D 46CE6804     - mov r9,[victoria3.exe+588A8D8]
victoria3.exe+11FDA92 - BA 33F304B5           - mov edx,B504F333
victoria3.exe+11FDA97 - 48 8D 04 11           - lea rax,[rcx+rdx]
victoria3.exe+11FDA9B - 49 B8 66E6096A01000000 - mov r8,000000016A09E666
victoria3.exe+11FDAA5 - 49 3B C0              - cmp rax,r8
victoria3.exe+11FDAA8 - 77 2D                 - ja victoria3.exe+11FDAD7
victoria3.exe+11FDAAA - 49 8D 04 11           - lea rax,[r9+rdx]
victoria3.exe+11FDAAE - 49 3B C0              - cmp rax,r8
victoria3.exe+11FDAB1 - 77 24                 - ja victoria3.exe+11FDAD7
victoria3.exe+11FDAB3 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+11FDAB7 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+11FDAC1 - 49 8B C2              - mov rax,r10
victoria3.exe+11FDAC4 - 48 F7 E9              - imul rcx
victoria3.exe+11FDAC7 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FDACB - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDACE - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDAD2 - 48 03 D0              - add rdx,rax
victoria3.exe+11FDAD5 - EB 58                 - jmp victoria3.exe+11FDB2F
victoria3.exe+11FDAD7 - 4D 8B C1              - mov r8,r9
victoria3.exe+11FDADA - 4C 3B C9              - cmp r9,rcx
victoria3.exe+11FDADD - 4C 0F4C C1            - cmovl r8,rcx
victoria3.exe+11FDAE1 - 4C 0F4F C9            - cmovg r9,rcx
victoria3.exe+11FDAE5 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+11FDAEF - 49 8B C2              - mov rax,r10
victoria3.exe+11FDAF2 - 49 F7 E8              - imul r8
victoria3.exe+11FDAF5 - 48 8B CA              - mov rcx,rdx
victoria3.exe+11FDAF8 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+11FDAFC - 48 8B C1              - mov rax,rcx
victoria3.exe+11FDAFF - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDB03 - 48 03 C8              - add rcx,rax
victoria3.exe+11FDB06 - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+11FDB0D - 4C 2B C0              - sub r8,rax
victoria3.exe+11FDB10 - 4D 0FAF C1            - imul r8,r9
victoria3.exe+11FDB14 - 49 8B C2              - mov rax,r10
victoria3.exe+11FDB17 - 49 F7 E8              - imul r8
victoria3.exe+11FDB1A - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FDB1E - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDB21 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDB25 - 48 03 D0              - add rdx,rax
victoria3.exe+11FDB28 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+11FDB2C - 48 03 D1              - add rdx,rcx
victoria3.exe+11FDB2F - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDB32 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDB36 - 84 C0                 - test al,al
victoria3.exe+11FDB38 - 49 8B C2              - mov rax,r10
victoria3.exe+11FDB3B - 48 8D 8A B03CFFFF     - lea rcx,[rdx-0000C350]
victoria3.exe+11FDB42 - 75 07                 - jne victoria3.exe+11FDB4B
victoria3.exe+11FDB44 - 48 8D 8A 50C30000     - lea rcx,[rdx+0000C350]
victoria3.exe+11FDB4B - 48 F7 E9              - imul rcx
victoria3.exe+11FDB4E - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FDB52 - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDB55 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDB59 - 48 03 D0              - add rdx,rax
victoria3.exe+11FDB5C - B9 01000000           - mov ecx,00000001
victoria3.exe+11FDB61 - 3B D1                 - cmp edx,ecx
victoria3.exe+11FDB63 - 0F4F CA               - cmovg ecx,edx
victoria3.exe+11FDB66 - 29 4F 04              - sub [rdi+04],ecx
victoria3.exe+11FDB69 - 32 DB                 - xor bl,bl
victoria3.exe+11FDB6B - E9 EEFEFFFF           - jmp victoria3.exe+11FDA5E




# 7FF7EACB7358

victoria3.exe+E37126 - CC                    - int 3 
victoria3.exe+E37127 - CC                    - int 3 
victoria3.exe+E37128 - CC                    - int 3 
victoria3.exe+E37129 - CC                    - int 3 
victoria3.exe+E3712A - CC                    - int 3 
victoria3.exe+E3712B - CC                    - int 3 
victoria3.exe+E3712C - CC                    - int 3 
victoria3.exe+E3712D - CC                    - int 3 
victoria3.exe+E3712E - CC                    - int 3 
victoria3.exe+E3712F - CC                    - int 3 
victoria3.exe+E37130 - 40 53                 - push rbx
victoria3.exe+E37132 - 55                    - push rbp
victoria3.exe+E37133 - 56                    - push rsi
victoria3.exe+E37134 - 57                    - push rdi
victoria3.exe+E37135 - 41 54                 - push r12
victoria3.exe+E37137 - 41 56                 - push r14
victoria3.exe+E37139 - 41 57                 - push r15
victoria3.exe+E3713B - 48 83 EC 50           - sub rsp,50
victoria3.exe+E3713F - 48 8B F1              - mov rsi,rcx
victoria3.exe+E37142 - 48 8B 89 F0000000     - mov rcx,[rcx+000000F0]
victoria3.exe+E37149 - 0FB6 41 40            - movzx eax,byte ptr [rcx+40]
victoria3.exe+E3714D - C0 E8 02              - shr al,02
victoria3.exe+E37150 - A8 01                 - test al,01
victoria3.exe+E37152 - 0F84 66040000         - je victoria3.exe+E375BE
victoria3.exe+E37158 - 48 8B 81 08010000     - mov rax,[rcx+00000108]
victoria3.exe+E3715F - 0FB6 50 40            - movzx edx,byte ptr [rax+40]
victoria3.exe+E37163 - C0 EA 04              - shr dl,04
victoria3.exe+E37166 - F6 C2 01              - test dl,01
victoria3.exe+E37169 - 0F85 4F040000         - jne victoria3.exe+E375BE
victoria3.exe+E3716F - 48 8B CE              - mov rcx,rsi
victoria3.exe+E37172 - E8 D9DBFFFF           - call victoria3.exe+E34D50
victoria3.exe+E37177 - 84 C0                 - test al,al
victoria3.exe+E37179 - 0F85 3F040000         - jne victoria3.exe+E375BE
victoria3.exe+E3717F - 48 8B 86 28010000     - mov rax,[rsi+00000128]
victoria3.exe+E37186 - 48 39 86 20010000     - cmp [rsi+00000120],rax
victoria3.exe+E3718D - 0F8F 2B040000         - jg victoria3.exe+E375BE
victoria3.exe+E37193 - 48 8B CE              - mov rcx,rsi
victoria3.exe+E37196 - E8 6552FFFF           - call victoria3.exe+E2C400
victoria3.exe+E3719B - 83 F8 01              - cmp eax,01
victoria3.exe+E3719E - 0F8C 1A040000         - jl victoria3.exe+E375BE
victoria3.exe+E371A4 - 48 8B CE              - mov rcx,rsi
victoria3.exe+E371A7 - E8 24040000           - call victoria3.exe+E375D0
victoria3.exe+E371AC - 84 C0                 - test al,al
victoria3.exe+E371AE - 0F84 0A040000         - je victoria3.exe+E375BE
victoria3.exe+E371B4 - 48 8B 9E 30020000     - mov rbx,[rsi+00000230]
victoria3.exe+E371BB - 48 63 86 3C020000     - movsxd  rax,dword ptr [rsi+0000023C]
victoria3.exe+E371C2 - 4C 8D 34 83           - lea r14,[rbx+rax*4]
victoria3.exe+E371C6 - 49 3B DE              - cmp rbx,r14
victoria3.exe+E371C9 - 0F84 EF030000         - je victoria3.exe+E375BE
victoria3.exe+E371CF - 4C 8D 3D F2AA5903     - lea r15,[victoria3.exe+43D1CC8]
victoria3.exe+E371D6 - 4C 8D 25 6F0EA504     - lea r12,[victoria3.exe+588804C]
victoria3.exe+E371DD - 0F1F 00               - nop dword ptr [rax]
victoria3.exe+E371E0 - 8B 03                 - mov eax,[rbx]
victoria3.exe+E371E2 - 48 8D 8C 24 90000000  - lea rcx,[rsp+00000090]
victoria3.exe+E371EA - 89 84 24 90000000     - mov [rsp+00000090],eax
victoria3.exe+E371F1 - E8 AA31E1FF           - call victoria3.exe+C4A3A0
victoria3.exe+E371F6 - 48 8B F8              - mov rdi,rax
victoria3.exe+E371F9 - 0FB6 40 30            - movzx eax,byte ptr [rax+30]
victoria3.exe+E371FD - 3C 03                 - cmp al,03
victoria3.exe+E371FF - 74 08                 - je victoria3.exe+E37209
victoria3.exe+E37201 - 3C 02                 - cmp al,02
victoria3.exe+E37203 - 0F84 E2000000         - je victoria3.exe+E372EB
victoria3.exe+E37209 - 48 8D 94 24 98000000  - lea rdx,[rsp+00000098]
victoria3.exe+E37211 - 48 8D 4F 20           - lea rcx,[rdi+20]
victoria3.exe+E37215 - E8 46470100           - call victoria3.exe+E4B960
victoria3.exe+E3721A - 48 8B C8              - mov rcx,rax
victoria3.exe+E3721D - E8 8E33E1FF           - call victoria3.exe+C4A5B0
victoria3.exe+E37222 - 83 78 18 FF           - cmp dword ptr [rax+18],-01
victoria3.exe+E37226 - 0F84 D1000000         - je victoria3.exe+E372FD
victoria3.exe+E3722C - 80 7F 30 02           - cmp byte ptr [rdi+30],02
victoria3.exe+E37230 - 75 07                 - jne victoria3.exe+E37239
victoria3.exe+E37232 - BA FFFFFFFF           - mov edx,FFFFFFFF
victoria3.exe+E37237 - EB 1C                 - jmp victoria3.exe+E37255
victoria3.exe+E37239 - 48 8D 94 24 A0000000  - lea rdx,[rsp+000000A0]
victoria3.exe+E37241 - 48 8D 4F 20           - lea rcx,[rdi+20]
victoria3.exe+E37245 - E8 16470100           - call victoria3.exe+E4B960
victoria3.exe+E3724A - 48 8B C8              - mov rcx,rax
victoria3.exe+E3724D - E8 5E33E1FF           - call victoria3.exe+C4A5B0
victoria3.exe+E37252 - 8B 50 18              - mov edx,[rax+18]
victoria3.exe+E37255 - 4C 8B 05 ECA9AB04     - mov r8,[victoria3.exe+58F1C48]
victoria3.exe+E3725C - 4D 85 C0              - test r8,r8
victoria3.exe+E3725F - 75 51                 - jne victoria3.exe+E372B2
victoria3.exe+E37261 - 83 FA FF              - cmp edx,-01
victoria3.exe+E37264 - 74 71                 - je victoria3.exe+E372D7
victoria3.exe+E37266 - 48 8D 15 D3D3A404     - lea rdx,[victoria3.exe+5884640]
victoria3.exe+E3726D - 48 8D 0D 2C8E4F04     - lea rcx,[victoria3.exe+53300A0]
victoria3.exe+E37274 - E8 37FF2F03           - call victoria3.exe+41371B0
victoria3.exe+E37279 - 48 89 84 24 90000000  - mov [rsp+00000090],rax
victoria3.exe+E37281 - 48 8D 84 24 90000000  - lea rax,[rsp+00000090]
victoria3.exe+E37289 - 48 89 44 24 30        - mov [rsp+30],rax
victoria3.exe+E3728E - 48 8D 44 24 40        - lea rax,[rsp+40]
victoria3.exe+E37293 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+E37298 - 4C 89 64 24 20        - mov [rsp+20],r12
victoria3.exe+E3729D - 4C 89 7C 24 40        - mov [rsp+40],r15
victoria3.exe+E372A2 - 48 C7 44 24 48 2F000000 - mov qword ptr [rsp+48],0000002F
victoria3.exe+E372AB - E8 B09897FF           - call victoria3.exe+7B0B60
victoria3.exe+E372B0 - EB 25                 - jmp victoria3.exe+E372D7
victoria3.exe+E372B2 - 8B C2                 - mov eax,edx
victoria3.exe+E372B4 - 25 FFFFFF00           - and eax,00FFFFFF
victoria3.exe+E372B9 - 41 3B 40 2C           - cmp eax,[r8+2C]
victoria3.exe+E372BD - 73 18                 - jae victoria3.exe+E372D7
victoria3.exe+E372BF - 8B C8                 - mov ecx,eax
victoria3.exe+E372C1 - 49 8B 40 20           - mov rax,[r8+20]
victoria3.exe+E372C5 - 48 03 C9              - add rcx,rcx
victoria3.exe+E372C8 - 48 8B 4C C8 08        - mov rcx,[rax+rcx*8+08]
victoria3.exe+E372CD - 48 85 C9              - test rcx,rcx
victoria3.exe+E372D0 - 74 05                 - je victoria3.exe+E372D7
victoria3.exe+E372D2 - 39 51 08              - cmp [rcx+08],edx
victoria3.exe+E372D5 - 74 07                 - je victoria3.exe+E372DE
victoria3.exe+E372D7 - 48 8B 0D DA8DAB04     - mov rcx,[victoria3.exe+58F00B8]
victoria3.exe+E372DE - E8 1DA2F1FF           - call victoria3.exe+D51500
victoria3.exe+E372E3 - 3B 05 EB24A504        - cmp eax,[victoria3.exe+58897D4]
victoria3.exe+E372E9 - 7F 12                 - jg victoria3.exe+E372FD
victoria3.exe+E372EB - 48 83 C3 04           - add rbx,04
victoria3.exe+E372EF - 49 3B DE              - cmp rbx,r14
victoria3.exe+E372F2 - 0F85 E8FEFFFF         - jne victoria3.exe+E371E0
victoria3.exe+E372F8 - E9 C1020000           - jmp victoria3.exe+E375BE
victoria3.exe+E372FD - 48 8B 86 F0000000     - mov rax,[rsi+000000F0]
victoria3.exe+E37304 - 48 8B 88 08010000     - mov rcx,[rax+00000108]
victoria3.exe+E3730B - 8B 41 40              - mov eax,[rcx+40]
victoria3.exe+E3730E - 48 C1 E8 14           - shr rax,14
victoria3.exe+E37312 - A8 01                 - test al,01
victoria3.exe+E37314 - 0F84 37010000         - je victoria3.exe+E37451
victoria3.exe+E3731A - 8B 86 E4000000        - mov eax,[rsi+000000E4]
victoria3.exe+E37320 - 48 8D 8C 24 90000000  - lea rcx,[rsp+00000090]
victoria3.exe+E37328 - 89 84 24 90000000     - mov [rsp+00000090],eax
victoria3.exe+E3732F - E8 6C2399FF           - call victoria3.exe+7C96A0
victoria3.exe+E37334 - 48 63 90 581D0000     - movsxd  rdx,dword ptr [rax+00001D58]
victoria3.exe+E3733B - 4C 69 DA A0860100     - imul r11,rdx,000186A0
victoria3.exe+E37342 - 4D 85 DB              - test r11,r11
victoria3.exe+E37345 - 7F 11                 - jg victoria3.exe+E37358
victoria3.exe+E37347 - B0 01                 - mov al,01
victoria3.exe+E37349 - 48 83 C4 50           - add rsp,50
victoria3.exe+E3734D - 41 5F                 - pop r15
victoria3.exe+E3734F - 41 5E                 - pop r14
victoria3.exe+E37351 - 41 5C                 - pop r12
victoria3.exe+E37353 - 5F                    - pop rdi
victoria3.exe+E37354 - 5E                    - pop rsi
victoria3.exe+E37355 - 5D                    - pop rbp
victoria3.exe+E37356 - 5B                    - pop rbx
victoria3.exe+E37357 - C3                    - ret 
victoria3.exe+E37358 - 2B 90 5C1D0000        - sub edx,[rax+00001D5C]
victoria3.exe+E3735E - 48 63 C2              - movsxd  rax,edx
victoria3.exe+E37361 - 48 69 D8 A0860100     - imul rbx,rax,000186A0
victoria3.exe+E37368 - 48 3B 1D E92AA504     - cmp rbx,[victoria3.exe+5889E58]
victoria3.exe+E3736F - 0F8C 49020000         - jl victoria3.exe+E375BE
victoria3.exe+E37375 - 48 B8 A38D23D6E2530000 - mov rax,000053E2D6238DA3
victoria3.exe+E3737F - 48 B9 461B47ACC5A70000 - mov rcx,0000A7C5AC471B46
victoria3.exe+E37389 - 48 03 C3              - add rax,rbx
victoria3.exe+E3738C - 48 3B C1              - cmp rax,rcx
victoria3.exe+E3738F - 77 18                 - ja victoria3.exe+E373A9
victoria3.exe+E37391 - 48 69 C3 A0860100     - imul rax,rbx,000186A0
victoria3.exe+E37398 - 48 99                 - cqo 
victoria3.exe+E3739A - 49 F7 FB              - idiv r11
victoria3.exe+E3739D - 48 3B 05 AC2AA504     - cmp rax,[victoria3.exe+5889E50]
victoria3.exe+E373A4 - E9 0F020000           - jmp victoria3.exe+E375B8
victoria3.exe+E373A9 - 48 B8 00E40B5402000000 - mov rax,00000002540BE400
victoria3.exe+E373B3 - 49 8B CB              - mov rcx,r11
victoria3.exe+E373B6 - 48 F7 D9              - neg rcx
victoria3.exe+E373B9 - 49 0F48 CB            - cmovs rcx,r11
victoria3.exe+E373BD - 48 3B C8              - cmp rcx,rax
victoria3.exe+E373C0 - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+E373CA - 7C 28                 - jl victoria3.exe+E373F4
victoria3.exe+E373CC - 49 F7 EB              - imul r11
victoria3.exe+E373CF - 48 8B C3              - mov rax,rbx
victoria3.exe+E373D2 - 4C 8B C2              - mov r8,rdx
victoria3.exe+E373D5 - 48 99                 - cqo 
victoria3.exe+E373D7 - 49 C1 F8 0E           - sar r8,0E
victoria3.exe+E373DB - 49 8B C8              - mov rcx,r8
victoria3.exe+E373DE - 48 C1 E9 3F           - shr rcx,3F
victoria3.exe+E373E2 - 4C 03 C1              - add r8,rcx
victoria3.exe+E373E5 - 49 F7 F8              - idiv r8
victoria3.exe+E373E8 - 48 3B 05 612AA504     - cmp rax,[victoria3.exe+5889E50]
victoria3.exe+E373EF - E9 C4010000           - jmp victoria3.exe+E375B8
victoria3.exe+E373F4 - 48 F7 EB              - imul rbx
victoria3.exe+E373F7 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+E373FB - 48 8B C2              - mov rax,rdx
victoria3.exe+E373FE - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+E37402 - 48 03 D0              - add rdx,rax
victoria3.exe+E37405 - 48 69 CA A0860100     - imul rcx,rdx,000186A0
victoria3.exe+E3740C - 48 8B C1              - mov rax,rcx
victoria3.exe+E3740F - 48 2B D9              - sub rbx,rcx
victoria3.exe+E37412 - 48 99                 - cqo 
victoria3.exe+E37414 - 49 F7 FB              - idiv r11
victoria3.exe+E37417 - 4C 8B D0              - mov r10,rax
victoria3.exe+E3741A - 4C 8B CA              - mov r9,rdx
victoria3.exe+E3741D - 48 69 C3 A0860100     - imul rax,rbx,000186A0
victoria3.exe+E37424 - 49 69 CA A0860100     - imul rcx,r10,000186A0
victoria3.exe+E3742B - 48 99                 - cqo 
victoria3.exe+E3742D - 49 F7 FB              - idiv r11
victoria3.exe+E37430 - 4C 8B C0              - mov r8,rax
victoria3.exe+E37433 - 49 69 C1 A0860100     - imul rax,r9,000186A0
victoria3.exe+E3743A - 48 99                 - cqo 
victoria3.exe+E3743C - 49 F7 FB              - idiv r11
victoria3.exe+E3743F - 49 03 C0              - add rax,r8
victoria3.exe+E37442 - 48 03 C1              - add rax,rcx
victoria3.exe+E37445 - 48 3B 05 042AA504     - cmp rax,[victoria3.exe+5889E50]
victoria3.exe+E3744C - E9 67010000           - jmp victoria3.exe+E375B8
victoria3.exe+E37451 - 48 8D 94 24 90000000  - lea rdx,[rsp+00000090]
victoria3.exe+E37459 - 48 8B CE              - mov rcx,rsi
victoria3.exe+E3745C - E8 0F9FFFFF           - call victoria3.exe+E31370
victoria3.exe+E37461 - BF A0860100           - mov edi,000186A0
victoria3.exe+E37466 - 8B DF                 - mov ebx,edi
victoria3.exe+E37468 - 48 2B 18              - sub rbx,[rax]
victoria3.exe+E3746B - 48 3B 1D 262AA504     - cmp rbx,[victoria3.exe+5889E98]
victoria3.exe+E37472 - 0F8C 46010000         - jl victoria3.exe+E375BE
victoria3.exe+E37478 - 48 8D 94 24 90000000  - lea rdx,[rsp+00000090]
victoria3.exe+E37480 - 48 8B CE              - mov rcx,rsi
victoria3.exe+E37483 - E8 084EFFFF           - call victoria3.exe+E2C290
victoria3.exe+E37488 - 48 63 8E E8000000     - movsxd  rcx,dword ptr [rsi+000000E8]
victoria3.exe+E3748F - 41 BA 33F304B5        - mov r10d,B504F333
victoria3.exe+E37495 - 48 69 D1 A0860100     - imul rdx,rcx,000186A0
victoria3.exe+E3749C - 48 2B 38              - sub rdi,[rax]
victoria3.exe+E3749F - 49 BB 66E6096A01000000 - mov r11,000000016A09E666
victoria3.exe+E374A9 - 4A 8D 04 12           - lea rax,[rdx+r10]
victoria3.exe+E374AD - 49 3B C3              - cmp rax,r11
victoria3.exe+E374B0 - 77 2D                 - ja victoria3.exe+E374DF
victoria3.exe+E374B2 - 4A 8D 04 17           - lea rax,[rdi+r10]
victoria3.exe+E374B6 - 49 3B C3              - cmp rax,r11
victoria3.exe+E374B9 - 77 24                 - ja victoria3.exe+E374DF
victoria3.exe+E374BB - 48 0FAF D7            - imul rdx,rdi
victoria3.exe+E374BF - 49 B9 09E1D1C6116BF129 - mov r9,29F16B11C6D1E109
victoria3.exe+E374C9 - 49 8B C1              - mov rax,r9
victoria3.exe+E374CC - 48 F7 EA              - imul rdx
victoria3.exe+E374CF - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+E374D3 - 48 8B C2              - mov rax,rdx
victoria3.exe+E374D6 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+E374DA - 48 03 D0              - add rdx,rax
victoria3.exe+E374DD - EB 58                 - jmp victoria3.exe+E37537
victoria3.exe+E374DF - 48 3B FA              - cmp rdi,rdx
victoria3.exe+E374E2 - 4C 8B C7              - mov r8,rdi
victoria3.exe+E374E5 - 49 B9 09E1D1C6116BF129 - mov r9,29F16B11C6D1E109
victoria3.exe+E374EF - 4C 0F4C C2            - cmovl r8,rdx
victoria3.exe+E374F3 - 48 0F4F FA            - cmovg rdi,rdx
victoria3.exe+E374F7 - 49 8B C1              - mov rax,r9
victoria3.exe+E374FA - 49 F7 E8              - imul r8
victoria3.exe+E374FD - 48 8B CA              - mov rcx,rdx
victoria3.exe+E37500 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+E37504 - 48 8B C1              - mov rax,rcx
victoria3.exe+E37507 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+E3750B - 48 03 C8              - add rcx,rax
victoria3.exe+E3750E - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+E37515 - 48 0FAF CF            - imul rcx,rdi
victoria3.exe+E37519 - 4C 2B C0              - sub r8,rax
victoria3.exe+E3751C - 49 8B C1              - mov rax,r9
victoria3.exe+E3751F - 4C 0FAF C7            - imul r8,rdi
victoria3.exe+E37523 - 49 F7 E8              - imul r8
victoria3.exe+E37526 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+E3752A - 48 8B C2              - mov rax,rdx
victoria3.exe+E3752D - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+E37531 - 48 03 D0              - add rdx,rax
victoria3.exe+E37534 - 48 03 D1              - add rdx,rcx
victoria3.exe+E37537 - 4A 8D 04 12           - lea rax,[rdx+r10]
victoria3.exe+E3753B - 49 3B C3              - cmp rax,r11
victoria3.exe+E3753E - 77 23                 - ja victoria3.exe+E37563
victoria3.exe+E37540 - 4A 8D 04 13           - lea rax,[rbx+r10]
victoria3.exe+E37544 - 49 3B C3              - cmp rax,r11
victoria3.exe+E37547 - 77 1A                 - ja victoria3.exe+E37563
victoria3.exe+E37549 - 48 0FAF D3            - imul rdx,rbx
victoria3.exe+E3754D - 49 8B C1              - mov rax,r9
victoria3.exe+E37550 - 48 F7 EA              - imul rdx
victoria3.exe+E37553 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+E37557 - 48 8B C2              - mov rax,rdx
victoria3.exe+E3755A - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+E3755E - 48 03 D0              - add rdx,rax
victoria3.exe+E37561 - EB 4E                 - jmp victoria3.exe+E375B1
victoria3.exe+E37563 - 48 3B DA              - cmp rbx,rdx
victoria3.exe+E37566 - 4C 8B C3              - mov r8,rbx
victoria3.exe+E37569 - 49 8B C1              - mov rax,r9
victoria3.exe+E3756C - 4C 0F4C C2            - cmovl r8,rdx
victoria3.exe+E37570 - 48 0F4F DA            - cmovg rbx,rdx
victoria3.exe+E37574 - 49 F7 E8              - imul r8
victoria3.exe+E37577 - 48 8B CA              - mov rcx,rdx
victoria3.exe+E3757A - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+E3757E - 48 8B C1              - mov rax,rcx
victoria3.exe+E37581 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+E37585 - 48 03 C8              - add rcx,rax
victoria3.exe+E37588 - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+E3758F - 48 0FAF CB            - imul rcx,rbx
victoria3.exe+E37593 - 4C 2B C0              - sub r8,rax
victoria3.exe+E37596 - 49 8B C1              - mov rax,r9
victoria3.exe+E37599 - 4C 0FAF C3            - imul r8,rbx
victoria3.exe+E3759D - 49 F7 E8              - imul r8
victoria3.exe+E375A0 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+E375A4 - 48 8B C2              - mov rax,rdx
victoria3.exe+E375A7 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+E375AB - 48 03 D0              - add rdx,rax
victoria3.exe+E375AE - 48 03 D1              - add rdx,rcx
victoria3.exe+E375B1 - 48 3B 15 E828A504     - cmp rdx,[victoria3.exe+5889EA0]
victoria3.exe+E375B8 - 0F8D 89FDFFFF         - jnl victoria3.exe+E37347
victoria3.exe+E375BE - 32 C0                 - xor al,al
victoria3.exe+E375C0 - 48 83 C4 50           - add rsp,50
victoria3.exe+E375C4 - 41 5F                 - pop r15
victoria3.exe+E375C6 - 41 5E                 - pop r14
victoria3.exe+E375C8 - 41 5C                 - pop r12
victoria3.exe+E375CA - 5F                    - pop rdi
victoria3.exe+E375CB - 5E                    - pop rsi
victoria3.exe+E375CC - 5D                    - pop rbp
victoria3.exe+E375CD - 5B                    - pop rbx
victoria3.exe+E375CE - C3                    - ret 



# 7FF7EB0AB9C7

victoria3.exe+122B9A0 - 48 89 5C 24 20        - mov [rsp+20],rbx
victoria3.exe+122B9A5 - 89 54 24 10           - mov [rsp+10],edx
victoria3.exe+122B9A9 - 55                    - push rbp
victoria3.exe+122B9AA - 56                    - push rsi
victoria3.exe+122B9AB - 57                    - push rdi
victoria3.exe+122B9AC - 41 54                 - push r12
victoria3.exe+122B9AE - 41 55                 - push r13
victoria3.exe+122B9B0 - 41 56                 - push r14
victoria3.exe+122B9B2 - 41 57                 - push r15
victoria3.exe+122B9B4 - 48 81 EC B0020000     - sub rsp,000002B0
victoria3.exe+122B9BB - 8B DA                 - mov ebx,edx
victoria3.exe+122B9BD - 48 8B F1              - mov rsi,rcx
victoria3.exe+122B9C0 - 33 D2                 - xor edx,edx
victoria3.exe+122B9C2 - E8 89E2FFFF           - call victoria3.exe+1229C50
victoria3.exe+122B9C7 - 89 86 581D0000        - mov [rsi+00001D58],eax
victoria3.exe+122B9CD - 33 D2                 - xor edx,edx
victoria3.exe+122B9CF - 48 8B CE              - mov rcx,rsi
victoria3.exe+122B9D2 - E8 99EAFFFF           - call victoria3.exe+122A470
victoria3.exe+122B9D7 - 44 8B F8              - mov r15d,eax
victoria3.exe+122B9DA - 89 86 5C1D0000        - mov [rsi+00001D5C],eax
victoria3.exe+122B9E0 - 85 C0                 - test eax,eax
victoria3.exe+122B9E2 - 0F8E 38030000         - jng victoria3.exe+122BD20
victoria3.exe+122B9E8 - 80 BE B8110000 00     - cmp byte ptr [rsi+000011B8],00
victoria3.exe+122B9EF - 74 24                 - je victoria3.exe+122BA15
victoria3.exe+122B9F1 - 8B 86 480B0000        - mov eax,[rsi+00000B48]
victoria3.exe+122B9F7 - 83 F8 FF              - cmp eax,-01
victoria3.exe+122B9FA - 74 19                 - je victoria3.exe+122BA15
victoria3.exe+122B9FC - 89 84 24 F0020000     - mov [rsp+000002F0],eax
victoria3.exe+122BA03 - 48 8D 8C 24 F0020000  - lea rcx,[rsp+000002F0]
victoria3.exe+122BA0B - E8 A07959FF           - call victoria3.exe+7C33B0
victoria3.exe+122BA10 - 8B 48 10              - mov ecx,[rax+10]
victoria3.exe+122BA13 - EB 20                 - jmp victoria3.exe+122BA35
victoria3.exe+122BA15 - 8B 86 480E0000        - mov eax,[rsi+00000E48]
victoria3.exe+122BA1B - 89 84 24 F0020000     - mov [rsp+000002F0],eax
victoria3.exe+122BA22 - 48 8D 8C 24 F0020000  - lea rcx,[rsp+000002F0]
victoria3.exe+122BA2A - E8 815058FF           - call victoria3.exe+7B0AB0
victoria3.exe+122BA2F - 8B 88 D4090000        - mov ecx,[rax+000009D4]
victoria3.exe+122BA35 - 89 8C 24 F0020000     - mov [rsp+000002F0],ecx
victoria3.exe+122BA3C - 48 8D 8C 24 F0020000  - lea rcx,[rsp+000002F0]
victoria3.exe+122BA44 - E8 374959FF           - call victoria3.exe+7C0380
victoria3.exe+122BA49 - 48 8D 88 48080000     - lea rcx,[rax+00000848]
victoria3.exe+122BA50 - E8 5B5058FF           - call victoria3.exe+7B0AB0
victoria3.exe+122BA55 - 48 8B E8              - mov rbp,rax
victoria3.exe+122BA58 - 83 3D E13AEB03 00     - cmp dword ptr [victoria3.exe+50DF540],00
victoria3.exe+122BA5F - 75 18                 - jne victoria3.exe+122BA79
victoria3.exe+122BA61 - 48 8D 05 1E646C04     - lea rax,[victoria3.exe+58F1E86]
victoria3.exe+122BA68 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122BA6D - 48 8D 0D 5C011B03     - lea rcx,[victoria3.exe+43DBBD0]
victoria3.exe+122BA74 - E8 476D8702           - call victoria3.exe+3AA27C0
victoria3.exe+122BA79 - 48 8B 0D D0CF6804     - mov rcx,[victoria3.exe+58B8A50]
victoria3.exe+122BA80 - 48 8B 91 08060000     - mov rdx,[rcx+00000608]
victoria3.exe+122BA87 - 4C 8B AA 20010000     - mov r13,[rdx+00000120]
victoria3.exe+122BA8E - 44 2B BE 581D0000     - sub r15d,[rsi+00001D58]
victoria3.exe+122BA95 - 45 32 E4              - xor r12b,r12b
victoria3.exe+122BA98 - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+122BA9D - E8 1E77C0FF           - call victoria3.exe+E331C0
victoria3.exe+122BAA2 - 90                    - nop 
victoria3.exe+122BAA3 - 4C 8B B6 D81D0000     - mov r14,[rsi+00001DD8]
victoria3.exe+122BAAA - 48 63 86 E41D0000     - movsxd  rax,dword ptr [rsi+00001DE4]
victoria3.exe+122BAB1 - 49 8D 04 C6           - lea rax,[r14+rax*8]
victoria3.exe+122BAB5 - 48 89 84 24 F0020000  - mov [rsp+000002F0],rax
victoria3.exe+122BABD - 4C 3B F0              - cmp r14,rax
victoria3.exe+122BAC0 - 0F84 F2010000         - je victoria3.exe+122BCB8
victoria3.exe+122BAC6 - 66 66 0F1F 84 00 00000000  - nop word ptr [rax+rax+00000000]
victoria3.exe+122BAD0 - 49 8B 3E              - mov rdi,[r14]
victoria3.exe+122BAD3 - 80 BE B8110000 00     - cmp byte ptr [rsi+000011B8],00
victoria3.exe+122BADA - 75 33                 - jne victoria3.exe+122BB0F
victoria3.exe+122BADC - 33 D2                 - xor edx,edx
victoria3.exe+122BADE - 33 C9                 - xor ecx,ecx
victoria3.exe+122BAE0 - 48 63 85 14240000     - movsxd  rax,dword ptr [rbp+00002414]
victoria3.exe+122BAE7 - 85 C0                 - test eax,eax
victoria3.exe+122BAE9 - 7E 24                 - jle victoria3.exe+122BB0F
victoria3.exe+122BAEB - 4C 8B C0              - mov r8,rax
victoria3.exe+122BAEE - 48 8B 85 08240000     - mov rax,[rbp+00002408]
victoria3.exe+122BAF5 - 48 39 38              - cmp [rax],rdi
victoria3.exe+122BAF8 - 74 10                 - je victoria3.exe+122BB0A
victoria3.exe+122BAFA - FF C2                 - inc edx
victoria3.exe+122BAFC - 48 FF C1              - inc rcx
victoria3.exe+122BAFF - 48 83 C0 08           - add rax,08
victoria3.exe+122BB03 - 49 3B C8              - cmp rcx,r8
victoria3.exe+122BB06 - 7C ED                 - jl victoria3.exe+122BAF5
victoria3.exe+122BB08 - EB 05                 - jmp victoria3.exe+122BB0F
victoria3.exe+122BB0A - 83 FA FF              - cmp edx,-01
victoria3.exe+122BB0D - 75 60                 - jne victoria3.exe+122BB6F
victoria3.exe+122BB0F - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BB12 - 48 8B CD              - mov rcx,rbp
victoria3.exe+122BB15 - E8 668FA0FF           - call victoria3.exe+C34A80
victoria3.exe+122BB1A - 34 01                 - xor al,01
victoria3.exe+122BB1C - 75 51                 - jne victoria3.exe+122BB6F
victoria3.exe+122BB1E - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BB21 - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BB24 - E8 A7EFFFFF           - call victoria3.exe+122AAD0
victoria3.exe+122BB29 - 84 C0                 - test al,al
victoria3.exe+122BB2B - 0F85 6E010000         - jne victoria3.exe+122BC9F
victoria3.exe+122BB31 - 48 63 5F 10           - movsxd  rbx,dword ptr [rdi+10]
victoria3.exe+122BB35 - 8B CB                 - mov ecx,ebx
victoria3.exe+122BB37 - E8 F4AADFFF           - call victoria3.exe+1026630
victoria3.exe+122BB3C - 84 C0                 - test al,al
victoria3.exe+122BB3E - 74 2F                 - je victoria3.exe+122BB6F
victoria3.exe+122BB40 - 0FB6 C3               - movzx eax,bl
victoria3.exe+122BB43 - 24 3F                 - and al,3F
victoria3.exe+122BB45 - 0FB6 C8               - movzx ecx,al
victoria3.exe+122BB48 - 48 8B C3              - mov rax,rbx
victoria3.exe+122BB4B - 48 C1 E8 06           - shr rax,06
victoria3.exe+122BB4F - 49 8B 84 C5 C8050000  - mov rax,[r13+rax*8+000005C8]
victoria3.exe+122BB57 - 48 0FA3 C8            - bt rax,rcx
victoria3.exe+122BB5B - 73 12                 - jae victoria3.exe+122BB6F
victoria3.exe+122BB5D - 49 8B 85 B0050000     - mov rax,[r13+000005B0]
victoria3.exe+122BB64 - 48 83 3C D8  00       - cmp qword ptr [rax+rbx*8],00
victoria3.exe+122BB69 - 0F8F 30010000         - jg victoria3.exe+122BC9F
victoria3.exe+122BB6F - 48 63 5F 10           - movsxd  rbx,dword ptr [rdi+10]
victoria3.exe+122BB73 - 8B CB                 - mov ecx,ebx
victoria3.exe+122BB75 - E8 B6AADFFF           - call victoria3.exe+1026630
victoria3.exe+122BB7A - 84 C0                 - test al,al
victoria3.exe+122BB7C - 74 2A                 - je victoria3.exe+122BBA8
victoria3.exe+122BB7E - 0FB6 C3               - movzx eax,bl
victoria3.exe+122BB81 - 24 3F                 - and al,3F
victoria3.exe+122BB83 - 0FB6 C8               - movzx ecx,al
victoria3.exe+122BB86 - 48 8B C3              - mov rax,rbx
victoria3.exe+122BB89 - 48 C1 E8 06           - shr rax,06
victoria3.exe+122BB8D - 48 8B 84 C6 A81D0000  - mov rax,[rsi+rax*8+00001DA8]
victoria3.exe+122BB95 - 48 0FA3 C8            - bt rax,rcx
victoria3.exe+122BB99 - 73 0D                 - jae victoria3.exe+122BBA8
victoria3.exe+122BB9B - 48 8B 8E 901D0000     - mov rcx,[rsi+00001D90]
victoria3.exe+122BBA2 - 48 8B 0C D9           - mov rcx,[rcx+rbx*8]
victoria3.exe+122BBA6 - EB 02                 - jmp victoria3.exe+122BBAA
victoria3.exe+122BBA8 - 33 C9                 - xor ecx,ecx
victoria3.exe+122BBAA - 49 BC 09E1D1C6116BF129 - mov r12,29F16B11C6D1E109
victoria3.exe+122BBB4 - 49 8B C4              - mov rax,r12
victoria3.exe+122BBB7 - 48 F7 E9              - imul rcx
victoria3.exe+122BBBA - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122BBBE - 48 8B C2              - mov rax,rdx
victoria3.exe+122BBC1 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122BBC5 - 48 03 D0              - add rdx,rax
victoria3.exe+122BBC8 - 8B DA                 - mov ebx,edx
victoria3.exe+122BBCA - F7 DB                 - neg ebx
victoria3.exe+122BBCC - 0F48 DA               - cmovs ebx,edx
victoria3.exe+122BBCF - 44 2B FB              - sub r15d,ebx
victoria3.exe+122BBD2 - 4C 8B C7              - mov r8,rdi
victoria3.exe+122BBD5 - 48 8D 94 24 00030000  - lea rdx,[rsp+00000300]
victoria3.exe+122BBDD - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BBE0 - E8 6BEFFFFF           - call victoria3.exe+122AB50
victoria3.exe+122BBE5 - 4C 8B 08              - mov r9,[rax]
victoria3.exe+122BBE8 - 48 63 DB              - movsxd  rbx,ebx
victoria3.exe+122BBEB - 48 69 CB A0860100     - imul rcx,rbx,000186A0
victoria3.exe+122BBF2 - BA 33F304B5           - mov edx,B504F333
victoria3.exe+122BBF7 - 48 8D 04 11           - lea rax,[rcx+rdx]
victoria3.exe+122BBFB - 49 B8 66E6096A01000000 - mov r8,000000016A09E666
victoria3.exe+122BC05 - 49 3B C0              - cmp rax,r8
victoria3.exe+122BC08 - 77 0F                 - ja victoria3.exe+122BC19
victoria3.exe+122BC0A - 49 8D 04 11           - lea rax,[r9+rdx]
victoria3.exe+122BC0E - 49 3B C0              - cmp rax,r8
victoria3.exe+122BC11 - 77 06                 - ja victoria3.exe+122BC19
victoria3.exe+122BC13 - 49 0FAF D9            - imul rbx,r9
victoria3.exe+122BC17 - EB 4E                 - jmp victoria3.exe+122BC67
victoria3.exe+122BC19 - 4D 8B C1              - mov r8,r9
victoria3.exe+122BC1C - 4C 3B C9              - cmp r9,rcx
victoria3.exe+122BC1F - 4C 0F4C C1            - cmovl r8,rcx
victoria3.exe+122BC23 - 4C 0F4F C9            - cmovg r9,rcx
victoria3.exe+122BC27 - 49 8B C4              - mov rax,r12
victoria3.exe+122BC2A - 49 F7 E8              - imul r8
victoria3.exe+122BC2D - 48 8B CA              - mov rcx,rdx
victoria3.exe+122BC30 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+122BC34 - 48 8B C1              - mov rax,rcx
victoria3.exe+122BC37 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122BC3B - 48 03 C8              - add rcx,rax
victoria3.exe+122BC3E - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+122BC45 - 4C 2B C0              - sub r8,rax
victoria3.exe+122BC48 - 4D 0FAF C1            - imul r8,r9
victoria3.exe+122BC4C - 49 8B C4              - mov rax,r12
victoria3.exe+122BC4F - 49 F7 E8              - imul r8
victoria3.exe+122BC52 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122BC56 - 48 8B DA              - mov rbx,rdx
victoria3.exe+122BC59 - 48 C1 EB 3F           - shr rbx,3F
victoria3.exe+122BC5D - 48 03 DA              - add rbx,rdx
victoria3.exe+122BC60 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+122BC64 - 48 03 D9              - add rbx,rcx
victoria3.exe+122BC67 - 4C 8B C3              - mov r8,rbx
victoria3.exe+122BC6A - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BC6D - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+122BC72 - E8 C9BDDFFF           - call victoria3.exe+1027A40
victoria3.exe+122BC77 - 4C 8B C3              - mov r8,rbx
victoria3.exe+122BC7A - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BC7D - 48 8D 8C 24 70010000  - lea rcx,[rsp+00000170]
victoria3.exe+122BC85 - E8 B6BDDFFF           - call victoria3.exe+1027A40
victoria3.exe+122BC8A - 48 8D 8E 881D0000     - lea rcx,[rsi+00001D88]
victoria3.exe+122BC91 - 45 33 C0              - xor r8d,r8d
victoria3.exe+122BC94 - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BC97 - E8 C4BADFFF           - call victoria3.exe+1027760
victoria3.exe+122BC9C - 41 B4 01              - mov r12b,01
victoria3.exe+122BC9F - 49 83 C6 08           - add r14,08
victoria3.exe+122BCA3 - 4C 3B B4 24 F0020000  - cmp r14,[rsp+000002F0]
victoria3.exe+122BCAB - 0F85 1FFEFFFF         - jne victoria3.exe+122BAD0
victoria3.exe+122BCB1 - 8B 9C 24 F8020000     - mov ebx,[rsp+000002F8]
victoria3.exe+122BCB8 - 45 85 FF              - test r15d,r15d
victoria3.exe+122BCBB - 7E 35                 - jle victoria3.exe+122BCF2
victoria3.exe+122BCBD - 0FAF 5E 08            - imul ebx,[rsi+08]
victoria3.exe+122BCC1 - 89 9C 24 F0020000     - mov [rsp+000002F0],ebx
victoria3.exe+122BCC8 - B8 9FBAA65E           - mov eax,5EA6BA9F
victoria3.exe+122BCCD - 2B C3                 - sub eax,ebx
victoria3.exe+122BCCF - 89 84 24 F4020000     - mov [rsp+000002F4],eax
victoria3.exe+122BCD6 - 4C 8D 8C 24 F0020000  - lea r9,[rsp+000002F0]
victoria3.exe+122BCDE - 4C 8D 44 24 30        - lea r8,[rsp+30]
victoria3.exe+122BCE3 - 41 8B D7              - mov edx,r15d
victoria3.exe+122BCE6 - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BCE9 - E8 52000000           - call victoria3.exe+122BD40
victoria3.exe+122BCEE - 85 C0                 - test eax,eax
victoria3.exe+122BCF0 - 7F 05                 - jg victoria3.exe+122BCF7
victoria3.exe+122BCF2 - 45 84 E4              - test r12b,r12b
victoria3.exe+122BCF5 - 74 1F                 - je victoria3.exe+122BD16
victoria3.exe+122BCF7 - 48 8B 06              - mov rax,[rsi]
victoria3.exe+122BCFA - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BCFD - FF 50 08              - call qword ptr [rax+08]
victoria3.exe+122BD00 - 84 C0                 - test al,al
victoria3.exe+122BD02 - 74 12                 - je victoria3.exe+122BD16
victoria3.exe+122BD04 - 48 8D 8E 701D0000     - lea rcx,[rsi+00001D70]
victoria3.exe+122BD0B - BA 03000000           - mov edx,00000003
victoria3.exe+122BD10 - E8 DB09D8FF           - call victoria3.exe+FAC6F0
victoria3.exe+122BD15 - 90                    - nop 
victoria3.exe+122BD16 - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+122BD1B - E8 907AC0FF           - call victoria3.exe+E337B0
victoria3.exe+122BD20 - 48 8B 9C 24 08030000  - mov rbx,[rsp+00000308]
victoria3.exe+122BD28 - 48 81 C4 B0020000     - add rsp,000002B0
victoria3.exe+122BD2F - 41 5F                 - pop r15
victoria3.exe+122BD31 - 41 5E                 - pop r14
victoria3.exe+122BD33 - 41 5D                 - pop r13
victoria3.exe+122BD35 - 41 5C                 - pop r12
victoria3.exe+122BD37 - 5F                    - pop rdi
victoria3.exe+122BD38 - 5E                    - pop rsi
victoria3.exe+122BD39 - 5D                    - pop rbp
victoria3.exe+122BD3A - C3                    - ret 
victoria3.exe+122BD3B - CC                    - int 3 
victoria3.exe+122BD3C - CC                    - int 3 
victoria3.exe+122BD3D - CC                    - int 3 
victoria3.exe+122BD3E - CC                    - int 3 
victoria3.exe+122BD3F - CC                    - int 3 
victoria3.exe+122BD40 - 48 89 5C 24 08        - mov [rsp+08],rbx
victoria3.exe+122BD45 - 48 89 6C 24 10        - mov [rsp+10],rbp
victoria3.exe+122BD4A - 48 89 74 24 18        - mov [rsp+18],rsi
victoria3.exe+122BD4F - 57                    - push rdi
victoria3.exe+122BD50 - 41 54                 - push r12
victoria3.exe+122BD52 - 41 55                 - push r13
victoria3.exe+122BD54 - 41 56                 - push r14
victoria3.exe+122BD56 - 41 57                 - push r15
victoria3.exe+122BD58 - 48 81 EC F0000000     - sub rsp,000000F0
victoria3.exe+122BD5F - 4D 8B F1              - mov r14,r9
victoria3.exe+122BD62 - 49 8B F8              - mov rdi,r8
victoria3.exe+122BD65 - 44 8B FA              - mov r15d,edx
victoria3.exe+122BD68 - 48 8B E9              - mov rbp,rcx
victoria3.exe+122BD6B - 48 8D 05 E6D01903     - lea rax,[victoria3.exe+43C8E58]
victoria3.exe+122BD72 - 48 89 44 24 50        - mov [rsp+50],rax
victoria3.exe+122BD77 - 48 8D 4C 24 58        - lea rcx,[rsp+58]
victoria3.exe+122BD7C - E8 1F653EFF           - call victoria3.exe+6122A0
victoria3.exe+122BD81 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+122BD85 - C5F81144 24 70        - vmovups [rsp+70],xmm0
victoria3.exe+122BD8B - 48 8D 8C 24 80000000  - lea rcx,[rsp+00000080]
victoria3.exe+122BD93 - E8 08653EFF           - call victoria3.exe+6122A0
victoria3.exe+122BD98 - 33 F6                 - xor esi,esi
victoria3.exe+122BD9A - 89 B4 24 98000000     - mov [rsp+00000098],esi
victoria3.exe+122BDA1 - 45 85 FF              - test r15d,r15d
victoria3.exe+122BDA4 - 0F8E CF000000         - jng victoria3.exe+122BE79
victoria3.exe+122BDAA - 41 BC 30020000        - mov r12d,00000230
victoria3.exe+122BDB0 - 41 BD 90010000        - mov r13d,00000190
victoria3.exe+122BDB6 - 66 66 0F1F 84 00 00000000  - nop word ptr [rax+rax+00000000]
victoria3.exe+122BDC0 - 4C 89 74 24 20        - mov [rsp+20],r14
victoria3.exe+122BDC5 - 41 B9 01000000        - mov r9d,00000001
victoria3.exe+122BDCB - 4C 8B C7              - mov r8,rdi
victoria3.exe+122BDCE - 48 8D 94 24 A0000000  - lea rdx,[rsp+000000A0]
victoria3.exe+122BDD6 - 48 8B CD              - mov rcx,rbp
victoria3.exe+122BDD9 - E8 72EEFFFF           - call victoria3.exe+122AC50
victoria3.exe+122BDDE - 48 8B 9C 24 A0000000  - mov rbx,[rsp+000000A0]
victoria3.exe+122BDE6 - 48 8B 03              - mov rax,[rbx]
victoria3.exe+122BDE9 - 48 8B CB              - mov rcx,rbx
victoria3.exe+122BDEC - FF 10                 - call qword ptr [rax]
victoria3.exe+122BDEE - 84 C0                 - test al,al
victoria3.exe+122BDF0 - 0F84 83000000         - je victoria3.exe+122BE79
victoria3.exe+122BDF6 - 0FB6 94 24 A8000000   - movzx edx,byte ptr [rsp+000000A8]
victoria3.exe+122BDFE - 84 D2                 - test dl,dl
victoria3.exe+122BE00 - 41 0F94 C3            - sete r11b
victoria3.exe+122BE04 - 41 B9 E0010000        - mov r9d,000001E0
victoria3.exe+122BE0A - 84 D2                 - test dl,dl
victoria3.exe+122BE0C - 4D 0F44 CC            - cmove r9,r12
victoria3.exe+122BE10 - 4C 03 CF              - add r9,rdi
victoria3.exe+122BE13 - 41 BA 40010000        - mov r10d,00000140
victoria3.exe+122BE19 - 45 84 DB              - test r11b,r11b
victoria3.exe+122BE1C - 4D 0F44 D5            - cmove r10,r13
victoria3.exe+122BE20 - 4C 03 D7              - add r10,rdi
victoria3.exe+122BE23 - 48 8D 47 50           - lea rax,[rdi+50]
victoria3.exe+122BE27 - 4C 8B C7              - mov r8,rdi
victoria3.exe+122BE2A - 45 84 DB              - test r11b,r11b
victoria3.exe+122BE2D - 4C 0F44 C0            - cmove r8,rax
victoria3.exe+122BE31 - 48 8D 85 881D0000     - lea rax,[rbp+00001D88]
victoria3.exe+122BE38 - 4C 89 4C 24 40        - mov [rsp+40],r9
victoria3.exe+122BE3D - 4C 89 54 24 38        - mov [rsp+38],r10
victoria3.exe+122BE42 - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+122BE47 - 48 89 4C 24 30        - mov [rsp+30],rcx
victoria3.exe+122BE4C - 4C 89 44 24 28        - mov [rsp+28],r8
victoria3.exe+122BE51 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+122BE56 - 4C 8B 8C 24 E0000000  - mov r9,[rsp+000000E0]
victoria3.exe+122BE5E - 4C 8B 84 24 D8000000  - mov r8,[rsp+000000D8]
victoria3.exe+122BE66 - 48 8B CB              - mov rcx,rbx
victoria3.exe+122BE69 - E8 B2F0FCFF           - call victoria3.exe+11FAF20
victoria3.exe+122BE6E - FF C6                 - inc esi
victoria3.exe+122BE70 - 41 3B F7              - cmp esi,r15d
victoria3.exe+122BE73 - 0F8C 47FFFFFF         - jl victoria3.exe+122BDC0
victoria3.exe+122BE79 - 48 8B 94 24 80000000  - mov rdx,[rsp+00000080]
victoria3.exe+122BE81 - 48 85 D2              - test rdx,rdx
victoria3.exe+122BE84 - 74 0E                 - je victoria3.exe+122BE94
victoria3.exe+122BE86 - 48 8B 8C 24 90000000  - mov rcx,[rsp+00000090]
victoria3.exe+122BE8E - 48 8B 01              - mov rax,[rcx]
victoria3.exe+122BE91 - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+122BE94 - 48 8B 54 24 58        - mov rdx,[rsp+58]
victoria3.exe+122BE99 - 48 85 D2              - test rdx,rdx
victoria3.exe+122BE9C - 74 0C                 - je victoria3.exe+122BEAA
victoria3.exe+122BE9E - 48 8B 4C 24 68        - mov rcx,[rsp+68]
victoria3.exe+122BEA3 - 4C 8B 01              - mov r8,[rcx]
victoria3.exe+122BEA6 - 41 FF 50 10           - call qword ptr [r8+10]
victoria3.exe+122BEAA - 8B C6                 - mov eax,esi
victoria3.exe+122BEAC - 4C 8D 9C 24 F0000000  - lea r11,[rsp+000000F0]
victoria3.exe+122BEB4 - 49 8B 5B 30           - mov rbx,[r11+30]
victoria3.exe+122BEB8 - 49 8B 6B 38           - mov rbp,[r11+38]
victoria3.exe+122BEBC - 49 8B 73 40           - mov rsi,[r11+40]
victoria3.exe+122BEC0 - 49 8B E3              - mov rsp,r11
victoria3.exe+122BEC3 - 41 5F                 - pop r15
victoria3.exe+122BEC5 - 41 5E                 - pop r14
victoria3.exe+122BEC7 - 41 5D                 - pop r13
victoria3.exe+122BEC9 - 41 5C                 - pop r12
victoria3.exe+122BECB - 5F                    - pop rdi
victoria3.exe+122BECC - C3                    - ret 
victoria3.exe+122BECD - CC                    - int 3 
victoria3.exe+122BECE - CC                    - int 3 
victoria3.exe+122BECF - CC                    - int 3 
victoria3.exe+122BED0 - 48 89 5C 24 10        - mov [rsp+10],rbx
victoria3.exe+122BED5 - 48 89 74 24 18        - mov [rsp+18],rsi
victoria3.exe+122BEDA - 57                    - push rdi
victoria3.exe+122BEDB - 48 83 EC 40           - sub rsp,40
victoria3.exe+122BEDF - 83 3D 5A36EB03 00     - cmp dword ptr [victoria3.exe+50DF540],00
victoria3.exe+122BEE6 - 48 8B FA              - mov rdi,rdx
victoria3.exe+122BEE9 - 48 8B F1              - mov rsi,rcx
victoria3.exe+122BEEC - 75 18                 - jne victoria3.exe+122BF06
victoria3.exe+122BEEE - 48 8D 05 915F6C04     - lea rax,[victoria3.exe+58F1E86]
victoria3.exe+122BEF5 - 48 8D 0D D4FC1A03     - lea rcx,[victoria3.exe+43DBBD0]
victoria3.exe+122BEFC - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122BF01 - E8 BA688702           - call victoria3.exe+3AA27C0
victoria3.exe+122BF06 - 48 8B 05 43CB6804     - mov rax,[victoria3.exe+58B8A50]
victoria3.exe+122BF0D - 48 8D 8E F01D0000     - lea rcx,[rsi+00001DF0]
victoria3.exe+122BF14 - 4C 8D 4C 24 50        - lea r9,[rsp+50]
victoria3.exe+122BF19 - 48 8D 54 24 30        - lea rdx,[rsp+30]
victoria3.exe+122BF1E - 4C 8B 80 08060000     - mov r8,[rax+00000608]
victoria3.exe+122BF25 - 49 8B 58 08           - mov rbx,[r8+08]
victoria3.exe+122BF29 - 48 89 7C 24 50        - mov [rsp+50],rdi
victoria3.exe+122BF2E - 44 8B 47 14           - mov r8d,[rdi+14]
victoria3.exe+122BF32 - E8 09880100           - call victoria3.exe+1244740
victoria3.exe+122BF37 - 48 8B 44 24 30        - mov rax,[rsp+30]
victoria3.exe+122BF3C - 48 8B 74 24 60        - mov rsi,[rsp+60]
victoria3.exe+122BF41 - 48 89 58 10           - mov [rax+10],rbx
victoria3.exe+122BF45 - 48 8B 5C 24 58        - mov rbx,[rsp+58]
victoria3.exe+122BF4A - 48 83 C4 40           - add rsp,40
victoria3.exe+122BF4E - 5F                    - pop rdi
victoria3.exe+122BF4F - C3                    - ret 
victoria3.exe+122BF50 - 40 53                 - push rbx
victoria3.exe+122BF52 - 48 83 EC 20           - sub rsp,20
victoria3.exe+122BF56 - 33 D2                 - xor edx,edx
victoria3.exe+122BF58 - 48 8B D9              - mov rbx,rcx
victoria3.exe+122BF5B - E8 F0DCFFFF           - call victoria3.exe+1229C50
victoria3.exe+122BF60 - 33 D2                 - xor edx,edx
victoria3.exe+122BF62 - 89 83 581D0000        - mov [rbx+00001D58],eax
victoria3.exe+122BF68 - 48 8B CB              - mov rcx,rbx
victoria3.exe+122BF6B - E8 00E5FFFF           - call victoria3.exe+122A470
victoria3.exe+122BF70 - 89 83 5C1D0000        - mov [rbx+00001D5C],eax
victoria3.exe+122BF76 - 48 83 C4 20           - add rsp,20
victoria3.exe+122BF7A - 5B                    - pop rbx
victoria3.exe+122BF7B - C3                    - ret 
victoria3.exe+122BF7C - CC                    - int 3 
victoria3.exe+122BF7D - CC                    - int 3 
victoria3.exe+122BF7E - CC                    - int 3 
victoria3.exe+122BF7F - CC                    - int 3 
victoria3.exe+122BF80 - 48 89 5C 24 10        - mov [rsp+10],rbx
victoria3.exe+122BF85 - 48 89 6C 24 18        - mov [rsp+18],rbp
victoria3.exe+122BF8A - 48 89 74 24 20        - mov [rsp+20],rsi
victoria3.exe+122BF8F - 57                    - push rdi
victoria3.exe+122BF90 - B8 50100000           - mov eax,00001050
victoria3.exe+122BF95 - E8 D69AF002           - call victoria3.exe+4135A70
victoria3.exe+122BF9A - 48 2B E0              - sub rsp,rax
victoria3.exe+122BF9D - 48 8B F9              - mov rdi,rcx
victoria3.exe+122BFA0 - C7 81 E41D0000 00000000 - mov [rcx+00001DE4],00000000
victoria3.exe+122BFAA - E8 71D5FFFF           - call victoria3.exe+1229520
victoria3.exe+122BFAF - 84 C0                 - test al,al
victoria3.exe+122BFB1 - 0F84 14010000         - je victoria3.exe+122C0CB
victoria3.exe+122BFB7 - E8 040958FF           - call victoria3.exe+7AC8C0
victoria3.exe+122BFBC - 48 8B 30              - mov rsi,[rax]
victoria3.exe+122BFBF - 48 85 F6              - test rsi,rsi
victoria3.exe+122BFC2 - 75 2B                 - jne victoria3.exe+122BFEF
victoria3.exe+122BFC4 - 48 8D 05 25E21803     - lea rax,[victoria3.exe+43BA1F0]
victoria3.exe+122BFCB - 48 89 44 24 30        - mov [rsp+30],rax
victoria3.exe+122BFD0 - C7 44 24 38 1E000000  - mov [rsp+38],0000001E
victoria3.exe+122BFD8 - 40 88 74 24 3C        - mov [rsp+3C],sil
victoria3.exe+122BFDD - 45 33 C9              - xor r9d,r9d
victoria3.exe+122BFE0 - 4C 8D 44 24 30        - lea r8,[rsp+30]
victoria3.exe+122BFE5 - BA 04000000           - mov edx,00000004
victoria3.exe+122BFEA - E8 F1258D02           - call victoria3.exe+3AFE5E0
victoria3.exe+122BFEF - 48 8B 9E 80000000     - mov rbx,[rsi+00000080]
victoria3.exe+122BFF6 - 48 63 86 8C000000     - movsxd  rax,dword ptr [rsi+0000008C]
victoria3.exe+122BFFD - 48 8D 34 C3           - lea rsi,[rbx+rax*8]
victoria3.exe+122C001 - 48 3B DE              - cmp rbx,rsi
victoria3.exe+122C004 - 74 44                 - je victoria3.exe+122C04A
victoria3.exe+122C006 - 66 66 0F1F 84 00 00000000  - nop word ptr [rax+rax+00000000]
victoria3.exe+122C010 - 48 8B 13              - mov rdx,[rbx]
victoria3.exe+122C013 - 48 89 94 24 60100000  - mov [rsp+00001060],rdx
victoria3.exe+122C01B - F6 42 40 01           - test byte ptr [rdx+40],01
victoria3.exe+122C01F - 75 20                 - jne victoria3.exe+122C041
victoria3.exe+122C021 - 48 8B CF              - mov rcx,rdi
victoria3.exe+122C024 - E8 A7EAFFFF           - call victoria3.exe+122AAD0
victoria3.exe+122C029 - 3C 02                 - cmp al,02
victoria3.exe+122C02B - 74 14                 - je victoria3.exe+122C041
victoria3.exe+122C02D - 48 8D 8F D81D0000     - lea rcx,[rdi+00001DD8]
victoria3.exe+122C034 - 48 8D 94 24 60100000  - lea rdx,[rsp+00001060]
victoria3.exe+122C03C - E8 AF7C40FF           - call victoria3.exe+633CF0
victoria3.exe+122C041 - 48 83 C3 08           - add rbx,08
victoria3.exe+122C045 - 48 3B DE              - cmp rbx,rsi
victoria3.exe+122C048 - 75 C6                 - jne victoria3.exe+122C010
victoria3.exe+122C04A - 48 8B B7 D81D0000     - mov rsi,[rdi+00001DD8]
victoria3.exe+122C051 - 48 63 9F E41D0000     - movsxd  rbx,dword ptr [rdi+00001DE4]
victoria3.exe+122C058 - 48 8D 2C DE           - lea rbp,[rsi+rbx*8]
victoria3.exe+122C05C - 48 83 FB 20           - cmp rbx,20
victoria3.exe+122C060 - 7F 10                 - jg victoria3.exe+122C072
victoria3.exe+122C062 - 4C 8B C7              - mov r8,rdi
victoria3.exe+122C065 - 48 8B D5              - mov rdx,rbp
victoria3.exe+122C068 - 48 8B CE              - mov rcx,rsi
victoria3.exe+122C06B - E8 C0120100           - call victoria3.exe+123D330
victoria3.exe+122C070 - EB 59                 - jmp victoria3.exe+122C0CB
victoria3.exe+122C072 - 48 8B C3              - mov rax,rbx
victoria3.exe+122C075 - 48 99                 - cqo 
victoria3.exe+122C077 - 48 2B C2              - sub rax,rdx
victoria3.exe+122C07A - 48 D1 F8              - sar rax,1
victoria3.exe+122C07D - 48 8B D3              - mov rdx,rbx
victoria3.exe+122C080 - 48 2B D0              - sub rdx,rax
victoria3.exe+122C083 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122C088 - E8 63D7A2FF           - call victoria3.exe+C597F0
victoria3.exe+122C08D - 90                    - nop 
victoria3.exe+122C08E - 48 89 7C 24 28        - mov [rsp+28],rdi
victoria3.exe+122C093 - 48 8B 44 24 48        - mov rax,[rsp+48]
victoria3.exe+122C098 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+122C09D - 4C 8B 4C 24 40        - mov r9,[rsp+40]
victoria3.exe+122C0A2 - 4C 8B C3              - mov r8,rbx
victoria3.exe+122C0A5 - 48 8B D5              - mov rdx,rbp
victoria3.exe+122C0A8 - 48 8B CE              - mov rcx,rsi
victoria3.exe+122C0AB - E8 A0140100           - call victoria3.exe+123D550
victoria3.exe+122C0B0 - 90                    - nop 
victoria3.exe+122C0B1 - 48 81 7C 24 48 00020000 - cmp qword ptr [rsp+48],00000200
victoria3.exe+122C0BA - 76 0F                 - jna victoria3.exe+122C0CB
victoria3.exe+122C0BC - 48 8B 4C 24 40        - mov rcx,[rsp+40]
victoria3.exe+122C0C1 - 48 85 C9              - test rcx,rcx
victoria3.exe+122C0C4 - 74 05                 - je victoria3.exe+122C0CB
victoria3.exe+122C0C6 - E8 6542EF02           - call victoria3.exe+4120330
victoria3.exe+122C0CB - 4C 8D 9C 24 50100000  - lea r11,[rsp+00001050]
victoria3.exe+122C0D3 - 49 8B 5B 18           - mov rbx,[r11+18]
victoria3.exe+122C0D7 - 49 8B 6B 20           - mov rbp,[r11+20]
victoria3.exe+122C0DB - 49 8B 73 28           - mov rsi,[r11+28]
victoria3.exe+122C0DF - 49 8B E3              - mov rsp,r11
victoria3.exe+122C0E2 - 5F                    - pop rdi
victoria3.exe+122C0E3 - C3                    - ret 



# 7FF7EB0ABA8E
victoria3.exe+122B99D - CC                    - int 3 
victoria3.exe+122B99E - CC                    - int 3 
victoria3.exe+122B99F - CC                    - int 3 
victoria3.exe+122B9A0 - 48 89 5C 24 20        - mov [rsp+20],rbx
victoria3.exe+122B9A5 - 89 54 24 10           - mov [rsp+10],edx
victoria3.exe+122B9A9 - 55                    - push rbp
victoria3.exe+122B9AA - 56                    - push rsi
victoria3.exe+122B9AB - 57                    - push rdi
victoria3.exe+122B9AC - 41 54                 - push r12
victoria3.exe+122B9AE - 41 55                 - push r13
victoria3.exe+122B9B0 - 41 56                 - push r14
victoria3.exe+122B9B2 - 41 57                 - push r15
victoria3.exe+122B9B4 - 48 81 EC B0020000     - sub rsp,000002B0
victoria3.exe+122B9BB - 8B DA                 - mov ebx,edx
victoria3.exe+122B9BD - 48 8B F1              - mov rsi,rcx
victoria3.exe+122B9C0 - 33 D2                 - xor edx,edx
victoria3.exe+122B9C2 - E8 89E2FFFF           - call victoria3.exe+1229C50
victoria3.exe+122B9C7 - 89 86 581D0000        - mov [rsi+00001D58],eax
victoria3.exe+122B9CD - 33 D2                 - xor edx,edx
victoria3.exe+122B9CF - 48 8B CE              - mov rcx,rsi
victoria3.exe+122B9D2 - E8 99EAFFFF           - call victoria3.exe+122A470
victoria3.exe+122B9D7 - 44 8B F8              - mov r15d,eax
victoria3.exe+122B9DA - 89 86 5C1D0000        - mov [rsi+00001D5C],eax
victoria3.exe+122B9E0 - 85 C0                 - test eax,eax
victoria3.exe+122B9E2 - 0F8E 38030000         - jng victoria3.exe+122BD20
victoria3.exe+122B9E8 - 80 BE B8110000 00     - cmp byte ptr [rsi+000011B8],00
victoria3.exe+122B9EF - 74 24                 - je victoria3.exe+122BA15
victoria3.exe+122B9F1 - 8B 86 480B0000        - mov eax,[rsi+00000B48]
victoria3.exe+122B9F7 - 83 F8 FF              - cmp eax,-01
victoria3.exe+122B9FA - 74 19                 - je victoria3.exe+122BA15
victoria3.exe+122B9FC - 89 84 24 F0020000     - mov [rsp+000002F0],eax
victoria3.exe+122BA03 - 48 8D 8C 24 F0020000  - lea rcx,[rsp+000002F0]
victoria3.exe+122BA0B - E8 A07959FF           - call victoria3.exe+7C33B0
victoria3.exe+122BA10 - 8B 48 10              - mov ecx,[rax+10]
victoria3.exe+122BA13 - EB 20                 - jmp victoria3.exe+122BA35
victoria3.exe+122BA15 - 8B 86 480E0000        - mov eax,[rsi+00000E48]
victoria3.exe+122BA1B - 89 84 24 F0020000     - mov [rsp+000002F0],eax
victoria3.exe+122BA22 - 48 8D 8C 24 F0020000  - lea rcx,[rsp+000002F0]
victoria3.exe+122BA2A - E8 815058FF           - call victoria3.exe+7B0AB0
victoria3.exe+122BA2F - 8B 88 D4090000        - mov ecx,[rax+000009D4]
victoria3.exe+122BA35 - 89 8C 24 F0020000     - mov [rsp+000002F0],ecx
victoria3.exe+122BA3C - 48 8D 8C 24 F0020000  - lea rcx,[rsp+000002F0]
victoria3.exe+122BA44 - E8 374959FF           - call victoria3.exe+7C0380
victoria3.exe+122BA49 - 48 8D 88 48080000     - lea rcx,[rax+00000848]
victoria3.exe+122BA50 - E8 5B5058FF           - call victoria3.exe+7B0AB0
victoria3.exe+122BA55 - 48 8B E8              - mov rbp,rax
victoria3.exe+122BA58 - 83 3D E13AEB03 00     - cmp dword ptr [victoria3.exe+50DF540],00
victoria3.exe+122BA5F - 75 18                 - jne victoria3.exe+122BA79
victoria3.exe+122BA61 - 48 8D 05 1E646C04     - lea rax,[victoria3.exe+58F1E86]
victoria3.exe+122BA68 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122BA6D - 48 8D 0D 5C011B03     - lea rcx,[victoria3.exe+43DBBD0]
victoria3.exe+122BA74 - E8 476D8702           - call victoria3.exe+3AA27C0
victoria3.exe+122BA79 - 48 8B 0D D0CF6804     - mov rcx,[victoria3.exe+58B8A50]
victoria3.exe+122BA80 - 48 8B 91 08060000     - mov rdx,[rcx+00000608]
victoria3.exe+122BA87 - 4C 8B AA 20010000     - mov r13,[rdx+00000120]
victoria3.exe+122BA8E - 44 2B BE 581D0000     - sub r15d,[rsi+00001D58]
victoria3.exe+122BA95 - 45 32 E4              - xor r12b,r12b
victoria3.exe+122BA98 - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+122BA9D - E8 1E77C0FF           - call victoria3.exe+E331C0
victoria3.exe+122BAA2 - 90                    - nop 
victoria3.exe+122BAA3 - 4C 8B B6 D81D0000     - mov r14,[rsi+00001DD8]
victoria3.exe+122BAAA - 48 63 86 E41D0000     - movsxd  rax,dword ptr [rsi+00001DE4]
victoria3.exe+122BAB1 - 49 8D 04 C6           - lea rax,[r14+rax*8]
victoria3.exe+122BAB5 - 48 89 84 24 F0020000  - mov [rsp+000002F0],rax
victoria3.exe+122BABD - 4C 3B F0              - cmp r14,rax
victoria3.exe+122BAC0 - 0F84 F2010000         - je victoria3.exe+122BCB8
victoria3.exe+122BAC6 - 66 66 0F1F 84 00 00000000  - nop word ptr [rax+rax+00000000]
victoria3.exe+122BAD0 - 49 8B 3E              - mov rdi,[r14]
victoria3.exe+122BAD3 - 80 BE B8110000 00     - cmp byte ptr [rsi+000011B8],00
victoria3.exe+122BADA - 75 33                 - jne victoria3.exe+122BB0F
victoria3.exe+122BADC - 33 D2                 - xor edx,edx
victoria3.exe+122BADE - 33 C9                 - xor ecx,ecx
victoria3.exe+122BAE0 - 48 63 85 14240000     - movsxd  rax,dword ptr [rbp+00002414]
victoria3.exe+122BAE7 - 85 C0                 - test eax,eax
victoria3.exe+122BAE9 - 7E 24                 - jle victoria3.exe+122BB0F
victoria3.exe+122BAEB - 4C 8B C0              - mov r8,rax
victoria3.exe+122BAEE - 48 8B 85 08240000     - mov rax,[rbp+00002408]
victoria3.exe+122BAF5 - 48 39 38              - cmp [rax],rdi
victoria3.exe+122BAF8 - 74 10                 - je victoria3.exe+122BB0A
victoria3.exe+122BAFA - FF C2                 - inc edx
victoria3.exe+122BAFC - 48 FF C1              - inc rcx
victoria3.exe+122BAFF - 48 83 C0 08           - add rax,08
victoria3.exe+122BB03 - 49 3B C8              - cmp rcx,r8
victoria3.exe+122BB06 - 7C ED                 - jl victoria3.exe+122BAF5
victoria3.exe+122BB08 - EB 05                 - jmp victoria3.exe+122BB0F
victoria3.exe+122BB0A - 83 FA FF              - cmp edx,-01
victoria3.exe+122BB0D - 75 60                 - jne victoria3.exe+122BB6F
victoria3.exe+122BB0F - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BB12 - 48 8B CD              - mov rcx,rbp
victoria3.exe+122BB15 - E8 668FA0FF           - call victoria3.exe+C34A80
victoria3.exe+122BB1A - 34 01                 - xor al,01
victoria3.exe+122BB1C - 75 51                 - jne victoria3.exe+122BB6F
victoria3.exe+122BB1E - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BB21 - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BB24 - E8 A7EFFFFF           - call victoria3.exe+122AAD0
victoria3.exe+122BB29 - 84 C0                 - test al,al
victoria3.exe+122BB2B - 0F85 6E010000         - jne victoria3.exe+122BC9F
victoria3.exe+122BB31 - 48 63 5F 10           - movsxd  rbx,dword ptr [rdi+10]
victoria3.exe+122BB35 - 8B CB                 - mov ecx,ebx
victoria3.exe+122BB37 - E8 F4AADFFF           - call victoria3.exe+1026630
victoria3.exe+122BB3C - 84 C0                 - test al,al
victoria3.exe+122BB3E - 74 2F                 - je victoria3.exe+122BB6F
victoria3.exe+122BB40 - 0FB6 C3               - movzx eax,bl
victoria3.exe+122BB43 - 24 3F                 - and al,3F
victoria3.exe+122BB45 - 0FB6 C8               - movzx ecx,al
victoria3.exe+122BB48 - 48 8B C3              - mov rax,rbx
victoria3.exe+122BB4B - 48 C1 E8 06           - shr rax,06
victoria3.exe+122BB4F - 49 8B 84 C5 C8050000  - mov rax,[r13+rax*8+000005C8]
victoria3.exe+122BB57 - 48 0FA3 C8            - bt rax,rcx
victoria3.exe+122BB5B - 73 12                 - jae victoria3.exe+122BB6F
victoria3.exe+122BB5D - 49 8B 85 B0050000     - mov rax,[r13+000005B0]
victoria3.exe+122BB64 - 48 83 3C D8  00       - cmp qword ptr [rax+rbx*8],00
victoria3.exe+122BB69 - 0F8F 30010000         - jg victoria3.exe+122BC9F
victoria3.exe+122BB6F - 48 63 5F 10           - movsxd  rbx,dword ptr [rdi+10]
victoria3.exe+122BB73 - 8B CB                 - mov ecx,ebx
victoria3.exe+122BB75 - E8 B6AADFFF           - call victoria3.exe+1026630
victoria3.exe+122BB7A - 84 C0                 - test al,al
victoria3.exe+122BB7C - 74 2A                 - je victoria3.exe+122BBA8
victoria3.exe+122BB7E - 0FB6 C3               - movzx eax,bl
victoria3.exe+122BB81 - 24 3F                 - and al,3F
victoria3.exe+122BB83 - 0FB6 C8               - movzx ecx,al
victoria3.exe+122BB86 - 48 8B C3              - mov rax,rbx
victoria3.exe+122BB89 - 48 C1 E8 06           - shr rax,06
victoria3.exe+122BB8D - 48 8B 84 C6 A81D0000  - mov rax,[rsi+rax*8+00001DA8]
victoria3.exe+122BB95 - 48 0FA3 C8            - bt rax,rcx
victoria3.exe+122BB99 - 73 0D                 - jae victoria3.exe+122BBA8
victoria3.exe+122BB9B - 48 8B 8E 901D0000     - mov rcx,[rsi+00001D90]
victoria3.exe+122BBA2 - 48 8B 0C D9           - mov rcx,[rcx+rbx*8]
victoria3.exe+122BBA6 - EB 02                 - jmp victoria3.exe+122BBAA
victoria3.exe+122BBA8 - 33 C9                 - xor ecx,ecx
victoria3.exe+122BBAA - 49 BC 09E1D1C6116BF129 - mov r12,29F16B11C6D1E109
victoria3.exe+122BBB4 - 49 8B C4              - mov rax,r12
victoria3.exe+122BBB7 - 48 F7 E9              - imul rcx
victoria3.exe+122BBBA - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122BBBE - 48 8B C2              - mov rax,rdx
victoria3.exe+122BBC1 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122BBC5 - 48 03 D0              - add rdx,rax
victoria3.exe+122BBC8 - 8B DA                 - mov ebx,edx
victoria3.exe+122BBCA - F7 DB                 - neg ebx
victoria3.exe+122BBCC - 0F48 DA               - cmovs ebx,edx
victoria3.exe+122BBCF - 44 2B FB              - sub r15d,ebx
victoria3.exe+122BBD2 - 4C 8B C7              - mov r8,rdi
victoria3.exe+122BBD5 - 48 8D 94 24 00030000  - lea rdx,[rsp+00000300]
victoria3.exe+122BBDD - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BBE0 - E8 6BEFFFFF           - call victoria3.exe+122AB50
victoria3.exe+122BBE5 - 4C 8B 08              - mov r9,[rax]
victoria3.exe+122BBE8 - 48 63 DB              - movsxd  rbx,ebx
victoria3.exe+122BBEB - 48 69 CB A0860100     - imul rcx,rbx,000186A0
victoria3.exe+122BBF2 - BA 33F304B5           - mov edx,B504F333
victoria3.exe+122BBF7 - 48 8D 04 11           - lea rax,[rcx+rdx]
victoria3.exe+122BBFB - 49 B8 66E6096A01000000 - mov r8,000000016A09E666
victoria3.exe+122BC05 - 49 3B C0              - cmp rax,r8
victoria3.exe+122BC08 - 77 0F                 - ja victoria3.exe+122BC19
victoria3.exe+122BC0A - 49 8D 04 11           - lea rax,[r9+rdx]
victoria3.exe+122BC0E - 49 3B C0              - cmp rax,r8
victoria3.exe+122BC11 - 77 06                 - ja victoria3.exe+122BC19
victoria3.exe+122BC13 - 49 0FAF D9            - imul rbx,r9
victoria3.exe+122BC17 - EB 4E                 - jmp victoria3.exe+122BC67
victoria3.exe+122BC19 - 4D 8B C1              - mov r8,r9
victoria3.exe+122BC1C - 4C 3B C9              - cmp r9,rcx
victoria3.exe+122BC1F - 4C 0F4C C1            - cmovl r8,rcx
victoria3.exe+122BC23 - 4C 0F4F C9            - cmovg r9,rcx
victoria3.exe+122BC27 - 49 8B C4              - mov rax,r12
victoria3.exe+122BC2A - 49 F7 E8              - imul r8
victoria3.exe+122BC2D - 48 8B CA              - mov rcx,rdx
victoria3.exe+122BC30 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+122BC34 - 48 8B C1              - mov rax,rcx
victoria3.exe+122BC37 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122BC3B - 48 03 C8              - add rcx,rax
victoria3.exe+122BC3E - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+122BC45 - 4C 2B C0              - sub r8,rax
victoria3.exe+122BC48 - 4D 0FAF C1            - imul r8,r9
victoria3.exe+122BC4C - 49 8B C4              - mov rax,r12
victoria3.exe+122BC4F - 49 F7 E8              - imul r8
victoria3.exe+122BC52 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122BC56 - 48 8B DA              - mov rbx,rdx
victoria3.exe+122BC59 - 48 C1 EB 3F           - shr rbx,3F
victoria3.exe+122BC5D - 48 03 DA              - add rbx,rdx
victoria3.exe+122BC60 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+122BC64 - 48 03 D9              - add rbx,rcx
victoria3.exe+122BC67 - 4C 8B C3              - mov r8,rbx
victoria3.exe+122BC6A - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BC6D - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+122BC72 - E8 C9BDDFFF           - call victoria3.exe+1027A40
victoria3.exe+122BC77 - 4C 8B C3              - mov r8,rbx
victoria3.exe+122BC7A - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BC7D - 48 8D 8C 24 70010000  - lea rcx,[rsp+00000170]
victoria3.exe+122BC85 - E8 B6BDDFFF           - call victoria3.exe+1027A40
victoria3.exe+122BC8A - 48 8D 8E 881D0000     - lea rcx,[rsi+00001D88]
victoria3.exe+122BC91 - 45 33 C0              - xor r8d,r8d
victoria3.exe+122BC94 - 48 8B D7              - mov rdx,rdi
victoria3.exe+122BC97 - E8 C4BADFFF           - call victoria3.exe+1027760
victoria3.exe+122BC9C - 41 B4 01              - mov r12b,01
victoria3.exe+122BC9F - 49 83 C6 08           - add r14,08
victoria3.exe+122BCA3 - 4C 3B B4 24 F0020000  - cmp r14,[rsp+000002F0]
victoria3.exe+122BCAB - 0F85 1FFEFFFF         - jne victoria3.exe+122BAD0
victoria3.exe+122BCB1 - 8B 9C 24 F8020000     - mov ebx,[rsp+000002F8]
victoria3.exe+122BCB8 - 45 85 FF              - test r15d,r15d
victoria3.exe+122BCBB - 7E 35                 - jle victoria3.exe+122BCF2
victoria3.exe+122BCBD - 0FAF 5E 08            - imul ebx,[rsi+08]
victoria3.exe+122BCC1 - 89 9C 24 F0020000     - mov [rsp+000002F0],ebx
victoria3.exe+122BCC8 - B8 9FBAA65E           - mov eax,5EA6BA9F
victoria3.exe+122BCCD - 2B C3                 - sub eax,ebx
victoria3.exe+122BCCF - 89 84 24 F4020000     - mov [rsp+000002F4],eax
victoria3.exe+122BCD6 - 4C 8D 8C 24 F0020000  - lea r9,[rsp+000002F0]
victoria3.exe+122BCDE - 4C 8D 44 24 30        - lea r8,[rsp+30]
victoria3.exe+122BCE3 - 41 8B D7              - mov edx,r15d
victoria3.exe+122BCE6 - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BCE9 - E8 52000000           - call victoria3.exe+122BD40
victoria3.exe+122BCEE - 85 C0                 - test eax,eax
victoria3.exe+122BCF0 - 7F 05                 - jg victoria3.exe+122BCF7
victoria3.exe+122BCF2 - 45 84 E4              - test r12b,r12b
victoria3.exe+122BCF5 - 74 1F                 - je victoria3.exe+122BD16
victoria3.exe+122BCF7 - 48 8B 06              - mov rax,[rsi]
victoria3.exe+122BCFA - 48 8B CE              - mov rcx,rsi
victoria3.exe+122BCFD - FF 50 08              - call qword ptr [rax+08]
victoria3.exe+122BD00 - 84 C0                 - test al,al
victoria3.exe+122BD02 - 74 12                 - je victoria3.exe+122BD16
victoria3.exe+122BD04 - 48 8D 8E 701D0000     - lea rcx,[rsi+00001D70]
victoria3.exe+122BD0B - BA 03000000           - mov edx,00000003
victoria3.exe+122BD10 - E8 DB09D8FF           - call victoria3.exe+FAC6F0
victoria3.exe+122BD15 - 90                    - nop 
victoria3.exe+122BD16 - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+122BD1B - E8 907AC0FF           - call victoria3.exe+E337B0
victoria3.exe+122BD20 - 48 8B 9C 24 08030000  - mov rbx,[rsp+00000308]
victoria3.exe+122BD28 - 48 81 C4 B0020000     - add rsp,000002B0
victoria3.exe+122BD2F - 41 5F                 - pop r15
victoria3.exe+122BD31 - 41 5E                 - pop r14
victoria3.exe+122BD33 - 41 5D                 - pop r13
victoria3.exe+122BD35 - 41 5C                 - pop r12
victoria3.exe+122BD37 - 5F                    - pop rdi
victoria3.exe+122BD38 - 5E                    - pop rsi
victoria3.exe+122BD39 - 5D                    - pop rbp
victoria3.exe+122BD3A - C3                    - ret 

# 7FF7EB0A9218
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
victoria3.exe+12294D3 - 4C 89 64 24 20        - mov [rsp+20],r12
victoria3.exe+12294D8 - 45 33 C9              - xor r9d,r9d
victoria3.exe+12294DB - 45 33 C0              - xor r8d,r8d
victoria3.exe+12294DE - 33 D2                 - xor edx,edx
victoria3.exe+12294E0 - 33 C9                 - xor ecx,ecx
victoria3.exe+12294E2 - E8 75BCF102           - call victoria3.exe+414515C
victoria3.exe+12294E7 - CC                    - int 3 

# 7FF7EB091346 
victoria3.exe+1211174 - CC                    - int 3 
victoria3.exe+1211175 - CC                    - int 3 
victoria3.exe+1211176 - CC                    - int 3 
victoria3.exe+1211177 - CC                    - int 3 
victoria3.exe+1211178 - CC                    - int 3 
victoria3.exe+1211179 - CC                    - int 3 
victoria3.exe+121117A - CC                    - int 3 
victoria3.exe+121117B - CC                    - int 3 
victoria3.exe+121117C - CC                    - int 3 
victoria3.exe+121117D - CC                    - int 3 
victoria3.exe+121117E - CC                    - int 3 
victoria3.exe+121117F - CC                    - int 3 
victoria3.exe+1211180 - 48 89 5C 24 08        - mov [rsp+08],rbx
victoria3.exe+1211185 - 48 89 74 24 10        - mov [rsp+10],rsi
victoria3.exe+121118A - 48 89 7C 24 18        - mov [rsp+18],rdi
victoria3.exe+121118F - 4C 89 64 24 20        - mov [rsp+20],r12
victoria3.exe+1211194 - 55                    - push rbp
victoria3.exe+1211195 - 41 56                 - push r14
victoria3.exe+1211197 - 41 57                 - push r15
victoria3.exe+1211199 - 48 8D AC 24 30FFFFFF  - lea rbp,[rsp-000000D0]
victoria3.exe+12111A1 - 48 81 EC D0010000     - sub rsp,000001D0
victoria3.exe+12111A8 - 48 8B F2              - mov rsi,rdx
victoria3.exe+12111AB - 48 8B F9              - mov rdi,rcx
victoria3.exe+12111AE - 33 D2                 - xor edx,edx
victoria3.exe+12111B0 - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+12111B5 - E8 56081B00           - call victoria3.exe+13C1A10
victoria3.exe+12111BA - 90                    - nop 
victoria3.exe+12111BB - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+12111BF - C5F81144 24 30        - vmovups [rsp+30],xmm0
victoria3.exe+12111C5 - C5FA6F0D F3 4D5F03    - vmovdqu xmm1,xmm0,[victoria3.exe+4805FC0]
victoria3.exe+12111CD - C5FA7F4C 24 40        - vmovdqu [rsp+40],xmm1
victoria3.exe+12111D3 - C6 44 24 30 00        - mov byte ptr [rsp+30],00
victoria3.exe+12111D8 - 48 8D 05 19C52603     - lea rax,[victoria3.exe+447D6F8]
victoria3.exe+12111DF - 48 89 45 90           - mov [rbp-70],rax
victoria3.exe+12111E3 - 48 8D 45 90           - lea rax,[rbp-70]
victoria3.exe+12111E7 - 48 89 45 C8           - mov [rbp-38],rax
victoria3.exe+12111EB - 48 8B CF              - mov rcx,rdi
victoria3.exe+12111EE - E8 DDE90100           - call victoria3.exe+122FBD0
victoria3.exe+12111F3 - 48 63 C8              - movsxd  rcx,eax
victoria3.exe+12111F6 - 48 69 D1 A0860100     - imul rdx,rcx,000186A0
victoria3.exe+12111FD - 4C 8B 0D 3C8C6704     - mov r9,[victoria3.exe+5889E40]
victoria3.exe+1211204 - 41 BF 33F304B5        - mov r15d,B504F333
victoria3.exe+121120A - 4A 8D 04 3A           - lea rax,[rdx+r15]
victoria3.exe+121120E - 49 BC 66E6096A01000000 - mov r12,000000016A09E666
victoria3.exe+1211218 - 49 3B C4              - cmp rax,r12
victoria3.exe+121121B - 77 2D                 - ja victoria3.exe+121124A
victoria3.exe+121121D - 4B 8D 04 39           - lea rax,[r9+r15]
victoria3.exe+1211221 - 49 3B C4              - cmp rax,r12
victoria3.exe+1211224 - 77 24                 - ja victoria3.exe+121124A
victoria3.exe+1211226 - 49 0FAF D1            - imul rdx,r9
victoria3.exe+121122A - 48 BB 09E1D1C6116BF129 - mov rbx,29F16B11C6D1E109
victoria3.exe+1211234 - 48 8B C3              - mov rax,rbx
victoria3.exe+1211237 - 48 F7 EA              - imul rdx
victoria3.exe+121123A - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+121123E - 48 8B C2              - mov rax,rdx
victoria3.exe+1211241 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+1211245 - 48 03 D0              - add rdx,rax
victoria3.exe+1211248 - EB 58                 - jmp victoria3.exe+12112A2
victoria3.exe+121124A - 4D 8B C1              - mov r8,r9
victoria3.exe+121124D - 4C 3B CA              - cmp r9,rdx
victoria3.exe+1211250 - 4C 0F4C C2            - cmovl r8,rdx
victoria3.exe+1211254 - 4C 0F4F CA            - cmovg r9,rdx
victoria3.exe+1211258 - 48 BB 09E1D1C6116BF129 - mov rbx,29F16B11C6D1E109
victoria3.exe+1211262 - 48 8B C3              - mov rax,rbx
victoria3.exe+1211265 - 49 F7 E8              - imul r8
victoria3.exe+1211268 - 48 8B CA              - mov rcx,rdx
victoria3.exe+121126B - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+121126F - 48 8B C1              - mov rax,rcx
victoria3.exe+1211272 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+1211276 - 48 03 C8              - add rcx,rax
victoria3.exe+1211279 - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+1211280 - 4C 2B C0              - sub r8,rax
victoria3.exe+1211283 - 4D 0FAF C1            - imul r8,r9
victoria3.exe+1211287 - 48 8B C3              - mov rax,rbx
victoria3.exe+121128A - 49 F7 E8              - imul r8
victoria3.exe+121128D - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+1211291 - 48 8B C2              - mov rax,rdx
victoria3.exe+1211294 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+1211298 - 48 03 D0              - add rdx,rax
victoria3.exe+121129B - 49 0FAF C9            - imul rcx,r9
victoria3.exe+121129F - 48 03 D1              - add rdx,rcx
victoria3.exe+12112A2 - 4C 8D 4C 24 30        - lea r9,[rsp+30]
victoria3.exe+12112A7 - 4C 8D 45 90           - lea r8,[rbp-70]
victoria3.exe+12112AB - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+12112B0 - E8 9BD49DFF           - call victoria3.exe+BEE750
victoria3.exe+12112B5 - 90                    - nop 
victoria3.exe+12112B6 - 45 33 F6              - xor r14d,r14d
victoria3.exe+12112B9 - 48 8B 4D C8           - mov rcx,[rbp-38]
victoria3.exe+12112BD - 48 85 C9              - test rcx,rcx
victoria3.exe+12112C0 - 74 14                 - je victoria3.exe+12112D6
victoria3.exe+12112C2 - 48 8D 45 90           - lea rax,[rbp-70]
victoria3.exe+12112C6 - 48 3B C8              - cmp rcx,rax
victoria3.exe+12112C9 - 0F95 C2               - setne dl
victoria3.exe+12112CC - 48 8B 01              - mov rax,[rcx]
victoria3.exe+12112CF - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+12112D2 - 4C 89 75 C8           - mov [rbp-38],r14
victoria3.exe+12112D6 - 48 8B 44 24 48        - mov rax,[rsp+48]
victoria3.exe+12112DB - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+12112DF - 76 35                 - jna victoria3.exe+1211316
victoria3.exe+12112E1 - 48 8B 54 24 30        - mov rdx,[rsp+30]
victoria3.exe+12112E6 - 48 8B CA              - mov rcx,rdx
victoria3.exe+12112E9 - 48 FF C0              - inc rax
victoria3.exe+12112EC - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+12112F2 - 72 15                 - jb victoria3.exe+1211309
victoria3.exe+12112F4 - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+12112F8 - 48 2B CA              - sub rcx,rdx
victoria3.exe+12112FB - 48 83 E9 08           - sub rcx,08
victoria3.exe+12112FF - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+1211303 - 0F87 60040000         - ja victoria3.exe+1211769
victoria3.exe+1211309 - 48 85 D2              - test rdx,rdx
victoria3.exe+121130C - 74 08                 - je victoria3.exe+1211316
victoria3.exe+121130E - 48 8B CA              - mov rcx,rdx
victoria3.exe+1211311 - E8 1AF0F002           - call victoria3.exe+4120330
victoria3.exe+1211316 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+121131A - C5F81144 24 30        - vmovups [rsp+30],xmm0
victoria3.exe+1211320 - C5FA6F0D 98 4C5F03    - vmovdqu xmm1,xmm0,[victoria3.exe+4805FC0]
victoria3.exe+1211328 - C5FA7F4C 24 40        - vmovdqu [rsp+40],xmm1
victoria3.exe+121132E - C6 44 24 30 00        - mov byte ptr [rsp+30],00
victoria3.exe+1211333 - 48 8D 05 F6C32603     - lea rax,[victoria3.exe+447D730]
victoria3.exe+121133A - 48 89 45 D0           - mov [rbp-30],rax
victoria3.exe+121133E - 48 8D 45 D0           - lea rax,[rbp-30]
victoria3.exe+1211342 - 48 89 45 08           - mov [rbp+08],rax
victoria3.exe+1211346 - 48 63 87 581D0000     - movsxd  rax,dword ptr [rdi+00001D58]
victoria3.exe+121134D - 48 69 C8 A0860100     - imul rcx,rax,000186A0
victoria3.exe+1211354 - 4C 8B 0D A58A6704     - mov r9,[victoria3.exe+5889E00]
victoria3.exe+121135B - 4A 8D 04 39           - lea rax,[rcx+r15]
victoria3.exe+121135F - 49 3B C4              - cmp rax,r12
victoria3.exe+1211362 - 77 23                 - ja victoria3.exe+1211387
victoria3.exe+1211364 - 4B 8D 04 39           - lea rax,[r9+r15]
victoria3.exe+1211368 - 49 3B C4              - cmp rax,r12
victoria3.exe+121136B - 77 1A                 - ja victoria3.exe+1211387
victoria3.exe+121136D - 49 0FAF C9            - imul rcx,r9
victoria3.exe+1211371 - 48 8B C3              - mov rax,rbx
victoria3.exe+1211374 - 48 F7 E9              - imul rcx
victoria3.exe+1211377 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+121137B - 48 8B C2              - mov rax,rdx
victoria3.exe+121137E - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+1211382 - 48 03 D0              - add rdx,rax
victoria3.exe+1211385 - EB 4E                 - jmp victoria3.exe+12113D5
victoria3.exe+1211387 - 4D 8B C1              - mov r8,r9
victoria3.exe+121138A - 4C 3B C9              - cmp r9,rcx
victoria3.exe+121138D - 4C 0F4C C1            - cmovl r8,rcx
victoria3.exe+1211391 - 4C 0F4F C9            - cmovg r9,rcx
victoria3.exe+1211395 - 48 8B C3              - mov rax,rbx
victoria3.exe+1211398 - 49 F7 E8              - imul r8
victoria3.exe+121139B - 48 8B CA              - mov rcx,rdx
victoria3.exe+121139E - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+12113A2 - 48 8B C1              - mov rax,rcx
victoria3.exe+12113A5 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+12113A9 - 48 03 C8              - add rcx,rax
victoria3.exe+12113AC - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+12113B3 - 4C 2B C0              - sub r8,rax
victoria3.exe+12113B6 - 4D 0FAF C1            - imul r8,r9
victoria3.exe+12113BA - 48 8B C3              - mov rax,rbx
victoria3.exe+12113BD - 49 F7 E8              - imul r8
victoria3.exe+12113C0 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+12113C4 - 48 8B C2              - mov rax,rdx
victoria3.exe+12113C7 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+12113CB - 48 03 D0              - add rdx,rax
victoria3.exe+12113CE - 49 0FAF C9            - imul rcx,r9
victoria3.exe+12113D2 - 48 03 D1              - add rdx,rcx
victoria3.exe+12113D5 - 4C 8D 4C 24 30        - lea r9,[rsp+30]
victoria3.exe+12113DA - 4C 8D 45 D0           - lea r8,[rbp-30]
victoria3.exe+12113DE - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+12113E3 - E8 68D39DFF           - call victoria3.exe+BEE750
victoria3.exe+12113E8 - 90                    - nop 
victoria3.exe+12113E9 - 48 8B 4D 08           - mov rcx,[rbp+08]
victoria3.exe+12113ED - 48 85 C9              - test rcx,rcx
victoria3.exe+12113F0 - 74 14                 - je victoria3.exe+1211406
victoria3.exe+12113F2 - 48 8D 45 D0           - lea rax,[rbp-30]
victoria3.exe+12113F6 - 48 3B C8              - cmp rcx,rax
victoria3.exe+12113F9 - 0F95 C2               - setne dl
victoria3.exe+12113FC - 48 8B 01              - mov rax,[rcx]
victoria3.exe+12113FF - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+1211402 - 4C 89 75 08           - mov [rbp+08],r14
victoria3.exe+1211406 - 48 8B 44 24 48        - mov rax,[rsp+48]
victoria3.exe+121140B - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+121140F - 76 35                 - jna victoria3.exe+1211446
victoria3.exe+1211411 - 48 8B 54 24 30        - mov rdx,[rsp+30]
victoria3.exe+1211416 - 48 8B CA              - mov rcx,rdx
victoria3.exe+1211419 - 48 FF C0              - inc rax
victoria3.exe+121141C - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+1211422 - 72 15                 - jb victoria3.exe+1211439
victoria3.exe+1211424 - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+1211428 - 48 2B CA              - sub rcx,rdx
victoria3.exe+121142B - 48 83 E9 08           - sub rcx,08
victoria3.exe+121142F - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+1211433 - 0F87 45030000         - ja victoria3.exe+121177E
victoria3.exe+1211439 - 48 85 D2              - test rdx,rdx
victoria3.exe+121143C - 74 08                 - je victoria3.exe+1211446
victoria3.exe+121143E - 48 8B CA              - mov rcx,rdx
victoria3.exe+1211441 - E8 EAEEF002           - call victoria3.exe+4120330
victoria3.exe+1211446 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+121144A - C5F81144 24 30        - vmovups [rsp+30],xmm0
victoria3.exe+1211450 - C5FA6F0D 68 4B5F03    - vmovdqu xmm1,xmm0,[victoria3.exe+4805FC0]
victoria3.exe+1211458 - C5FA7F4C 24 40        - vmovdqu [rsp+40],xmm1
victoria3.exe+121145E - C6 44 24 30 00        - mov byte ptr [rsp+30],00
victoria3.exe+1211463 - 48 8D 05 FEC22603     - lea rax,[victoria3.exe+447D768]
victoria3.exe+121146A - 48 89 45 10           - mov [rbp+10],rax
victoria3.exe+121146E - 48 8D 45 10           - lea rax,[rbp+10]
victoria3.exe+1211472 - 48 89 45 48           - mov [rbp+48],rax
victoria3.exe+1211476 - 48 8B 87 780B0000     - mov rax,[rdi+00000B78]
victoria3.exe+121147D - 4C 8B 15 B4896704     - mov r10,[victoria3.exe+5889E38]
victoria3.exe+1211484 - 4D 8B DE              - mov r11,r14
victoria3.exe+1211487 - 48 85 C0              - test rax,rax
victoria3.exe+121148A - 4C 0F4F D8            - cmovg r11,rax
victoria3.exe+121148E - 4D 85 D2              - test r10,r10
victoria3.exe+1211491 - 75 0A                 - jne victoria3.exe+121149D
victoria3.exe+1211493 - B9 FFFFFFFF           - mov ecx,FFFFFFFF
victoria3.exe+1211498 - E9 BE000000           - jmp victoria3.exe+121155B
victoria3.exe+121149D - 48 B8 A38D23D6E2530000 - mov rax,000053E2D6238DA3
victoria3.exe+12114A7 - 49 03 C3              - add rax,r11
victoria3.exe+12114AA - 48 B9 461B47ACC5A70000 - mov rcx,0000A7C5AC471B46
victoria3.exe+12114B4 - 48 3B C1              - cmp rax,rcx
victoria3.exe+12114B7 - 77 14                 - ja victoria3.exe+12114CD
victoria3.exe+12114B9 - 49 69 C3 A0860100     - imul rax,r11,000186A0
victoria3.exe+12114C0 - 48 99                 - cqo 
victoria3.exe+12114C2 - 49 F7 FA              - idiv r10
victoria3.exe+12114C5 - 48 8B C8              - mov rcx,rax
victoria3.exe+12114C8 - E9 8E000000           - jmp victoria3.exe+121155B
victoria3.exe+12114CD - 49 8B CA              - mov rcx,r10
victoria3.exe+12114D0 - 48 F7 D9              - neg rcx
victoria3.exe+12114D3 - 49 0F48 CA            - cmovs rcx,r10
victoria3.exe+12114D7 - 48 B8 00E40B5402000000 - mov rax,00000002540BE400
victoria3.exe+12114E1 - 48 3B C8              - cmp rcx,rax
victoria3.exe+12114E4 - 48 8B C3              - mov rax,rbx
victoria3.exe+12114E7 - 7C 21                 - jl victoria3.exe+121150A
victoria3.exe+12114E9 - 49 F7 EA              - imul r10
victoria3.exe+12114EC - 4C 8B C2              - mov r8,rdx
victoria3.exe+12114EF - 49 C1 F8 0E           - sar r8,0E
victoria3.exe+12114F3 - 49 8B C8              - mov rcx,r8
victoria3.exe+12114F6 - 48 C1 E9 3F           - shr rcx,3F
victoria3.exe+12114FA - 4C 03 C1              - add r8,rcx
victoria3.exe+12114FD - 49 8B C3              - mov rax,r11
victoria3.exe+1211500 - 48 99                 - cqo 
victoria3.exe+1211502 - 49 F7 F8              - idiv r8
victoria3.exe+1211505 - 48 8B C8              - mov rcx,rax
victoria3.exe+1211508 - EB 51                 - jmp victoria3.exe+121155B
victoria3.exe+121150A - 49 F7 EB              - imul r11
victoria3.exe+121150D - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+1211511 - 48 8B C2              - mov rax,rdx
victoria3.exe+1211514 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+1211518 - 48 03 D0              - add rdx,rax
victoria3.exe+121151B - 48 69 CA A0860100     - imul rcx,rdx,000186A0
victoria3.exe+1211522 - 48 8B C1              - mov rax,rcx
victoria3.exe+1211525 - 48 99                 - cqo 
victoria3.exe+1211527 - 49 F7 FA              - idiv r10
victoria3.exe+121152A - 4C 8B C2              - mov r8,rdx
victoria3.exe+121152D - 4C 8B C8              - mov r9,rax
victoria3.exe+1211530 - 4C 2B D9              - sub r11,rcx
victoria3.exe+1211533 - 49 69 C3 A0860100     - imul rax,r11,000186A0
victoria3.exe+121153A - 48 99                 - cqo 
victoria3.exe+121153C - 49 F7 FA              - idiv r10
victoria3.exe+121153F - 48 8B C8              - mov rcx,rax
victoria3.exe+1211542 - 49 69 C0 A0860100     - imul rax,r8,000186A0
victoria3.exe+1211549 - 48 99                 - cqo 
victoria3.exe+121154B - 49 F7 FA              - idiv r10
victoria3.exe+121154E - 48 03 C8              - add rcx,rax
victoria3.exe+1211551 - 49 69 C1 A0860100     - imul rax,r9,000186A0
victoria3.exe+1211558 - 48 03 C8              - add rcx,rax
victoria3.exe+121155B - 4C 8D 4C 24 30        - lea r9,[rsp+30]
victoria3.exe+1211560 - 4C 8D 45 10           - lea r8,[rbp+10]
victoria3.exe+1211564 - 48 8B D1              - mov rdx,rcx
victoria3.exe+1211567 - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+121156C - E8 DFD19DFF           - call victoria3.exe+BEE750
victoria3.exe+1211571 - 90                    - nop 
victoria3.exe+1211572 - 48 8B 4D 48           - mov rcx,[rbp+48]
victoria3.exe+1211576 - 48 85 C9              - test rcx,rcx
victoria3.exe+1211579 - 74 14                 - je victoria3.exe+121158F
victoria3.exe+121157B - 48 8D 45 10           - lea rax,[rbp+10]
victoria3.exe+121157F - 48 3B C8              - cmp rcx,rax
victoria3.exe+1211582 - 0F95 C2               - setne dl
victoria3.exe+1211585 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+1211588 - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+121158B - 4C 89 75 48           - mov [rbp+48],r14
victoria3.exe+121158F - 48 8B 44 24 48        - mov rax,[rsp+48]
victoria3.exe+1211594 - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+1211598 - 76 35                 - jna victoria3.exe+12115CF
victoria3.exe+121159A - 48 8B 54 24 30        - mov rdx,[rsp+30]
victoria3.exe+121159F - 48 8B CA              - mov rcx,rdx
victoria3.exe+12115A2 - 48 FF C0              - inc rax
victoria3.exe+12115A5 - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+12115AB - 72 15                 - jb victoria3.exe+12115C2
victoria3.exe+12115AD - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+12115B1 - 48 2B CA              - sub rcx,rdx
victoria3.exe+12115B4 - 48 83 E9 08           - sub rcx,08
victoria3.exe+12115B8 - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+12115BC - 0F87 D1010000         - ja victoria3.exe+1211793
victoria3.exe+12115C2 - 48 85 D2              - test rdx,rdx
victoria3.exe+12115C5 - 74 08                 - je victoria3.exe+12115CF
victoria3.exe+12115C7 - 48 8B CA              - mov rcx,rdx
victoria3.exe+12115CA - E8 61EDF002           - call victoria3.exe+4120330
victoria3.exe+12115CF - 48 8B CF              - mov rcx,rdi
victoria3.exe+12115D2 - E8 89E20100           - call victoria3.exe+122F860
victoria3.exe+12115D7 - 84 C0                 - test al,al
victoria3.exe+12115D9 - 74 7B                 - je victoria3.exe+1211656
victoria3.exe+12115DB - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+12115DF - C5F81144 24 30        - vmovups [rsp+30],xmm0
victoria3.exe+12115E5 - C5FA6F0D D3 495F03    - vmovdqu xmm1,xmm0,[victoria3.exe+4805FC0]
victoria3.exe+12115ED - C5FA7F4C 24 40        - vmovdqu [rsp+40],xmm1
victoria3.exe+12115F3 - C6 44 24 30 00        - mov byte ptr [rsp+30],00
victoria3.exe+12115F8 - 48 8D 05 89C02603     - lea rax,[victoria3.exe+447D688]
victoria3.exe+12115FF - 48 89 45 50           - mov [rbp+50],rax
victoria3.exe+1211603 - 48 8D 45 50           - lea rax,[rbp+50]
victoria3.exe+1211607 - 48 89 85 88000000     - mov [rbp+00000088],rax
victoria3.exe+121160E - 4C 8D 4C 24 30        - lea r9,[rsp+30]
victoria3.exe+1211613 - 4C 8D 45 50           - lea r8,[rbp+50]
victoria3.exe+1211617 - 48 8B 15 DA876704     - mov rdx,[victoria3.exe+5889DF8]
victoria3.exe+121161E - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+1211623 - E8 28D19DFF           - call victoria3.exe+BEE750
victoria3.exe+1211628 - 90                    - nop 
victoria3.exe+1211629 - 48 8B 8D 88000000     - mov rcx,[rbp+00000088]
victoria3.exe+1211630 - 48 85 C9              - test rcx,rcx
victoria3.exe+1211633 - 74 17                 - je victoria3.exe+121164C
victoria3.exe+1211635 - 48 8D 45 50           - lea rax,[rbp+50]
victoria3.exe+1211639 - 48 3B C8              - cmp rcx,rax
victoria3.exe+121163C - 0F95 C2               - setne dl
victoria3.exe+121163F - 48 8B 01              - mov rax,[rcx]
victoria3.exe+1211642 - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+1211645 - 4C 89 B5 88000000     - mov [rbp+00000088],r14
victoria3.exe+121164C - 48 8D 4C 24 30        - lea rcx,[rsp+30]
victoria3.exe+1211651 - E8 8A4140FF           - call victoria3.exe+6157E0
victoria3.exe+1211656 - 48 8B 57 68           - mov rdx,[rdi+68]
victoria3.exe+121165A - 48 81 FA A0860100     - cmp rdx,000186A0
victoria3.exe+1211661 - 0F8D B2000000         - jnl victoria3.exe+1211719
victoria3.exe+1211667 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+121166B - C5F81144 24 30        - vmovups [rsp+30],xmm0
victoria3.exe+1211671 - C5FA6F0D 47 495F03    - vmovdqu xmm1,xmm0,[victoria3.exe+4805FC0]
victoria3.exe+1211679 - C5FA7F4C 24 40        - vmovdqu [rsp+40],xmm1
victoria3.exe+121167F - C6 44 24 30 00        - mov byte ptr [rsp+30],00
victoria3.exe+1211684 - 48 8D 05 35C02603     - lea rax,[victoria3.exe+447D6C0]
victoria3.exe+121168B - 48 89 85 90000000     - mov [rbp+00000090],rax
victoria3.exe+1211692 - 48 8D 85 90000000     - lea rax,[rbp+00000090]
victoria3.exe+1211699 - 48 89 85 C8000000     - mov [rbp+000000C8],rax
victoria3.exe+12116A0 - 4C 8D 4C 24 30        - lea r9,[rsp+30]
victoria3.exe+12116A5 - 4C 8D 85 90000000     - lea r8,[rbp+00000090]
victoria3.exe+12116AC - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+12116B1 - E8 FAD59DFF           - call victoria3.exe+BEECB0
victoria3.exe+12116B6 - 90                    - nop 
victoria3.exe+12116B7 - 48 8B 8D C8000000     - mov rcx,[rbp+000000C8]
victoria3.exe+12116BE - 48 85 C9              - test rcx,rcx
victoria3.exe+12116C1 - 74 1A                 - je victoria3.exe+12116DD
victoria3.exe+12116C3 - 48 8D 85 90000000     - lea rax,[rbp+00000090]
victoria3.exe+12116CA - 48 3B C8              - cmp rcx,rax
victoria3.exe+12116CD - 0F95 C2               - setne dl
victoria3.exe+12116D0 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+12116D3 - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+12116D6 - 4C 89 B5 C8000000     - mov [rbp+000000C8],r14
victoria3.exe+12116DD - 48 8B 44 24 48        - mov rax,[rsp+48]
victoria3.exe+12116E2 - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+12116E6 - 76 31                 - jna victoria3.exe+1211719
victoria3.exe+12116E8 - 48 8B 54 24 30        - mov rdx,[rsp+30]
victoria3.exe+12116ED - 48 8B CA              - mov rcx,rdx
victoria3.exe+12116F0 - 48 FF C0              - inc rax
victoria3.exe+12116F3 - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+12116F9 - 72 11                 - jb victoria3.exe+121170C
victoria3.exe+12116FB - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+12116FF - 48 2B CA              - sub rcx,rdx
victoria3.exe+1211702 - 48 83 E9 08           - sub rcx,08
victoria3.exe+1211706 - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+121170A - 77 48                 - ja victoria3.exe+1211754
victoria3.exe+121170C - 48 85 D2              - test rdx,rdx
victoria3.exe+121170F - 74 08                 - je victoria3.exe+1211719
victoria3.exe+1211711 - 48 8B CA              - mov rcx,rdx
victoria3.exe+1211714 - E8 17ECF002           - call victoria3.exe+4120330
victoria3.exe+1211719 - 48 8B D6              - mov rdx,rsi
victoria3.exe+121171C - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+1211721 - E8 2A0C1B00           - call victoria3.exe+13C2350
victoria3.exe+1211726 - 90                    - nop 
victoria3.exe+1211727 - 48 8D 4D 88           - lea rcx,[rbp-78]
victoria3.exe+121172B - E8 E075A3FF           - call victoria3.exe+C48D10
victoria3.exe+1211730 - 48 8B C6              - mov rax,rsi
victoria3.exe+1211733 - 4C 8D 9C 24 D0010000  - lea r11,[rsp+000001D0]
victoria3.exe+121173B - 49 8B 5B 20           - mov rbx,[r11+20]
victoria3.exe+121173F - 49 8B 73 28           - mov rsi,[r11+28]
victoria3.exe+1211743 - 49 8B 7B 30           - mov rdi,[r11+30]
victoria3.exe+1211747 - 4D 8B 63 38           - mov r12,[r11+38]
victoria3.exe+121174B - 49 8B E3              - mov rsp,r11
victoria3.exe+121174E - 41 5F                 - pop r15
victoria3.exe+1211750 - 41 5E                 - pop r14
victoria3.exe+1211752 - 5D                    - pop rbp
victoria3.exe+1211753 - C3                    - ret 


# 7FF7EB07D5C9
victoria3.exe+11FD534 - 4C 8B AC 24 60030000  - mov r13,[rsp+00000360]
victoria3.exe+11FD53C - 4C 89 6C 24 38        - mov [rsp+38],r13
victoria3.exe+11FD541 - 48 8B 84 24 58030000  - mov rax,[rsp+00000358]
victoria3.exe+11FD549 - 48 89 44 24 30        - mov [rsp+30],rax
victoria3.exe+11FD54E - 48 8B AC 24 50030000  - mov rbp,[rsp+00000350]
victoria3.exe+11FD556 - 48 89 6C 24 28        - mov [rsp+28],rbp
victoria3.exe+11FD55B - 48 8B 84 24 48030000  - mov rax,[rsp+00000348]
victoria3.exe+11FD563 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+11FD568 - 4C 8B CB              - mov r9,rbx
victoria3.exe+11FD56B - 4C 8B 84 24 38030000  - mov r8,[rsp+00000338]
victoria3.exe+11FD573 - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+11FD578 - 48 8B CF              - mov rcx,rdi
victoria3.exe+11FD57B - E8 F0FDFFFF           - call victoria3.exe+11FD370
victoria3.exe+11FD580 - 90                    - nop 
victoria3.exe+11FD581 - 48 8B 8F F8000000     - mov rcx,[rdi+000000F8]
victoria3.exe+11FD588 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+11FD58B - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD58D - 84 C0                 - test al,al
victoria3.exe+11FD58F - 74 11                 - je victoria3.exe+11FD5A2
victoria3.exe+11FD591 - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+11FD596 - 48 8D 8F F8000000     - lea rcx,[rdi+000000F8]
victoria3.exe+11FD59D - E8 FEE7FFFF           - call victoria3.exe+11FBDA0
victoria3.exe+11FD5A2 - 48 8B 0E              - mov rcx,[rsi]
victoria3.exe+11FD5A5 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+11FD5A8 - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD5AA - 84 C0                 - test al,al
victoria3.exe+11FD5AC - 74 0D                 - je victoria3.exe+11FD5BB
victoria3.exe+11FD5AE - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+11FD5B3 - 48 8B CE              - mov rcx,rsi
victoria3.exe+11FD5B6 - E8 E5E7FFFF           - call victoria3.exe+11FBDA0
victoria3.exe+11FD5BB - 41 8B 86 5C1D0000     - mov eax,[r14+00001D5C]
victoria3.exe+11FD5C2 - 89 84 24 30030000     - mov [rsp+00000330],eax
victoria3.exe+11FD5C9 - 41 8B 86 581D0000     - mov eax,[r14+00001D58]
victoria3.exe+11FD5D0 - 89 44 24 50           - mov [rsp+50],eax
victoria3.exe+11FD5D4 - 48 8B 8F F8000000     - mov rcx,[rdi+000000F8]
victoria3.exe+11FD5DB - 48 8B 01              - mov rax,[rcx]
victoria3.exe+11FD5DE - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD5E0 - BB 60000000           - mov ebx,00000060
victoria3.exe+11FD5E5 - 48 BA 66E6096A01000000 - mov rdx,000000016A09E666
victoria3.exe+11FD5EF - 41 B8 33F304B5        - mov r8d,B504F333
victoria3.exe+11FD5F5 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+11FD5FF - 84 C0                 - test al,al
victoria3.exe+11FD601 - 0F84 53020000         - je victoria3.exe+11FD85A
victoria3.exe+11FD607 - 48 8B 1D 1AD36804     - mov rbx,[victoria3.exe+588A928]
victoria3.exe+11FD60E - 83 3D 2B1FEE03 00     - cmp dword ptr [victoria3.exe+50DF540],00
victoria3.exe+11FD615 - 75 32                 - jne victoria3.exe+11FD649
victoria3.exe+11FD617 - 48 8D 05 68486F04     - lea rax,[victoria3.exe+58F1E86]
victoria3.exe+11FD61E - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+11FD623 - 48 8D 0D A6E51D03     - lea rcx,[victoria3.exe+43DBBD0]
victoria3.exe+11FD62A - E8 91518A02           - call victoria3.exe+3AA27C0
victoria3.exe+11FD62F - 48 BA 66E6096A01000000 - mov rdx,000000016A09E666
victoria3.exe+11FD639 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+11FD643 - 41 B8 33F304B5        - mov r8d,B504F333
victoria3.exe+11FD649 - 48 8B 05 00B46B04     - mov rax,[victoria3.exe+58B8A50]
victoria3.exe+11FD650 - 48 8B 88 08060000     - mov rcx,[rax+00000608]
victoria3.exe+11FD657 - 80 B9 48010000 00     - cmp byte ptr [rcx+00000148],00
victoria3.exe+11FD65E - 0F84 8A000000         - je victoria3.exe+11FD6EE
victoria3.exe+11FD664 - 4C 8B 0D 85D26804     - mov r9,[victoria3.exe+588A8F0]
victoria3.exe+11FD66B - 4A 8D 04 03           - lea rax,[rbx+r8]
victoria3.exe+11FD66F - 48 3B C2              - cmp rax,rdx
victoria3.exe+11FD672 - 77 26                 - ja victoria3.exe+11FD69A
victoria3.exe+11FD674 - 4B 8D 04 01           - lea rax,[r9+r8]
victoria3.exe+11FD678 - 48 3B C2              - cmp rax,rdx
victoria3.exe+11FD67B - 77 1D                 - ja victoria3.exe+11FD69A
victoria3.exe+11FD67D - 49 0FAF D9            - imul rbx,r9
victoria3.exe+11FD681 - 49 8B C2              - mov rax,r10
victoria3.exe+11FD684 - 48 F7 EB              - imul rbx
victoria3.exe+11FD687 - 48 8B DA              - mov rbx,rdx
victoria3.exe+11FD68A - 48 C1 FB 0E           - sar rbx,0E
victoria3.exe+11FD68E - 48 8B C3              - mov rax,rbx
victoria3.exe+11FD691 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD695 - 48 03 D8              - add rbx,rax
victoria3.exe+11FD698 - EB 54                 - jmp victoria3.exe+11FD6EE
victoria3.exe+11FD69A - 4D 8B C1              - mov r8,r9
victoria3.exe+11FD69D - 4C 3B CB              - cmp r9,rbx
victoria3.exe+11FD6A0 - 4C 0F4C C3            - cmovl r8,rbx
victoria3.exe+11FD6A4 - 4C 0F4F CB            - cmovg r9,rbx
victoria3.exe+11FD6A8 - 49 8B C2              - mov rax,r10
victoria3.exe+11FD6AB - 49 F7 E8              - imul r8
victoria3.exe+11FD6AE - 48 8B CA              - mov rcx,rdx
victoria3.exe+11FD6B1 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+11FD6B5 - 48 8B C1              - mov rax,rcx
victoria3.exe+11FD6B8 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD6BC - 48 03 C8              - add rcx,rax
victoria3.exe+11FD6BF - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+11FD6C6 - 4C 2B C0              - sub r8,rax
victoria3.exe+11FD6C9 - 4D 0FAF C1            - imul r8,r9
victoria3.exe+11FD6CD - 49 8B C2              - mov rax,r10
victoria3.exe+11FD6D0 - 49 F7 E8              - imul r8
victoria3.exe+11FD6D3 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FD6D7 - 48 8B DA              - mov rbx,rdx
victoria3.exe+11FD6DA - 48 C1 EB 3F           - shr rbx,3F
victoria3.exe+11FD6DE - 48 03 DA              - add rbx,rdx
victoria3.exe+11FD6E1 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+11FD6E5 - 48 03 D9              - add rbx,rcx
victoria3.exe+11FD6E8 - 41 B8 33F304B5        - mov r8d,B504F333
victoria3.exe+11FD6EE - 4C 8B 8F 18010000     - mov r9,[rdi+00000118]
victoria3.exe+11FD6F5 - 44 8B 9C 24 30030000  - mov r11d,[rsp+00000330]
victoria3.exe+11FD6FD - 44 3B 5C 24 50        - cmp r11d,[rsp+50]
victoria3.exe+11FD702 - 0F8C C0000000         - jl victoria3.exe+11FD7C8
victoria3.exe+11FD708 - 48 8B 87 F8000000     - mov rax,[rdi+000000F8]
victoria3.exe+11FD70F - 48 39 87 B0000000     - cmp [rdi+000000B0],rax
victoria3.exe+11FD716 - 0F84 AC000000         - je victoria3.exe+11FD7C8
victoria3.exe+11FD71C - 4C 8B 15 EDD16804     - mov r10,[victoria3.exe+588A910]
victoria3.exe+11FD723 - 4B 8D 04 01           - lea rax,[r9+r8]
victoria3.exe+11FD727 - 48 B9 66E6096A01000000 - mov rcx,000000016A09E666
victoria3.exe+11FD731 - 48 3B C1              - cmp rax,rcx
victoria3.exe+11FD734 - 77 2D                 - ja victoria3.exe+11FD763
victoria3.exe+11FD736 - 4B 8D 04 02           - lea rax,[r10+r8]
victoria3.exe+11FD73A - 48 3B C1              - cmp rax,rcx
victoria3.exe+11FD73D - 77 24                 - ja victoria3.exe+11FD763
victoria3.exe+11FD73F - 49 8B C9              - mov rcx,r9
victoria3.exe+11FD742 - 49 0FAF CA            - imul rcx,r10
victoria3.exe+11FD746 - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+11FD750 - 48 F7 E9              - imul rcx
victoria3.exe+11FD753 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FD757 - 48 8B C2              - mov rax,rdx
victoria3.exe+11FD75A - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD75E - 48 03 D0              - add rdx,rax
victoria3.exe+11FD761 - EB 5C                 - jmp victoria3.exe+11FD7BF
victoria3.exe+11FD763 - 4D 8B C2              - mov r8,r10
victoria3.exe+11FD766 - 4D 3B D1              - cmp r10,r9
victoria3.exe+11FD769 - 4D 0F4C C1            - cmovl r8,r9
victoria3.exe+11FD76D - 4D 0F4F D1            - cmovg r10,r9
victoria3.exe+11FD771 - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+11FD77B - 49 F7 E8              - imul r8
victoria3.exe+11FD77E - 48 8B CA              - mov rcx,rdx
victoria3.exe+11FD781 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+11FD785 - 48 8B C1              - mov rax,rcx
victoria3.exe+11FD788 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD78C - 48 03 C8              - add rcx,rax
victoria3.exe+11FD78F - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+11FD796 - 4C 2B C0              - sub r8,rax
victoria3.exe+11FD799 - 4D 0FAF C2            - imul r8,r10
victoria3.exe+11FD79D - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+11FD7A7 - 49 F7 E8              - imul r8
victoria3.exe+11FD7AA - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FD7AE - 48 8B C2              - mov rax,rdx
victoria3.exe+11FD7B1 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD7B5 - 48 03 D0              - add rdx,rax
victoria3.exe+11FD7B8 - 49 0FAF CA            - imul rcx,r10
victoria3.exe+11FD7BC - 48 03 D1              - add rdx,rcx
victoria3.exe+11FD7BF - 48 3B 97 D0000000     - cmp rdx,[rdi+000000D0]
victoria3.exe+11FD7C6 - 7C 09                 - jl victoria3.exe+11FD7D1
victoria3.exe+11FD7C8 - 4C 3B CB              - cmp r9,rbx
victoria3.exe+11FD7CB - 0F8D 82000000         - jnl victoria3.exe+11FD853
victoria3.exe+11FD7D1 - 0FB6 97 00010000      - movzx edx,byte ptr [rdi+00000100]
victoria3.exe+11FD7D8 - 4D 8B D5              - mov r10,r13
victoria3.exe+11FD7DB - 84 D2                 - test dl,dl
victoria3.exe+11FD7DD - 4C 0F44 94 24 58030000  - cmove r10,[rsp+00000358]
victoria3.exe+11FD7E6 - 4C 8B CD              - mov r9,rbp
victoria3.exe+11FD7E9 - 4C 0F44 8C 24 48030000  - cmove r9,[rsp+00000348]
victoria3.exe+11FD7F2 - 48 8B 8C 24 40030000  - mov rcx,[rsp+00000340]
victoria3.exe+11FD7FA - 48 0F44 8C 24 38030000  - cmove rcx,[rsp+00000338]
victoria3.exe+11FD803 - BB 60000000           - mov ebx,00000060
victoria3.exe+11FD808 - 8B C3                 - mov eax,ebx
victoria3.exe+11FD80A - 41 B8 10000000        - mov r8d,00000010
victoria3.exe+11FD810 - 41 0F45 C0            - cmovne eax,r8d
victoria3.exe+11FD814 - 48 03 C7              - add rax,rdi
victoria3.exe+11FD817 - 4C 89 54 24 40        - mov [rsp+40],r10
victoria3.exe+11FD81C - 4C 89 4C 24 38        - mov [rsp+38],r9
victoria3.exe+11FD821 - 48 89 4C 24 30        - mov [rsp+30],rcx
victoria3.exe+11FD826 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+11FD82B - 49 8D 86 881D0000     - lea rax,[r14+00001D88]
victoria3.exe+11FD832 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+11FD837 - 4C 8B 4E 40           - mov r9,[rsi+40]
victoria3.exe+11FD83B - 4C 8B 87 30010000     - mov r8,[rdi+00000130]
victoria3.exe+11FD842 - 48 8B 8F F8000000     - mov rcx,[rdi+000000F8]
victoria3.exe+11FD849 - E8 D2D6FFFF           - call victoria3.exe+11FAF20
victoria3.exe+11FD84E - 40 B5 01              - mov bpl,01
victoria3.exe+11FD851 - EB 27                 - jmp victoria3.exe+11FD87A
victoria3.exe+11FD853 - BB 60000000           - mov ebx,00000060
victoria3.exe+11FD858 - EB 08                 - jmp victoria3.exe+11FD862
victoria3.exe+11FD85A - 44 8B 9C 24 30030000  - mov r11d,[rsp+00000330]
victoria3.exe+11FD862 - 44 3B 5C 24 50        - cmp r11d,[rsp+50]
victoria3.exe+11FD867 - 7C 0E                 - jl victoria3.exe+11FD877
victoria3.exe+11FD869 - C7 47 04 00000000     - mov [rdi+04],00000000
victoria3.exe+11FD870 - 32 DB                 - xor bl,bl
victoria3.exe+11FD872 - E9 E7010000           - jmp victoria3.exe+11FDA5E
victoria3.exe+11FD877 - 40 32 ED              - xor bpl,bpl
victoria3.exe+11FD87A - 48 8B CE              - mov rcx,rsi
victoria3.exe+11FD87D - E8 FEE3FFFF           - call victoria3.exe+11FBC80
victoria3.exe+11FD882 - 84 C0                 - test al,al
victoria3.exe+11FD884 - 0F84 E6010000         - je victoria3.exe+11FDA70
victoria3.exe+11FD88A - 0FB6 AF B8000000      - movzx ebp,byte ptr [rdi+000000B8]
victoria3.exe+11FD891 - 40 84 ED              - test bpl,bpl
victoria3.exe+11FD894 - 4C 0F44 AC 24 58030000  - cmove r13,[rsp+00000358]
victoria3.exe+11FD89D - 48 8B 84 24 50030000  - mov rax,[rsp+00000350]
victoria3.exe+11FD8A5 - 48 0F44 84 24 48030000  - cmove rax,[rsp+00000348]
victoria3.exe+11FD8AE - 48 89 84 24 50030000  - mov [rsp+00000350],rax
victoria3.exe+11FD8B6 - 48 8B 84 24 40030000  - mov rax,[rsp+00000340]
victoria3.exe+11FD8BE - 48 0F44 84 24 38030000  - cmove rax,[rsp+00000338]
victoria3.exe+11FD8C7 - 48 89 84 24 40030000  - mov [rsp+00000340],rax
victoria3.exe+11FD8CF - B8 10000000           - mov eax,00000010
victoria3.exe+11FD8D4 - 48 0F45 D8            - cmovne rbx,rax
victoria3.exe+11FD8D8 - 48 03 DF              - add rbx,rdi
victoria3.exe+11FD8DB - 48 89 9C 24 30030000  - mov [rsp+00000330],rbx
victoria3.exe+11FD8E3 - 48 8B B7 F0000000     - mov rsi,[rdi+000000F0]
victoria3.exe+11FD8EA - 48 8B 9F E8000000     - mov rbx,[rdi+000000E8]
victoria3.exe+11FD8F1 - 4C 8B BF B0000000     - mov r15,[rdi+000000B0]
victoria3.exe+11FD8F8 - 49 8B 07              - mov rax,[r15]
victoria3.exe+11FD8FB - 49 8B CF              - mov rcx,r15
victoria3.exe+11FD8FE - FF 10                 - call qword ptr [rax]
victoria3.exe+11FD900 - 84 C0                 - test al,al
victoria3.exe+11FD902 - 0F84 19010000         - je victoria3.exe+11FDA21
victoria3.exe+11FD908 - 41 0FB6 47 40         - movzx eax,byte ptr [r15+40]
victoria3.exe+11FD90D - A8 02                 - test al,02
victoria3.exe+11FD90F - 0F84 0C010000         - je victoria3.exe+11FDA21
victoria3.exe+11FD915 - A8 01                 - test al,01
victoria3.exe+11FD917 - 0F85 04010000         - jne victoria3.exe+11FDA21
victoria3.exe+11FD91D - B8 A0860100           - mov eax,000186A0
victoria3.exe+11FD922 - 49 C7 C0 6079FEFF     - mov r8,FFFFFFFFFFFE7960
victoria3.exe+11FD929 - 40 80 FD 01           - cmp bpl,01
victoria3.exe+11FD92D - 4C 0F44 C0            - cmove r8,rax
victoria3.exe+11FD931 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FD934 - 49 8D 8E 881D0000     - lea rcx,[r14+00001D88]
victoria3.exe+11FD93B - E8 30A0E2FF           - call victoria3.exe+1027970
victoria3.exe+11FD940 - 4C 8B C3              - mov r8,rbx
victoria3.exe+11FD943 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FD946 - 48 8B 8C 24 30030000  - mov rcx,[rsp+00000330]
victoria3.exe+11FD94E - E8 1DA0E2FF           - call victoria3.exe+1027970
victoria3.exe+11FD953 - 4C 8B C3              - mov r8,rbx
victoria3.exe+11FD956 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FD959 - 48 8B 8C 24 40030000  - mov rcx,[rsp+00000340]
victoria3.exe+11FD961 - E8 0AA0E2FF           - call victoria3.exe+1027970
victoria3.exe+11FD966 - 4C 8B C3              - mov r8,rbx
victoria3.exe+11FD969 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FD96C - 48 8B 8C 24 50030000  - mov rcx,[rsp+00000350]
victoria3.exe+11FD974 - E8 F79FE2FF           - call victoria3.exe+1027970
victoria3.exe+11FD979 - BA 33F304B5           - mov edx,B504F333
victoria3.exe+11FD97E - 48 8D 0C 13           - lea rcx,[rbx+rdx]
victoria3.exe+11FD982 - 48 B8 66E6096A01000000 - mov rax,000000016A09E666
victoria3.exe+11FD98C - 48 3B C8              - cmp rcx,rax
victoria3.exe+11FD98F - 77 2A                 - ja victoria3.exe+11FD9BB
victoria3.exe+11FD991 - 48 8D 0C 16           - lea rcx,[rsi+rdx]
victoria3.exe+11FD995 - 48 3B C8              - cmp rcx,rax
victoria3.exe+11FD998 - 77 21                 - ja victoria3.exe+11FD9BB
victoria3.exe+11FD99A - 48 0FAF F3            - imul rsi,rbx
victoria3.exe+11FD99E - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+11FD9A8 - 48 F7 EE              - imul rsi
victoria3.exe+11FD9AB - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FD9AF - 48 8B C2              - mov rax,rdx
victoria3.exe+11FD9B2 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD9B6 - 48 03 D0              - add rdx,rax
victoria3.exe+11FD9B9 - EB 58                 - jmp victoria3.exe+11FDA13
victoria3.exe+11FD9BB - 48 8B CE              - mov rcx,rsi
victoria3.exe+11FD9BE - 48 3B F3              - cmp rsi,rbx
victoria3.exe+11FD9C1 - 48 0F4C CB            - cmovl rcx,rbx
victoria3.exe+11FD9C5 - 48 0F4F F3            - cmovg rsi,rbx
victoria3.exe+11FD9C9 - 49 B9 09E1D1C6116BF129 - mov r9,29F16B11C6D1E109
victoria3.exe+11FD9D3 - 49 8B C1              - mov rax,r9
victoria3.exe+11FD9D6 - 48 F7 E9              - imul rcx
victoria3.exe+11FD9D9 - 4C 8B C2              - mov r8,rdx
victoria3.exe+11FD9DC - 49 C1 F8 0E           - sar r8,0E
victoria3.exe+11FD9E0 - 49 8B C0              - mov rax,r8
victoria3.exe+11FD9E3 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FD9E7 - 4C 03 C0              - add r8,rax
victoria3.exe+11FD9EA - 49 69 C0 A0860100     - imul rax,r8,000186A0
victoria3.exe+11FD9F1 - 48 2B C8              - sub rcx,rax
victoria3.exe+11FD9F4 - 48 0FAF CE            - imul rcx,rsi
victoria3.exe+11FD9F8 - 49 8B C1              - mov rax,r9
victoria3.exe+11FD9FB - 48 F7 E9              - imul rcx
victoria3.exe+11FD9FE - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FDA02 - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDA05 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDA09 - 48 03 D0              - add rdx,rax
victoria3.exe+11FDA0C - 4C 0FAF C6            - imul r8,rsi
victoria3.exe+11FDA10 - 49 03 D0              - add rdx,r8
victoria3.exe+11FDA13 - 4C 8B C2              - mov r8,rdx
victoria3.exe+11FDA16 - 49 8B D7              - mov rdx,r15
victoria3.exe+11FDA19 - 49 8B CD              - mov rcx,r13
victoria3.exe+11FDA1C - E8 4F9FE2FF           - call victoria3.exe+1027970
victoria3.exe+11FDA21 - 45 84 E4              - test r12b,r12b
victoria3.exe+11FDA24 - 75 0F                 - jne victoria3.exe+11FDA35
victoria3.exe+11FDA26 - 48 8B 97 B0000000     - mov rdx,[rdi+000000B0]
victoria3.exe+11FDA2D - 49 8B CE              - mov rcx,r14
victoria3.exe+11FDA30 - E8 9BE40200           - call victoria3.exe+122BED0
victoria3.exe+11FDA35 - FF 4F 04              - dec [rdi+04]
victoria3.exe+11FDA38 - 49 8B CE              - mov rcx,r14
victoria3.exe+11FDA3B - E8 10E50200           - call victoria3.exe+122BF50
victoria3.exe+11FDA40 - 48 C7 84 24 30030000 03000000 - mov qword ptr [rsp+00000330],00000003
victoria3.exe+11FDA4C - 49 8B D6              - mov rdx,r14
victoria3.exe+11FDA4F - 48 8D 8C 24 30030000  - lea rcx,[rsp+00000330]
victoria3.exe+11FDA57 - E8 B489A4FF           - call victoria3.exe+C46410
victoria3.exe+11FDA5C - B3 01                 - mov bl,01
victoria3.exe+11FDA5E - 48 8D 4C 24 60        - lea rcx,[rsp+60]
victoria3.exe+11FDA63 - E8 485DC3FF           - call victoria3.exe+E337B0
victoria3.exe+11FDA68 - 0FB6 C3               - movzx eax,bl
victoria3.exe+11FDA6B - E9 B0FAFFFF           - jmp victoria3.exe+11FD520
victoria3.exe+11FDA70 - 40 84 ED              - test bpl,bpl
victoria3.exe+11FDA73 - 75 C0                 - jne victoria3.exe+11FDA35
victoria3.exe+11FDA75 - 45 84 E4              - test r12b,r12b
victoria3.exe+11FDA78 - 74 07                 - je victoria3.exe+11FDA81
victoria3.exe+11FDA7A - FF 4F 04              - dec [rdi+04]
victoria3.exe+11FDA7D - 32 DB                 - xor bl,bl
victoria3.exe+11FDA7F - EB DD                 - jmp victoria3.exe+11FDA5E
victoria3.exe+11FDA81 - 48 63 07              - movsxd  rax,dword ptr [rdi]
victoria3.exe+11FDA84 - 48 69 C8 A0860100     - imul rcx,rax,000186A0
victoria3.exe+11FDA8B - 4C 8B 0D 46CE6804     - mov r9,[victoria3.exe+588A8D8]
victoria3.exe+11FDA92 - BA 33F304B5           - mov edx,B504F333
victoria3.exe+11FDA97 - 48 8D 04 11           - lea rax,[rcx+rdx]
victoria3.exe+11FDA9B - 49 B8 66E6096A01000000 - mov r8,000000016A09E666
victoria3.exe+11FDAA5 - 49 3B C0              - cmp rax,r8
victoria3.exe+11FDAA8 - 77 2D                 - ja victoria3.exe+11FDAD7
victoria3.exe+11FDAAA - 49 8D 04 11           - lea rax,[r9+rdx]
victoria3.exe+11FDAAE - 49 3B C0              - cmp rax,r8
victoria3.exe+11FDAB1 - 77 24                 - ja victoria3.exe+11FDAD7
victoria3.exe+11FDAB3 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+11FDAB7 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+11FDAC1 - 49 8B C2              - mov rax,r10
victoria3.exe+11FDAC4 - 48 F7 E9              - imul rcx
victoria3.exe+11FDAC7 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FDACB - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDACE - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDAD2 - 48 03 D0              - add rdx,rax
victoria3.exe+11FDAD5 - EB 58                 - jmp victoria3.exe+11FDB2F
victoria3.exe+11FDAD7 - 4D 8B C1              - mov r8,r9
victoria3.exe+11FDADA - 4C 3B C9              - cmp r9,rcx
victoria3.exe+11FDADD - 4C 0F4C C1            - cmovl r8,rcx
victoria3.exe+11FDAE1 - 4C 0F4F C9            - cmovg r9,rcx
victoria3.exe+11FDAE5 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+11FDAEF - 49 8B C2              - mov rax,r10
victoria3.exe+11FDAF2 - 49 F7 E8              - imul r8
victoria3.exe+11FDAF5 - 48 8B CA              - mov rcx,rdx
victoria3.exe+11FDAF8 - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+11FDAFC - 48 8B C1              - mov rax,rcx
victoria3.exe+11FDAFF - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDB03 - 48 03 C8              - add rcx,rax
victoria3.exe+11FDB06 - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+11FDB0D - 4C 2B C0              - sub r8,rax
victoria3.exe+11FDB10 - 4D 0FAF C1            - imul r8,r9
victoria3.exe+11FDB14 - 49 8B C2              - mov rax,r10
victoria3.exe+11FDB17 - 49 F7 E8              - imul r8
victoria3.exe+11FDB1A - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FDB1E - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDB21 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDB25 - 48 03 D0              - add rdx,rax
victoria3.exe+11FDB28 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+11FDB2C - 48 03 D1              - add rdx,rcx
victoria3.exe+11FDB2F - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDB32 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDB36 - 84 C0                 - test al,al
victoria3.exe+11FDB38 - 49 8B C2              - mov rax,r10
victoria3.exe+11FDB3B - 48 8D 8A B03CFFFF     - lea rcx,[rdx-0000C350]
victoria3.exe+11FDB42 - 75 07                 - jne victoria3.exe+11FDB4B
victoria3.exe+11FDB44 - 48 8D 8A 50C30000     - lea rcx,[rdx+0000C350]
victoria3.exe+11FDB4B - 48 F7 E9              - imul rcx
victoria3.exe+11FDB4E - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+11FDB52 - 48 8B C2              - mov rax,rdx
victoria3.exe+11FDB55 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+11FDB59 - 48 03 D0              - add rdx,rax
victoria3.exe+11FDB5C - B9 01000000           - mov ecx,00000001
victoria3.exe+11FDB61 - 3B D1                 - cmp edx,ecx
victoria3.exe+11FDB63 - 0F4F CA               - cmovg ecx,edx
victoria3.exe+11FDB66 - 29 4F 04              - sub [rdi+04],ecx
victoria3.exe+11FDB69 - 32 DB                 - xor bl,bl
victoria3.exe+11FDB6B - E9 EEFEFFFF           - jmp victoria3.exe+11FDA5E
victoria3.exe+11FDB70 - CC                    - int 3 
victoria3.exe+11FDB71 - CC                    - int 3 
victoria3.exe+11FDB72 - CC                    - int 3 
victoria3.exe+11FDB73 - CC                    - int 3 
victoria3.exe+11FDB74 - CC                    - int 3 
victoria3.exe+11FDB75 - CC                    - int 3 
victoria3.exe+11FDB76 - CC                    - int 3 
victoria3.exe+11FDB77 - CC                    - int 3 
victoria3.exe+11FDB78 - CC                    - int 3 
victoria3.exe+11FDB79 - CC                    - int 3 
victoria3.exe+11FDB7A - CC                    - int 3 
victoria3.exe+11FDB7B - CC                    - int 3 
victoria3.exe+11FDB7C - CC                    - int 3 
victoria3.exe+11FDB7D - CC                    - int 3 
victoria3.exe+11FDB7E - CC                    - int 3 
victoria3.exe+11FDB7F - CC                    - int 3 


# 7FF7EACB7334
victoria3.exe+E37126 - CC                    - int 3 
victoria3.exe+E37127 - CC                    - int 3 
victoria3.exe+E37128 - CC                    - int 3 
victoria3.exe+E37129 - CC                    - int 3 
victoria3.exe+E3712A - CC                    - int 3 
victoria3.exe+E3712B - CC                    - int 3 
victoria3.exe+E3712C - CC                    - int 3 
victoria3.exe+E3712D - CC                    - int 3 
victoria3.exe+E3712E - CC                    - int 3 
victoria3.exe+E3712F - CC                    - int 3 
victoria3.exe+E37130 - 40 53                 - push rbx
victoria3.exe+E37132 - 55                    - push rbp
victoria3.exe+E37133 - 56                    - push rsi
victoria3.exe+E37134 - 57                    - push rdi
victoria3.exe+E37135 - 41 54                 - push r12
victoria3.exe+E37137 - 41 56                 - push r14
victoria3.exe+E37139 - 41 57                 - push r15
victoria3.exe+E3713B - 48 83 EC 50           - sub rsp,50
victoria3.exe+E3713F - 48 8B F1              - mov rsi,rcx
victoria3.exe+E37142 - 48 8B 89 F0000000     - mov rcx,[rcx+000000F0]
victoria3.exe+E37149 - 0FB6 41 40            - movzx eax,byte ptr [rcx+40]
victoria3.exe+E3714D - C0 E8 02              - shr al,02
victoria3.exe+E37150 - A8 01                 - test al,01
victoria3.exe+E37152 - 0F84 66040000         - je victoria3.exe+E375BE
victoria3.exe+E37158 - 48 8B 81 08010000     - mov rax,[rcx+00000108]
victoria3.exe+E3715F - 0FB6 50 40            - movzx edx,byte ptr [rax+40]
victoria3.exe+E37163 - C0 EA 04              - shr dl,04
victoria3.exe+E37166 - F6 C2 01              - test dl,01
victoria3.exe+E37169 - 0F85 4F040000         - jne victoria3.exe+E375BE
victoria3.exe+E3716F - 48 8B CE              - mov rcx,rsi
victoria3.exe+E37172 - E8 D9DBFFFF           - call victoria3.exe+E34D50
victoria3.exe+E37177 - 84 C0                 - test al,al
victoria3.exe+E37179 - 0F85 3F040000         - jne victoria3.exe+E375BE
victoria3.exe+E3717F - 48 8B 86 28010000     - mov rax,[rsi+00000128]
victoria3.exe+E37186 - 48 39 86 20010000     - cmp [rsi+00000120],rax
victoria3.exe+E3718D - 0F8F 2B040000         - jg victoria3.exe+E375BE
victoria3.exe+E37193 - 48 8B CE              - mov rcx,rsi
victoria3.exe+E37196 - E8 6552FFFF           - call victoria3.exe+E2C400
victoria3.exe+E3719B - 83 F8 01              - cmp eax,01
victoria3.exe+E3719E - 0F8C 1A040000         - jl victoria3.exe+E375BE
victoria3.exe+E371A4 - 48 8B CE              - mov rcx,rsi
victoria3.exe+E371A7 - E8 24040000           - call victoria3.exe+E375D0
victoria3.exe+E371AC - 84 C0                 - test al,al
victoria3.exe+E371AE - 0F84 0A040000         - je victoria3.exe+E375BE
victoria3.exe+E371B4 - 48 8B 9E 30020000     - mov rbx,[rsi+00000230]
victoria3.exe+E371BB - 48 63 86 3C020000     - movsxd  rax,dword ptr [rsi+0000023C]
victoria3.exe+E371C2 - 4C 8D 34 83           - lea r14,[rbx+rax*4]
victoria3.exe+E371C6 - 49 3B DE              - cmp rbx,r14
victoria3.exe+E371C9 - 0F84 EF030000         - je victoria3.exe+E375BE
victoria3.exe+E371CF - 4C 8D 3D F2AA5903     - lea r15,[victoria3.exe+43D1CC8]
victoria3.exe+E371D6 - 4C 8D 25 6F0EA504     - lea r12,[victoria3.exe+588804C]
victoria3.exe+E371DD - 0F1F 00               - nop dword ptr [rax]
victoria3.exe+E371E0 - 8B 03                 - mov eax,[rbx]
victoria3.exe+E371E2 - 48 8D 8C 24 90000000  - lea rcx,[rsp+00000090]
victoria3.exe+E371EA - 89 84 24 90000000     - mov [rsp+00000090],eax
victoria3.exe+E371F1 - E8 AA31E1FF           - call victoria3.exe+C4A3A0
victoria3.exe+E371F6 - 48 8B F8              - mov rdi,rax
victoria3.exe+E371F9 - 0FB6 40 30            - movzx eax,byte ptr [rax+30]
victoria3.exe+E371FD - 3C 03                 - cmp al,03
victoria3.exe+E371FF - 74 08                 - je victoria3.exe+E37209
victoria3.exe+E37201 - 3C 02                 - cmp al,02
victoria3.exe+E37203 - 0F84 E2000000         - je victoria3.exe+E372EB
victoria3.exe+E37209 - 48 8D 94 24 98000000  - lea rdx,[rsp+00000098]
victoria3.exe+E37211 - 48 8D 4F 20           - lea rcx,[rdi+20]
victoria3.exe+E37215 - E8 46470100           - call victoria3.exe+E4B960
victoria3.exe+E3721A - 48 8B C8              - mov rcx,rax
victoria3.exe+E3721D - E8 8E33E1FF           - call victoria3.exe+C4A5B0
victoria3.exe+E37222 - 83 78 18 FF           - cmp dword ptr [rax+18],-01
victoria3.exe+E37226 - 0F84 D1000000         - je victoria3.exe+E372FD
victoria3.exe+E3722C - 80 7F 30 02           - cmp byte ptr [rdi+30],02
victoria3.exe+E37230 - 75 07                 - jne victoria3.exe+E37239
victoria3.exe+E37232 - BA FFFFFFFF           - mov edx,FFFFFFFF
victoria3.exe+E37237 - EB 1C                 - jmp victoria3.exe+E37255
victoria3.exe+E37239 - 48 8D 94 24 A0000000  - lea rdx,[rsp+000000A0]
victoria3.exe+E37241 - 48 8D 4F 20           - lea rcx,[rdi+20]
victoria3.exe+E37245 - E8 16470100           - call victoria3.exe+E4B960
victoria3.exe+E3724A - 48 8B C8              - mov rcx,rax
victoria3.exe+E3724D - E8 5E33E1FF           - call victoria3.exe+C4A5B0
victoria3.exe+E37252 - 8B 50 18              - mov edx,[rax+18]
victoria3.exe+E37255 - 4C 8B 05 ECA9AB04     - mov r8,[victoria3.exe+58F1C48]
victoria3.exe+E3725C - 4D 85 C0              - test r8,r8
victoria3.exe+E3725F - 75 51                 - jne victoria3.exe+E372B2
victoria3.exe+E37261 - 83 FA FF              - cmp edx,-01
victoria3.exe+E37264 - 74 71                 - je victoria3.exe+E372D7
victoria3.exe+E37266 - 48 8D 15 D3D3A404     - lea rdx,[victoria3.exe+5884640]
victoria3.exe+E3726D - 48 8D 0D 2C8E4F04     - lea rcx,[victoria3.exe+53300A0]
victoria3.exe+E37274 - E8 37FF2F03           - call victoria3.exe+41371B0
victoria3.exe+E37279 - 48 89 84 24 90000000  - mov [rsp+00000090],rax
victoria3.exe+E37281 - 48 8D 84 24 90000000  - lea rax,[rsp+00000090]
victoria3.exe+E37289 - 48 89 44 24 30        - mov [rsp+30],rax
victoria3.exe+E3728E - 48 8D 44 24 40        - lea rax,[rsp+40]
victoria3.exe+E37293 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+E37298 - 4C 89 64 24 20        - mov [rsp+20],r12
victoria3.exe+E3729D - 4C 89 7C 24 40        - mov [rsp+40],r15
victoria3.exe+E372A2 - 48 C7 44 24 48 2F000000 - mov qword ptr [rsp+48],0000002F
victoria3.exe+E372AB - E8 B09897FF           - call victoria3.exe+7B0B60
victoria3.exe+E372B0 - EB 25                 - jmp victoria3.exe+E372D7
victoria3.exe+E372B2 - 8B C2                 - mov eax,edx
victoria3.exe+E372B4 - 25 FFFFFF00           - and eax,00FFFFFF
victoria3.exe+E372B9 - 41 3B 40 2C           - cmp eax,[r8+2C]
victoria3.exe+E372BD - 73 18                 - jae victoria3.exe+E372D7
victoria3.exe+E372BF - 8B C8                 - mov ecx,eax
victoria3.exe+E372C1 - 49 8B 40 20           - mov rax,[r8+20]
victoria3.exe+E372C5 - 48 03 C9              - add rcx,rcx
victoria3.exe+E372C8 - 48 8B 4C C8 08        - mov rcx,[rax+rcx*8+08]
victoria3.exe+E372CD - 48 85 C9              - test rcx,rcx
victoria3.exe+E372D0 - 74 05                 - je victoria3.exe+E372D7
victoria3.exe+E372D2 - 39 51 08              - cmp [rcx+08],edx
victoria3.exe+E372D5 - 74 07                 - je victoria3.exe+E372DE
victoria3.exe+E372D7 - 48 8B 0D DA8DAB04     - mov rcx,[victoria3.exe+58F00B8]
victoria3.exe+E372DE - E8 1DA2F1FF           - call victoria3.exe+D51500
victoria3.exe+E372E3 - 3B 05 EB24A504        - cmp eax,[victoria3.exe+58897D4]
victoria3.exe+E372E9 - 7F 12                 - jg victoria3.exe+E372FD
victoria3.exe+E372EB - 48 83 C3 04           - add rbx,04
victoria3.exe+E372EF - 49 3B DE              - cmp rbx,r14
victoria3.exe+E372F2 - 0F85 E8FEFFFF         - jne victoria3.exe+E371E0
victoria3.exe+E372F8 - E9 C1020000           - jmp victoria3.exe+E375BE
victoria3.exe+E372FD - 48 8B 86 F0000000     - mov rax,[rsi+000000F0]
victoria3.exe+E37304 - 48 8B 88 08010000     - mov rcx,[rax+00000108]
victoria3.exe+E3730B - 8B 41 40              - mov eax,[rcx+40]
victoria3.exe+E3730E - 48 C1 E8 14           - shr rax,14
victoria3.exe+E37312 - A8 01                 - test al,01
victoria3.exe+E37314 - 0F84 37010000         - je victoria3.exe+E37451
victoria3.exe+E3731A - 8B 86 E4000000        - mov eax,[rsi+000000E4]
victoria3.exe+E37320 - 48 8D 8C 24 90000000  - lea rcx,[rsp+00000090]
victoria3.exe+E37328 - 89 84 24 90000000     - mov [rsp+00000090],eax
victoria3.exe+E3732F - E8 6C2399FF           - call victoria3.exe+7C96A0
victoria3.exe+E37334 - 48 63 90 581D0000     - movsxd  rdx,dword ptr [rax+00001D58]
victoria3.exe+E3733B - 4C 69 DA A0860100     - imul r11,rdx,000186A0
victoria3.exe+E37342 - 4D 85 DB              - test r11,r11
victoria3.exe+E37345 - 7F 11                 - jg victoria3.exe+E37358
victoria3.exe+E37347 - B0 01                 - mov al,01
victoria3.exe+E37349 - 48 83 C4 50           - add rsp,50
victoria3.exe+E3734D - 41 5F                 - pop r15
victoria3.exe+E3734F - 41 5E                 - pop r14
victoria3.exe+E37351 - 41 5C                 - pop r12
victoria3.exe+E37353 - 5F                    - pop rdi
victoria3.exe+E37354 - 5E                    - pop rsi
victoria3.exe+E37355 - 5D                    - pop rbp
victoria3.exe+E37356 - 5B                    - pop rbx
victoria3.exe+E37357 - C3                    - ret 




| 函数 | 作用判断 |
|---|---|
| `+122B9A0` | 重算并写入贸易中心容量字段，最重要 |
| `+11FD470` | 使用容量字段进行复杂定点数分配，可能接近贸易路线数量计算 |
| `+E37130` | 计算可用容量/剩余容量相关条件 |
| `+1211180` | 使用总容量计算比例或限制值 |
| `+1228B90` | 批量对象/容器处理，暂不能确认 |
| `+1229C50` | 生成 `+1D58` 的实际子函数 |
| `+122A470` | 生成 `+1D5C` 的实际子函数 |