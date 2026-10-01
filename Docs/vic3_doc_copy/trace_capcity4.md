# victoria3.exe+19DBFE9
victoria3.exe+19DBF8E - CC                    - int 3 
victoria3.exe+19DBF8F - CC                    - int 3 
victoria3.exe+19DBF90 - 48 83 EC 38           - sub rsp,38
victoria3.exe+19DBF94 - 4D 8B C8              - mov r9,r8
victoria3.exe+19DBF97 - 4C 8B C2              - mov r8,rdx
victoria3.exe+19DBF9A - 48 8B D1              - mov rdx,rcx
victoria3.exe+19DBF9D - 48 8D 0D BC71FFFF     - lea rcx,[victoria3.exe+19D3160]
victoria3.exe+19DBFA4 - E8 17EFE0FF           - call victoria3.exe+17EAEC0
victoria3.exe+19DBFA9 - 48 83 C4 38           - add rsp,38
victoria3.exe+19DBFAD - C3                    - ret 
victoria3.exe+19DBFAE - CC                    - int 3 
victoria3.exe+19DBFAF - CC                    - int 3 
victoria3.exe+19DBFB0 - 48 83 EC 38           - sub rsp,38
victoria3.exe+19DBFB4 - 4D 8B C8              - mov r9,r8
victoria3.exe+19DBFB7 - 4C 8B C2              - mov r8,rdx
victoria3.exe+19DBFBA - 48 8B D1              - mov rdx,rcx
victoria3.exe+19DBFBD - 48 8D 0D 0C72FFFF     - lea rcx,[victoria3.exe+19D31D0]
victoria3.exe+19DBFC4 - E8 F7EEE0FF           - call victoria3.exe+17EAEC0
victoria3.exe+19DBFC9 - 48 83 C4 38           - add rsp,38
victoria3.exe+19DBFCD - C3                    - ret 
victoria3.exe+19DBFCE - CC                    - int 3 
victoria3.exe+19DBFCF - CC                    - int 3 
victoria3.exe+19DBFD0 - 48 83 EC 38           - sub rsp,38
victoria3.exe+19DBFD4 - 4D 8B C8              - mov r9,r8
victoria3.exe+19DBFD7 - 4C 8B C2              - mov r8,rdx
victoria3.exe+19DBFDA - 48 8B D1              - mov rdx,rcx
victoria3.exe+19DBFDD - 48 8D 0D 4C72FFFF     - lea rcx,[victoria3.exe+19D3230]
victoria3.exe+19DBFE4 - E8 A7A05DFF           - call victoria3.exe+FB6090
victoria3.exe+19DBFE9 - 48 83 C4 38           - add rsp,38
victoria3.exe+19DBFED - C3                    - ret 


# victoria3.exe+3A1BE70
victoria3.exe+3A1BDFB - CC                    - int 3 
victoria3.exe+3A1BDFC - CC                    - int 3 
victoria3.exe+3A1BDFD - CC                    - int 3 
victoria3.exe+3A1BDFE - CC                    - int 3 
victoria3.exe+3A1BDFF - CC                    - int 3 
victoria3.exe+3A1BE00 - 48 89 5C 24 10        - mov [rsp+10],rbx
victoria3.exe+3A1BE05 - 48 89 74 24 18        - mov [rsp+18],rsi
victoria3.exe+3A1BE0A - 48 89 7C 24 20        - mov [rsp+20],rdi
victoria3.exe+3A1BE0F - 55                    - push rbp
victoria3.exe+3A1BE10 - 41 56                 - push r14
victoria3.exe+3A1BE12 - 41 57                 - push r15
victoria3.exe+3A1BE14 - 48 8D 6C 24 B9        - lea rbp,[rsp-47]
victoria3.exe+3A1BE19 - 48 81 EC B0000000     - sub rsp,000000B0
victoria3.exe+3A1BE20 - 4D 8B F1              - mov r14,r9
victoria3.exe+3A1BE23 - 49 8B F0              - mov rsi,r8
victoria3.exe+3A1BE26 - 48 8B FA              - mov rdi,rdx
victoria3.exe+3A1BE29 - 48 8B D9              - mov rbx,rcx
victoria3.exe+3A1BE2C - 45 33 FF              - xor r15d,r15d
victoria3.exe+3A1BE2F - 48 8B D1              - mov rdx,rcx
victoria3.exe+3A1BE32 - 48 8D 4D 67           - lea rcx,[rbp+67]
victoria3.exe+3A1BE36 - E8 F5F10000           - call victoria3.exe+3A2B030
victoria3.exe+3A1BE3B - 90                    - nop 
victoria3.exe+3A1BE3C - 48 8B 43 30           - mov rax,[rbx+30]
victoria3.exe+3A1BE40 - 48 85 C0              - test rax,rax
victoria3.exe+3A1BE43 - 75 05                 - jne victoria3.exe+3A1BE4A
victoria3.exe+3A1BE45 - E8 666CD9FC           - call victoria3.exe+7B2AB0
victoria3.exe+3A1BE4A - 4C 89 75 07           - mov [rbp+07],r14
victoria3.exe+3A1BE4E - 8B 4B 1C              - mov ecx,[rbx+1C]
victoria3.exe+3A1BE51 - 89 4D 0F              - mov [rbp+0F],ecx
victoria3.exe+3A1BE54 - 48 89 45 17           - mov [rbp+17],rax
victoria3.exe+3A1BE58 - 8B 43 20              - mov eax,[rbx+20]
victoria3.exe+3A1BE5B - 83 F8 02              - cmp eax,02
victoria3.exe+3A1BE5E - 75 19                 - jne victoria3.exe+3A1BE79
victoria3.exe+3A1BE60 - 48 8B 43 28           - mov rax,[rbx+28]
victoria3.exe+3A1BE64 - 4C 8D 45 07           - lea r8,[rbp+07]
victoria3.exe+3A1BE68 - 48 8B D6              - mov rdx,rsi
victoria3.exe+3A1BE6B - 48 8B 0F              - mov rcx,[rdi]
victoria3.exe+3A1BE6E - FF D0                 - call rax
victoria3.exe+3A1BE70 - 44 0FB6 F0            - movzx r14d,al
victoria3.exe+3A1BE74 - E9 2C010000           - jmp victoria3.exe+3A1BFA5
victoria3.exe+3A1BE79 - 83 F8 01              - cmp eax,01
victoria3.exe+3A1BE7C - 75 22                 - jne victoria3.exe+3A1BEA0
victoria3.exe+3A1BE7E - 48 8B 43 28           - mov rax,[rbx+28]
victoria3.exe+3A1BE82 - 80 7F 08 00           - cmp byte ptr [rdi+08],00
victoria3.exe+3A1BE86 - 49 8B CF              - mov rcx,r15
victoria3.exe+3A1BE89 - 75 03                 - jne victoria3.exe+3A1BE8E
victoria3.exe+3A1BE8B - 48 8B 0F              - mov rcx,[rdi]
victoria3.exe+3A1BE8E - 4C 8D 45 07           - lea r8,[rbp+07]
victoria3.exe+3A1BE92 - 48 8B D6              - mov rdx,rsi
victoria3.exe+3A1BE95 - FF D0                 - call rax
victoria3.exe+3A1BE97 - 44 0FB6 F0            - movzx r14d,al
victoria3.exe+3A1BE9B - E9 05010000           - jmp victoria3.exe+3A1BFA5
victoria3.exe+3A1BEA0 - 48 8B 43 50           - mov rax,[rbx+50]
victoria3.exe+3A1BEA4 - 48 85 C0              - test rax,rax
victoria3.exe+3A1BEA7 - 74 1A                 - je victoria3.exe+3A1BEC3
victoria3.exe+3A1BEA9 - 8B 48 10              - mov ecx,[rax+10]
victoria3.exe+3A1BEAC - 48 83 78 18 0F        - cmp qword ptr [rax+18],0F
victoria3.exe+3A1BEB1 - 76 03                 - jna victoria3.exe+3A1BEB6
victoria3.exe+3A1BEB3 - 48 8B 00              - mov rax,[rax]
victoria3.exe+3A1BEB6 - 48 89 45 C7           - mov [rbp-39],rax
victoria3.exe+3A1BEBA - 89 4D CF              - mov [rbp-31],ecx
victoria3.exe+3A1BEBD - C6 45 D3 00           - mov byte ptr [rbp-2D],00
victoria3.exe+3A1BEC1 - EB 0C                 - jmp victoria3.exe+3A1BECF
victoria3.exe+3A1BEC3 - 4C 89 7D C7           - mov [rbp-39],r15
victoria3.exe+3A1BEC7 - 44 89 7D CF           - mov [rbp-31],r15d
victoria3.exe+3A1BECB - C6 45 D3 01           - mov byte ptr [rbp-2D],01
victoria3.exe+3A1BECF - 48 8D 45 C7           - lea rax,[rbp-39]
victoria3.exe+3A1BED3 - 48 89 45 D7           - mov [rbp-29],rax
victoria3.exe+3A1BED7 - 48 8D 05 2201C0FC     - lea rax,[victoria3.exe+61C000]
victoria3.exe+3A1BEDE - 48 89 45 DF           - mov [rbp-21],rax
victoria3.exe+3A1BEE2 - 48 C7 45 E7 0F000000  - mov qword ptr [rbp-19],0000000F
victoria3.exe+3A1BEEA - 48 8D 45 D7           - lea rax,[rbp-29]
victoria3.exe+3A1BEEE - 48 89 45 EF           - mov [rbp-11],rax
victoria3.exe+3A1BEF2 - 48 8D 05 D798DC00     - lea rax,[victoria3.exe+47E57D0]
victoria3.exe+3A1BEF9 - 48 89 45 F7           - mov [rbp-09],rax
victoria3.exe+3A1BEFD - 48 C7 45 FF 19000000  - mov qword ptr [rbp-01],00000019
victoria3.exe+3A1BF05 - 4C 8D 45 E7           - lea r8,[rbp-19]
victoria3.exe+3A1BF09 - 48 8D 55 F7           - lea rdx,[rbp-09]
victoria3.exe+3A1BF0D - 48 8D 4D 1F           - lea rcx,[rbp+1F]
victoria3.exe+3A1BF11 - E8 5A406F00           - call victoria3.exe+410FF70
victoria3.exe+3A1BF16 - 90                    - nop 
victoria3.exe+3A1BF17 - 48 8D 45 1F           - lea rax,[rbp+1F]
victoria3.exe+3A1BF1B - 48 83 7D 37 0F        - cmp qword ptr [rbp+37],0F
victoria3.exe+3A1BF20 - 48 0F47 45 1F         - cmova rax,[rbp+1F]
victoria3.exe+3A1BF25 - 48 89 45 D7           - mov [rbp-29],rax
victoria3.exe+3A1BF29 - 8B 45 2F              - mov eax,[rbp+2F]
victoria3.exe+3A1BF2C - 89 45 DF              - mov [rbp-21],eax
victoria3.exe+3A1BF2F - C6 45 E3 00           - mov byte ptr [rbp-1D],00
victoria3.exe+3A1BF33 - C5F81045 D7           - vmovups xmm0,[rbp-29]
victoria3.exe+3A1BF38 - C5F97F45 F7           - vmovdqa [rbp-09],xmm0
victoria3.exe+3A1BF3D - 48 8D 45 F7           - lea rax,[rbp-09]
victoria3.exe+3A1BF41 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+3A1BF46 - BA 4D000000           - mov edx,0000004D
victoria3.exe+3A1BF4B - 41 B9 04000000        - mov r9d,00000004
victoria3.exe+3A1BF51 - 41 B8 03000000        - mov r8d,00000003
victoria3.exe+3A1BF57 - 48 8D 0D C298DC00     - lea rcx,[victoria3.exe+47E5820]
victoria3.exe+3A1BF5E - E8 6D600E00           - call victoria3.exe+3B01FD0
victoria3.exe+3A1BF63 - 90                    - nop 
victoria3.exe+3A1BF64 - 48 8B 45 37           - mov rax,[rbp+37]
victoria3.exe+3A1BF68 - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+3A1BF6C - 76 34                 - jna victoria3.exe+3A1BFA2
victoria3.exe+3A1BF6E - 48 8B 55 1F           - mov rdx,[rbp+1F]
victoria3.exe+3A1BF72 - 48 8B CA              - mov rcx,rdx
victoria3.exe+3A1BF75 - 48 FF C0              - inc rax
victoria3.exe+3A1BF78 - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+3A1BF7E - 72 15                 - jb victoria3.exe+3A1BF95
victoria3.exe+3A1BF80 - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+3A1BF84 - 48 2B CA              - sub rcx,rdx
victoria3.exe+3A1BF87 - 48 83 E9 08           - sub rcx,08
victoria3.exe+3A1BF8B - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+3A1BF8F - 0F87 8D000000         - ja victoria3.exe+3A1C022
victoria3.exe+3A1BF95 - 48 85 D2              - test rdx,rdx
victoria3.exe+3A1BF98 - 74 08                 - je victoria3.exe+3A1BFA2
victoria3.exe+3A1BF9A - 48 8B CA              - mov rcx,rdx
victoria3.exe+3A1BF9D - E8 8E437000           - call victoria3.exe+4120330
victoria3.exe+3A1BFA2 - 45 32 F6              - xor r14b,r14b
victoria3.exe+3A1BFA5 - 48 8B 05 2CD7EC01     - mov rax,[victoria3.exe+58E96D8]
victoria3.exe+3A1BFAC - 48 85 C0              - test rax,rax
victoria3.exe+3A1BFAF - 74 50                 - je victoria3.exe+3A1C001
victoria3.exe+3A1BFB1 - 80 78 18 00           - cmp byte ptr [rax+18],00
victoria3.exe+3A1BFB5 - 74 4A                 - je victoria3.exe+3A1C001
victoria3.exe+3A1BFB7 - 8B 50 20              - mov edx,[rax+20]
victoria3.exe+3A1BFBA - 48 C1 E2 06           - shl rdx,06
victoria3.exe+3A1BFBE - 48 8B 00              - mov rax,[rax]
victoria3.exe+3A1BFC1 - 48 63 4C 02 2C        - movsxd  rcx,dword ptr [rdx+rax+2C]
victoria3.exe+3A1BFC6 - 48 8B 44 02 20        - mov rax,[rdx+rax+20]
victoria3.exe+3A1BFCB - 48 8B 74 C8 F8        - mov rsi,[rax+rcx*8-08]
victoria3.exe+3A1BFD0 - 8B 06                 - mov eax,[rsi]
victoria3.exe+3A1BFD2 - 85 C0                 - test eax,eax
victoria3.exe+3A1BFD4 - 7E 06                 - jle victoria3.exe+3A1BFDC
victoria3.exe+3A1BFD6 - FF C8                 - dec eax
victoria3.exe+3A1BFD8 - 89 06                 - mov [rsi],eax
victoria3.exe+3A1BFDA - EB 25                 - jmp victoria3.exe+3A1C001
victoria3.exe+3A1BFDC - 48 8B BE 90000000     - mov rdi,[rsi+00000090]
victoria3.exe+3A1BFE3 - 48 8D 4F 28           - lea rcx,[rdi+28]
victoria3.exe+3A1BFE7 - E8 646B0700           - call victoria3.exe+3A92B50
victoria3.exe+3A1BFEC - C5FB1147 30           - vmovsd [rdi+30],xmm0
victoria3.exe+3A1BFF1 - C6 47 38 01           - mov byte ptr [rdi+38],01
victoria3.exe+3A1BFF5 - C5FB1147 20           - vmovsd [rdi+20],xmm0
victoria3.exe+3A1BFFA - 4C 89 BE 90000000     - mov [rsi+00000090],r15
victoria3.exe+3A1C001 - 41 0FB6 C6            - movzx eax,r14b
victoria3.exe+3A1C005 - 4C 8D 9C 24 B0000000  - lea r11,[rsp+000000B0]
victoria3.exe+3A1C00D - 49 8B 5B 28           - mov rbx,[r11+28]
victoria3.exe+3A1C011 - 49 8B 73 30           - mov rsi,[r11+30]
victoria3.exe+3A1C015 - 49 8B 7B 38           - mov rdi,[r11+38]
victoria3.exe+3A1C019 - 49 8B E3              - mov rsp,r11
victoria3.exe+3A1C01C - 41 5F                 - pop r15
victoria3.exe+3A1C01E - 41 5E                 - pop r14
victoria3.exe+3A1C020 - 5D                    - pop rbp
victoria3.exe+3A1C021 - C3                    - ret 


# victoria3.exe+3A1C36A
victoria3.exe+3A1C276 - CC                    - int 3 
victoria3.exe+3A1C277 - CC                    - int 3 
victoria3.exe+3A1C278 - CC                    - int 3 
victoria3.exe+3A1C279 - CC                    - int 3 
victoria3.exe+3A1C27A - CC                    - int 3 
victoria3.exe+3A1C27B - CC                    - int 3 
victoria3.exe+3A1C27C - CC                    - int 3 
victoria3.exe+3A1C27D - CC                    - int 3 
victoria3.exe+3A1C27E - CC                    - int 3 
victoria3.exe+3A1C27F - CC                    - int 3 
victoria3.exe+3A1C280 - 48 89 5C 24 18        - mov [rsp+18],rbx
victoria3.exe+3A1C285 - 48 89 54 24 10        - mov [rsp+10],rdx
victoria3.exe+3A1C28A - 55                    - push rbp
victoria3.exe+3A1C28B - 56                    - push rsi
victoria3.exe+3A1C28C - 57                    - push rdi
victoria3.exe+3A1C28D - 48 8B EC              - mov rbp,rsp
victoria3.exe+3A1C290 - 48 83 EC 60           - sub rsp,60
victoria3.exe+3A1C294 - 48 8B FA              - mov rdi,rdx
victoria3.exe+3A1C297 - 48 8B D9              - mov rbx,rcx
victoria3.exe+3A1C29A - 48 8B 31              - mov rsi,[rcx]
victoria3.exe+3A1C29D - 48 85 F6              - test rsi,rsi
victoria3.exe+3A1C2A0 - 74 2B                 - je victoria3.exe+3A1C2CD
victoria3.exe+3A1C2A2 - E8 1947C1FC           - call victoria3.exe+6309C0
victoria3.exe+3A1C2A7 - 48 89 07              - mov [rdi],rax
victoria3.exe+3A1C2AA - 48 8B 06              - mov rax,[rsi]
victoria3.exe+3A1C2AD - 4C 8B C0              - mov r8,rax
victoria3.exe+3A1C2B0 - 49 83 E0 FE           - and r8,-02
victoria3.exe+3A1C2B4 - 48 8D 56 08           - lea rdx,[rsi+08]
victoria3.exe+3A1C2B8 - A8 01                 - test al,01
victoria3.exe+3A1C2BA - 74 03                 - je victoria3.exe+3A1C2BF
victoria3.exe+3A1C2BC - 48 8B 12              - mov rdx,[rdx]
victoria3.exe+3A1C2BF - 48 8B CF              - mov rcx,rdi
victoria3.exe+3A1C2C2 - E8 99511BFD           - call victoria3.exe+BD1460
victoria3.exe+3A1C2C7 - 90                    - nop 
victoria3.exe+3A1C2C8 - E9 26010000           - jmp victoria3.exe+3A1C3F3
victoria3.exe+3A1C2CD - 80 79 20 00           - cmp byte ptr [rcx+20],00
victoria3.exe+3A1C2D1 - 0F84 14010000         - je victoria3.exe+3A1C3EB
victoria3.exe+3A1C2D7 - E8 9407C0FC           - call victoria3.exe+61CA70
victoria3.exe+3A1C2DC - 48 8B 43 08           - mov rax,[rbx+08]
victoria3.exe+3A1C2E0 - 0FB6 50 44            - movzx edx,byte ptr [rax+44]
victoria3.exe+3A1C2E4 - 48 63 48 4C           - movsxd  rcx,dword ptr [rax+4C]
victoria3.exe+3A1C2E8 - 48 8B 43 10           - mov rax,[rbx+10]
victoria3.exe+3A1C2EC - 83 F9 FF              - cmp ecx,-01
victoria3.exe+3A1C2EF - 74 20                 - je victoria3.exe+3A1C311
victoria3.exe+3A1C2F1 - 3B 48 0C              - cmp ecx,[rax+0C]
victoria3.exe+3A1C2F4 - 7D 1B                 - jnl victoria3.exe+3A1C311
victoria3.exe+3A1C2F6 - 48 8B D1              - mov rdx,rcx
victoria3.exe+3A1C2F9 - 48 C1 E2 04           - shl rdx,04
victoria3.exe+3A1C2FD - 48 03 10              - add rdx,[rax]
victoria3.exe+3A1C300 - 48 8B 02              - mov rax,[rdx]
victoria3.exe+3A1C303 - 48 89 45 C8           - mov [rbp-38],rax
victoria3.exe+3A1C307 - C6 45 D0 00           - mov byte ptr [rbp-30],00
victoria3.exe+3A1C30B - 48 8D 42 08           - lea rax,[rdx+08]
victoria3.exe+3A1C30F - EB 19                 - jmp victoria3.exe+3A1C32A
victoria3.exe+3A1C311 - 48 C7 45 C8 00000000  - mov qword ptr [rbp-38],00000000
victoria3.exe+3A1C319 - 84 D2                 - test dl,dl
victoria3.exe+3A1C31B - C6 45 D0 01           - mov byte ptr [rbp-30],01
victoria3.exe+3A1C31F - 75 04                 - jne victoria3.exe+3A1C325
victoria3.exe+3A1C321 - C6 45 D0 00           - mov byte ptr [rbp-30],00
victoria3.exe+3A1C325 - E8 4607C0FC           - call victoria3.exe+61CA70
victoria3.exe+3A1C32A - 8B 00                 - mov eax,[rax]
victoria3.exe+3A1C32C - 89 45 20              - mov [rbp+20],eax
victoria3.exe+3A1C32F - E8 8C46C1FC           - call victoria3.exe+6309C0
victoria3.exe+3A1C334 - 48 89 45 D8           - mov [rbp-28],rax
victoria3.exe+3A1C338 - 48 8B 73 08           - mov rsi,[rbx+08]
victoria3.exe+3A1C33C - 48 8B 5B 18           - mov rbx,[rbx+18]
victoria3.exe+3A1C340 - 4C 8B CB              - mov r9,rbx
victoria3.exe+3A1C343 - 4C 8D 45 20           - lea r8,[rbp+20]
victoria3.exe+3A1C347 - 48 8D 55 C8           - lea rdx,[rbp-38]
victoria3.exe+3A1C34B - 48 8B CE              - mov rcx,rsi
victoria3.exe+3A1C34E - E8 2DF2FFFF           - call victoria3.exe+3A1B580
victoria3.exe+3A1C353 - 84 C0                 - test al,al
victoria3.exe+3A1C355 - 74 2E                 - je victoria3.exe+3A1C385
victoria3.exe+3A1C357 - 4C 8B CB              - mov r9,rbx
victoria3.exe+3A1C35A - 4C 8D 45 D8           - lea r8,[rbp-28]
victoria3.exe+3A1C35E - 48 8D 55 C8           - lea rdx,[rbp-38]
victoria3.exe+3A1C362 - 48 8B CE              - mov rcx,rsi
victoria3.exe+3A1C365 - E8 96FAFFFF           - call victoria3.exe+3A1BE00
victoria3.exe+3A1C36A - 84 C0                 - test al,al
victoria3.exe+3A1C36C - 74 17                 - je victoria3.exe+3A1C385
victoria3.exe+3A1C36E - E8 4D46C1FC           - call victoria3.exe+6309C0
victoria3.exe+3A1C373 - 48 89 07              - mov [rdi],rax
victoria3.exe+3A1C376 - 48 8D 55 D8           - lea rdx,[rbp-28]
victoria3.exe+3A1C37A - 48 8B CF              - mov rcx,rdi
victoria3.exe+3A1C37D - E8 DE88D7FC           - call victoria3.exe+794C60
victoria3.exe+3A1C382 - 90                    - nop 
victoria3.exe+3A1C383 - EB 08                 - jmp victoria3.exe+3A1C38D
victoria3.exe+3A1C385 - E8 3646C1FC           - call victoria3.exe+6309C0
victoria3.exe+3A1C38A - 48 89 07              - mov [rdi],rax
victoria3.exe+3A1C38D - 48 8B 5D D8           - mov rbx,[rbp-28]
victoria3.exe+3A1C391 - 48 83 E3 FE           - and rbx,-02
victoria3.exe+3A1C395 - E8 2646C1FC           - call victoria3.exe+6309C0
victoria3.exe+3A1C39A - 48 3B D8              - cmp rbx,rax
victoria3.exe+3A1C39D - 74 32                 - je victoria3.exe+3A1C3D1
victoria3.exe+3A1C39F - 48 8B 55 D8           - mov rdx,[rbp-28]
victoria3.exe+3A1C3A3 - 48 8B CA              - mov rcx,rdx
victoria3.exe+3A1C3A6 - 48 83 E1 FE           - and rcx,-02
victoria3.exe+3A1C3AA - 48 8B 01              - mov rax,[rcx]
victoria3.exe+3A1C3AD - F6 C2 01              - test dl,01
victoria3.exe+3A1C3B0 - 48 8D 55 E0           - lea rdx,[rbp-20]
victoria3.exe+3A1C3B4 - 48 0F45 55 E0         - cmovne rdx,[rbp-20]
victoria3.exe+3A1C3B9 - FF 50 18              - call qword ptr [rax+18]
victoria3.exe+3A1C3BC - 0FB6 5D D8            - movzx ebx,byte ptr [rbp-28]
victoria3.exe+3A1C3C0 - 83 E3 01              - and ebx,01
victoria3.exe+3A1C3C3 - E8 F845C1FC           - call victoria3.exe+6309C0
victoria3.exe+3A1C3C8 - 48 0B D8              - or rbx,rax
victoria3.exe+3A1C3CB - 48 89 5D D8           - mov [rbp-28],rbx
victoria3.exe+3A1C3CF - EB 04                 - jmp victoria3.exe+3A1C3D5
victoria3.exe+3A1C3D1 - 48 8B 5D D8           - mov rbx,[rbp-28]
victoria3.exe+3A1C3D5 - F6 C3 01              - test bl,01
victoria3.exe+3A1C3D8 - 74 0F                 - je victoria3.exe+3A1C3E9
victoria3.exe+3A1C3DA - 48 8B 4D E0           - mov rcx,[rbp-20]
victoria3.exe+3A1C3DE - 48 85 C9              - test rcx,rcx
victoria3.exe+3A1C3E1 - 74 06                 - je victoria3.exe+3A1C3E9
victoria3.exe+3A1C3E3 - E8 483F7000           - call victoria3.exe+4120330
victoria3.exe+3A1C3E8 - 90                    - nop 
victoria3.exe+3A1C3E9 - EB 08                 - jmp victoria3.exe+3A1C3F3
victoria3.exe+3A1C3EB - E8 D045C1FC           - call victoria3.exe+6309C0
victoria3.exe+3A1C3F0 - 48 89 07              - mov [rdi],rax
victoria3.exe+3A1C3F3 - 48 8B C7              - mov rax,rdi
victoria3.exe+3A1C3F6 - 48 8B 9C 24 90000000  - mov rbx,[rsp+00000090]
victoria3.exe+3A1C3FE - 48 83 C4 60           - add rsp,60
victoria3.exe+3A1C402 - 5F                    - pop rdi
victoria3.exe+3A1C403 - 5E                    - pop rsi
victoria3.exe+3A1C404 - 5D                    - pop rbp
victoria3.exe+3A1C405 - C3                    - ret 


# victoria3.exe+17F4802
victoria3.exe+17F4795 - CC                    - int 3 
victoria3.exe+17F4796 - CC                    - int 3 
victoria3.exe+17F4797 - CC                    - int 3 
victoria3.exe+17F4798 - CC                    - int 3 
victoria3.exe+17F4799 - CC                    - int 3 
victoria3.exe+17F479A - CC                    - int 3 
victoria3.exe+17F479B - CC                    - int 3 
victoria3.exe+17F479C - CC                    - int 3 
victoria3.exe+17F479D - CC                    - int 3 
victoria3.exe+17F479E - CC                    - int 3 
victoria3.exe+17F479F - CC                    - int 3 
victoria3.exe+17F47A0 - 48 89 5C 24 08        - mov [rsp+08],rbx
victoria3.exe+17F47A5 - 48 89 6C 24 10        - mov [rsp+10],rbp
victoria3.exe+17F47AA - 48 89 74 24 18        - mov [rsp+18],rsi
victoria3.exe+17F47AF - 48 89 7C 24 20        - mov [rsp+20],rdi
victoria3.exe+17F47B4 - 41 56                 - push r14
victoria3.exe+17F47B6 - 48 81 EC 80050000     - sub rsp,00000580
victoria3.exe+17F47BD - 49 8B F1              - mov rsi,r9
victoria3.exe+17F47C0 - 4D 8B F0              - mov r14,r8
victoria3.exe+17F47C3 - 49 8B 11              - mov rdx,[r9]
victoria3.exe+17F47C6 - 8B 52 0C              - mov edx,[rdx+0C]
victoria3.exe+17F47C9 - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+17F47CE - E8 EDAFF3FE           - call victoria3.exe+72F7C0
victoria3.exe+17F47D3 - 90                    - nop 
victoria3.exe+17F47D4 - 8B 46 08              - mov eax,[rsi+08]
victoria3.exe+17F47D7 - 48 8D 3C 80           - lea rdi,[rax+rax*4]
victoria3.exe+17F47DB - 48 8B 06              - mov rax,[rsi]
victoria3.exe+17F47DE - 48 8B 08              - mov rcx,[rax]
victoria3.exe+17F47E1 - 48 8D 1C F9           - lea rbx,[rcx+rdi*8]
victoria3.exe+17F47E5 - 48 8B CB              - mov rcx,rbx
victoria3.exe+17F47E8 - E8 032C0000           - call victoria3.exe+17F73F0
victoria3.exe+17F47ED - 84 C0                 - test al,al
victoria3.exe+17F47EF - 0F84 0C010000         - je victoria3.exe+17F4901
victoria3.exe+17F47F5 - 48 8D 54 24 20        - lea rdx,[rsp+20]
victoria3.exe+17F47FA - 48 8B CB              - mov rcx,rbx
victoria3.exe+17F47FD - E8 7E7A2202           - call victoria3.exe+3A1C280
victoria3.exe+17F4802 - 90                    - nop 
victoria3.exe+17F4803 - 48 8B 4C 24 50        - mov rcx,[rsp+50]
victoria3.exe+17F4808 - 48 8D 0C F9           - lea rcx,[rcx+rdi*8]
victoria3.exe+17F480C - 48 8B D0              - mov rdx,rax
victoria3.exe+17F480F - E8 4C04FAFE           - call victoria3.exe+794C60
victoria3.exe+17F4814 - 90                    - nop 
victoria3.exe+17F4815 - 48 8B 5C 24 20        - mov rbx,[rsp+20]
victoria3.exe+17F481A - 48 83 E3 FE           - and rbx,-02
victoria3.exe+17F481E - E8 9DC1E3FE           - call victoria3.exe+6309C0
victoria3.exe+17F4823 - 48 3B D8              - cmp rbx,rax
victoria3.exe+17F4826 - 74 37                 - je victoria3.exe+17F485F
victoria3.exe+17F4828 - 48 8B 54 24 20        - mov rdx,[rsp+20]
victoria3.exe+17F482D - 48 8B CA              - mov rcx,rdx
victoria3.exe+17F4830 - 48 83 E1 FE           - and rcx,-02
victoria3.exe+17F4834 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+17F4837 - F6 C2 01              - test dl,01
victoria3.exe+17F483A - 48 8D 54 24 28        - lea rdx,[rsp+28]
victoria3.exe+17F483F - 48 0F45 54 24 28      - cmovne rdx,[rsp+28]
victoria3.exe+17F4845 - FF 50 18              - call qword ptr [rax+18]
victoria3.exe+17F4848 - 0FB6 5C 24 20         - movzx ebx,byte ptr [rsp+20]
victoria3.exe+17F484D - 83 E3 01              - and ebx,01
victoria3.exe+17F4850 - E8 6BC1E3FE           - call victoria3.exe+6309C0
victoria3.exe+17F4855 - 48 0B D8              - or rbx,rax
victoria3.exe+17F4858 - 48 89 5C 24 20        - mov [rsp+20],rbx
victoria3.exe+17F485D - EB 05                 - jmp victoria3.exe+17F4864
victoria3.exe+17F485F - 48 8B 5C 24 20        - mov rbx,[rsp+20]
victoria3.exe+17F4864 - F6 C3 01              - test bl,01
victoria3.exe+17F4867 - 74 10                 - je victoria3.exe+17F4879
victoria3.exe+17F4869 - 48 8B 4C 24 28        - mov rcx,[rsp+28]
victoria3.exe+17F486E - 48 85 C9              - test rcx,rcx
victoria3.exe+17F4871 - 74 06                 - je victoria3.exe+17F4879
victoria3.exe+17F4873 - E8 B8BA9202           - call victoria3.exe+4120330
victoria3.exe+17F4878 - 90                    - nop 
victoria3.exe+17F4879 - 48 8B 44 24 50        - mov rax,[rsp+50]
victoria3.exe+17F487E - 48 8B 1C F8           - mov rbx,[rax+rdi*8]
victoria3.exe+17F4882 - 48 83 E3 FE           - and rbx,-02
victoria3.exe+17F4886 - E8 E584FBFE           - call victoria3.exe+7ACD70
victoria3.exe+17F488B - 48 3B D8              - cmp rbx,rax
victoria3.exe+17F488E - 75 71                 - jne victoria3.exe+17F4901
victoria3.exe+17F4890 - 8B 46 08              - mov eax,[rsi+08]
victoria3.exe+17F4893 - 48 8D 3C 80           - lea rdi,[rax+rax*4]
victoria3.exe+17F4897 - 48 8B 74 24 50        - mov rsi,[rsp+50]
victoria3.exe+17F489C - 48 8B 1C FE           - mov rbx,[rsi+rdi*8]
victoria3.exe+17F48A0 - 48 83 E3 FE           - and rbx,-02
victoria3.exe+17F48A4 - E8 671C83FF           - call victoria3.exe+1026510
victoria3.exe+17F48A9 - 48 8B 2C FE           - mov rbp,[rsi+rdi*8]
victoria3.exe+17F48AD - 48 83 E5 FE           - and rbp,-02
victoria3.exe+17F48B1 - 48 3B D8              - cmp rbx,rax
victoria3.exe+17F48B4 - 75 07                 - jne victoria3.exe+17F48BD
victoria3.exe+17F48B6 - E8 551C83FF           - call victoria3.exe+1026510
victoria3.exe+17F48BB - EB 05                 - jmp victoria3.exe+17F48C2
victoria3.exe+17F48BD - E8 AE84FBFE           - call victoria3.exe+7ACD70
victoria3.exe+17F48C2 - 48 3B E8              - cmp rbp,rax
victoria3.exe+17F48C5 - 74 04                 - je victoria3.exe+17F48CB
victoria3.exe+17F48C7 - 33 C9                 - xor ecx,ecx
victoria3.exe+17F48C9 - EB 11                 - jmp victoria3.exe+17F48DC
victoria3.exe+17F48CB - 48 8D 4E 08           - lea rcx,[rsi+08]
victoria3.exe+17F48CF - F6 04 FE  01          - test byte ptr [rsi+rdi*8],01
victoria3.exe+17F48D3 - 48 8D 0C F9           - lea rcx,[rcx+rdi*8]
victoria3.exe+17F48D7 - 74 03                 - je victoria3.exe+17F48DC
victoria3.exe+17F48D9 - 48 8B 09              - mov rcx,[rcx]
victoria3.exe+17F48DC - 8B 09                 - mov ecx,[rcx]
victoria3.exe+17F48DE - E8 8DEEFFFF           - call victoria3.exe+17F3770
victoria3.exe+17F48E3 - C5FA1184 24 B0 050000 - vmovss [rsp+000005B0],xmm0
victoria3.exe+17F48EC - 48 8D 94 24 B0050000  - lea rdx,[rsp+000005B0]
victoria3.exe+17F48F4 - 49 8B CE              - mov rcx,r14
victoria3.exe+17F48F7 - E8 848BFFFF           - call victoria3.exe+17ED480
victoria3.exe+17F48FC - 40 B5 01              - mov bpl,01
victoria3.exe+17F48FF - EB 03                 - jmp victoria3.exe+17F4904
victoria3.exe+17F4901 - 40 32 ED              - xor bpl,bpl
victoria3.exe+17F4904 - 48 8B 54 24 50        - mov rdx,[rsp+50]
victoria3.exe+17F4909 - 48 85 D2              - test rdx,rdx
victoria3.exe+17F490C - 74 55                 - je victoria3.exe+17F4963
victoria3.exe+17F490E - 48 63 74 24 5C        - movsxd  rsi,dword ptr [rsp+5C]
victoria3.exe+17F4913 - 48 85 F6              - test rsi,rsi
victoria3.exe+17F4916 - 7E 37                 - jle victoria3.exe+17F494F
victoria3.exe+17F4918 - 33 FF                 - xor edi,edi
victoria3.exe+17F491A - 66 0F1F 44 00 00      - nop word ptr [rax+rax+00]
victoria3.exe+17F4920 - 48 8D 1C 17           - lea rbx,[rdi+rdx]
victoria3.exe+17F4924 - 48 8B CB              - mov rcx,rbx
victoria3.exe+17F4927 - E8 F4E0FBFE           - call victoria3.exe+7B2A20
victoria3.exe+17F492C - F6 03 01              - test byte ptr [rbx],01
victoria3.exe+17F492F - 74 0F                 - je victoria3.exe+17F4940
victoria3.exe+17F4931 - 48 8B 4B 08           - mov rcx,[rbx+08]
victoria3.exe+17F4935 - 48 85 C9              - test rcx,rcx
victoria3.exe+17F4938 - 74 06                 - je victoria3.exe+17F4940
victoria3.exe+17F493A - E8 F1B99202           - call victoria3.exe+4120330
victoria3.exe+17F493F - 90                    - nop 
victoria3.exe+17F4940 - 48 83 C7 28           - add rdi,28
victoria3.exe+17F4944 - 48 83 EE 01           - sub rsi,01
victoria3.exe+17F4948 - 48 8B 54 24 50        - mov rdx,[rsp+50]
victoria3.exe+17F494D - 75 D1                 - jne victoria3.exe+17F4920
victoria3.exe+17F494F - C7 44 24 5C 00000000  - mov [rsp+5C],00000000
victoria3.exe+17F4957 - 48 8B 4C 24 60        - mov rcx,[rsp+60]
victoria3.exe+17F495C - 4C 8B 01              - mov r8,[rcx]
victoria3.exe+17F495F - 41 FF 50 10           - call qword ptr [r8+10]
victoria3.exe+17F4963 - 40 0FB6 C5            - movzx eax,bpl
victoria3.exe+17F4967 - 4C 8D 9C 24 80050000  - lea r11,[rsp+00000580]
victoria3.exe+17F496F - 49 8B 5B 10           - mov rbx,[r11+10]
victoria3.exe+17F4973 - 49 8B 6B 18           - mov rbp,[r11+18]
victoria3.exe+17F4977 - 49 8B 73 20           - mov rsi,[r11+20]
victoria3.exe+17F497B - 49 8B 7B 28           - mov rdi,[r11+28]
victoria3.exe+17F497F - 49 8B E3              - mov rsp,r11
victoria3.exe+17F4982 - 41 5E                 - pop r14
victoria3.exe+17F4984 - C3                    - ret 


# victoria3.exe+17F37AF
victoria3.exe+17F3795 - CC                    - int 3 
victoria3.exe+17F3796 - CC                    - int 3 
victoria3.exe+17F3797 - CC                    - int 3 
victoria3.exe+17F3798 - CC                    - int 3 
victoria3.exe+17F3799 - CC                    - int 3 
victoria3.exe+17F379A - CC                    - int 3 
victoria3.exe+17F379B - CC                    - int 3 
victoria3.exe+17F379C - CC                    - int 3 
victoria3.exe+17F379D - CC                    - int 3 
victoria3.exe+17F379E - CC                    - int 3 
victoria3.exe+17F379F - CC                    - int 3 
victoria3.exe+17F37A0 - 48 83 EC 38           - sub rsp,38
victoria3.exe+17F37A4 - 4D 8B C8              - mov r9,r8
victoria3.exe+17F37A7 - 4C 8B C2              - mov r8,rdx
victoria3.exe+17F37AA - E8 F10F0000           - call victoria3.exe+17F47A0
victoria3.exe+17F37AF - 48 83 C4 38           - add rsp,38
victoria3.exe+17F37B3 - C3                    - ret 

结论：不像