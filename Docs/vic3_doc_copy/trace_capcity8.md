# 命中断点，且条件 
7FF7EB07D5C9:
R14 == 0x32FDB11DB60
victoria3.exe+11FD5C9 - 41 8B 86 581D0000     - mov eax,[r14+00001D58]

# 补充 victoria3.exe+1229218 附近反编译 opcode

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
victoria3.exe+11FDB80 - 4C 8B CA              - mov r9,rdx
victoria3.exe+11FDB83 - 41 81 E8 DD270000     - sub r8d,000027DD
victoria3.exe+11FDB8A - 74 1A                 - je victoria3.exe+11FDBA6
victoria3.exe+11FDB8C - 41 83 F8 63           - cmp r8d,63
victoria3.exe+11FDB90 - 74 08                 - je victoria3.exe+11FDB9A
victoria3.exe+11FDB92 - 48 8B CA              - mov rcx,rdx
victoria3.exe+11FDB95 - E9 A65C8F02           - jmp victoria3.exe+3AF3840
victoria3.exe+11FDB9A - 48 8D 51 0C           - lea rdx,[rcx+0C]
victoria3.exe+11FDB9E - 49 8B C9              - mov rcx,r9
victoria3.exe+11FDBA1 - E9 9A7A9DFF           - jmp victoria3.exe+BD5640
victoria3.exe+11FDBA6 - 48 8D 51 08           - lea rdx,[rcx+08]
victoria3.exe+11FDBAA - 49 8B C9              - mov rcx,r9
victoria3.exe+11FDBAD - E9 8E7A9DFF           - jmp victoria3.exe+BD5640
victoria3.exe+11FDBB2 - CC                    - int 3 
victoria3.exe+11FDBB3 - CC                    - int 3 
victoria3.exe+11FDBB4 - CC                    - int 3 
victoria3.exe+11FDBB5 - CC                    - int 3 
victoria3.exe+11FDBB6 - CC                    - int 3 
victoria3.exe+11FDBB7 - CC                    - int 3 
victoria3.exe+11FDBB8 - CC                    - int 3 
victoria3.exe+11FDBB9 - CC                    - int 3 
victoria3.exe+11FDBBA - CC                    - int 3 
victoria3.exe+11FDBBB - CC                    - int 3 
victoria3.exe+11FDBBC - CC                    - int 3 
victoria3.exe+11FDBBD - CC                    - int 3 
victoria3.exe+11FDBBE - CC                    - int 3 
victoria3.exe+11FDBBF - CC                    - int 3 
victoria3.exe+11FDBC0 - 48 89 5C 24 08        - mov [rsp+08],rbx
victoria3.exe+11FDBC5 - 57                    - push rdi
victoria3.exe+11FDBC6 - 48 83 EC 20           - sub rsp,20
victoria3.exe+11FDBCA - 83 79 08 FF           - cmp dword ptr [rcx+08],-01
victoria3.exe+11FDBCE - 48 8B DA              - mov rbx,rdx
victoria3.exe+11FDBD1 - 48 8B F9              - mov rdi,rcx
victoria3.exe+11FDBD4 - 74 3A                 - je victoria3.exe+11FDC10
victoria3.exe+11FDBD6 - 48 8B CA              - mov rcx,rdx
victoria3.exe+11FDBD9 - E8 E2918F02           - call victoria3.exe+3AF6DC0
victoria3.exe+11FDBDE - BA DD270000           - mov edx,000027DD
victoria3.exe+11FDBE3 - 48 8B CB              - mov rcx,rbx
victoria3.exe+11FDBE6 - E8 75948F02           - call victoria3.exe+3AF7060
victoria3.exe+11FDBEB - BA 01000000           - mov edx,00000001
victoria3.exe+11FDBF0 - 48 8B CB              - mov rcx,rbx
victoria3.exe+11FDBF3 - E8 68948F02           - call victoria3.exe+3AF7060
victoria3.exe+11FDBF8 - 8B 57 08              - mov edx,[rdi+08]
victoria3.exe+11FDBFB - 48 8B CB              - mov rcx,rbx
victoria3.exe+11FDBFE - E8 ED978F02           - call victoria3.exe+3AF73F0
victoria3.exe+11FDC03 - BA 10000000           - mov edx,00000010
victoria3.exe+11FDC08 - 48 8B CB              - mov rcx,rbx
victoria3.exe+11FDC0B - E8 50948F02           - call victoria3.exe+3AF7060
victoria3.exe+11FDC10 - 83 7F 0C FF           - cmp dword ptr [rdi+0C],-01
victoria3.exe+11FDC14 - 74 3A                 - je victoria3.exe+11FDC50
victoria3.exe+11FDC16 - 48 8B CB              - mov rcx,rbx
victoria3.exe+11FDC19 - E8 A2918F02           - call victoria3.exe+3AF6DC0
victoria3.exe+11FDC1E - BA 40280000           - mov edx,00002840
victoria3.exe+11FDC23 - 48 8B CB              - mov rcx,rbx
victoria3.exe+11FDC26 - E8 35948F02           - call victoria3.exe+3AF7060
victoria3.exe+11FDC2B - BA 01000000           - mov edx,00000001
victoria3.exe+11FDC30 - 48 8B CB              - mov rcx,rbx
victoria3.exe+11FDC33 - E8 28948F02           - call victoria3.exe+3AF7060
victoria3.exe+11FDC38 - 8B 57 0C              - mov edx,[rdi+0C]
victoria3.exe+11FDC3B - 48 8B CB              - mov rcx,rbx
victoria3.exe+11FDC3E - E8 AD978F02           - call victoria3.exe+3AF73F0
victoria3.exe+11FDC43 - BA 10000000           - mov edx,00000010
victoria3.exe+11FDC48 - 48 8B CB              - mov rcx,rbx
victoria3.exe+11FDC4B - E8 10948F02           - call victoria3.exe+3AF7060
victoria3.exe+11FDC50 - 48 8B 5C 24 30        - mov rbx,[rsp+30]
victoria3.exe+11FDC55 - 48 83 C4 20           - add rsp,20
victoria3.exe+11FDC59 - 5F                    - pop rdi
victoria3.exe+11FDC5A - C3                    - ret 


# +11FD470 函数整体伪代码（根据当前反汇编整理）

下面的伪代码只表达当前反汇编能够确认的控制流。`RDI`、`RDI+4`、`RDI+D0` 等字段的业务名称仍需通过更多命中记录确认；固定精度数值统一记为 `fixed`，其内部比例单位通常为 100000。

```text
function ProcessEntry(entry, arg2, arg3, arg4):
    // Windows x64 参数：RCX=entry，RDX=arg2，R8=arg3，R9=arg4
    RDI = entry
    RBX = arg3

    // 从 entry+8 取得关联对象。当前记录中它返回贸易中心对象候选值。
    center = C4A660(entry + 8)
    R14 = center

    // 关联对象的虚函数检查；失败则直接返回 false。
    if not center.vfunc_08(center):
        return false

    // entry+4 必须为正，否则直接返回 false。
    if signed32(entry.field_04) <= 0:
        return false

    // 读取若干全局/上下文状态，并检查 entry+F8、entry+B0 的状态。
    contextFlag = Global_588B8A50.field_608.byte_148
    objectF8 = entry.ptr_F8

    if not objectF8.vfunc_00(objectF8):
        if not entry.ptr_B0.vfunc_00(entry.ptr_B0):
            if contextFlag == 0:
                entry.field_04 = 0
                return false

    // 调用内部处理函数。它可能产生临时状态并修改 entry 的关联数据。
    // RDI、RBX 以及栈上的 arg2/arg4 会作为后续计算的输入。
    ProcessEntryData(
        entry,
        temp_stack_object,
        saved_arg2,
        saved_arg4,
        saved_arg5,
        saved_arg6,
        saved_arg7
    )

    // 读取贸易中心对象的两个相关字段。
    used_or_state = int32(center.field_1D5C)   // [RSP+330]
    capacity      = int32(center.field_1D58)   // [RSP+50]

    // 读取当前全局定点数，并计算一个与容量相关的 fixed 值。
    // 这里的 0x186A0 = 100000，0xB504F333 是定点偏移/基准常量。
    baseA = Global_588A928
    baseB = Global_588A8F0
    capacity_value = InterpolateFixed(
        baseA,
        baseB,
        offset = 0xB504F333,
        scale = 100000
    )

    // 读取当前条目的比较阈值和第二个动态值。
    threshold = int64(entry.field_D0)
    entry_value = int64(entry.field_118)

    // 第一组条件：计算结果不能低于 entry+ D0。
    // 第二组条件：entry+118 对应的值必须达到计算出的全局基准。
    if capacity_value < threshold:
        goto UPDATE_ENTRY

    if entry_value < baseA:
        goto UPDATE_ENTRY

    // 当前条目达到限制条件。此路径不会执行后面的数量扣减，
    // 而是继续比较贸易中心的 1D5C 和 1D58。
    if used_or_state < capacity:
        // 尚未达到容量上限，当前条目仍保持可处理状态。
        return FinishWithoutDecrement(entry)
    else:
        // 已使用/状态值达到或超过容量，清空当前条目的剩余数量。
        entry.field_04 = 0
        return FinishWithoutDecrement(entry)


UPDATE_ENTRY:
    // 根据条目字段和全局值计算本轮要扣除的数量。
    // 这些计算使用同一套带溢出保护的 fixed-point 插值。
    amount = InterpolateFixed(
        left  = int64(entry.field_00) * 100000,
        right = Global_588A8D8,
        offset = 0xB504F333,
        scale = 100000
    )

    // amount 至少为 1，避免 entry+4 永远不减少。
    decrement = max(amount, 1)
    entry.field_04 = entry.field_04 - decrement

    // 根据状态标志选择回调参数，向后续函数提交本轮更新。
    if entry.flag_100 == 0:
        callback_arg1 = saved_arg7
        callback_arg2 = saved_arg6
        callback_arg3 = saved_arg5
        callback_kind = 0x60
    else:
        callback_arg1 = saved_arg4
        callback_arg2 = saved_arg3
        callback_arg3 = saved_arg2
        callback_kind = 0x70

    UpdateEntryState(
        center_field_1D88,
        callback_arg1,
        callback_arg2,
        callback_arg3,
        entry.ptr_130,
        entry.ptr_B0,
        callback_kind
    )

    // 如果关联对象仍然有效，则继续通知/更新关联状态。
    if center.vfunc_00(center):
        UpdateAssociatedState(entry.ptr_B0, ...)

    // 本轮处理完成后减少引用/剩余计数。
    decrement entry.field_04 if this path requires one-unit cleanup

    // 重新计算或刷新贸易中心对象。
    RecalculateTradeCenter(center)       // call +122BF50

    return true


// 说明：
// 1. `InterpolateFixed` 不是实际函数名，而是对多组 imul、sar 0x0E、
//    溢出判断和 cmov 指令的抽象。反汇编显示它在多个位置重复出现。
// 2. `RDI+4` 确实会被 dec、sub 或直接写 0，但它究竟是商品数量、
//    订单数量还是待处理迭代计数，还需要结合不同商品的 RDI 样本确认。
// 3. 当前记录中 `RSP+330=184`、`RSP+50=170`，因此会走
//    `used_or_state >= capacity` 的清零分支，执行 `mov [rdi+4],0`。
```



# 接下来的操作（已完成）
断点
victoria3.exe+11FD5C9
条件：
R14 == 32FDB11DB60
当前已命中

命中后记录：
（取值全部按 Type:4Bytes）
RSP
3366E321AF0
[RSP+330]       ; +1D5C
184
[RSP+50]        ; +1D58
170
RDI
3366E321A40
[RDI]
16
[RDI+4]
16
[RDI+D0]
11402220
[RDI+100]
3936945409
[RDI+B0]
1367619472
[RDI+F8]
1367648256
[RDI+118]
7240140
[RDI+130]
750000

RSI
3366E321AF0
RBX
332D1102770

单步执行到 victoria3.exe+11FD7BF
victoria3.exe+11FD7BF - 48 3B 97 D0000000     - cmp rdx,[rdi+000000D0]
RDI : 3366E321A40
RDX : 00DCF398
[RDI] = 16
[RDX] = ?? (无法显示)

单步执行到 victoria3.exe+11FD7C8
victoria3.exe+11FD7C8 - 4C 3B CB              - cmp r9,rbx
RBX:002625A0
R9：006E79CC
[RBX] = ?? (无法显示)
[R9] = ?? (无法显示)

单步执行到 victoria3.exe+11FD803
不会执行到这里，直接跳到了 victoria3.exe+11FD853 - BB 60000000           - mov ebx,00000060
RBX:002625A0
[RBX] = ?? (无法显示)

单步执行到 victoria3.exe+11FDA35
不会执行到这里，直接跳到了 victoria3.exe+11FDA5E - 48 8D 4C 24 60        - lea rcx,[rsp+60]
RCX:1512531CF00
RSP:AE769CD360
[RCX] = ?? (无法显示)
[RSP] = 00000000

# 对话
这批记录很有用，而且纠正了之前对部分寄存器的判断。

在 `+11FD5C9` 命中时，实际关系是：

```text
[R14+1D5C] = [RSP+330] = 184
[R14+1D58] = [RSP+50]  = 170
```

也就是说当前对象的 `+1D5C` 大于 `+1D58`。这可能表示已分配/已使用值已经超过当前允许容量。

几个寄存器的数值也能对应回字段：

```text
R9  = 0x006E79CC = 7,240,140
[RDI+118] = 7,240,140

RBX = 0x002625A0 = 2,500,000
```

因此在：

```asm
+11FD7BF  cmp rdx,[rdi+D0]
```

当时：

```text
RDX       = 0x00DCF398 = 14,479,512
[RDI+D0]  = 11,402,220
```

所以：

```text
RDX >= [RDI+D0]
```

`jl +11FD7D1` 不会跳转。

随后：

```asm
+11FD7C8  cmp r9,rbx
```

比较的是：

```text
7,240,140 >= 2,500,000
```

因此：

```asm
+11FD7CB  jnl +11FD853
```

跳转成立。你没有执行到 `+11FD803` 是正确的。

更关键的是，跳到 `+11FD853` 后还会执行：

```asm
+11FD853  mov ebx,60
+11FD862  cmp r11d,[rsp+50]
+11FD867  jl  +11FD877
+11FD869  mov [rdi+04],00000000
```

此时：

```text
R11D       = [RSP+330] = 184
[RSP+50]   = 170
```

所以：

```text
184 < 170     为假
```

不会跳到 `+11FD877`，而是执行：

```text
[RDI+4] = 0
```

你命中后最终跳到 `+11FDA5E`，很可能就是因为中间已经执行了 `+11FD869`，然后进入统一清理路径。

这说明当前这次处理的含义很可能是：

```text
当前条目原本有 16 个待处理单位
+1D5C = 184
+1D58 = 170
由于已使用值达到或超过允许值
将 [RDI+4] 清零
```

因此当前样本已经出现了“容量达到上限后停止当前条目”的行为，和贸易容量限制过程相当吻合。

需要注意：

```text
RBX = 0x2625A0
[R9]、[RBX]
```

这里的 `RBX` 和 `R9` 是普通数值，不是指针。不要再用 `[RBX]` 或 `[R9]` 去查看内存。它们分别是：

```text
RBX = 2,500,000
R9  = 7,240,140
```

同样，`[RSP]` 也不是这里要看的局部变量。应该使用：

```text
[RSP+330]
[RSP+50]
```

继续验证时，建议在以下位置设置断点：

```text
victoria3.exe+11FD869
条件：
R14 == 32FDB11DB60
```

命中时记录：

```text
RDI
[RDI]
[RDI+4]
[RSP+330]
[RSP+50]
[RDI+D0]
[RDI+118]
```

执行 `mov [rdi+4],0` 后再次读取：

```text
[RDI+4]
```

如果确实从 `16` 变成 `0`，就可以确认这条路径是在容量限制下终止当前条目。

还应在：

```text
victoria3.exe+11FD877
victoria3.exe+11FD7D1
victoria3.exe+11FDA35
victoria3.exe+11FDA38
```

分别设置断点。它们对应不同结果：

- `+11FD7D1`：第一组计算没有达到阈值，进入更新路径；
- `+11FD877`：`[RSP+330] < [RSP+50]`，允许继续处理；
- `+11FD869`：已达到或超过容量，清零 `[RDI+4]`；
- `+11FDA35`：另一条成功处理路径，执行 `dec [RDI+4]`；
- `+11FDA38`：随后调用 `+122BF50` 重新处理贸易中心对象。

特别要观察以下两种样本的差异：

```text
[RSP+330] < [RSP+50]
```

和：

```text
[RSP+330] >= [RSP+50]
```

如果第一种情况下 `[RDI+4]` 减少，而第二种情况下 `[RDI+4]` 被清零，那么 `+11FD470` 基本可以确认是在根据贸易中心容量决定当前条目还能分配多少。


# victoria3.exe+1229218 调用栈
已经单步到了 victoria3.exe+11FDA5E - 48 8D 4C 24 60        - lea rcx,[rsp+60]
大概率还在同一个栈内
Stacktrace
PC                      Stack       Frame       Return                          Parameters
victoria3.exe+11FDA5E   AE769CD360  AE769CD680  victoria3.exe+131D21E           000000B8,D1102720,D1102770,769CD870,...
victoria3.exe+131D21E   AE769CD690  AE769CE9D0  victoria3.exe+7B8563            3496A416,6E330180,503D8190,E6AE3CF0,...
victoria3.exe+7B8563    AE769CE9E0  AE769CEE30  victoria3.exe+7BE76D            0000021B,00000000,D121F078,00000000,...
victoria3.exe+7BE76D    AE769CEE40  AE769CF150  victoria3.exe+7D65A8            BA96AF00,7C057308,00000035,B97400AC,...
victoria3.exe+7D65A8    AE769CF160  AE769CF200  victoria3.exe+137C9E7           D1D59B88,00000003,7C057300,00000000,...
victoria3.exe+137C9E7   AE769CF210  AE769CF330  victoria3.exe+CC0D4D            00000000,D1D59B88,00000000,769CF420,...
victoria3.exe+CC0D4D    AE769CF340  AE769CF490  victoria3.exe+34624D9           0000000F,00000000,00000001,769CF5C0,...
victoria3.exe+34624D9   AE769CF4A0  AE769CF4E0  victoria3.exe+346253C           769CF520,00000000,00000000,00000000,...
victoria3.exe+346253C   AE769CF4F0  AE769CF540  victoria3.exe+332786F           769CF5B0,00000000,EF7625A0,769C003D,...
victoria3.exe+332786F   AE769CF550  AE769CF770  victoria3.exe+332BCE9           EF762500,00000001,00000000,00000000,...
victoria3.exe+332BCE9   AE769CF780  AE769CF830  victoria3.exe+3ACE43D           00000000,00000001,EF762658,00000000,...
victoria3.exe+3ACE43D   AE769CF840  AE769CF860  victoria3.exe+3ACD8CE           B1FE81C0,00000000,769CF868,769CF870,...
victoria3.exe+3ACD8CE   AE769CF870  AE769CF890  victoria3.exe+3B27992           00000000,00000000,00000005,00000005,...
victoria3.exe+3B27992   AE769CF8A0  AE769CF8C0  victoria3.exe+4160DCA           502C9D30,00000000,00000000,00000000,...
victoria3.exe+4160DCA   AE769CF8D0  AE769CF8F0  KERNEL32.BaseThreadInitThunk+17 00000000,00000000,00000000,...
KERNEL32.BaseThreadInitThunk+17 AE769CF900 AE769CF920 ntdll.RtlUserThreadStart+2C 00000000,00000000,FFFFFB30,FFFFFB30,...
ntdll.RtlUserThreadStart+2C AE769CF930 AE769CF970 00000000                        00000000,00000000,00000000,...




# victoria3.exe+131D21E 附近 opcode

victoria3.exe+131C2A8 - CC                    - int 3 
victoria3.exe+131C2A9 - CC                    - int 3 
victoria3.exe+131C2AA - CC                    - int 3 
victoria3.exe+131C2AB - CC                    - int 3 
victoria3.exe+131C2AC - CC                    - int 3 
victoria3.exe+131C2AD - CC                    - int 3 
victoria3.exe+131C2AE - CC                    - int 3 
victoria3.exe+131C2AF - CC                    - int 3 
victoria3.exe+131C2B0 - 40 55                 - push rbp
victoria3.exe+131C2B2 - 53                    - push rbx
victoria3.exe+131C2B3 - 56                    - push rsi
victoria3.exe+131C2B4 - 57                    - push rdi
victoria3.exe+131C2B5 - 41 54                 - push r12
victoria3.exe+131C2B7 - 41 55                 - push r13
victoria3.exe+131C2B9 - 41 56                 - push r14
victoria3.exe+131C2BB - 41 57                 - push r15
victoria3.exe+131C2BD - 48 8D AC 24 F8EDFFFF  - lea rbp,[rsp-00001208]
victoria3.exe+131C2C5 - B8 08130000           - mov eax,00001308
victoria3.exe+131C2CA - E8 A197E102           - call victoria3.exe+4135A70
victoria3.exe+131C2CF - 48 2B E0              - sub rsp,rax
victoria3.exe+131C2D2 - C5F829B4 24 F0 120000 - vmovaps [rsp+000012F0],xmm6
victoria3.exe+131C2DB - 48 8B D9              - mov rbx,rcx
victoria3.exe+131C2DE - E8 6DB24BFF           - call victoria3.exe+7D7550
victoria3.exe+131C2E3 - 48 8D 3D AE8E1603     - lea rdi,[victoria3.exe+4485198]
victoria3.exe+131C2EA - 48 8D 35 AFB71203     - lea rsi,[victoria3.exe+4447AA0]
victoria3.exe+131C2F1 - 80 B8 48010000 00     - cmp byte ptr [rax+00000148],00
victoria3.exe+131C2F8 - 74 07                 - je victoria3.exe+131C301
victoria3.exe+131C2FA - B8 01000000           - mov eax,00000001
victoria3.exe+131C2FF - EB 24                 - jmp victoria3.exe+131C325
victoria3.exe+131C301 - C7 44 24 58 F7030000  - mov [rsp+58],000003F7
victoria3.exe+131C309 - C7 44 24 5C 5A000000  - mov [rsp+5C],0000005A
victoria3.exe+131C311 - 48 89 7C 24 60        - mov [rsp+60],rdi
victoria3.exe+131C316 - 48 89 74 24 68        - mov [rsp+68],rsi
victoria3.exe+131C31B - 48 8D 54 24 58        - lea rdx,[rsp+58]
victoria3.exe+131C320 - E8 CB2A1402           - call victoria3.exe+345EDF0
victoria3.exe+131C325 - 89 85 50120000        - mov [rbp+00001250],eax
victoria3.exe+131C32B - C7 45 D8 FA030000     - mov [rbp-28],000003FA
victoria3.exe+131C332 - C7 45 DC 02000000     - mov [rbp-24],00000002
victoria3.exe+131C339 - 48 89 7D E0           - mov [rbp-20],rdi
victoria3.exe+131C33D - 48 89 75 E8           - mov [rbp-18],rsi
victoria3.exe+131C341 - 48 8D BB F0000000     - lea rdi,[rbx+000000F0]
victoria3.exe+131C348 - 48 89 BD 68120000     - mov [rbp+00001268],rdi
victoria3.exe+131C34F - 48 89 7C 24 58        - mov [rsp+58],rdi
victoria3.exe+131C354 - 48 8D 85 50120000     - lea rax,[rbp+00001250]
victoria3.exe+131C35B - 48 89 44 24 60        - mov [rsp+60],rax
victoria3.exe+131C360 - 48 8B 0D 11D45C04     - mov rcx,[victoria3.exe+58E9778]
victoria3.exe+131C367 - 8B 47 0C              - mov eax,[rdi+0C]
victoria3.exe+131C36A - 48 89 4C 24 70        - mov [rsp+70],rcx
victoria3.exe+131C36F - 48 C7 44 24 78 01000000 - mov qword ptr [rsp+78],00000001
victoria3.exe+131C378 - 33 F6                 - xor esi,esi
victoria3.exe+131C37A - 89 45 80              - mov [rbp-80],eax
victoria3.exe+131C37D - 48 85 C9              - test rcx,rcx
victoria3.exe+131C380 - 75 07                 - jne victoria3.exe+131C389
victoria3.exe+131C382 - B9 01000000           - mov ecx,00000001
victoria3.exe+131C387 - EB 09                 - jmp victoria3.exe+131C392
victoria3.exe+131C389 - 8B 89 48060000        - mov ecx,[rcx+00000648]
victoria3.exe+131C38F - 90                    - nop 
victoria3.exe+131C390 - FF C1                 - inc ecx
victoria3.exe+131C392 - 89 4D 84              - mov [rbp-7C],ecx
victoria3.exe+131C395 - 99                    - cdq 
victoria3.exe+131C396 - F7 F9                 - idiv ecx
victoria3.exe+131C398 - 8B C8                 - mov ecx,eax
victoria3.exe+131C39A - B8 56555555           - mov eax,55555556
victoria3.exe+131C39F - F7 E9                 - imul ecx
victoria3.exe+131C3A1 - 8B C2                 - mov eax,edx
victoria3.exe+131C3A3 - C1 E8 1F              - shr eax,1F
victoria3.exe+131C3A6 - 03 D0                 - add edx,eax
victoria3.exe+131C3A8 - B8 01000000           - mov eax,00000001
victoria3.exe+131C3AD - 3B D0                 - cmp edx,eax
victoria3.exe+131C3AF - 0F4F C2               - cmovg eax,edx
victoria3.exe+131C3B2 - 89 45 88              - mov [rbp-78],eax
victoria3.exe+131C3B5 - C7 45 8C 01000000     - mov [rbp-74],00000001
victoria3.exe+131C3BC - 48 8D 45 D8           - lea rax,[rbp-28]
victoria3.exe+131C3C0 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+131C3C5 - 48 8D 54 24 58        - lea rdx,[rsp+58]
victoria3.exe+131C3CA - 48 8D 4C 24 70        - lea rcx,[rsp+70]
victoria3.exe+131C3CF - E8 1C9D0000           - call victoria3.exe+13260F0
victoria3.exe+131C3D4 - 48 89 74 24 40        - mov [rsp+40],rsi
victoria3.exe+131C3D9 - 48 89 74 24 48        - mov [rsp+48],rsi
victoria3.exe+131C3DE - B9 40000000           - mov ecx,00000040
victoria3.exe+131C3E3 - 65 48 8B 04 25 58000000  - mov rax,gs:[00000058]
victoria3.exe+131C3EC - 48 8B 00              - mov rax,[rax]
victoria3.exe+131C3EF - 48 89 85 60120000     - mov [rbp+00001260],rax
victoria3.exe+131C3F6 - 8B 04 01              - mov eax,[rcx+rax]
victoria3.exe+131C3F9 - 39 05 01965604        - cmp [victoria3.exe+5885A00],eax
victoria3.exe+131C3FF - 0F8F FF100000         - jg victoria3.exe+131D504
victoria3.exe+131C405 - 48 8D 0D B419DA03     - lea rcx,[victoria3.exe+50BDDC0]
victoria3.exe+131C40C - 48 89 4C 24 50        - mov [rsp+50],rcx
victoria3.exe+131C411 - 8B 9B FC000000        - mov ebx,[rbx+000000FC]
victoria3.exe+131C417 - 3B 5C 24 48           - cmp ebx,[rsp+48]
victoria3.exe+131C41B - 7E 28                 - jle victoria3.exe+131C445
victoria3.exe+131C41D - 48 8D 14 9B           - lea rdx,[rbx+rbx*4]
victoria3.exe+131C421 - 48 C1 E2 06           - shl rdx,06
victoria3.exe+131C425 - 48 8B 05 9419DA03     - mov rax,[victoria3.exe+50BDDC0]
victoria3.exe+131C42C - 41 B8 08000000        - mov r8d,00000008
victoria3.exe+131C432 - FF 50 08              - call qword ptr [rax+08]
victoria3.exe+131C435 - 44 8B C3              - mov r8d,ebx
victoria3.exe+131C438 - 48 8B D0              - mov rdx,rax
victoria3.exe+131C43B - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+131C440 - E8 7BAB0000           - call victoria3.exe+1326FC0
victoria3.exe+131C445 - 4C 8B 37              - mov r14,[rdi]
victoria3.exe+131C448 - 48 63 47 0C           - movsxd  rax,dword ptr [rdi+0C]
victoria3.exe+131C44C - 4D 8D 2C C6           - lea r13,[r14+rax*8]
victoria3.exe+131C450 - 4D 3B F5              - cmp r14,r13
victoria3.exe+131C453 - 0F84 68010000         - je victoria3.exe+131C5C1
victoria3.exe+131C459 - C5FA1035 C7 964E03    - vmovss xmm6,[victoria3.exe+4805B28]
victoria3.exe+131C461 - 49 8B 1E              - mov rbx,[r14]
victoria3.exe+131C464 - 48 8B CB              - mov rcx,rbx
victoria3.exe+131C467 - E8 A456F1FF           - call victoria3.exe+1231B10
victoria3.exe+131C46C - 83 B8 E8000000 00     - cmp dword ptr [rax+000000E8],00
victoria3.exe+131C473 - 0F8E 3B010000         - jng victoria3.exe+131C5B4
victoria3.exe+131C479 - 8B 83 480E0000        - mov eax,[rbx+00000E48]
victoria3.exe+131C47F - 89 85 58120000        - mov [rbp+00001258],eax
victoria3.exe+131C485 - 48 8D 8D 58120000     - lea rcx,[rbp+00001258]
victoria3.exe+131C48C - E8 1F4649FF           - call victoria3.exe+7B0AB0
victoria3.exe+131C491 - 48 8B 88 E0080000     - mov rcx,[rax+000008E0]
victoria3.exe+131C498 - 48 83 C1 10           - add rcx,10
victoria3.exe+131C49C - 44 0FB7 05 50A9DB03   - movzx r8d,word ptr [victoria3.exe+50D6DF4]
victoria3.exe+131C4A4 - 48 8D 55 D8           - lea rdx,[rbp-28]
victoria3.exe+131C4A8 - E8 A37C52FF           - call victoria3.exe+844150
victoria3.exe+131C4AD - 48 83 38 00           - cmp qword ptr [rax],00
victoria3.exe+131C4B1 - 0F8F FD000000         - jg victoria3.exe+131C5B4
victoria3.exe+131C4B7 - 45 33 C0              - xor r8d,r8d
victoria3.exe+131C4BA - 48 8D 54 24 58        - lea rdx,[rsp+58]
victoria3.exe+131C4BF - 48 8B CB              - mov rcx,rbx
victoria3.exe+131C4C2 - E8 3941EFFF           - call victoria3.exe+1210600
victoria3.exe+131C4C7 - 48 83 38 00           - cmp qword ptr [rax],00
victoria3.exe+131C4CB - 0F8E E3000000         - jng victoria3.exe+131C5B4
victoria3.exe+131C4D1 - 48 63 44 24 4C        - movsxd  rax,dword ptr [rsp+4C]
victoria3.exe+131C4D6 - 8B 54 24 48           - mov edx,[rsp+48]
victoria3.exe+131C4DA - 3B C2                 - cmp eax,edx
victoria3.exe+131C4DC - 0F85 B9000000         - jne victoria3.exe+131C59B
victoria3.exe+131C4E2 - 8D 48 01              - lea ecx,[rax+01]
victoria3.exe+131C4E5 - C5F857C0              - vxorps xmm0,xmm0,xmm0
victoria3.exe+131C4E9 - C5FA2AC2              - vcvtsi2ss xmm0,xmm0,edx
victoria3.exe+131C4ED - C5FA59CE              - vmulss xmm1,xmm0,xmm6
victoria3.exe+131C4F1 - C5FA2CC1              - vcvttss2si eax,xmm1
victoria3.exe+131C4F5 - 3B C8                 - cmp ecx,eax
victoria3.exe+131C4F7 - 0F4C C8               - cmovl ecx,eax
victoria3.exe+131C4FA - 44 8B F9              - mov r15d,ecx
victoria3.exe+131C4FD - 48 8D 14 89           - lea rdx,[rcx+rcx*4]
victoria3.exe+131C501 - 48 C1 E2 06           - shl rdx,06
victoria3.exe+131C505 - 48 8B 4C 24 50        - mov rcx,[rsp+50]
victoria3.exe+131C50A - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131C50D - 41 B8 08000000        - mov r8d,00000008
victoria3.exe+131C513 - FF 50 08              - call qword ptr [rax+08]
victoria3.exe+131C516 - 4C 8B E0              - mov r12,rax
victoria3.exe+131C519 - 48 63 4C 24 4C        - movsxd  rcx,dword ptr [rsp+4C]
victoria3.exe+131C51E - 48 8D 0C 89           - lea rcx,[rcx+rcx*4]
victoria3.exe+131C522 - 48 C1 E1 06           - shl rcx,06
victoria3.exe+131C526 - 48 03 C8              - add rcx,rax
victoria3.exe+131C529 - 48 8B D3              - mov rdx,rbx
victoria3.exe+131C52C - E8 FF0CEEFF           - call victoria3.exe+11FD230
victoria3.exe+131C531 - 49 8B FC              - mov rdi,r12
victoria3.exe+131C534 - 48 63 54 24 4C        - movsxd  rdx,dword ptr [rsp+4C]
victoria3.exe+131C539 - 48 8D 34 92           - lea rsi,[rdx+rdx*4]
victoria3.exe+131C53D - 48 C1 E6 06           - shl rsi,06
victoria3.exe+131C541 - 48 8B 5C 24 40        - mov rbx,[rsp+40]
victoria3.exe+131C546 - 48 03 F3              - add rsi,rbx
victoria3.exe+131C549 - 48 3B DE              - cmp rbx,rsi
victoria3.exe+131C54C - 74 2C                 - je victoria3.exe+131C57A
victoria3.exe+131C54E - 66 90                 - nop 2
victoria3.exe+131C550 - 48 8B CF              - mov rcx,rdi
victoria3.exe+131C553 - 48 81 C7 40010000     - add rdi,00000140
victoria3.exe+131C55A - 48 8B D3              - mov rdx,rbx
victoria3.exe+131C55D - E8 6ED80000           - call victoria3.exe+1329DD0
victoria3.exe+131C562 - 48 8B CB              - mov rcx,rbx
victoria3.exe+131C565 - E8 26D90000           - call victoria3.exe+1329E90
victoria3.exe+131C56A - 48 81 C3 40010000     - add rbx,00000140
victoria3.exe+131C571 - 48 3B DE              - cmp rbx,rsi
victoria3.exe+131C574 - 75 DA                 - jne victoria3.exe+131C550
victoria3.exe+131C576 - 8B 54 24 4C           - mov edx,[rsp+4C]
victoria3.exe+131C57A - 8D 5A 01              - lea ebx,[rdx+01]
victoria3.exe+131C57D - C7 44 24 4C 00000000  - mov [rsp+4C],00000000
victoria3.exe+131C585 - 45 8B C7              - mov r8d,r15d
victoria3.exe+131C588 - 49 8B D4              - mov rdx,r12
victoria3.exe+131C58B - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+131C590 - E8 2BAA0000           - call victoria3.exe+1326FC0
victoria3.exe+131C595 - 89 5C 24 4C           - mov [rsp+4C],ebx
victoria3.exe+131C599 - EB 19                 - jmp victoria3.exe+131C5B4
victoria3.exe+131C59B - 48 8D 0C 80           - lea rcx,[rax+rax*4]
victoria3.exe+131C59F - 48 C1 E1 06           - shl rcx,06
victoria3.exe+131C5A3 - 48 03 4C 24 40        - add rcx,[rsp+40]
victoria3.exe+131C5A8 - 48 8B D3              - mov rdx,rbx
victoria3.exe+131C5AB - E8 800CEEFF           - call victoria3.exe+11FD230
victoria3.exe+131C5B0 - FF 44 24 4C           - inc [rsp+4C]
victoria3.exe+131C5B4 - 49 83 C6 08           - add r14,08
victoria3.exe+131C5B8 - 4D 3B F5              - cmp r14,r13
victoria3.exe+131C5BB - 0F85 A0FEFFFF         - jne victoria3.exe+131C461
victoria3.exe+131C5C1 - 48 63 44 24 4C        - movsxd  rax,dword ptr [rsp+4C]
victoria3.exe+131C5C6 - 4C 8D 24 80           - lea r12,[rax+rax*4]
victoria3.exe+131C5CA - 49 C1 E4 06           - shl r12,06
victoria3.exe+131C5CE - 4C 8B 74 24 40        - mov r14,[rsp+40]
victoria3.exe+131C5D3 - 4D 03 E6              - add r12,r14
victoria3.exe+131C5D6 - 4C 89 A5 58120000     - mov [rbp+00001258],r12
victoria3.exe+131C5DD - 4D 8B FC              - mov r15,r12
victoria3.exe+131C5E0 - 4D 2B FE              - sub r15,r14
victoria3.exe+131C5E3 - 49 C1 FF 06           - sar r15,06
victoria3.exe+131C5E7 - 48 B8 CDCCCCCCCCCCCCCC - mov rax,CCCCCCCCCCCCCCCD
victoria3.exe+131C5F1 - 4C 0FAF F8            - imul r15,rax
victoria3.exe+131C5F5 - 49 83 FF 20           - cmp r15,20
victoria3.exe+131C5F9 - 0F8F C4050000         - jg victoria3.exe+131CBC3
victoria3.exe+131C5FF - 4D 3B F4              - cmp r14,r12
victoria3.exe+131C602 - 0F84 07070000         - je victoria3.exe+131CD0F
victoria3.exe+131C608 - 49 8D B6 40010000     - lea rsi,[r14+00000140]
victoria3.exe+131C60F - 49 3B F4              - cmp rsi,r12
victoria3.exe+131C612 - 0F84 F7060000         - je victoria3.exe+131CD0F
victoria3.exe+131C618 - 0F1F 84 00 00000000   - nop dword ptr [rax+rax+00000000]
victoria3.exe+131C620 - 48 8B DE              - mov rbx,rsi
victoria3.exe+131C623 - 8B 06                 - mov eax,[rsi]
victoria3.exe+131C625 - 89 85 30010000        - mov [rbp+00000130],eax
victoria3.exe+131C62B - 8B 46 04              - mov eax,[rsi+04]
victoria3.exe+131C62E - 89 85 34010000        - mov [rbp+00000134],eax
victoria3.exe+131C634 - 8B 46 08              - mov eax,[rsi+08]
victoria3.exe+131C637 - 89 85 38010000        - mov [rbp+00000138],eax
victoria3.exe+131C63D - 8B 46 0C              - mov eax,[rsi+0C]
victoria3.exe+131C640 - 89 85 3C010000        - mov [rbp+0000013C],eax
victoria3.exe+131C646 - 48 8D 56 10           - lea rdx,[rsi+10]
victoria3.exe+131C64A - 48 8D 8D 40010000     - lea rcx,[rbp+00000140]
victoria3.exe+131C651 - C5F877                - vzeroupper 
victoria3.exe+131C654 - E8 C7C89DFF           - call victoria3.exe+CF8F20
victoria3.exe+131C659 - 90                    - nop 
victoria3.exe+131C65A - 48 8D 56 60           - lea rdx,[rsi+60]
victoria3.exe+131C65E - 48 8D 8D 90010000     - lea rcx,[rbp+00000190]
victoria3.exe+131C665 - E8 B6C89DFF           - call victoria3.exe+CF8F20
victoria3.exe+131C66A - C5FC1086 B0 000000    - vmovups ymm0,[rsi+000000B0]
victoria3.exe+131C672 - C5FC1185 E0 010000    - vmovups [rbp+000001E0],ymm0
victoria3.exe+131C67A - C5FC108E D0 000000    - vmovups ymm1,[rsi+000000D0]
victoria3.exe+131C682 - C5FC118D 00 020000    - vmovups [rbp+00000200],ymm1
victoria3.exe+131C68A - C5FB1086 F0 000000    - vmovsd xmm0,[rsi+000000F0]
victoria3.exe+131C692 - C5FB1185 20 020000    - vmovsd [rbp+00000220],xmm0
victoria3.exe+131C69A - C5FC108E F8 000000    - vmovups ymm1,[rsi+000000F8]
victoria3.exe+131C6A2 - C5FC118D 28 020000    - vmovups [rbp+00000228],ymm1
victoria3.exe+131C6AA - C5FC1086 18 010000    - vmovups ymm0,[rsi+00000118]
victoria3.exe+131C6B2 - C5FC1185 48 020000    - vmovups [rbp+00000248],ymm0
victoria3.exe+131C6BA - C5FB108E 38 010000    - vmovsd xmm1,[rsi+00000138]
victoria3.exe+131C6C2 - C5FB118D 68 020000    - vmovsd [rbp+00000268],xmm1
victoria3.exe+131C6CA - 8B 8D 34010000        - mov ecx,[rbp+00000134]
victoria3.exe+131C6D0 - 41 3B 4E 04           - cmp ecx,[r14+04]
victoria3.exe+131C6D4 - 0F8E 20020000         - jng victoria3.exe+131C8FA
victoria3.exe+131C6DA - 49 3B F6              - cmp rsi,r14
victoria3.exe+131C6DD - 0F84 0F010000         - je victoria3.exe+131C7F2
victoria3.exe+131C6E3 - 48 8D BE 48010000     - lea rdi,[rsi+00000148]
victoria3.exe+131C6EA - 66 0F1F 44 00 00      - nop word ptr [rax+rax+00]
victoria3.exe+131C6F0 - 48 8D BF C0FEFFFF     - lea rdi,[rdi-00000140]
victoria3.exe+131C6F7 - 48 8D 9F B8FEFFFF     - lea rbx,[rdi-00000148]
victoria3.exe+131C6FE - 8B 03                 - mov eax,[rbx]
victoria3.exe+131C700 - 89 47 F8              - mov [rdi-08],eax
victoria3.exe+131C703 - 8B 87 BCFEFFFF        - mov eax,[rdi-00000144]
victoria3.exe+131C709 - 89 47 FC              - mov [rdi-04],eax
victoria3.exe+131C70C - 8B 87 C0FEFFFF        - mov eax,[rdi-00000140]
victoria3.exe+131C712 - 89 07                 - mov [rdi],eax
victoria3.exe+131C714 - 8B 87 C4FEFFFF        - mov eax,[rdi-0000013C]
victoria3.exe+131C71A - 89 47 04              - mov [rdi+04],eax
victoria3.exe+131C71D - 48 8D 97 D0FEFFFF     - lea rdx,[rdi-00000130]
victoria3.exe+131C724 - 48 8D 4F 10           - lea rcx,[rdi+10]
victoria3.exe+131C728 - C5F877                - vzeroupper 
victoria3.exe+131C72B - E8 304F8BFF           - call victoria3.exe+BD1660
victoria3.exe+131C730 - C5F81087 E8 FEFFFF    - vmovups xmm0,[rdi-00000118]
victoria3.exe+131C738 - C5F81147 28           - vmovups [rdi+28],xmm0
victoria3.exe+131C73D - 48 8D 97 F8FEFFFF     - lea rdx,[rdi-00000108]
victoria3.exe+131C744 - 48 8D 4F 38           - lea rcx,[rdi+38]
victoria3.exe+131C748 - E8 039D92FF           - call victoria3.exe+C46450
victoria3.exe+131C74D - 8B 87 10FFFFFF        - mov eax,[rdi-000000F0]
victoria3.exe+131C753 - 89 47 50              - mov [rdi+50],eax
victoria3.exe+131C756 - 48 8D 97 20FFFFFF     - lea rdx,[rdi-000000E0]
victoria3.exe+131C75D - 48 8D 4F 60           - lea rcx,[rdi+60]
victoria3.exe+131C761 - E8 FA4E8BFF           - call victoria3.exe+BD1660
victoria3.exe+131C766 - C5F81087 38 FFFFFF    - vmovups xmm0,[rdi-000000C8]
victoria3.exe+131C76E - C5F81147 78           - vmovups [rdi+78],xmm0
victoria3.exe+131C773 - 48 8D 97 48FFFFFF     - lea rdx,[rdi-000000B8]
victoria3.exe+131C77A - 48 8D 8F 88000000     - lea rcx,[rdi+00000088]
victoria3.exe+131C781 - E8 CA9C92FF           - call victoria3.exe+C46450
victoria3.exe+131C786 - 8B 87 60FFFFFF        - mov eax,[rdi-000000A0]
victoria3.exe+131C78C - 89 87 A0000000        - mov [rdi+000000A0],eax
victoria3.exe+131C792 - C5FC1087 68 FFFFFF    - vmovups ymm0,[rdi-00000098]
victoria3.exe+131C79A - C5FC1187 A8 000000    - vmovups [rdi+000000A8],ymm0
victoria3.exe+131C7A2 - C5FC104F 88           - vmovups ymm1,[rdi-78]
victoria3.exe+131C7A7 - C5FC118F C8 000000    - vmovups [rdi+000000C8],ymm1
victoria3.exe+131C7AF - C5FB1047 A8           - vmovsd xmm0,[rdi-58]
victoria3.exe+131C7B4 - C5FB1187 E8 000000    - vmovsd [rdi+000000E8],xmm0
victoria3.exe+131C7BC - C5FC1047 B0           - vmovups ymm0,[rdi-50]
victoria3.exe+131C7C1 - C5FC1187 F0 000000    - vmovups [rdi+000000F0],ymm0
victoria3.exe+131C7C9 - C5FC104F D0           - vmovups ymm1,[rdi-30]
victoria3.exe+131C7CE - C5FC118F 10 010000    - vmovups [rdi+00000110],ymm1
victoria3.exe+131C7D6 - C5FB1047 F0           - vmovsd xmm0,[rdi-10]
victoria3.exe+131C7DB - C5FB1187 30 010000    - vmovsd [rdi+00000130],xmm0
victoria3.exe+131C7E3 - 49 3B DE              - cmp rbx,r14
victoria3.exe+131C7E6 - 0F85 04FFFFFF         - jne victoria3.exe+131C6F0
victoria3.exe+131C7EC - 8B 8D 34010000        - mov ecx,[rbp+00000134]
victoria3.exe+131C7F2 - 8B 85 30010000        - mov eax,[rbp+00000130]
victoria3.exe+131C7F8 - 41 89 06              - mov [r14],eax
victoria3.exe+131C7FB - 41 89 4E 04           - mov [r14+04],ecx
victoria3.exe+131C7FF - 8B 85 38010000        - mov eax,[rbp+00000138]
victoria3.exe+131C805 - 41 89 46 08           - mov [r14+08],eax
victoria3.exe+131C809 - 8B 85 3C010000        - mov eax,[rbp+0000013C]
victoria3.exe+131C80F - 41 89 46 0C           - mov [r14+0C],eax
victoria3.exe+131C813 - 49 8D 4E 18           - lea rcx,[r14+18]
victoria3.exe+131C817 - 48 8D 95 48010000     - lea rdx,[rbp+00000148]
victoria3.exe+131C81E - C5F877                - vzeroupper 
victoria3.exe+131C821 - E8 3A4E8BFF           - call victoria3.exe+BD1660
victoria3.exe+131C826 - C5F81085 60 010000    - vmovups xmm0,[rbp+00000160]
victoria3.exe+131C82E - C4C1781146 30         - vmovups [r14+30],xmm0
victoria3.exe+131C834 - 49 8D 4E 40           - lea rcx,[r14+40]
victoria3.exe+131C838 - 48 8D 95 70010000     - lea rdx,[rbp+00000170]
victoria3.exe+131C83F - E8 0C9C92FF           - call victoria3.exe+C46450
victoria3.exe+131C844 - 8B 85 88010000        - mov eax,[rbp+00000188]
victoria3.exe+131C84A - 41 89 46 58           - mov [r14+58],eax
victoria3.exe+131C84E - 49 8D 4E 68           - lea rcx,[r14+68]
victoria3.exe+131C852 - 48 8D 95 98010000     - lea rdx,[rbp+00000198]
victoria3.exe+131C859 - E8 024E8BFF           - call victoria3.exe+BD1660
victoria3.exe+131C85E - C5F81085 B0 010000    - vmovups xmm0,[rbp+000001B0]
victoria3.exe+131C866 - C4C1781186 80 000000  - vmovups [r14+00000080],xmm0
victoria3.exe+131C86F - 49 8D 8E 90000000     - lea rcx,[r14+00000090]
victoria3.exe+131C876 - 48 8D 95 C0010000     - lea rdx,[rbp+000001C0]
victoria3.exe+131C87D - E8 CE9B92FF           - call victoria3.exe+C46450
victoria3.exe+131C882 - 8B 85 D8010000        - mov eax,[rbp+000001D8]
victoria3.exe+131C888 - 41 89 86 A8000000     - mov [r14+000000A8],eax
victoria3.exe+131C88F - C5FC1085 E0 010000    - vmovups ymm0,[rbp+000001E0]
victoria3.exe+131C897 - C4C17C1186 B0 000000  - vmovups [r14+000000B0],ymm0
victoria3.exe+131C8A0 - C5FC108D 00 020000    - vmovups ymm1,[rbp+00000200]
victoria3.exe+131C8A8 - C4C17C118E D0 000000  - vmovups [r14+000000D0],ymm1
victoria3.exe+131C8B1 - C5FB1085 20 020000    - vmovsd xmm0,[rbp+00000220]
victoria3.exe+131C8B9 - C4C17B1186 F0 000000  - vmovsd [r14+000000F0],xmm0
victoria3.exe+131C8C2 - C5FC108D 28 020000    - vmovups ymm1,[rbp+00000228]
victoria3.exe+131C8CA - C4C17C118E F8 000000  - vmovups [r14+000000F8],ymm1
victoria3.exe+131C8D3 - C5FC1085 48 020000    - vmovups ymm0,[rbp+00000248]
victoria3.exe+131C8DB - C4C17C1186 18 010000  - vmovups [r14+00000118],ymm0
victoria3.exe+131C8E4 - C5FB108D 68 020000    - vmovsd xmm1,[rbp+00000268]
victoria3.exe+131C8EC - C4C17B118E 38 010000  - vmovsd [r14+00000138],xmm1
victoria3.exe+131C8F5 - E9 03020000           - jmp victoria3.exe+131CAFD
victoria3.exe+131C8FA - 48 8D BE C0FEFFFF     - lea rdi,[rsi-00000140]
victoria3.exe+131C901 - 3B 8E C4FEFFFF        - cmp ecx,[rsi-0000013C]
victoria3.exe+131C907 - 0F8E FB000000         - jng victoria3.exe+131CA08
victoria3.exe+131C90D - 0F1F 00               - nop dword ptr [rax]
victoria3.exe+131C910 - 8B 07                 - mov eax,[rdi]
victoria3.exe+131C912 - 89 03                 - mov [rbx],eax
victoria3.exe+131C914 - 8B 47 04              - mov eax,[rdi+04]
victoria3.exe+131C917 - 89 43 04              - mov [rbx+04],eax
victoria3.exe+131C91A - 8B 47 08              - mov eax,[rdi+08]
victoria3.exe+131C91D - 89 43 08              - mov [rbx+08],eax
victoria3.exe+131C920 - 8B 47 0C              - mov eax,[rdi+0C]
victoria3.exe+131C923 - 89 43 0C              - mov [rbx+0C],eax
victoria3.exe+131C926 - 48 8D 57 18           - lea rdx,[rdi+18]
victoria3.exe+131C92A - 48 8D 4B 18           - lea rcx,[rbx+18]
victoria3.exe+131C92E - C5F877                - vzeroupper 
victoria3.exe+131C931 - E8 2A4D8BFF           - call victoria3.exe+BD1660
victoria3.exe+131C936 - C5F81047 30           - vmovups xmm0,[rdi+30]
victoria3.exe+131C93B - C5F81143 30           - vmovups [rbx+30],xmm0
victoria3.exe+131C940 - 48 8D 57 40           - lea rdx,[rdi+40]
victoria3.exe+131C944 - 48 8D 4B 40           - lea rcx,[rbx+40]
victoria3.exe+131C948 - E8 039B92FF           - call victoria3.exe+C46450
victoria3.exe+131C94D - 8B 47 58              - mov eax,[rdi+58]
victoria3.exe+131C950 - 89 43 58              - mov [rbx+58],eax
victoria3.exe+131C953 - 48 8D 57 68           - lea rdx,[rdi+68]
victoria3.exe+131C957 - 48 8D 4B 68           - lea rcx,[rbx+68]
victoria3.exe+131C95B - E8 004D8BFF           - call victoria3.exe+BD1660
victoria3.exe+131C960 - C5F81087 80 000000    - vmovups xmm0,[rdi+00000080]
victoria3.exe+131C968 - C5F81183 80 000000    - vmovups [rbx+00000080],xmm0
victoria3.exe+131C970 - 48 8D 97 90000000     - lea rdx,[rdi+00000090]
victoria3.exe+131C977 - 48 8D 8B 90000000     - lea rcx,[rbx+00000090]
victoria3.exe+131C97E - E8 CD9A92FF           - call victoria3.exe+C46450
victoria3.exe+131C983 - 8B 87 A8000000        - mov eax,[rdi+000000A8]
victoria3.exe+131C989 - 89 83 A8000000        - mov [rbx+000000A8],eax
victoria3.exe+131C98F - C5FC1087 B0 000000    - vmovups ymm0,[rdi+000000B0]
victoria3.exe+131C997 - C5FC1183 B0 000000    - vmovups [rbx+000000B0],ymm0
victoria3.exe+131C99F - C5FC108F D0 000000    - vmovups ymm1,[rdi+000000D0]
victoria3.exe+131C9A7 - C5FC118B D0 000000    - vmovups [rbx+000000D0],ymm1
victoria3.exe+131C9AF - C5FB1087 F0 000000    - vmovsd xmm0,[rdi+000000F0]
victoria3.exe+131C9B7 - C5FB1183 F0 000000    - vmovsd [rbx+000000F0],xmm0
victoria3.exe+131C9BF - C5FC1087 F8 000000    - vmovups ymm0,[rdi+000000F8]
victoria3.exe+131C9C7 - C5FC1183 F8 000000    - vmovups [rbx+000000F8],ymm0
victoria3.exe+131C9CF - C5FC108F 18 010000    - vmovups ymm1,[rdi+00000118]
victoria3.exe+131C9D7 - C5FC118B 18 010000    - vmovups [rbx+00000118],ymm1
victoria3.exe+131C9DF - C5FB1087 38 010000    - vmovsd xmm0,[rdi+00000138]
victoria3.exe+131C9E7 - C5FB1183 38 010000    - vmovsd [rbx+00000138],xmm0
victoria3.exe+131C9EF - 48 8B DF              - mov rbx,rdi
victoria3.exe+131C9F2 - 48 81 EF 40010000     - sub rdi,00000140
victoria3.exe+131C9F9 - 8B 8D 34010000        - mov ecx,[rbp+00000134]
victoria3.exe+131C9FF - 3B 4F 04              - cmp ecx,[rdi+04]
victoria3.exe+131CA02 - 0F8F 08FFFFFF         - jg victoria3.exe+131C910
victoria3.exe+131CA08 - 8B 85 30010000        - mov eax,[rbp+00000130]
victoria3.exe+131CA0E - 89 03                 - mov [rbx],eax
victoria3.exe+131CA10 - 89 4B 04              - mov [rbx+04],ecx
victoria3.exe+131CA13 - 8B 85 38010000        - mov eax,[rbp+00000138]
victoria3.exe+131CA19 - 89 43 08              - mov [rbx+08],eax
victoria3.exe+131CA1C - 8B 85 3C010000        - mov eax,[rbp+0000013C]
victoria3.exe+131CA22 - 89 43 0C              - mov [rbx+0C],eax
victoria3.exe+131CA25 - 48 8D 4B 18           - lea rcx,[rbx+18]
victoria3.exe+131CA29 - 48 8D 95 48010000     - lea rdx,[rbp+00000148]
victoria3.exe+131CA30 - C5F877                - vzeroupper 
victoria3.exe+131CA33 - E8 284C8BFF           - call victoria3.exe+BD1660
victoria3.exe+131CA38 - C5F81085 60 010000    - vmovups xmm0,[rbp+00000160]
victoria3.exe+131CA40 - C5F81143 30           - vmovups [rbx+30],xmm0
victoria3.exe+131CA45 - 48 8D 4B 40           - lea rcx,[rbx+40]
victoria3.exe+131CA49 - 48 8D 95 70010000     - lea rdx,[rbp+00000170]
victoria3.exe+131CA50 - E8 FB9992FF           - call victoria3.exe+C46450
victoria3.exe+131CA55 - 8B 85 88010000        - mov eax,[rbp+00000188]
victoria3.exe+131CA5B - 89 43 58              - mov [rbx+58],eax
victoria3.exe+131CA5E - 48 8D 4B 68           - lea rcx,[rbx+68]
victoria3.exe+131CA62 - 48 8D 95 98010000     - lea rdx,[rbp+00000198]
victoria3.exe+131CA69 - E8 F24B8BFF           - call victoria3.exe+BD1660
victoria3.exe+131CA6E - C5F81085 B0 010000    - vmovups xmm0,[rbp+000001B0]
victoria3.exe+131CA76 - C5F81183 80 000000    - vmovups [rbx+00000080],xmm0
victoria3.exe+131CA7E - 48 8D 8B 90000000     - lea rcx,[rbx+00000090]
victoria3.exe+131CA85 - 48 8D 95 C0010000     - lea rdx,[rbp+000001C0]
victoria3.exe+131CA8C - E8 BF9992FF           - call victoria3.exe+C46450
victoria3.exe+131CA91 - 8B 85 D8010000        - mov eax,[rbp+000001D8]
victoria3.exe+131CA97 - 89 83 A8000000        - mov [rbx+000000A8],eax
victoria3.exe+131CA9D - C5FC1085 E0 010000    - vmovups ymm0,[rbp+000001E0]
victoria3.exe+131CAA5 - C5FC1183 B0 000000    - vmovups [rbx+000000B0],ymm0
victoria3.exe+131CAAD - C5FC108D 00 020000    - vmovups ymm1,[rbp+00000200]
victoria3.exe+131CAB5 - C5FC118B D0 000000    - vmovups [rbx+000000D0],ymm1
victoria3.exe+131CABD - C5FB1085 20 020000    - vmovsd xmm0,[rbp+00000220]
victoria3.exe+131CAC5 - C5FB1183 F0 000000    - vmovsd [rbx+000000F0],xmm0
victoria3.exe+131CACD - C5FC108D 28 020000    - vmovups ymm1,[rbp+00000228]
victoria3.exe+131CAD5 - C5FC118B F8 000000    - vmovups [rbx+000000F8],ymm1
victoria3.exe+131CADD - C5FC1085 48 020000    - vmovups ymm0,[rbp+00000248]
victoria3.exe+131CAE5 - C5FC1183 18 010000    - vmovups [rbx+00000118],ymm0
victoria3.exe+131CAED - C5FB108D 68 020000    - vmovsd xmm1,[rbp+00000268]
victoria3.exe+131CAF5 - C5FB118B 38 010000    - vmovsd [rbx+00000138],xmm1
victoria3.exe+131CAFD - 48 8B 95 C0010000     - mov rdx,[rbp+000001C0]
victoria3.exe+131CB04 - 33 DB                 - xor ebx,ebx
victoria3.exe+131CB06 - 48 85 D2              - test rdx,rdx
victoria3.exe+131CB09 - 74 23                 - je victoria3.exe+131CB2E
victoria3.exe+131CB0B - 89 9D CC010000        - mov [rbp+000001CC],ebx
victoria3.exe+131CB11 - 48 8B 8D D0010000     - mov rcx,[rbp+000001D0]
victoria3.exe+131CB18 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131CB1B - C5F877                - vzeroupper 
victoria3.exe+131CB1E - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131CB21 - 48 89 9D C0010000     - mov [rbp+000001C0],rbx
victoria3.exe+131CB28 - 89 9D C8010000        - mov [rbp+000001C8],ebx
victoria3.exe+131CB2E - 48 8B 95 98010000     - mov rdx,[rbp+00000198]
victoria3.exe+131CB35 - 48 85 D2              - test rdx,rdx
victoria3.exe+131CB38 - 74 23                 - je victoria3.exe+131CB5D
victoria3.exe+131CB3A - 89 9D A4010000        - mov [rbp+000001A4],ebx
victoria3.exe+131CB40 - 48 8B 8D A8010000     - mov rcx,[rbp+000001A8]
victoria3.exe+131CB47 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131CB4A - C5F877                - vzeroupper 
victoria3.exe+131CB4D - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131CB50 - 48 89 9D 98010000     - mov [rbp+00000198],rbx
victoria3.exe+131CB57 - 89 9D A0010000        - mov [rbp+000001A0],ebx
victoria3.exe+131CB5D - 48 8B 95 70010000     - mov rdx,[rbp+00000170]
victoria3.exe+131CB64 - 48 85 D2              - test rdx,rdx
victoria3.exe+131CB67 - 74 23                 - je victoria3.exe+131CB8C
victoria3.exe+131CB69 - 89 9D 7C010000        - mov [rbp+0000017C],ebx
victoria3.exe+131CB6F - 48 8B 8D 80010000     - mov rcx,[rbp+00000180]
victoria3.exe+131CB76 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131CB79 - C5F877                - vzeroupper 
victoria3.exe+131CB7C - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131CB7F - 48 89 9D 70010000     - mov [rbp+00000170],rbx
victoria3.exe+131CB86 - 89 9D 78010000        - mov [rbp+00000178],ebx
victoria3.exe+131CB8C - 48 8B 95 48010000     - mov rdx,[rbp+00000148]
victoria3.exe+131CB93 - 48 85 D2              - test rdx,rdx
victoria3.exe+131CB96 - 74 16                 - je victoria3.exe+131CBAE
victoria3.exe+131CB98 - 89 9D 54010000        - mov [rbp+00000154],ebx
victoria3.exe+131CB9E - 48 8B 8D 58010000     - mov rcx,[rbp+00000158]
victoria3.exe+131CBA5 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131CBA8 - C5F877                - vzeroupper 
victoria3.exe+131CBAB - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131CBAE - 48 81 C6 40010000     - add rsi,00000140
victoria3.exe+131CBB5 - 49 3B F4              - cmp rsi,r12
victoria3.exe+131CBB8 - 0F85 62FAFFFF         - jne victoria3.exe+131C620
victoria3.exe+131CBBE - E9 4C010000           - jmp victoria3.exe+131CD0F
victoria3.exe+131CBC3 - 49 8B C7              - mov rax,r15
victoria3.exe+131CBC6 - 48 99                 - cqo 
victoria3.exe+131CBC8 - 48 2B C2              - sub rax,rdx
victoria3.exe+131CBCB - 48 D1 F8              - sar rax,1
victoria3.exe+131CBCE - 49 8B FF              - mov rdi,r15
victoria3.exe+131CBD1 - 48 2B F8              - sub rdi,rax
victoria3.exe+131CBD4 - 48 B8 FFFFFFFFFFFFFF7F - mov rax,7FFFFFFFFFFFFFFF
victoria3.exe+131CBDE - 48 3B F8              - cmp rdi,rax
victoria3.exe+131CBE1 - 48 0F4C C7            - cmovl rax,rdi
victoria3.exe+131CBE5 - 48 83 FF 0C           - cmp rdi,0C
victoria3.exe+131CBE9 - 76 4F                 - jna victoria3.exe+131CC3A
victoria3.exe+131CBEB - 48 8B F8              - mov rdi,rax
victoria3.exe+131CBEE - 48 B8 CCCCCCCCCCCCCC00 - mov rax,00CCCCCCCCCCCCCC
victoria3.exe+131CBF8 - 48 3B F8              - cmp rdi,rax
victoria3.exe+131CBFB - 77 38                 - ja victoria3.exe+131CC35
victoria3.exe+131CBFD - 48 85 FF              - test rdi,rdi
victoria3.exe+131CC00 - 7E 33                 - jle victoria3.exe+131CC35
victoria3.exe+131CC02 - 48 8D 0C BF           - lea rcx,[rdi+rdi*4]
victoria3.exe+131CC06 - 48 C1 E1 06           - shl rcx,06
victoria3.exe+131CC0A - E8 912EE002           - call victoria3.exe+411FAA0
victoria3.exe+131CC0F - 48 8B F0              - mov rsi,rax
victoria3.exe+131CC12 - 48 85 C0              - test rax,rax
victoria3.exe+131CC15 - 75 07                 - jne victoria3.exe+131CC1E
victoria3.exe+131CC17 - 48 D1 EF              - shr rdi,1
victoria3.exe+131CC1A - 75 E6                 - jne victoria3.exe+131CC02
victoria3.exe+131CC1C - EB 17                 - jmp victoria3.exe+131CC35
victoria3.exe+131CC1E - 48 83 FF 0C           - cmp rdi,0C
victoria3.exe+131CC22 - 76 09                 - jna victoria3.exe+131CC2D
victoria3.exe+131CC24 - 48 89 85 E0020000     - mov [rbp+000002E0],rax
victoria3.exe+131CC2B - EB 1B                 - jmp victoria3.exe+131CC48
victoria3.exe+131CC2D - 48 8B C8              - mov rcx,rax
victoria3.exe+131CC30 - E8 FB36E002           - call victoria3.exe+4120330
victoria3.exe+131CC35 - BF 0C000000           - mov edi,0000000C
victoria3.exe+131CC3A - 48 8D B5 F0020000     - lea rsi,[rbp+000002F0]
victoria3.exe+131CC41 - 48 89 B5 E0020000     - mov [rbp+000002E0],rsi
victoria3.exe+131CC48 - 48 89 BD E8020000     - mov [rbp+000002E8],rdi
victoria3.exe+131CC4F - 4D 8B EF              - mov r13,r15
victoria3.exe+131CC52 - 49 D1 FD              - sar r13,1
victoria3.exe+131CC55 - 4D 2B FD              - sub r15,r13
victoria3.exe+131CC58 - 4F 8D 24 BF           - lea r12,[r15+r15*4]
victoria3.exe+131CC5C - 49 C1 E4 06           - shl r12,06
victoria3.exe+131CC60 - 4D 03 E6              - add r12,r14
victoria3.exe+131CC63 - 0FB6 9D 50120000      - movzx ebx,byte ptr [rbp+00001250]
victoria3.exe+131CC6A - 4C 8B CE              - mov r9,rsi
victoria3.exe+131CC6D - 4D 8B C7              - mov r8,r15
victoria3.exe+131CC70 - 49 8B D4              - mov rdx,r12
victoria3.exe+131CC73 - 49 8B CE              - mov rcx,r14
victoria3.exe+131CC76 - 4C 3B FF              - cmp r15,rdi
victoria3.exe+131CC79 - 7F 24                 - jg victoria3.exe+131CC9F
victoria3.exe+131CC7B - 88 5C 24 20           - mov [rsp+20],bl
victoria3.exe+131CC7F - E8 0CEE0000           - call victoria3.exe+132BA90
victoria3.exe+131CC84 - 88 5C 24 20           - mov [rsp+20],bl
victoria3.exe+131CC88 - 4C 8B CE              - mov r9,rsi
victoria3.exe+131CC8B - 4D 8B C5              - mov r8,r13
victoria3.exe+131CC8E - 48 8B 95 58120000     - mov rdx,[rbp+00001258]
victoria3.exe+131CC95 - 49 8B CC              - mov rcx,r12
victoria3.exe+131CC98 - E8 F3ED0000           - call victoria3.exe+132BA90
victoria3.exe+131CC9D - EB 2C                 - jmp victoria3.exe+131CCCB
victoria3.exe+131CC9F - 88 5C 24 28           - mov [rsp+28],bl
victoria3.exe+131CCA3 - 48 89 7C 24 20        - mov [rsp+20],rdi
victoria3.exe+131CCA8 - E8 53C00000           - call victoria3.exe+1328D00
victoria3.exe+131CCAD - 88 5C 24 28           - mov [rsp+28],bl
victoria3.exe+131CCB1 - 48 89 7C 24 20        - mov [rsp+20],rdi
victoria3.exe+131CCB6 - 4C 8B CE              - mov r9,rsi
victoria3.exe+131CCB9 - 4D 8B C5              - mov r8,r13
victoria3.exe+131CCBC - 48 8B 95 58120000     - mov rdx,[rbp+00001258]
victoria3.exe+131CCC3 - 49 8B CC              - mov rcx,r12
victoria3.exe+131CCC6 - E8 35C00000           - call victoria3.exe+1328D00
victoria3.exe+131CCCB - 88 5C 24 38           - mov [rsp+38],bl
victoria3.exe+131CCCF - 48 89 7C 24 30        - mov [rsp+30],rdi
victoria3.exe+131CCD4 - 48 89 74 24 28        - mov [rsp+28],rsi
victoria3.exe+131CCD9 - 4C 89 6C 24 20        - mov [rsp+20],r13
victoria3.exe+131CCDE - 4D 8B CF              - mov r9,r15
victoria3.exe+131CCE1 - 4C 8B 85 58120000     - mov r8,[rbp+00001258]
victoria3.exe+131CCE8 - 49 8B D4              - mov rdx,r12
victoria3.exe+131CCEB - 49 8B CE              - mov rcx,r14
victoria3.exe+131CCEE - E8 2DF00000           - call victoria3.exe+132BD20
victoria3.exe+131CCF3 - 90                    - nop 
victoria3.exe+131CCF4 - 48 83 BD E8020000 0C  - cmp qword ptr [rbp+000002E8],0C
victoria3.exe+131CCFC - 76 11                 - jna victoria3.exe+131CD0F
victoria3.exe+131CCFE - 48 8B 8D E0020000     - mov rcx,[rbp+000002E0]
victoria3.exe+131CD05 - 48 85 C9              - test rcx,rcx
victoria3.exe+131CD08 - 74 05                 - je victoria3.exe+131CD0F
victoria3.exe+131CD0A - E8 2136E002           - call victoria3.exe+4120330
victoria3.exe+131CD0F - 48 8D 1D 42C10A03     - lea rbx,[victoria3.exe+43C8E58]
victoria3.exe+131CD16 - 48 89 9D E0000000     - mov [rbp+000000E0],rbx
victoria3.exe+131CD1D - 48 8D 8D E8000000     - lea rcx,[rbp+000000E8]
victoria3.exe+131CD24 - C5F877                - vzeroupper 
victoria3.exe+131CD27 - E8 74552FFF           - call victoria3.exe+6122A0
victoria3.exe+131CD2C - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+131CD30 - C5F81185 00 010000    - vmovups [rbp+00000100],xmm0
victoria3.exe+131CD38 - 48 8D 8D 10010000     - lea rcx,[rbp+00000110]
victoria3.exe+131CD3F - E8 5C552FFF           - call victoria3.exe+6122A0
victoria3.exe+131CD44 - 45 33 ED              - xor r13d,r13d
victoria3.exe+131CD47 - 44 89 AD 28010000     - mov [rbp+00000128],r13d
victoria3.exe+131CD4E - 48 89 9D 90000000     - mov [rbp+00000090],rbx
victoria3.exe+131CD55 - 48 8D 8D 98000000     - lea rcx,[rbp+00000098]
victoria3.exe+131CD5C - E8 3F552FFF           - call victoria3.exe+6122A0
victoria3.exe+131CD61 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+131CD65 - C5F81185 B0 000000    - vmovups [rbp+000000B0],xmm0
victoria3.exe+131CD6D - 48 8D 8D C0000000     - lea rcx,[rbp+000000C0]
victoria3.exe+131CD74 - E8 27552FFF           - call victoria3.exe+6122A0
victoria3.exe+131CD79 - 44 89 AD D8000000     - mov [rbp+000000D8],r13d
victoria3.exe+131CD80 - 48 89 5D 40           - mov [rbp+40],rbx
victoria3.exe+131CD84 - 48 8D 4D 48           - lea rcx,[rbp+48]
victoria3.exe+131CD88 - E8 13552FFF           - call victoria3.exe+6122A0
victoria3.exe+131CD8D - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+131CD91 - C5F81145 60           - vmovups [rbp+60],xmm0
victoria3.exe+131CD96 - 48 8D 4D 70           - lea rcx,[rbp+70]
victoria3.exe+131CD9A - E8 01552FFF           - call victoria3.exe+6122A0
victoria3.exe+131CD9F - 44 89 AD 88000000     - mov [rbp+00000088],r13d
victoria3.exe+131CDA6 - 48 89 5D F0           - mov [rbp-10],rbx
victoria3.exe+131CDAA - 48 8D 4D F8           - lea rcx,[rbp-08]
victoria3.exe+131CDAE - E8 ED542FFF           - call victoria3.exe+6122A0
victoria3.exe+131CDB3 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+131CDB7 - C5F81145 10           - vmovups [rbp+10],xmm0
victoria3.exe+131CDBC - 48 8D 4D 20           - lea rcx,[rbp+20]
victoria3.exe+131CDC0 - E8 DB542FFF           - call victoria3.exe+6122A0
victoria3.exe+131CDC5 - 44 89 6D 38           - mov [rbp+38],r13d
victoria3.exe+131CDC9 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+131CDCD - 33 C0                 - xor eax,eax
victoria3.exe+131CDCF - C5FC1145 B0           - vmovups [rbp-50],ymm0
victoria3.exe+131CDD4 - 48 89 45 D0           - mov [rbp-30],rax
victoria3.exe+131CDD8 - 48 8D 05 2903DD03     - lea rax,[victoria3.exe+50ED108]
victoria3.exe+131CDDF - 48 89 45 B8           - mov [rbp-48],rax
victoria3.exe+131CDE3 - 4C 89 6D C0           - mov [rbp-40],r13
victoria3.exe+131CDE7 - 44 88 6D C8           - mov [rbp-38],r13b
victoria3.exe+131CDEB - C5FA1005 C9 8C4E03    - vmovss xmm0,[victoria3.exe+4805ABC]
victoria3.exe+131CDF3 - C5FA1145 CC           - vmovss [rbp-34],xmm0
victoria3.exe+131CDF8 - 48 8B 85 60120000     - mov rax,[rbp+00001260]
victoria3.exe+131CDFF - B9 40000000           - mov ecx,00000040
victoria3.exe+131CE04 - 8B 04 01              - mov eax,[rcx+rax]
victoria3.exe+131CE07 - 39 05 F38B5604        - cmp [victoria3.exe+5885A00],eax
victoria3.exe+131CE0D - 0F8F B8060000         - jg victoria3.exe+131D4CB
victoria3.exe+131CE13 - 48 8D 05 A60FDA03     - lea rax,[victoria3.exe+50BDDC0]
victoria3.exe+131CE1A - 48 89 45 D0           - mov [rbp-30],rax
victoria3.exe+131CE1E - 44 8B 74 24 4C        - mov r14d,[rsp+4C]
victoria3.exe+131CE23 - 45 85 F6              - test r14d,r14d
victoria3.exe+131CE26 - 0F8E 7D000000         - jng victoria3.exe+131CEA9
victoria3.exe+131CE2C - C5FA1015 AC 8C4E03    - vmovss xmm2,[victoria3.exe+4805AE0]
victoria3.exe+131CE34 - C5EA5E45 CC           - vdivss xmm0,xmm2,[rbp-34]
victoria3.exe+131CE39 - C5FA5F0D 37 8D4E03    - vmaxss xmm1,xmm0,[victoria3.exe+4805B78]
victoria3.exe+131CE41 - C5F857C0              - vxorps xmm0,xmm0,xmm0
victoria3.exe+131CE45 - C4C17A2AC6            - vcvtsi2ss xmm0,xmm0,r14d
victoria3.exe+131CE4A - C5F259C8              - vmulss xmm1,xmm1,xmm0
victoria3.exe+131CE4E - C5F258D2              - vaddss xmm2,xmm1,xmm2
victoria3.exe+131CE52 - C5FA2CC2              - vcvttss2si eax,xmm2
victoria3.exe+131CE56 - 83 F8 01              - cmp eax,01
victoria3.exe+131CE59 - 7F 05                 - jg victoria3.exe+131CE60
victoria3.exe+131CE5B - 41 8B CD              - mov ecx,r13d
victoria3.exe+131CE5E - EB 19                 - jmp victoria3.exe+131CE79
victoria3.exe+131CE60 - FF C8                 - dec eax
victoria3.exe+131CE62 - B9 20000000           - mov ecx,00000020
victoria3.exe+131CE67 - 0FBD D0               - bsr edx,eax
victoria3.exe+131CE6A - 74 09                 - je victoria3.exe+131CE75
victoria3.exe+131CE6C - B8 1F000000           - mov eax,0000001F
victoria3.exe+131CE71 - 2B C2                 - sub eax,edx
victoria3.exe+131CE73 - EB 02                 - jmp victoria3.exe+131CE77
victoria3.exe+131CE75 - 8B C1                 - mov eax,ecx
victoria3.exe+131CE77 - 2B C8                 - sub ecx,eax
victoria3.exe+131CE79 - BA 03000000           - mov edx,00000003
victoria3.exe+131CE7E - 3B CA                 - cmp ecx,edx
victoria3.exe+131CE80 - 0F4F D1               - cmovg edx,ecx
victoria3.exe+131CE83 - 8B CA                 - mov ecx,edx
victoria3.exe+131CE85 - 41 B8 01000000        - mov r8d,00000001
victoria3.exe+131CE8B - 41 D3 E0              - shl r8d,cl
victoria3.exe+131CE8E - 8B 45 C4              - mov eax,[rbp-3C]
victoria3.exe+131CE91 - FF C0                 - inc eax
victoria3.exe+131CE93 - 44 3B C0              - cmp r8d,eax
victoria3.exe+131CE96 - 7E 11                 - jle victoria3.exe+131CEA9
victoria3.exe+131CE98 - 48 8D 4D B0           - lea rcx,[rbp-50]
victoria3.exe+131CE9C - C5F877                - vzeroupper 
victoria3.exe+131CE9F - E8 FCCA0000           - call victoria3.exe+13299A0
victoria3.exe+131CEA4 - 44 8B 74 24 4C        - mov r14d,[rsp+4C]
victoria3.exe+131CEA9 - 48 8D 35 D08C0B03     - lea rsi,[victoria3.exe+43D5B80]
victoria3.exe+131CEB0 - 49 BF 6766666666666666 - mov r15,6666666666666667
victoria3.exe+131CEBA - 45 32 E4              - xor r12b,r12b
victoria3.exe+131CEBD - 49 63 C6              - movsxd  rax,r14d
victoria3.exe+131CEC0 - 48 8D 3C 80           - lea rdi,[rax+rax*4]
victoria3.exe+131CEC4 - 48 C1 E7 06           - shl rdi,06
victoria3.exe+131CEC8 - 4C 8B 4C 24 40        - mov r9,[rsp+40]
victoria3.exe+131CECD - 49 03 F9              - add rdi,r9
victoria3.exe+131CED0 - 4C 3B CF              - cmp r9,rdi
victoria3.exe+131CED3 - 0F84 13010000         - je victoria3.exe+131CFEC
victoria3.exe+131CED9 - 49 8D 59 04           - lea rbx,[r9+04]
victoria3.exe+131CEDD - 0F1F 00               - nop dword ptr [rax]
victoria3.exe+131CEE0 - 83 3B 00              - cmp dword ptr [rbx],00
victoria3.exe+131CEE3 - 0F8F E5000000         - jg victoria3.exe+131CFCE
victoria3.exe+131CEE9 - 48 81 EF 40010000     - sub rdi,00000140
victoria3.exe+131CEF0 - 8B 07                 - mov eax,[rdi]
victoria3.exe+131CEF2 - 89 43 FC              - mov [rbx-04],eax
victoria3.exe+131CEF5 - 8B 47 04              - mov eax,[rdi+04]
victoria3.exe+131CEF8 - 89 03                 - mov [rbx],eax
victoria3.exe+131CEFA - 8B 47 08              - mov eax,[rdi+08]
victoria3.exe+131CEFD - 89 43 04              - mov [rbx+04],eax
victoria3.exe+131CF00 - 8B 47 0C              - mov eax,[rdi+0C]
victoria3.exe+131CF03 - 89 43 08              - mov [rbx+08],eax
victoria3.exe+131CF06 - 48 8D 57 18           - lea rdx,[rdi+18]
victoria3.exe+131CF0A - 48 8D 4B 14           - lea rcx,[rbx+14]
victoria3.exe+131CF0E - C5F877                - vzeroupper 
victoria3.exe+131CF11 - E8 4A478BFF           - call victoria3.exe+BD1660
victoria3.exe+131CF16 - C5F81047 30           - vmovups xmm0,[rdi+30]
victoria3.exe+131CF1B - C5F81143 2C           - vmovups [rbx+2C],xmm0
victoria3.exe+131CF20 - 48 8D 57 40           - lea rdx,[rdi+40]
victoria3.exe+131CF24 - 48 8D 4B 3C           - lea rcx,[rbx+3C]
victoria3.exe+131CF28 - E8 239592FF           - call victoria3.exe+C46450
victoria3.exe+131CF2D - 8B 47 58              - mov eax,[rdi+58]
victoria3.exe+131CF30 - 89 43 54              - mov [rbx+54],eax
victoria3.exe+131CF33 - 48 8D 57 68           - lea rdx,[rdi+68]
victoria3.exe+131CF37 - 48 8D 4B 64           - lea rcx,[rbx+64]
victoria3.exe+131CF3B - E8 20478BFF           - call victoria3.exe+BD1660
victoria3.exe+131CF40 - C5F81087 80 000000    - vmovups xmm0,[rdi+00000080]
victoria3.exe+131CF48 - C5F81143 7C           - vmovups [rbx+7C],xmm0
victoria3.exe+131CF4D - 48 8D 97 90000000     - lea rdx,[rdi+00000090]
victoria3.exe+131CF54 - 48 8D 8B 8C000000     - lea rcx,[rbx+0000008C]
victoria3.exe+131CF5B - E8 F09492FF           - call victoria3.exe+C46450
victoria3.exe+131CF60 - 8B 87 A8000000        - mov eax,[rdi+000000A8]
victoria3.exe+131CF66 - 89 83 A4000000        - mov [rbx+000000A4],eax
victoria3.exe+131CF6C - C5FC1087 B0 000000    - vmovups ymm0,[rdi+000000B0]
victoria3.exe+131CF74 - C5FC1183 AC 000000    - vmovups [rbx+000000AC],ymm0
victoria3.exe+131CF7C - C5FC108F D0 000000    - vmovups ymm1,[rdi+000000D0]
victoria3.exe+131CF84 - C5FC118B CC 000000    - vmovups [rbx+000000CC],ymm1
victoria3.exe+131CF8C - C5FB1087 F0 000000    - vmovsd xmm0,[rdi+000000F0]
victoria3.exe+131CF94 - C5FB1183 EC 000000    - vmovsd [rbx+000000EC],xmm0
victoria3.exe+131CF9C - C5FC1087 F8 000000    - vmovups ymm0,[rdi+000000F8]
victoria3.exe+131CFA4 - C5FC1183 F4 000000    - vmovups [rbx+000000F4],ymm0
victoria3.exe+131CFAC - C5FC108F 18 010000    - vmovups ymm1,[rdi+00000118]
victoria3.exe+131CFB4 - C5FC118B 14 010000    - vmovups [rbx+00000114],ymm1
victoria3.exe+131CFBC - C5FB1087 38 010000    - vmovsd xmm0,[rdi+00000138]
victoria3.exe+131CFC4 - C5FB1183 34 010000    - vmovsd [rbx+00000134],xmm0
victoria3.exe+131CFCC - EB 07                 - jmp victoria3.exe+131CFD5
victoria3.exe+131CFCE - 48 81 C3 40010000     - add rbx,00000140
victoria3.exe+131CFD5 - 48 8D 43 FC           - lea rax,[rbx-04]
victoria3.exe+131CFD9 - 48 3B C7              - cmp rax,rdi
victoria3.exe+131CFDC - 0F85 FEFEFFFF         - jne victoria3.exe+131CEE0
victoria3.exe+131CFE2 - 44 8B 74 24 4C        - mov r14d,[rsp+4C]
victoria3.exe+131CFE7 - 4C 8B 4C 24 40        - mov r9,[rsp+40]
victoria3.exe+131CFEC - 49 2B F9              - sub rdi,r9
victoria3.exe+131CFEF - 49 8B C7              - mov rax,r15
victoria3.exe+131CFF2 - 48 F7 EF              - imul rdi
victoria3.exe+131CFF5 - 48 8B FA              - mov rdi,rdx
victoria3.exe+131CFF8 - 48 C1 FF 07           - sar rdi,07
victoria3.exe+131CFFC - 48 8B C7              - mov rax,rdi
victoria3.exe+131CFFF - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+131D003 - 48 03 F8              - add rdi,rax
victoria3.exe+131D006 - 45 8B FE              - mov r15d,r14d
victoria3.exe+131D009 - 44 2B FF              - sub r15d,edi
victoria3.exe+131D00C - 45 85 FF              - test r15d,r15d
victoria3.exe+131D00F - 7E 70                 - jle victoria3.exe+131D081
victoria3.exe+131D011 - 49 63 C6              - movsxd  rax,r14d
victoria3.exe+131D014 - 48 8D 0C 80           - lea rcx,[rax+rax*4]
victoria3.exe+131D018 - 48 C1 E1 06           - shl rcx,06
victoria3.exe+131D01C - 49 03 C9              - add rcx,r9
victoria3.exe+131D01F - 48 63 C7              - movsxd  rax,edi
victoria3.exe+131D022 - 4C 8D 04 80           - lea r8,[rax+rax*4]
victoria3.exe+131D026 - 49 C1 E0 06           - shl r8,06
victoria3.exe+131D02A - 4D 03 C1              - add r8,r9
victoria3.exe+131D02D - 48 8B D1              - mov rdx,rcx
victoria3.exe+131D030 - C5F877                - vzeroupper 
victoria3.exe+131D033 - E8 78FF0000           - call victoria3.exe+132CFB0
victoria3.exe+131D038 - 8B 74 24 4C           - mov esi,[rsp+4C]
victoria3.exe+131D03C - 8B DE                 - mov ebx,esi
victoria3.exe+131D03E - 41 2B DE              - sub ebx,r14d
victoria3.exe+131D041 - 03 DF                 - add ebx,edi
victoria3.exe+131D043 - 3B DE                 - cmp ebx,esi
victoria3.exe+131D045 - 7D 29                 - jnl victoria3.exe+131D070
victoria3.exe+131D047 - 48 63 C3              - movsxd  rax,ebx
victoria3.exe+131D04A - 48 8D 3C 80           - lea rdi,[rax+rax*4]
victoria3.exe+131D04E - 48 C1 E7 06           - shl rdi,06
victoria3.exe+131D052 - 48 8B 4C 24 40        - mov rcx,[rsp+40]
victoria3.exe+131D057 - 48 03 CF              - add rcx,rdi
victoria3.exe+131D05A - E8 31CE0000           - call victoria3.exe+1329E90
victoria3.exe+131D05F - FF C3                 - inc ebx
victoria3.exe+131D061 - 48 81 C7 40010000     - add rdi,00000140
victoria3.exe+131D068 - 3B DE                 - cmp ebx,esi
victoria3.exe+131D06A - 7C E6                 - jl victoria3.exe+131D052
victoria3.exe+131D06C - 8B 74 24 4C           - mov esi,[rsp+4C]
victoria3.exe+131D070 - 41 2B F7              - sub esi,r15d
victoria3.exe+131D073 - 89 74 24 4C           - mov [rsp+4C],esi
victoria3.exe+131D077 - 44 8B F6              - mov r14d,esi
victoria3.exe+131D07A - 48 8D 35 FF8A0B03     - lea rsi,[victoria3.exe+43D5B80]
victoria3.exe+131D081 - C7 44 24 70 22040000  - mov [rsp+70],00000422
victoria3.exe+131D089 - C7 44 24 74 03000000  - mov [rsp+74],00000003
victoria3.exe+131D091 - 4C 8D 3D 00811603     - lea r15,[victoria3.exe+4485198]
victoria3.exe+131D098 - 4C 89 7C 24 78        - mov [rsp+78],r15
victoria3.exe+131D09D - 48 8D 05 FCA91203     - lea rax,[victoria3.exe+4447AA0]
victoria3.exe+131D0A4 - 48 89 45 80           - mov [rbp-80],rax
victoria3.exe+131D0A8 - 48 8D 44 24 40        - lea rax,[rsp+40]
victoria3.exe+131D0AD - 48 89 85 70020000     - mov [rbp+00000270],rax
victoria3.exe+131D0B4 - 48 8D 45 B0           - lea rax,[rbp-50]
victoria3.exe+131D0B8 - 48 89 85 78020000     - mov [rbp+00000278],rax
victoria3.exe+131D0BF - 48 8D 85 E0000000     - lea rax,[rbp+000000E0]
victoria3.exe+131D0C6 - 48 89 85 80020000     - mov [rbp+00000280],rax
victoria3.exe+131D0CD - 48 8D 85 90000000     - lea rax,[rbp+00000090]
victoria3.exe+131D0D4 - 48 89 85 88020000     - mov [rbp+00000288],rax
victoria3.exe+131D0DB - 48 8D 45 40           - lea rax,[rbp+40]
victoria3.exe+131D0DF - 48 89 85 90020000     - mov [rbp+00000290],rax
victoria3.exe+131D0E6 - 48 8D 45 F0           - lea rax,[rbp-10]
victoria3.exe+131D0EA - 48 89 85 98020000     - mov [rbp+00000298],rax
victoria3.exe+131D0F1 - 48 8D 85 50120000     - lea rax,[rbp+00001250]
victoria3.exe+131D0F8 - 48 89 85 A0020000     - mov [rbp+000002A0],rax
victoria3.exe+131D0FF - 48 8B 0D 72C65C04     - mov rcx,[victoria3.exe+58E9778]
victoria3.exe+131D106 - 48 89 4D 90           - mov [rbp-70],rcx
victoria3.exe+131D10A - 48 C7 45 98 01000000  - mov qword ptr [rbp-68],00000001
victoria3.exe+131D112 - 44 89 75 A0           - mov [rbp-60],r14d
victoria3.exe+131D116 - 48 85 C9              - test rcx,rcx
victoria3.exe+131D119 - 75 07                 - jne victoria3.exe+131D122
victoria3.exe+131D11B - B9 01000000           - mov ecx,00000001
victoria3.exe+131D120 - EB 09                 - jmp victoria3.exe+131D12B
victoria3.exe+131D122 - 8B 89 48060000        - mov ecx,[rcx+00000648]
victoria3.exe+131D128 - 90                    - nop 
victoria3.exe+131D129 - FF C1                 - inc ecx
victoria3.exe+131D12B - 89 4D A4              - mov [rbp-5C],ecx
victoria3.exe+131D12E - 41 8B C6              - mov eax,r14d
victoria3.exe+131D131 - 99                    - cdq 
victoria3.exe+131D132 - F7 F9                 - idiv ecx
victoria3.exe+131D134 - 8B C8                 - mov ecx,eax
victoria3.exe+131D136 - B8 56555555           - mov eax,55555556
victoria3.exe+131D13B - F7 E9                 - imul ecx
victoria3.exe+131D13D - 8B C2                 - mov eax,edx
victoria3.exe+131D13F - C1 E8 1F              - shr eax,1F
victoria3.exe+131D142 - 03 D0                 - add edx,eax
victoria3.exe+131D144 - B8 01000000           - mov eax,00000001
victoria3.exe+131D149 - 3B D0                 - cmp edx,eax
victoria3.exe+131D14B - 0F4F C2               - cmovg eax,edx
victoria3.exe+131D14E - 89 45 A8              - mov [rbp-58],eax
victoria3.exe+131D151 - C7 45 AC 01000000     - mov [rbp-54],00000001
victoria3.exe+131D158 - 48 8D 44 24 70        - lea rax,[rsp+70]
victoria3.exe+131D15D - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+131D162 - 48 8D 95 70020000     - lea rdx,[rbp+00000270]
victoria3.exe+131D169 - 48 8D 4D 90           - lea rcx,[rbp-70]
victoria3.exe+131D16D - C5F877                - vzeroupper 
victoria3.exe+131D170 - E8 0B910000           - call victoria3.exe+1326280
victoria3.exe+131D175 - 48 63 44 24 4C        - movsxd  rax,dword ptr [rsp+4C]
victoria3.exe+131D17A - 48 8D 3C 80           - lea rdi,[rax+rax*4]
victoria3.exe+131D17E - 48 C1 E7 06           - shl rdi,06
victoria3.exe+131D182 - 48 8B 5C 24 40        - mov rbx,[rsp+40]
victoria3.exe+131D187 - 48 03 FB              - add rdi,rbx
victoria3.exe+131D18A - 48 3B DF              - cmp rbx,rdi
victoria3.exe+131D18D - 0F84 A2000000         - je victoria3.exe+131D235
victoria3.exe+131D193 - 48 83 C3 0E           - add rbx,0E
victoria3.exe+131D197 - 66 0F1F 84 00 00000000  - nop word ptr [rax+rax+00000000]
victoria3.exe+131D1A0 - 4C 8D 4B FE           - lea r9,[rbx-02]
victoria3.exe+131D1A4 - 41 0FB6 01            - movzx eax,byte ptr [r9]
victoria3.exe+131D1A8 - 35 C59D1C81           - xor eax,811C9DC5
victoria3.exe+131D1AD - 69 C8 93010001        - imul ecx,eax,01000193
victoria3.exe+131D1B3 - 0FB6 43 FF            - movzx eax,byte ptr [rbx-01]
victoria3.exe+131D1B7 - 33 C8                 - xor ecx,eax
victoria3.exe+131D1B9 - 69 D1 93010001        - imul edx,ecx,01000193
victoria3.exe+131D1BF - 0FB6 03               - movzx eax,byte ptr [rbx]
victoria3.exe+131D1C2 - 33 D0                 - xor edx,eax
victoria3.exe+131D1C4 - 69 CA 93010001        - imul ecx,edx,01000193
victoria3.exe+131D1CA - 0FB6 43 01            - movzx eax,byte ptr [rbx+01]
victoria3.exe+131D1CE - 33 C8                 - xor ecx,eax
victoria3.exe+131D1D0 - 44 69 C1 93010001     - imul r8d,ecx,01000193
victoria3.exe+131D1D7 - 48 8D 55 D8           - lea rdx,[rbp-28]
victoria3.exe+131D1DB - 48 8D 4D B0           - lea rcx,[rbp-50]
victoria3.exe+131D1DF - E8 1CEF0000           - call victoria3.exe+132C100
victoria3.exe+131D1E4 - 48 8B 55 D8           - mov rdx,[rbp-28]
victoria3.exe+131D1E8 - 48 83 C2 10           - add rdx,10
victoria3.exe+131D1EC - 4C 8D 42 50           - lea r8,[rdx+50]
victoria3.exe+131D1F0 - 48 8D 4B F2           - lea rcx,[rbx-0E]
victoria3.exe+131D1F4 - 48 8D 45 F0           - lea rax,[rbp-10]
victoria3.exe+131D1F8 - 48 89 44 24 30        - mov [rsp+30],rax
victoria3.exe+131D1FD - 48 8D 45 40           - lea rax,[rbp+40]
victoria3.exe+131D201 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+131D206 - 48 8D 85 90000000     - lea rax,[rbp+00000090]
victoria3.exe+131D20D - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+131D212 - 4C 8D 8D E0000000     - lea r9,[rbp+000000E0]
victoria3.exe+131D219 - E8 5202EEFF           - call victoria3.exe+11FD470
victoria3.exe+131D21E - 44 0A E0              - or r12b,al
victoria3.exe+131D221 - 48 8D 9B 40010000     - lea rbx,[rbx+00000140]
victoria3.exe+131D228 - 48 8D 43 F2           - lea rax,[rbx-0E]
victoria3.exe+131D22C - 48 3B C7              - cmp rax,rdi
victoria3.exe+131D22F - 0F85 6BFFFFFF         - jne victoria3.exe+131D1A0
victoria3.exe+131D235 - 80 3D 29B45604 00     - cmp byte ptr [victoria3.exe+5888665],00
victoria3.exe+131D23C - 74 0D                 - je victoria3.exe+131D24B
victoria3.exe+131D23E - 80 3D 0C0CDA03 00     - cmp byte ptr [victoria3.exe+50BDE51],00
victoria3.exe+131D245 - 74 04                 - je victoria3.exe+131D24B
victoria3.exe+131D247 - B2 01                 - mov dl,01
victoria3.exe+131D249 - EB 02                 - jmp victoria3.exe+131D24D
victoria3.exe+131D24B - 32 D2                 - xor dl,dl
victoria3.exe+131D24D - 48 89 74 24 58        - mov [rsp+58],rsi
victoria3.exe+131D252 - C7 44 24 60 13000000  - mov [rsp+60],00000013
victoria3.exe+131D25A - C6 44 24 64 00        - mov byte ptr [rsp+64],00
victoria3.exe+131D25F - 4C 8D 4C 24 58        - lea r9,[rsp+58]
victoria3.exe+131D264 - 41 B0 01              - mov r8b,01
victoria3.exe+131D267 - 48 8D 8D 70020000     - lea rcx,[rbp+00000270]
victoria3.exe+131D26E - E8 9D6C49FF           - call victoria3.exe+7B3F10
victoria3.exe+131D273 - 48 8D 8D 70020000     - lea rcx,[rbp+00000270]
victoria3.exe+131D27A - E8 116E49FF           - call victoria3.exe+7B4090
victoria3.exe+131D27F - 45 84 E4              - test r12b,r12b
victoria3.exe+131D282 - 74 0A                 - je victoria3.exe+131D28E
victoria3.exe+131D284 - 44 8B 74 24 4C        - mov r14d,[rsp+4C]
victoria3.exe+131D289 - E9 22FCFFFF           - jmp victoria3.exe+131CEB0
victoria3.exe+131D28E - C7 44 24 70 41040000  - mov [rsp+70],00000441
victoria3.exe+131D296 - C7 44 24 74 02000000  - mov [rsp+74],00000002
victoria3.exe+131D29E - 4C 89 7C 24 78        - mov [rsp+78],r15
victoria3.exe+131D2A3 - 48 8D 05 F6A71203     - lea rax,[victoria3.exe+4447AA0]
victoria3.exe+131D2AA - 48 89 45 80           - mov [rbp-80],rax
victoria3.exe+131D2AE - 48 8B 85 68120000     - mov rax,[rbp+00001268]
victoria3.exe+131D2B5 - 48 89 44 24 58        - mov [rsp+58],rax
victoria3.exe+131D2BA - 48 8B 0D B7C45C04     - mov rcx,[victoria3.exe+58E9778]
victoria3.exe+131D2C1 - 8B 40 0C              - mov eax,[rax+0C]
victoria3.exe+131D2C4 - 48 89 4D 90           - mov [rbp-70],rcx
victoria3.exe+131D2C8 - 48 C7 45 98 01000000  - mov qword ptr [rbp-68],00000001
victoria3.exe+131D2D0 - 89 45 A0              - mov [rbp-60],eax
victoria3.exe+131D2D3 - 48 85 C9              - test rcx,rcx
victoria3.exe+131D2D6 - 75 07                 - jne victoria3.exe+131D2DF
victoria3.exe+131D2D8 - B9 01000000           - mov ecx,00000001
victoria3.exe+131D2DD - EB 09                 - jmp victoria3.exe+131D2E8
victoria3.exe+131D2DF - 8B 89 48060000        - mov ecx,[rcx+00000648]
victoria3.exe+131D2E5 - 90                    - nop 
victoria3.exe+131D2E6 - FF C1                 - inc ecx
victoria3.exe+131D2E8 - 89 4D A4              - mov [rbp-5C],ecx
victoria3.exe+131D2EB - 99                    - cdq 
victoria3.exe+131D2EC - F7 F9                 - idiv ecx
victoria3.exe+131D2EE - 8B C8                 - mov ecx,eax
victoria3.exe+131D2F0 - B8 56555555           - mov eax,55555556
victoria3.exe+131D2F5 - F7 E9                 - imul ecx
victoria3.exe+131D2F7 - 8B C2                 - mov eax,edx
victoria3.exe+131D2F9 - C1 E8 1F              - shr eax,1F
victoria3.exe+131D2FC - 03 D0                 - add edx,eax
victoria3.exe+131D2FE - B8 01000000           - mov eax,00000001
victoria3.exe+131D303 - 3B D0                 - cmp edx,eax
victoria3.exe+131D305 - 0F4F C2               - cmovg eax,edx
victoria3.exe+131D308 - 89 45 A8              - mov [rbp-58],eax
victoria3.exe+131D30B - C7 45 AC 01000000     - mov [rbp-54],00000001
victoria3.exe+131D312 - 48 8D 44 24 70        - lea rax,[rsp+70]
victoria3.exe+131D317 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+131D31C - 48 8D 54 24 58        - lea rdx,[rsp+58]
victoria3.exe+131D321 - 48 8D 4D 90           - lea rcx,[rbp-70]
victoria3.exe+131D325 - E8 06910000           - call victoria3.exe+1326430
victoria3.exe+131D32A - 90                    - nop 
victoria3.exe+131D32B - 48 8D 4D B0           - lea rcx,[rbp-50]
victoria3.exe+131D32F - E8 DC500000           - call victoria3.exe+1322410
victoria3.exe+131D334 - 90                    - nop 
victoria3.exe+131D335 - 48 8B 55 20           - mov rdx,[rbp+20]
victoria3.exe+131D339 - 48 85 D2              - test rdx,rdx
victoria3.exe+131D33C - 74 16                 - je victoria3.exe+131D354
victoria3.exe+131D33E - 44 89 6D 2C           - mov [rbp+2C],r13d
victoria3.exe+131D342 - 48 8B 4D 30           - mov rcx,[rbp+30]
victoria3.exe+131D346 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131D349 - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131D34C - 4C 89 6D 20           - mov [rbp+20],r13
victoria3.exe+131D350 - 44 89 6D 28           - mov [rbp+28],r13d
victoria3.exe+131D354 - 48 8B 55 F8           - mov rdx,[rbp-08]
victoria3.exe+131D358 - 48 85 D2              - test rdx,rdx
victoria3.exe+131D35B - 74 16                 - je victoria3.exe+131D373
victoria3.exe+131D35D - 44 89 6D 04           - mov [rbp+04],r13d
victoria3.exe+131D361 - 48 8B 4D 08           - mov rcx,[rbp+08]
victoria3.exe+131D365 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131D368 - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131D36B - 4C 89 6D F8           - mov [rbp-08],r13
victoria3.exe+131D36F - 44 89 6D 00           - mov [rbp+00],r13d
victoria3.exe+131D373 - 48 8B 55 70           - mov rdx,[rbp+70]
victoria3.exe+131D377 - 48 85 D2              - test rdx,rdx
victoria3.exe+131D37A - 74 19                 - je victoria3.exe+131D395
victoria3.exe+131D37C - 44 89 6D 7C           - mov [rbp+7C],r13d
victoria3.exe+131D380 - 48 8B 8D 80000000     - mov rcx,[rbp+00000080]
victoria3.exe+131D387 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131D38A - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131D38D - 4C 89 6D 70           - mov [rbp+70],r13
victoria3.exe+131D391 - 44 89 6D 78           - mov [rbp+78],r13d
victoria3.exe+131D395 - 48 8B 55 48           - mov rdx,[rbp+48]
victoria3.exe+131D399 - 48 85 D2              - test rdx,rdx
victoria3.exe+131D39C - 74 16                 - je victoria3.exe+131D3B4
victoria3.exe+131D39E - 44 89 6D 54           - mov [rbp+54],r13d
victoria3.exe+131D3A2 - 48 8B 4D 58           - mov rcx,[rbp+58]
victoria3.exe+131D3A6 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131D3A9 - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131D3AC - 4C 89 6D 48           - mov [rbp+48],r13
victoria3.exe+131D3B0 - 44 89 6D 50           - mov [rbp+50],r13d
victoria3.exe+131D3B4 - 48 8B 95 C0000000     - mov rdx,[rbp+000000C0]
victoria3.exe+131D3BB - 48 85 D2              - test rdx,rdx
victoria3.exe+131D3BE - 74 22                 - je victoria3.exe+131D3E2
victoria3.exe+131D3C0 - 44 89 AD CC000000     - mov [rbp+000000CC],r13d
victoria3.exe+131D3C7 - 48 8B 8D D0000000     - mov rcx,[rbp+000000D0]
victoria3.exe+131D3CE - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131D3D1 - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131D3D4 - 4C 89 AD C0000000     - mov [rbp+000000C0],r13
victoria3.exe+131D3DB - 44 89 AD C8000000     - mov [rbp+000000C8],r13d
victoria3.exe+131D3E2 - 48 8B 95 98000000     - mov rdx,[rbp+00000098]
victoria3.exe+131D3E9 - 48 85 D2              - test rdx,rdx
victoria3.exe+131D3EC - 74 22                 - je victoria3.exe+131D410
victoria3.exe+131D3EE - 44 89 AD A4000000     - mov [rbp+000000A4],r13d
victoria3.exe+131D3F5 - 48 8B 8D A8000000     - mov rcx,[rbp+000000A8]
victoria3.exe+131D3FC - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131D3FF - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131D402 - 4C 89 AD 98000000     - mov [rbp+00000098],r13
victoria3.exe+131D409 - 44 89 AD A0000000     - mov [rbp+000000A0],r13d
victoria3.exe+131D410 - 48 8B 95 10010000     - mov rdx,[rbp+00000110]
victoria3.exe+131D417 - 48 85 D2              - test rdx,rdx
victoria3.exe+131D41A - 74 22                 - je victoria3.exe+131D43E
victoria3.exe+131D41C - 44 89 AD 1C010000     - mov [rbp+0000011C],r13d
victoria3.exe+131D423 - 48 8B 8D 20010000     - mov rcx,[rbp+00000120]
victoria3.exe+131D42A - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131D42D - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131D430 - 4C 89 AD 10010000     - mov [rbp+00000110],r13
victoria3.exe+131D437 - 44 89 AD 18010000     - mov [rbp+00000118],r13d
victoria3.exe+131D43E - 48 8B 95 E8000000     - mov rdx,[rbp+000000E8]
victoria3.exe+131D445 - 48 85 D2              - test rdx,rdx
victoria3.exe+131D448 - 74 22                 - je victoria3.exe+131D46C
victoria3.exe+131D44A - 44 89 AD F4000000     - mov [rbp+000000F4],r13d
victoria3.exe+131D451 - 48 8B 8D F8000000     - mov rcx,[rbp+000000F8]
victoria3.exe+131D458 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131D45B - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131D45E - 4C 89 AD E8000000     - mov [rbp+000000E8],r13
victoria3.exe+131D465 - 44 89 AD F0000000     - mov [rbp+000000F0],r13d
victoria3.exe+131D46C - 48 8B 54 24 40        - mov rdx,[rsp+40]
victoria3.exe+131D471 - 48 85 D2              - test rdx,rdx
victoria3.exe+131D474 - 74 38                 - je victoria3.exe+131D4AE
victoria3.exe+131D476 - 8B 44 24 4C           - mov eax,[rsp+4C]
victoria3.exe+131D47A - 85 C0                 - test eax,eax
victoria3.exe+131D47C - 7E 20                 - jle victoria3.exe+131D49E
victoria3.exe+131D47E - 49 8B DD              - mov rbx,r13
victoria3.exe+131D481 - 8B F8                 - mov edi,eax
victoria3.exe+131D483 - 48 8D 0C 13           - lea rcx,[rbx+rdx]
victoria3.exe+131D487 - E8 04CA0000           - call victoria3.exe+1329E90
victoria3.exe+131D48C - 48 8D 9B 40010000     - lea rbx,[rbx+00000140]
victoria3.exe+131D493 - 48 83 EF 01           - sub rdi,01
victoria3.exe+131D497 - 48 8B 54 24 40        - mov rdx,[rsp+40]
victoria3.exe+131D49C - 75 E5                 - jne victoria3.exe+131D483
victoria3.exe+131D49E - 44 89 6C 24 4C        - mov [rsp+4C],r13d
victoria3.exe+131D4A3 - 48 8B 4C 24 50        - mov rcx,[rsp+50]
victoria3.exe+131D4A8 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+131D4AB - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+131D4AE - C5F828B4 24 F0 120000 - vmovaps xmm6,[rsp+000012F0]
victoria3.exe+131D4B7 - 48 81 C4 08130000     - add rsp,00001308
victoria3.exe+131D4BE - 41 5F                 - pop r15
victoria3.exe+131D4C0 - 41 5E                 - pop r14
victoria3.exe+131D4C2 - 41 5D                 - pop r13
victoria3.exe+131D4C4 - 41 5C                 - pop r12
victoria3.exe+131D4C6 - 5F                    - pop rdi
victoria3.exe+131D4C7 - 5E                    - pop rsi
victoria3.exe+131D4C8 - 5B                    - pop rbx
victoria3.exe+131D4C9 - 5D                    - pop rbp
victoria3.exe+131D4CA - C3                    - ret 


# +131D21E 函数整体伪代码（根据当前反汇编整理）

这一段函数的核心作用不是直接计算单个商品数量，而是建立/整理一个动态条目数组，然后遍历数组中的条目，计算条目标识并调用 `+11FD470`。因此它是目前发现的“遍历并进入单项容量处理函数”的强候选上层函数。

```text
function BuildAndProcessEntries(owner):
    RBX = owner

    // 建立较大的临时栈对象、上下文和若干容器。
    context = InitializeContext(owner)
    list = owner + 0xF0

    // 取得一个全局容器/资源表，并计算初始容量或桶数量。
    globalTable = [victoria3.exe+58E9778]
    elementCount = list.field_0C
    bucketCount = globalTable == null
        ? 1
        : globalTable.field_648 + 1

    // 下面的定点/整数除法最终得到至少为 1 的步长或批量大小。
    batchSize = max(floor(elementCount / bucketCount), 1)

    // 调用 +13260F0，初始化或扩展临时条目容器。
    container = InitializeContainer(
        list,
        owner + 0xF0,
        batchSize,
        context
    )

    // ------------------------------------------------------------
    // 第一阶段：遍历 owner+F0 指向的对象数组，筛选有效对象并建立条目。
    // ------------------------------------------------------------
    sourceBegin = [list]
    sourceCount = [list+0C]
    sourceEnd = sourceBegin + sourceCount * 8

    for sourceSlot from sourceBegin to sourceEnd step 8:
        sourceObject = [sourceSlot]
        if sourceObject == null:
            continue

        stateObject = ResolveObject(sourceObject)       // +1231B10
        if stateObject.field_E8 <= 0:
            continue

        // 读取 sourceObject+E48 对应的类型/索引值。
        typeValue = sourceObject.field_E48
        typeValue = NormalizeType(typeValue)             // +7B0AB0

        // 通过 +844150 读取一个属性，结果用于筛选。
        property = ReadProperty(
            sourceObject.field_E8 + 0x10,
            selector = [victoria3.exe+50D6DF4],
            output = temporary_value
        )
        if property <= 0:
            continue

        // +1210600 再读取一个关联值；返回值小于等于 0 时跳过。
        related = ReadRelatedValue(sourceObject, context)
        if related <= 0:
            continue

        // 比较当前索引与容器中的索引，必要时生成下一个索引。
        currentIndex = temporary_index
        if currentIndex == container.lastIndex:
            currentIndex = max(
                currentIndex + 1,
                truncate(container.lastIndex * XMM6)
            )

        // 从全局表取得一个槽位，并为当前条目分配/初始化记录。
        slot = AllocateSlot(globalTable, currentIndex)
        entry = CreateEntry(slot, sourceObject)           // +11FD230

        // 每个条目占 0x140 字节；复制或初始化条目的多个字段。
        CopyEntryFields(entry, sourceObject)

        // 条目数组索引递增，继续处理下一个源对象。
        container.lastIndex = currentIndex + 1

    // ------------------------------------------------------------
    // 第二阶段：完成容器长度调整，删除或移动不再需要的尾部条目。
    // ------------------------------------------------------------
    containerEnd = container.begin + container.count * 0x140
    entryCount = (containerEnd - container.begin) / 0x140

    if entryCount > 0x20:
        goto FINALIZE

    // 如果实际数量减少，调用 +132CFB0 调整区间，并删除多余记录。
    if entryCount changed:
        RemoveOrCompactRange(container, oldEnd, newEnd)

    // ------------------------------------------------------------
    // 第三阶段：重新遍历最终条目数组。
    // ------------------------------------------------------------
    processedCount = container.count
    entriesBegin = container.begin
    entriesEnd = entriesBegin + processedCount * 0x140

    if entriesBegin == entriesEnd:
        goto AFTER_PROCESSING

    // 这里的每个条目记录占 0x140 字节。
    for entryBase from entriesBegin to entriesEnd step 0x140:
        // +0x00/+0x04 等字段先被复制到临时栈结构，
        // 其中 +0x04 是后续 +11FD470 会减少或清零的候选字段。
        localEntry = CopyEntryToTemporary(entryBase)

        // 从条目头部的若干字节计算 32 位 FNV-1a 风格哈希。
        // 实际参与计算的字节是 entryBase-0x0E 到 entryBase-0x0B 附近。
        keyHash = 0x811C9DC5
        keyHash = (keyHash xor byte(entryBase-0x0E)) * 0x01000193
        keyHash = (keyHash xor byte(entryBase-0x0D)) * 0x01000193
        keyHash = (keyHash xor byte(entryBase-0x0C)) * 0x01000193
        keyHash = (keyHash xor byte(entryBase-0x0B)) * 0x01000193

        // +132C100 根据临时键/哈希取得关联上下文。
        associated = LookupAssociatedObject(
            temporary_map,
            keyHash,
            output = local_lookup
        )

        // 准备 +11FD470 的参数。
        // RCX = entryBase-0x0E，RDX/R8/R9 以及栈参数来自临时结构。
        result = ProcessEntry(
            entry = entryBase - 0x0E,
            arg2 = local_lookup,
            arg3 = entryBase + 0x42,
            arg4 = entryBase + 0x60,
            arg5 = rbp + 0x90,
            arg6 = rbp + 0x40,
            arg7 = rbp + 0xF0
        )                                      // call +11FD470

        anyProcessed = anyProcessed OR result

    // +131D21E 正是 +11FD470 返回后的汇合点。
    // AL 返回值被并入 R12B，用于表示本轮是否有条目发生处理。
    AFTER_PROCESSING:
    if debug_or_special_flags_enabled:
        EmitDebugOrSpecialEvent()

    return anyProcessed


// 结构和语义说明：
// 1. `+131D21E` 本身只有 `or r12b,al`，它不是计算指令；真正的单项处理
//    发生在上一条 call 的 `+11FD470`。
// 2. `+131D1A0` 到 `+131D22F` 是明确的条目遍历循环：每轮将 rbx
//    前进 0x140 字节，并再次调用 `+11FD470`。
// 3. 每个条目的 `+0x00/+0x04` 在 `+131C620` 附近被复制；其中 `+0x04`
//    与此前观察到的 `RDI+4` 对应，是识别“当前条目剩余量”的重点字段。
// 4. 该函数没有直接读取贸易中心 `+1D58`；容量读取发生在被调用的
//    `+11FD470` 内。因此它更像“条目收集/遍历调度器”，而不是容量计算本体。
```
