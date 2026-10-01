# 新的一批追踪函数
+1229C50
+122A470
+11FD370
+1027970
+122AB50
+122BD40

# victoria3.exe+1229C50
victoria3.exe+1229C4B - CC                    - int 3 
victoria3.exe+1229C4C - CC                    - int 3 
victoria3.exe+1229C4D - CC                    - int 3 
victoria3.exe+1229C4E - CC                    - int 3 
victoria3.exe+1229C4F - CC                    - int 3 
victoria3.exe+1229C50 - 48 89 5C 24 08        - mov [rsp+08],rbx
victoria3.exe+1229C55 - 55                    - push rbp
victoria3.exe+1229C56 - 56                    - push rsi
victoria3.exe+1229C57 - 57                    - push rdi
victoria3.exe+1229C58 - 41 54                 - push r12
victoria3.exe+1229C5A - 41 55                 - push r13
victoria3.exe+1229C5C - 41 56                 - push r14
victoria3.exe+1229C5E - 41 57                 - push r15
victoria3.exe+1229C60 - 48 8D AC 24 C0FEFFFF  - lea rbp,[rsp-00000140]
victoria3.exe+1229C68 - 48 81 EC 40020000     - sub rsp,00000240
victoria3.exe+1229C6F - C5F829B4 24 30 020000 - vmovaps [rsp+00000230],xmm6
victoria3.exe+1229C78 - 4C 8B FA              - mov r15,rdx
victoria3.exe+1229C7B - 4C 8B E9              - mov r13,rcx
victoria3.exe+1229C7E - 45 33 E4              - xor r12d,r12d
victoria3.exe+1229C81 - 44 89 A5 90010000     - mov [rbp+00000190],r12d
victoria3.exe+1229C88 - E8 93F8FFFF           - call victoria3.exe+1229520
victoria3.exe+1229C8D - 84 C0                 - test al,al
victoria3.exe+1229C8F - 75 07                 - jne victoria3.exe+1229C98
victoria3.exe+1229C91 - 33 C0                 - xor eax,eax
victoria3.exe+1229C93 - E9 67070000           - jmp victoria3.exe+122A3FF
victoria3.exe+1229C98 - 49 8B 9D 50190000     - mov rbx,[r13+00001950]
victoria3.exe+1229C9F - 48 89 5D A8           - mov [rbp-58],rbx
victoria3.exe+1229CA3 - 48 85 DB              - test rbx,rbx
victoria3.exe+1229CA6 - 74 04                 - je victoria3.exe+1229CAC
victoria3.exe+1229CA8 - F0 FF 43 08           - lock inc [rbx+08]
victoria3.exe+1229CAC - 41 8B 85 480E0000     - mov eax,[r13+00000E48]
victoria3.exe+1229CB3 - 89 85 90010000        - mov [rbp+00000190],eax
victoria3.exe+1229CB9 - 48 8D 8D 90010000     - lea rcx,[rbp+00000190]
victoria3.exe+1229CC0 - E8 EB6D58FF           - call victoria3.exe+7B0AB0
victoria3.exe+1229CC5 - 48 8B 88 E0080000     - mov rcx,[rax+000008E0]
victoria3.exe+1229CCC - 48 89 8D 98010000     - mov [rbp+00000198],rcx
victoria3.exe+1229CD3 - 48 85 C9              - test rcx,rcx
victoria3.exe+1229CD6 - 74 04                 - je victoria3.exe+1229CDC
victoria3.exe+1229CD8 - F0 FF 41 08           - lock inc [rcx+08]
victoria3.exe+1229CDC - 4D 85 FF              - test r15,r15
victoria3.exe+1229CDF - 0F95 C2               - setne dl
victoria3.exe+1229CE2 - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+1229CE6 - E8 257D1900           - call victoria3.exe+13C1A10
victoria3.exe+1229CEB - 90                    - nop 
victoria3.exe+1229CEC - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+1229CF0 - C5F81144 24 40        - vmovups [rsp+40],xmm0
victoria3.exe+1229CF6 - C5FA6F35 C2 C25D03    - vmovdqu xmm6,xmm0,[victoria3.exe+4805FC0]
victoria3.exe+1229CFE - C5FA7F74 24 50        - vmovdqu [rsp+50],xmm6
victoria3.exe+1229D04 - C6 44 24 40 00        - mov byte ptr [rsp+40],00
victoria3.exe+1229D09 - 44 0FB7 05 97D2EA03   - movzx r8d,word ptr [victoria3.exe+50D6FA8]
victoria3.exe+1229D11 - B8 FFFF0000           - mov eax,0000FFFF
victoria3.exe+1229D16 - 41 BE 01000000        - mov r14d,00000001
victoria3.exe+1229D1C - 66 44 3B C0           - cmp r8w,ax
victoria3.exe+1229D20 - 0F84 AA040000         - je victoria3.exe+122A1D0
victoria3.exe+1229D26 - 48 8D 45 30           - lea rax,[rbp+30]
victoria3.exe+1229D2A - 48 89 45 70           - mov [rbp+70],rax
victoria3.exe+1229D2E - 48 89 5D 78           - mov [rbp+78],rbx
victoria3.exe+1229D32 - 48 85 DB              - test rbx,rbx
victoria3.exe+1229D35 - 74 04                 - je victoria3.exe+1229D3B
victoria3.exe+1229D37 - F0 FF 43 08           - lock inc [rbx+08]
victoria3.exe+1229D3B - 66 44 89 85 80000000  - mov [rbp+00000080],r8w
victoria3.exe+1229D43 - 48 C7 85 88000000 A0860100 - mov qword ptr [rbp+00000088],000186A0
victoria3.exe+1229D4E - 48 8D 4B 10           - lea rcx,[rbx+10]
victoria3.exe+1229D52 - 48 8D 95 90010000     - lea rdx,[rbp+00000190]
victoria3.exe+1229D59 - E8 F2A361FF           - call victoria3.exe+844150
victoria3.exe+1229D5E - 48 8D 05 B3A02003     - lea rax,[victoria3.exe+4433E18]
victoria3.exe+1229D65 - 48 89 85 B0000000     - mov [rbp+000000B0],rax
victoria3.exe+1229D6C - 48 8D 44 24 40        - lea rax,[rsp+40]
victoria3.exe+1229D71 - 48 89 85 B8000000     - mov [rbp+000000B8],rax
victoria3.exe+1229D78 - 48 8D 8D B0000000     - lea rcx,[rbp+000000B0]
victoria3.exe+1229D7F - 48 89 8D E8000000     - mov [rbp+000000E8],rcx
victoria3.exe+1229D86 - 48 8B 9D 90010000     - mov rbx,[rbp+00000190]
victoria3.exe+1229D8D - 48 89 5D A0           - mov [rbp-60],rbx
victoria3.exe+1229D91 - 48 01 5D 38           - add [rbp+38],rbx
victoria3.exe+1229D95 - 80 7D 61 01           - cmp byte ptr [rbp+61],01
victoria3.exe+1229D99 - 0F85 0E040000         - jne victoria3.exe+122A1AD
victoria3.exe+1229D9F - 48 8B 75 68           - mov rsi,[rbp+68]
victoria3.exe+1229DA3 - 80 BE AC010000 00     - cmp byte ptr [rsi+000001AC],00
victoria3.exe+1229DAA - 74 09                 - je victoria3.exe+1229DB5
victoria3.exe+1229DAC - 48 85 DB              - test rbx,rbx
victoria3.exe+1229DAF - 0F84 F8030000         - je victoria3.exe+122A1AD
victoria3.exe+1229DB5 - 48 8D 55 B0           - lea rdx,[rbp-50]
victoria3.exe+1229DB9 - 48 8D 4D 70           - lea rcx,[rbp+70]
victoria3.exe+1229DBD - E8 BE3E9CFF           - call victoria3.exe+BEDC80
victoria3.exe+1229DC2 - 90                    - nop 
victoria3.exe+1229DC3 - 48 83 7D C0 00        - cmp qword ptr [rbp-40],00
victoria3.exe+1229DC8 - 75 09                 - jne victoria3.exe+1229DD3
victoria3.exe+1229DCA - 48 85 DB              - test rbx,rbx
victoria3.exe+1229DCD - 0F84 CA030000         - je victoria3.exe+122A19D
victoria3.exe+1229DD3 - 48 8D 8E 50010000     - lea rcx,[rsi+00000150]
victoria3.exe+1229DDA - E8 4130A2FF           - call victoria3.exe+C4CE20
victoria3.exe+1229DDF - 48 8B F8              - mov rdi,rax
victoria3.exe+1229DE2 - 44 89 70 28           - mov [rax+28],r14d
victoria3.exe+1229DE6 - 48 89 58 20           - mov [rax+20],rbx
victoria3.exe+1229DEA - 48 8B 8D E8000000     - mov rcx,[rbp+000000E8]
victoria3.exe+1229DF1 - 48 85 C9              - test rcx,rcx
victoria3.exe+1229DF4 - 0F84 41060000         - je victoria3.exe+122A43B
victoria3.exe+1229DFA - 48 8B 01              - mov rax,[rcx]
victoria3.exe+1229DFD - 48 8D 95 90000000     - lea rdx,[rbp+00000090]
victoria3.exe+1229E04 - FF 50 10              - call qword ptr [rax+10]
victoria3.exe+1229E07 - 44 89 B5 90010000     - mov [rbp+00000190],r14d
victoria3.exe+1229E0E - 48 83 BD A0000000 00  - cmp qword ptr [rbp+000000A0],00
victoria3.exe+1229E16 - 0F84 3F030000         - je victoria3.exe+122A15B
victoria3.exe+1229E1C - 8B 9E B0010000        - mov ebx,[rsi+000001B0]
victoria3.exe+1229E22 - 48 8B CF              - mov rcx,rdi
victoria3.exe+1229E25 - 48 83 7D C0 00        - cmp qword ptr [rbp-40],00
victoria3.exe+1229E2A - 0F85 80020000         - jne victoria3.exe+122A0B0
victoria3.exe+1229E30 - E8 CB283FFF           - call victoria3.exe+61C700
victoria3.exe+1229E35 - 48 8B D6              - mov rdx,rsi
victoria3.exe+1229E38 - 48 8B CF              - mov rcx,rdi
victoria3.exe+1229E3B - E8 608A1900           - call victoria3.exe+13C28A0
victoria3.exe+1229E40 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+1229E44 - 80 7D 61 01           - cmp byte ptr [rbp+61],01
victoria3.exe+1229E48 - 74 13                 - je victoria3.exe+1229E5D
victoria3.exe+1229E4A - C5F81145 D0           - vmovups [rbp-30],xmm0
victoria3.exe+1229E4F - C5FA7F75 E0           - vmovdqu [rbp-20],xmm6
victoria3.exe+1229E54 - C6 45 D0 00           - mov byte ptr [rbp-30],00
victoria3.exe+1229E58 - E9 D9010000           - jmp victoria3.exe+122A036
victoria3.exe+1229E5D - C5FA7F44 24 70        - vmovdqu [rsp+70],xmm0
victoria3.exe+1229E63 - C5F1EFC9              - vpxor xmm1,xmm1,xmm1
victoria3.exe+1229E67 - C5F8114C 24 60        - vmovups [rsp+60],xmm1
victoria3.exe+1229E6D - 48 C7 44 24 78 0F000000 - mov qword ptr [rsp+78],0000000F
victoria3.exe+1229E76 - C6 44 24 60 00        - mov byte ptr [rsp+60],00
victoria3.exe+1229E7B - 48 C7 44 24 70 03000000 - mov qword ptr [rsp+70],00000003
victoria3.exe+1229E84 - 8B 05 827D2003        - mov eax,[victoria3.exe+4431C0C]
victoria3.exe+1229E8A - 66 89 44 24 60        - mov [rsp+60],ax
victoria3.exe+1229E8F - 0FB6 05 787D2003      - movzx eax,byte ptr [victoria3.exe+4431C0E]
victoria3.exe+1229E96 - 88 44 24 62           - mov [rsp+62],al
victoria3.exe+1229E9A - C6 44 24 63 00        - mov byte ptr [rsp+63],00
victoria3.exe+1229E9F - 48 8B 55 68           - mov rdx,[rbp+68]
victoria3.exe+1229EA3 - 48 81 C2 88010000     - add rdx,00000188
victoria3.exe+1229EAA - 48 8D 4D F0           - lea rcx,[rbp-10]
victoria3.exe+1229EAE - E8 6D873EFF           - call victoria3.exe+612620
victoria3.exe+1229EB3 - C7 85 90010000 05000000 - mov [rbp+00000190],00000005
victoria3.exe+1229EBD - 41 B8 11000000        - mov r8d,00000011
victoria3.exe+1229EC3 - 48 8D 15 F67C2003     - lea rdx,[victoria3.exe+4431BC0]
victoria3.exe+1229ECA - 48 8D 4D F0           - lea rcx,[rbp-10]
victoria3.exe+1229ECE - E8 1DA07001           - call victoria3.exe+2933EF0
victoria3.exe+1229ED3 - 90                    - nop 
victoria3.exe+1229ED4 - C5FC1045 F0           - vmovups ymm0,[rbp-10]
victoria3.exe+1229ED9 - C5FC1145 10           - vmovups [rbp+10],ymm0
victoria3.exe+1229EDE - C5FA7F75 00           - vmovdqu [rbp+00],xmm6
victoria3.exe+1229EE3 - C6 45 F0 00           - mov byte ptr [rbp-10],00
victoria3.exe+1229EE7 - C7 85 90010000 0D000000 - mov [rbp+00000190],0000000D
victoria3.exe+1229EF1 - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+1229EF6 - 48 83 7C 24 78 0F     - cmp qword ptr [rsp+78],0F
victoria3.exe+1229EFC - 48 0F47 54 24 60      - cmova rdx,[rsp+60]
victoria3.exe+1229F02 - 4C 8B 44 24 70        - mov r8,[rsp+70]
victoria3.exe+1229F07 - 48 8D 4D 10           - lea rcx,[rbp+10]
victoria3.exe+1229F0B - C5F877                - vzeroupper 
victoria3.exe+1229F0E - E8 DD9F7001           - call victoria3.exe+2933EF0
victoria3.exe+1229F13 - 4C 8D 05 BA7C2003     - lea r8,[victoria3.exe+4431BD4]
victoria3.exe+1229F1A - 48 8D 55 10           - lea rdx,[rbp+10]
victoria3.exe+1229F1E - 48 8D 4D 80           - lea rcx,[rbp-80]
victoria3.exe+1229F22 - E8 D96E58FF           - call victoria3.exe+7B0E00
victoria3.exe+1229F27 - 90                    - nop 
victoria3.exe+1229F28 - 48 8B 45 28           - mov rax,[rbp+28]
victoria3.exe+1229F2C - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+1229F30 - 76 34                 - jna victoria3.exe+1229F66
victoria3.exe+1229F32 - 48 8B 55 10           - mov rdx,[rbp+10]
victoria3.exe+1229F36 - 48 8B CA              - mov rcx,rdx
victoria3.exe+1229F39 - 48 FF C0              - inc rax
victoria3.exe+1229F3C - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+1229F42 - 72 15                 - jb victoria3.exe+1229F59
victoria3.exe+1229F44 - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+1229F48 - 48 2B CA              - sub rcx,rdx
victoria3.exe+1229F4B - 48 83 E9 08           - sub rcx,08
victoria3.exe+1229F4F - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+1229F53 - 0F87 E8040000         - ja victoria3.exe+122A441
victoria3.exe+1229F59 - 48 85 D2              - test rdx,rdx
victoria3.exe+1229F5C - 74 08                 - je victoria3.exe+1229F66
victoria3.exe+1229F5E - 48 8B CA              - mov rcx,rdx
victoria3.exe+1229F61 - E8 CA63EF02           - call victoria3.exe+4120330
victoria3.exe+1229F66 - C5FA7F75 20           - vmovdqu [rbp+20],xmm6
victoria3.exe+1229F6B - C6 45 10 00           - mov byte ptr [rbp+10],00
victoria3.exe+1229F6F - 48 8B 45 08           - mov rax,[rbp+08]
victoria3.exe+1229F73 - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+1229F77 - 76 34                 - jna victoria3.exe+1229FAD
victoria3.exe+1229F79 - 48 8B 55 F0           - mov rdx,[rbp-10]
victoria3.exe+1229F7D - 48 8B CA              - mov rcx,rdx
victoria3.exe+1229F80 - 48 FF C0              - inc rax
victoria3.exe+1229F83 - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+1229F89 - 72 15                 - jb victoria3.exe+1229FA0
victoria3.exe+1229F8B - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+1229F8F - 48 2B CA              - sub rcx,rdx
victoria3.exe+1229F92 - 48 83 E9 08           - sub rcx,08
victoria3.exe+1229F96 - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+1229F9A - 0F87 B6040000         - ja victoria3.exe+122A456
victoria3.exe+1229FA0 - 48 85 D2              - test rdx,rdx
victoria3.exe+1229FA3 - 74 08                 - je victoria3.exe+1229FAD
victoria3.exe+1229FA5 - 48 8B CA              - mov rcx,rdx
victoria3.exe+1229FA8 - E8 8363EF02           - call victoria3.exe+4120330
victoria3.exe+1229FAD - C5FA7F75 00           - vmovdqu [rbp+00],xmm6
victoria3.exe+1229FB2 - C6 45 F0 00           - mov byte ptr [rbp-10],00
victoria3.exe+1229FB6 - 83 FB 01              - cmp ebx,01
victoria3.exe+1229FB9 - 75 09                 - jne victoria3.exe+1229FC4
victoria3.exe+1229FBB - 48 8D 15 1E7C2003     - lea rdx,[victoria3.exe+4431BE0]
victoria3.exe+1229FC2 - EB 0C                 - jmp victoria3.exe+1229FD0
victoria3.exe+1229FC4 - 83 FB 02              - cmp ebx,02
victoria3.exe+1229FC7 - 75 16                 - jne victoria3.exe+1229FDF
victoria3.exe+1229FC9 - 48 8D 15 587D2003     - lea rdx,[victoria3.exe+4431D28]
victoria3.exe+1229FD0 - 41 B8 09000000        - mov r8d,00000009
victoria3.exe+1229FD6 - 48 8D 4D 80           - lea rcx,[rbp-80]
victoria3.exe+1229FDA - E8 119F7001           - call victoria3.exe+2933EF0
victoria3.exe+1229FDF - C5FC1045 80           - vmovups ymm0,[rbp-80]
victoria3.exe+1229FE4 - C5FC1145 D0           - vmovups [rbp-30],ymm0
victoria3.exe+1229FE9 - C5FA7F75 90           - vmovdqu [rbp-70],xmm6
victoria3.exe+1229FEE - C6 45 80 00           - mov byte ptr [rbp-80],00
victoria3.exe+1229FF2 - 48 8B 44 24 78        - mov rax,[rsp+78]
victoria3.exe+1229FF7 - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+1229FFB - 76 39                 - jna victoria3.exe+122A036
victoria3.exe+1229FFD - 48 8B 54 24 60        - mov rdx,[rsp+60]
victoria3.exe+122A002 - 48 8B CA              - mov rcx,rdx
victoria3.exe+122A005 - 48 FF C0              - inc rax
victoria3.exe+122A008 - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+122A00E - 72 15                 - jb victoria3.exe+122A025
victoria3.exe+122A010 - 48 8B 52 F8           - mov rdx,[rdx-08]
victoria3.exe+122A014 - 48 2B CA              - sub rcx,rdx
victoria3.exe+122A017 - 48 83 E9 08           - sub rcx,08
victoria3.exe+122A01B - 48 83 F9 1F           - cmp rcx,1F
victoria3.exe+122A01F - 0F87 FE030000         - ja victoria3.exe+122A423
victoria3.exe+122A025 - 48 85 D2              - test rdx,rdx
victoria3.exe+122A028 - 74 0C                 - je victoria3.exe+122A036
victoria3.exe+122A02A - 48 8B CA              - mov rcx,rdx
victoria3.exe+122A02D - C5F877                - vzeroupper 
victoria3.exe+122A030 - E8 FB62EF02           - call victoria3.exe+4120330
victoria3.exe+122A035 - 90                    - nop 
victoria3.exe+122A036 - 48 8D 45 D0           - lea rax,[rbp-30]
victoria3.exe+122A03A - 48 83 7D E8 0F        - cmp qword ptr [rbp-18],0F
victoria3.exe+122A03F - 48 0F47 45 D0         - cmova rax,[rbp-30]
victoria3.exe+122A044 - 48 89 44 24 60        - mov [rsp+60],rax
victoria3.exe+122A049 - 8B 45 E0              - mov eax,[rbp-20]
victoria3.exe+122A04C - 89 44 24 68           - mov [rsp+68],eax
victoria3.exe+122A050 - C6 44 24 6C 00        - mov byte ptr [rsp+6C],00
victoria3.exe+122A055 - 48 8D 85 90000000     - lea rax,[rbp+00000090]
victoria3.exe+122A05C - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122A061 - 4C 8D 4D A0           - lea r9,[rbp-60]
victoria3.exe+122A065 - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+122A06A - 48 8D 4D 80           - lea rcx,[rbp-80]
victoria3.exe+122A06E - C5F877                - vzeroupper 
victoria3.exe+122A071 - E8 3A0AA2FF           - call victoria3.exe+C4AAB0
victoria3.exe+122A076 - 90                    - nop 
victoria3.exe+122A077 - 4C 8B 40 10           - mov r8,[rax+10]
victoria3.exe+122A07B - 48 83 78 18 0F        - cmp qword ptr [rax+18],0F
victoria3.exe+122A080 - 76 03                 - jna victoria3.exe+122A085
victoria3.exe+122A082 - 48 8B 00              - mov rax,[rax]
victoria3.exe+122A085 - 48 8B D0              - mov rdx,rax
victoria3.exe+122A088 - 48 8B CF              - mov rcx,rdi
victoria3.exe+122A08B - E8 609E7001           - call victoria3.exe+2933EF0
victoria3.exe+122A090 - 90                    - nop 
victoria3.exe+122A091 - 48 8D 4D 80           - lea rcx,[rbp-80]
victoria3.exe+122A095 - E8 46B73EFF           - call victoria3.exe+6157E0
victoria3.exe+122A09A - 90                    - nop 
victoria3.exe+122A09B - 48 8D 4D D0           - lea rcx,[rbp-30]
victoria3.exe+122A09F - E8 3CB73EFF           - call victoria3.exe+6157E0
victoria3.exe+122A0A4 - 44 89 A6 B0010000     - mov [rsi+000001B0],r12d
victoria3.exe+122A0AB - E9 E0000000           - jmp victoria3.exe+122A190
victoria3.exe+122A0B0 - E8 4B263FFF           - call victoria3.exe+61C700
victoria3.exe+122A0B5 - 48 8B D6              - mov rdx,rsi
victoria3.exe+122A0B8 - 48 8B CF              - mov rcx,rdi
victoria3.exe+122A0BB - E8 E0871900           - call victoria3.exe+13C28A0
victoria3.exe+122A0C0 - 89 5C 24 20           - mov [rsp+20],ebx
victoria3.exe+122A0C4 - 41 B1 01              - mov r9b,01
victoria3.exe+122A0C7 - 45 8B C6              - mov r8d,r14d
victoria3.exe+122A0CA - 48 8D 55 80           - lea rdx,[rbp-80]
victoria3.exe+122A0CE - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+122A0D2 - E8 C9519CFF           - call victoria3.exe+BEF2A0
victoria3.exe+122A0D7 - 90                    - nop 
victoria3.exe+122A0D8 - 48 8D 55 B0           - lea rdx,[rbp-50]
victoria3.exe+122A0DC - 48 8D 4D D0           - lea rcx,[rbp-30]
victoria3.exe+122A0E0 - E8 CBF7A801           - call victoria3.exe+2CB98B0
victoria3.exe+122A0E5 - 90                    - nop 
victoria3.exe+122A0E6 - 48 8D 4D 80           - lea rcx,[rbp-80]
victoria3.exe+122A0EA - 48 83 7D 98 0F        - cmp qword ptr [rbp-68],0F
victoria3.exe+122A0EF - 48 0F47 4D 80         - cmova rcx,[rbp-80]
victoria3.exe+122A0F4 - 48 89 4C 24 60        - mov [rsp+60],rcx
victoria3.exe+122A0F9 - 8B 4D 90              - mov ecx,[rbp-70]
victoria3.exe+122A0FC - 89 4C 24 68           - mov [rsp+68],ecx
victoria3.exe+122A100 - C6 44 24 6C 00        - mov byte ptr [rsp+6C],00
victoria3.exe+122A105 - 48 89 44 24 38        - mov [rsp+38],rax
victoria3.exe+122A10A - 48 8D 85 90000000     - lea rax,[rbp+00000090]
victoria3.exe+122A111 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122A116 - 4C 8D 4D A0           - lea r9,[rbp-60]
victoria3.exe+122A11A - 48 8D 54 24 60        - lea rdx,[rsp+60]
victoria3.exe+122A11F - 48 8D 4D 10           - lea rcx,[rbp+10]
victoria3.exe+122A123 - E8 482EA2FF           - call victoria3.exe+C4CF70
victoria3.exe+122A128 - 90                    - nop 
victoria3.exe+122A129 - 48 8B D0              - mov rdx,rax
victoria3.exe+122A12C - 48 8B CF              - mov rcx,rdi
victoria3.exe+122A12F - E8 5C998802           - call victoria3.exe+3AB3A90
victoria3.exe+122A134 - 90                    - nop 
victoria3.exe+122A135 - 48 8D 4D 10           - lea rcx,[rbp+10]
victoria3.exe+122A139 - E8 A2B63EFF           - call victoria3.exe+6157E0
victoria3.exe+122A13E - 90                    - nop 
victoria3.exe+122A13F - 48 8D 4D D0           - lea rcx,[rbp-30]
victoria3.exe+122A143 - E8 98B63EFF           - call victoria3.exe+6157E0
victoria3.exe+122A148 - 90                    - nop 
victoria3.exe+122A149 - 48 8D 4D 80           - lea rcx,[rbp-80]
victoria3.exe+122A14D - E8 8EB63EFF           - call victoria3.exe+6157E0
victoria3.exe+122A152 - 44 89 A6 B0010000     - mov [rsi+000001B0],r12d
victoria3.exe+122A159 - EB 35                 - jmp victoria3.exe+122A190
victoria3.exe+122A15B - 48 83 7D C0 00        - cmp qword ptr [rbp-40],00
victoria3.exe+122A160 - 74 2E                 - je victoria3.exe+122A190
victoria3.exe+122A162 - 48 8B CF              - mov rcx,rdi
victoria3.exe+122A165 - E8 96253FFF           - call victoria3.exe+61C700
victoria3.exe+122A16A - 48 8B D6              - mov rdx,rsi
victoria3.exe+122A16D - 48 8B CF              - mov rcx,rdi
victoria3.exe+122A170 - E8 2B871900           - call victoria3.exe+13C28A0
victoria3.exe+122A175 - 48 8D 55 B0           - lea rdx,[rbp-50]
victoria3.exe+122A179 - 48 83 7D C8 0F        - cmp qword ptr [rbp-38],0F
victoria3.exe+122A17E - 48 0F47 55 B0         - cmova rdx,[rbp-50]
victoria3.exe+122A183 - 4C 8B 45 C0           - mov r8,[rbp-40]
victoria3.exe+122A187 - 48 8B CF              - mov rcx,rdi
victoria3.exe+122A18A - E8 619D7001           - call victoria3.exe+2933EF0
victoria3.exe+122A18F - 90                    - nop 
victoria3.exe+122A190 - 48 8D 8D 90000000     - lea rcx,[rbp+00000090]
victoria3.exe+122A197 - E8 44B63EFF           - call victoria3.exe+6157E0
victoria3.exe+122A19C - 90                    - nop 
victoria3.exe+122A19D - 48 8D 4D B0           - lea rcx,[rbp-50]
victoria3.exe+122A1A1 - E8 3AB63EFF           - call victoria3.exe+6157E0
victoria3.exe+122A1A6 - 48 8B 8D E8000000     - mov rcx,[rbp+000000E8]
victoria3.exe+122A1AD - 48 85 C9              - test rcx,rcx
victoria3.exe+122A1B0 - 74 14                 - je victoria3.exe+122A1C6
victoria3.exe+122A1B2 - 48 8D 85 B0000000     - lea rax,[rbp+000000B0]
victoria3.exe+122A1B9 - 48 3B C8              - cmp rcx,rax
victoria3.exe+122A1BC - 0F95 C2               - setne dl
victoria3.exe+122A1BF - 48 8B 01              - mov rax,[rcx]
victoria3.exe+122A1C2 - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+122A1C5 - 90                    - nop 
victoria3.exe+122A1C6 - 48 8D 4D 78           - lea rcx,[rbp+78]
victoria3.exe+122A1CA - E8 915550FF           - call victoria3.exe+72F760
victoria3.exe+122A1CF - 90                    - nop 
victoria3.exe+122A1D0 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122A1D5 - E8 06B63EFF           - call victoria3.exe+6157E0
victoria3.exe+122A1DA - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+122A1DE - C5F81144 24 40        - vmovups [rsp+40],xmm0
victoria3.exe+122A1E4 - C5F1EFC9              - vpxor xmm1,xmm1,xmm1
victoria3.exe+122A1E8 - C5FA7F4C 24 50        - vmovdqu [rsp+50],xmm1
victoria3.exe+122A1EE - 45 33 C0              - xor r8d,r8d
victoria3.exe+122A1F1 - 48 8D 15 5A021903     - lea rdx,[victoria3.exe+43BA452]
victoria3.exe+122A1F8 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122A1FD - E8 3E833EFF           - call victoria3.exe+612540
victoria3.exe+122A202 - 90                    - nop 
victoria3.exe+122A203 - 48 8D 44 24 40        - lea rax,[rsp+40]
victoria3.exe+122A208 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+122A20D - 44 0FB7 0D 93CDEA03   - movzx r9d,word ptr [victoria3.exe+50D6FA8]
victoria3.exe+122A215 - 4C 8D 85 98010000     - lea r8,[rbp+00000198]
victoria3.exe+122A21C - 41 8B D6              - mov edx,r14d
victoria3.exe+122A21F - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+122A223 - E8 883D9CFF           - call victoria3.exe+BEDFB0
victoria3.exe+122A228 - 90                    - nop 
victoria3.exe+122A229 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122A22E - E8 ADB53EFF           - call victoria3.exe+6157E0
victoria3.exe+122A233 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+122A237 - C5F81144 24 40        - vmovups [rsp+40],xmm0
victoria3.exe+122A23D - C5F1EFC9              - vpxor xmm1,xmm1,xmm1
victoria3.exe+122A241 - C5FA7F4C 24 50        - vmovdqu [rsp+50],xmm1
victoria3.exe+122A247 - 45 33 C0              - xor r8d,r8d
victoria3.exe+122A24A - 48 8D 15 01021903     - lea rdx,[victoria3.exe+43BA452]
victoria3.exe+122A251 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122A256 - E8 E5823EFF           - call victoria3.exe+612540
victoria3.exe+122A25B - 90                    - nop 
victoria3.exe+122A25C - 48 8D 44 24 40        - lea rax,[rsp+40]
victoria3.exe+122A261 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+122A266 - 44 0FB7 0D 3ECDEA03   - movzx r9d,word ptr [victoria3.exe+50D6FAC]
victoria3.exe+122A26E - 4C 8D 45 A8           - lea r8,[rbp-58]
victoria3.exe+122A272 - BA 02000000           - mov edx,00000002
victoria3.exe+122A277 - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+122A27B - E8 303D9CFF           - call victoria3.exe+BEDFB0
victoria3.exe+122A280 - 90                    - nop 
victoria3.exe+122A281 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122A286 - E8 55B53EFF           - call victoria3.exe+6157E0
victoria3.exe+122A28B - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+122A28F - C5F81144 24 40        - vmovups [rsp+40],xmm0
victoria3.exe+122A295 - C5F1EFC9              - vpxor xmm1,xmm1,xmm1
victoria3.exe+122A299 - C5FA7F4C 24 50        - vmovdqu [rsp+50],xmm1
victoria3.exe+122A29F - 45 33 C0              - xor r8d,r8d
victoria3.exe+122A2A2 - 48 8D 15 A9011903     - lea rdx,[victoria3.exe+43BA452]
victoria3.exe+122A2A9 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122A2AE - E8 8D823EFF           - call victoria3.exe+612540
victoria3.exe+122A2B3 - 90                    - nop 
victoria3.exe+122A2B4 - 48 8D 44 24 40        - lea rax,[rsp+40]
victoria3.exe+122A2B9 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+122A2BE - 44 0FB7 0D E6CCEA03   - movzx r9d,word ptr [victoria3.exe+50D6FAC]
victoria3.exe+122A2C6 - 4C 8D 85 98010000     - lea r8,[rbp+00000198]
victoria3.exe+122A2CD - BA 02000000           - mov edx,00000002
victoria3.exe+122A2D2 - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+122A2D6 - E8 D53C9CFF           - call victoria3.exe+BEDFB0
victoria3.exe+122A2DB - 90                    - nop 
victoria3.exe+122A2DC - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122A2E1 - E8 FAB43EFF           - call victoria3.exe+6157E0
victoria3.exe+122A2E6 - 49 8B 5D 68           - mov rbx,[r13+68]
victoria3.exe+122A2EA - 48 81 FB A0860100     - cmp rbx,000186A0
victoria3.exe+122A2F1 - 0F8D 8E000000         - jnl victoria3.exe+122A385
victoria3.exe+122A2F7 - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+122A2FB - C5F81144 24 40        - vmovups [rsp+40],xmm0
victoria3.exe+122A301 - C5F1EFC9              - vpxor xmm1,xmm1,xmm1
victoria3.exe+122A305 - C5FA7F4C 24 50        - vmovdqu [rsp+50],xmm1
victoria3.exe+122A30B - 45 33 C0              - xor r8d,r8d
victoria3.exe+122A30E - 48 8D 15 3D011903     - lea rdx,[victoria3.exe+43BA452]
victoria3.exe+122A315 - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122A31A - E8 21823EFF           - call victoria3.exe+612540
victoria3.exe+122A31F - 90                    - nop 
victoria3.exe+122A320 - 48 8D 05 F9372503     - lea rax,[victoria3.exe+447DB20]
victoria3.exe+122A327 - 48 89 85 F0000000     - mov [rbp+000000F0],rax
victoria3.exe+122A32E - 48 8D 85 F0000000     - lea rax,[rbp+000000F0]
victoria3.exe+122A335 - 48 89 85 28010000     - mov [rbp+00000128],rax
victoria3.exe+122A33C - 4C 8D 4C 24 40        - lea r9,[rsp+40]
victoria3.exe+122A341 - 4C 8D 85 F0000000     - lea r8,[rbp+000000F0]
victoria3.exe+122A348 - 48 8B D3              - mov rdx,rbx
victoria3.exe+122A34B - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+122A34F - E8 5C499CFF           - call victoria3.exe+BEECB0
victoria3.exe+122A354 - 90                    - nop 
victoria3.exe+122A355 - 48 8B 8D 28010000     - mov rcx,[rbp+00000128]
victoria3.exe+122A35C - 48 85 C9              - test rcx,rcx
victoria3.exe+122A35F - 74 1A                 - je victoria3.exe+122A37B
victoria3.exe+122A361 - 48 8D 85 F0000000     - lea rax,[rbp+000000F0]
victoria3.exe+122A368 - 48 3B C8              - cmp rcx,rax
victoria3.exe+122A36B - 0F95 C2               - setne dl
victoria3.exe+122A36E - 48 8B 01              - mov rax,[rcx]
victoria3.exe+122A371 - FF 50 20              - call qword ptr [rax+20]
victoria3.exe+122A374 - 4C 89 A5 28010000     - mov [rbp+00000128],r12
victoria3.exe+122A37B - 48 8D 4C 24 40        - lea rcx,[rsp+40]
victoria3.exe+122A380 - E8 5BB43EFF           - call victoria3.exe+6157E0
victoria3.exe+122A385 - 4D 85 FF              - test r15,r15
victoria3.exe+122A388 - 74 1C                 - je victoria3.exe+122A3A6
victoria3.exe+122A38A - 49 8B CF              - mov rcx,r15
victoria3.exe+122A38D - E8 6E233FFF           - call victoria3.exe+61C700
victoria3.exe+122A392 - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+122A396 - E8 25821900           - call victoria3.exe+13C25C0
victoria3.exe+122A39B - 48 8B D0              - mov rdx,rax
victoria3.exe+122A39E - 49 8B CF              - mov rcx,r15
victoria3.exe+122A3A1 - E8 EA968802           - call victoria3.exe+3AB3A90
victoria3.exe+122A3A6 - 48 8D 95 90010000     - lea rdx,[rbp+00000190]
victoria3.exe+122A3AD - 48 8D 4D 30           - lea rcx,[rbp+30]
victoria3.exe+122A3B1 - E8 9A7F1900           - call victoria3.exe+13C2350
victoria3.exe+122A3B6 - 48 8B 08              - mov rcx,[rax]
victoria3.exe+122A3B9 - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+122A3C3 - 48 F7 E9              - imul rcx
victoria3.exe+122A3C6 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122A3CA - 48 8B C2              - mov rax,rdx
victoria3.exe+122A3CD - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122A3D1 - 48 03 D0              - add rdx,rax
victoria3.exe+122A3D4 - 83 FA 01              - cmp edx,01
victoria3.exe+122A3D7 - 44 0F4F F2            - cmovg r14d,edx
victoria3.exe+122A3DB - 48 8D 4D 68           - lea rcx,[rbp+68]
victoria3.exe+122A3DF - E8 2CE9A1FF           - call victoria3.exe+C48D10
victoria3.exe+122A3E4 - 90                    - nop 
victoria3.exe+122A3E5 - 48 8D 8D 98010000     - lea rcx,[rbp+00000198]
victoria3.exe+122A3EC - E8 6F5350FF           - call victoria3.exe+72F760
victoria3.exe+122A3F1 - 90                    - nop 
victoria3.exe+122A3F2 - 48 8D 4D A8           - lea rcx,[rbp-58]
victoria3.exe+122A3F6 - E8 655350FF           - call victoria3.exe+72F760
victoria3.exe+122A3FB - 90                    - nop 
victoria3.exe+122A3FC - 41 8B C6              - mov eax,r14d
victoria3.exe+122A3FF - 48 8B 9C 24 80020000  - mov rbx,[rsp+00000280]
victoria3.exe+122A407 - C5F828B4 24 30 020000 - vmovaps xmm6,[rsp+00000230]
victoria3.exe+122A410 - 48 81 C4 40020000     - add rsp,00000240
victoria3.exe+122A417 - 41 5F                 - pop r15
victoria3.exe+122A419 - 41 5E                 - pop r14
victoria3.exe+122A41B - 41 5D                 - pop r13
victoria3.exe+122A41D - 41 5C                 - pop r12
victoria3.exe+122A41F - 5F                    - pop rdi
victoria3.exe+122A420 - 5E                    - pop rsi
victoria3.exe+122A421 - 5D                    - pop rbp
victoria3.exe+122A422 - C3                    - ret 


# victoria3.exe+122A470
victoria3.exe+122A46A - CC                    - int 3 
victoria3.exe+122A46B - CC                    - int 3 
victoria3.exe+122A46C - CC                    - int 3 
victoria3.exe+122A46D - CC                    - int 3 
victoria3.exe+122A46E - CC                    - int 3 
victoria3.exe+122A46F - CC                    - int 3 
victoria3.exe+122A470 - 48 8B C4              - mov rax,rsp
victoria3.exe+122A473 - 48 89 50 10           - mov [rax+10],rdx
victoria3.exe+122A477 - 55                    - push rbp
victoria3.exe+122A478 - 53                    - push rbx
victoria3.exe+122A479 - 56                    - push rsi
victoria3.exe+122A47A - 57                    - push rdi
victoria3.exe+122A47B - 41 54                 - push r12
victoria3.exe+122A47D - 41 55                 - push r13
victoria3.exe+122A47F - 41 56                 - push r14
victoria3.exe+122A481 - 41 57                 - push r15
victoria3.exe+122A483 - 48 8D A8 F8FEFFFF     - lea rbp,[rax-00000108]
victoria3.exe+122A48A - 48 81 EC C8010000     - sub rsp,000001C8
victoria3.exe+122A491 - C5F82970 A8           - vmovaps [rax-58],xmm6
victoria3.exe+122A496 - C5F82978 98           - vmovaps [rax-68],xmm7
victoria3.exe+122A49B - 48 8B DA              - mov rbx,rdx
victoria3.exe+122A49E - 4C 8B F1              - mov r14,rcx
victoria3.exe+122A4A1 - 45 33 FF              - xor r15d,r15d
victoria3.exe+122A4A4 - 44 89 BD 10010000     - mov [rbp+00000110],r15d
victoria3.exe+122A4AB - 45 33 C0              - xor r8d,r8d
victoria3.exe+122A4AE - 33 C0                 - xor eax,eax
victoria3.exe+122A4B0 - 4C 8D 91 A81D0000     - lea r10,[rcx+00001DA8]
victoria3.exe+122A4B7 - 49 0FBC 0A            - bsf rcx,[r10]
victoria3.exe+122A4BB - 74 05                 - je victoria3.exe+122A4C2
victoria3.exe+122A4BD - 83 F9 40              - cmp ecx,40
victoria3.exe+122A4C0 - 75 12                 - jne victoria3.exe+122A4D4
victoria3.exe+122A4C2 - 48 FF C0              - inc rax
victoria3.exe+122A4C5 - 49 83 C2 08           - add r10,08
victoria3.exe+122A4C9 - 48 83 F8 02           - cmp rax,02
victoria3.exe+122A4CD - 72 E8                 - jb victoria3.exe+122A4B7
victoria3.exe+122A4CF - E9 96000000           - jmp victoria3.exe+122A56A
victoria3.exe+122A4D4 - 48 C1 E0 06           - shl rax,06
victoria3.exe+122A4D8 - 48 63 C9              - movsxd  rcx,ecx
victoria3.exe+122A4DB - 48 03 C1              - add rax,rcx
victoria3.exe+122A4DE - 48 83 F8 FF           - cmp rax,-01
victoria3.exe+122A4E2 - 0F84 82000000         - je victoria3.exe+122A56A
victoria3.exe+122A4E8 - 4D 8B 9E 901D0000     - mov r11,[r14+00001D90]
victoria3.exe+122A4EF - 90                    - nop 
victoria3.exe+122A4F0 - 48 63 C8              - movsxd  rcx,eax
victoria3.exe+122A4F3 - 49 8B 14 CB           - mov rdx,[r11+rcx*8]
victoria3.exe+122A4F7 - 48 8B CA              - mov rcx,rdx
victoria3.exe+122A4FA - 48 C1 E9 3F           - shr rcx,3F
victoria3.exe+122A4FE - 84 C9                 - test cl,cl
victoria3.exe+122A500 - 74 03                 - je victoria3.exe+122A505
victoria3.exe+122A502 - 48 F7 DA              - neg rdx
victoria3.exe+122A505 - 4C 03 C2              - add r8,rdx
victoria3.exe+122A508 - 48 8D 48 01           - lea rcx,[rax+01]
victoria3.exe+122A50C - 4C 8B D1              - mov r10,rcx
victoria3.exe+122A50F - 49 C1 EA 06           - shr r10,06
victoria3.exe+122A513 - 4B 8B 94 D6 A81D0000  - mov rdx,[r14+r10*8+00001DA8]
victoria3.exe+122A51B - 48 D3 EA              - shr rdx,cl
victoria3.exe+122A51E - 48 0FBC CA            - bsf rcx,rdx
victoria3.exe+122A522 - 74 10                 - je victoria3.exe+122A534
victoria3.exe+122A524 - 83 F9 40              - cmp ecx,40
victoria3.exe+122A527 - 74 0B                 - je victoria3.exe+122A534
victoria3.exe+122A529 - 48 63 C9              - movsxd  rcx,ecx
victoria3.exe+122A52C - 48 FF C0              - inc rax
victoria3.exe+122A52F - 48 03 C1              - add rax,rcx
victoria3.exe+122A532 - EB 30                 - jmp victoria3.exe+122A564
victoria3.exe+122A534 - 49 8D 42 01           - lea rax,[r10+01]
victoria3.exe+122A538 - 48 83 F8 02           - cmp rax,02
victoria3.exe+122A53C - 73 1F                 - jae victoria3.exe+122A55D
victoria3.exe+122A53E - 66 90                 - nop 2
victoria3.exe+122A540 - 49 0FBC 8C C6 A81D0000  - bsf rcx,[r14+rax*8+00001DA8]
victoria3.exe+122A549 - 74 09                 - je victoria3.exe+122A554
victoria3.exe+122A54B - 83 F9 40              - cmp ecx,40
victoria3.exe+122A54E - 0F85 A8000000         - jne victoria3.exe+122A5FC
victoria3.exe+122A554 - 48 FF C0              - inc rax
victoria3.exe+122A557 - 48 83 F8 02           - cmp rax,02
victoria3.exe+122A55B - 72 E3                 - jb victoria3.exe+122A540
victoria3.exe+122A55D - 48 C7 C0 FFFFFFFF     - mov rax,FFFFFFFFFFFFFFFF
victoria3.exe+122A564 - 48 83 F8 FF           - cmp rax,-01
victoria3.exe+122A568 - 75 86                 - jne victoria3.exe+122A4F0
victoria3.exe+122A56A - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+122A574 - 49 F7 E8              - imul r8
victoria3.exe+122A577 - 4C 8B E2              - mov r12,rdx
victoria3.exe+122A57A - 49 C1 FC 0E           - sar r12,0E
victoria3.exe+122A57E - 49 8B C4              - mov rax,r12
victoria3.exe+122A581 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122A585 - 4C 03 E0              - add r12,rax
victoria3.exe+122A588 - 48 85 DB              - test rbx,rbx
victoria3.exe+122A58B - 0F84 DA040000         - je victoria3.exe+122AA6B
victoria3.exe+122A591 - 49 8B B6 D81D0000     - mov rsi,[r14+00001DD8]
victoria3.exe+122A598 - 49 63 86 E41D0000     - movsxd  rax,dword ptr [r14+00001DE4]
victoria3.exe+122A59F - 4C 8D 2C C6           - lea r13,[rsi+rax*8]
victoria3.exe+122A5A3 - 49 3B F5              - cmp rsi,r13
victoria3.exe+122A5A6 - 0F84 BF040000         - je victoria3.exe+122AA6B
victoria3.exe+122A5AC - C5FA6F35 0C BA5D03    - vmovdqu xmm6,xmm0,[victoria3.exe+4805FC0]
victoria3.exe+122A5B4 - C5FA6F3D 54 BB5D03    - vmovdqu xmm7,xmm0,[victoria3.exe+4806110]
victoria3.exe+122A5BC - 0F1F 40 00            - nop dword ptr [rax+00]
victoria3.exe+122A5C0 - 48 8B 3E              - mov rdi,[rsi]
victoria3.exe+122A5C3 - 48 63 5F 10           - movsxd  rbx,dword ptr [rdi+10]
victoria3.exe+122A5C7 - 8B CB                 - mov ecx,ebx
victoria3.exe+122A5C9 - E8 62C0DFFF           - call victoria3.exe+1026630
victoria3.exe+122A5CE - 84 C0                 - test al,al
victoria3.exe+122A5D0 - 74 39                 - je victoria3.exe+122A60B
victoria3.exe+122A5D2 - 0FB6 C3               - movzx eax,bl
victoria3.exe+122A5D5 - 24 3F                 - and al,3F
victoria3.exe+122A5D7 - 0FB6 C8               - movzx ecx,al
victoria3.exe+122A5DA - 48 8B C3              - mov rax,rbx
victoria3.exe+122A5DD - 48 C1 E8 06           - shr rax,06
victoria3.exe+122A5E1 - 49 8B 84 C6 A81D0000  - mov rax,[r14+rax*8+00001DA8]
victoria3.exe+122A5E9 - 48 0FA3 C8            - bt rax,rcx
victoria3.exe+122A5ED - 73 1C                 - jae victoria3.exe+122A60B
victoria3.exe+122A5EF - 49 8B 8E 901D0000     - mov rcx,[r14+00001D90]
victoria3.exe+122A5F6 - 48 8B 0C D9           - mov rcx,[rcx+rbx*8]
victoria3.exe+122A5FA - EB 11                 - jmp victoria3.exe+122A60D
victoria3.exe+122A5FC - 48 C1 E0 06           - shl rax,06
victoria3.exe+122A600 - 48 63 C9              - movsxd  rcx,ecx
victoria3.exe+122A603 - 48 03 C1              - add rax,rcx
victoria3.exe+122A606 - E9 59FFFFFF           - jmp victoria3.exe+122A564
victoria3.exe+122A60B - 33 C9                 - xor ecx,ecx
victoria3.exe+122A60D - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+122A617 - 48 F7 E9              - imul rcx
victoria3.exe+122A61A - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122A61E - 48 8B C2              - mov rax,rdx
victoria3.exe+122A621 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122A625 - 48 03 D0              - add rdx,rax
victoria3.exe+122A628 - 8B DA                 - mov ebx,edx
victoria3.exe+122A62A - F7 DB                 - neg ebx
victoria3.exe+122A62C - 0F48 DA               - cmovs ebx,edx
victoria3.exe+122A62F - 89 9D 20010000        - mov [rbp+00000120],ebx
victoria3.exe+122A635 - 4C 8B C7              - mov r8,rdi
victoria3.exe+122A638 - 48 8D 95 28010000     - lea rdx,[rbp+00000128]
victoria3.exe+122A63F - 49 8B CE              - mov rcx,r14
victoria3.exe+122A642 - E8 09050000           - call victoria3.exe+122AB50
victoria3.exe+122A647 - 48 63 D3              - movsxd  rdx,ebx
victoria3.exe+122A64A - 4C 69 C2 A0860100     - imul r8,rdx,000186A0
victoria3.exe+122A651 - 41 B9 33F304B5        - mov r9d,B504F333
victoria3.exe+122A657 - 4B 8D 04 08           - lea rax,[r8+r9]
victoria3.exe+122A65B - 48 8B 8D 28010000     - mov rcx,[rbp+00000128]
victoria3.exe+122A662 - 49 BA 66E6096A01000000 - mov r10,000000016A09E666
victoria3.exe+122A66C - 49 3B C2              - cmp rax,r10
victoria3.exe+122A66F - 77 0F                 - ja victoria3.exe+122A680
victoria3.exe+122A671 - 4A 8D 04 09           - lea rax,[rcx+r9]
victoria3.exe+122A675 - 49 3B C2              - cmp rax,r10
victoria3.exe+122A678 - 77 06                 - ja victoria3.exe+122A680
victoria3.exe+122A67A - 48 0FAF D1            - imul rdx,rcx
victoria3.exe+122A67E - EB 58                 - jmp victoria3.exe+122A6D8
victoria3.exe+122A680 - 4C 8B C9              - mov r9,rcx
victoria3.exe+122A683 - 49 3B C8              - cmp rcx,r8
victoria3.exe+122A686 - 4D 0F4C C8            - cmovl r9,r8
victoria3.exe+122A68A - 49 0F4F C8            - cmovg rcx,r8
victoria3.exe+122A68E - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+122A698 - 49 8B C2              - mov rax,r10
victoria3.exe+122A69B - 49 F7 E9              - imul r9
victoria3.exe+122A69E - 4C 8B C2              - mov r8,rdx
victoria3.exe+122A6A1 - 49 C1 F8 0E           - sar r8,0E
victoria3.exe+122A6A5 - 49 8B C0              - mov rax,r8
victoria3.exe+122A6A8 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122A6AC - 4C 03 C0              - add r8,rax
victoria3.exe+122A6AF - 49 69 C0 A0860100     - imul rax,r8,000186A0
victoria3.exe+122A6B6 - 4C 2B C8              - sub r9,rax
victoria3.exe+122A6B9 - 4C 0FAF C9            - imul r9,rcx
victoria3.exe+122A6BD - 49 8B C2              - mov rax,r10
victoria3.exe+122A6C0 - 49 F7 E9              - imul r9
victoria3.exe+122A6C3 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122A6C7 - 48 8B C2              - mov rax,rdx
victoria3.exe+122A6CA - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122A6CE - 48 03 D0              - add rdx,rax
victoria3.exe+122A6D1 - 4C 0FAF C1            - imul r8,rcx
victoria3.exe+122A6D5 - 49 03 D0              - add rdx,r8
victoria3.exe+122A6D8 - 48 89 55 B0           - mov [rbp-50],rdx
victoria3.exe+122A6DC - 48 89 7C 24 78        - mov [rsp+78],rdi
victoria3.exe+122A6E1 - 48 C7 45 80 FFFFFFFF  - mov qword ptr [rbp-80],FFFFFFFFFFFFFFFF
victoria3.exe+122A6E9 - 48 8B 05 D84D6C04     - mov rax,[victoria3.exe+58EF4C8]
victoria3.exe+122A6F0 - 48 89 45 88           - mov [rbp-78],rax
victoria3.exe+122A6F4 - 48 8B 0D 2D786C04     - mov rcx,[victoria3.exe+58F1F28]
victoria3.exe+122A6FB - 48 8D 1D 3EAC1A03     - lea rbx,[victoria3.exe+43D5340]
victoria3.exe+122A702 - 48 85 C9              - test rcx,rcx
victoria3.exe+122A705 - 75 2D                 - jne victoria3.exe+122A734
victoria3.exe+122A707 - 48 89 5D 10           - mov [rbp+10],rbx
victoria3.exe+122A70B - 48 C7 45 18 47000000  - mov qword ptr [rbp+18],00000047
victoria3.exe+122A713 - 48 8D 45 10           - lea rax,[rbp+10]
victoria3.exe+122A717 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122A71C - 48 8D 05 C5266C04     - lea rax,[victoria3.exe+58ECDE8]
victoria3.exe+122A723 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+122A728 - E8 E36E57FF           - call victoria3.exe+7A1610
victoria3.exe+122A72D - 48 8B 0D F4776C04     - mov rcx,[victoria3.exe+58F1F28]
victoria3.exe+122A734 - 48 8D 54 24 78        - lea rdx,[rsp+78]
victoria3.exe+122A739 - E8 A26E9BFF           - call victoria3.exe+BE15E0
victoria3.exe+122A73E - 48 89 44 24 70        - mov [rsp+70],rax
victoria3.exe+122A743 - 41 8B 46 08           - mov eax,[r14+08]
victoria3.exe+122A747 - 89 85 10010000        - mov [rbp+00000110],eax
victoria3.exe+122A74D - 48 8B 0D C4776C04     - mov rcx,[victoria3.exe+58F1F18]
victoria3.exe+122A754 - 48 85 C9              - test rcx,rcx
victoria3.exe+122A757 - 75 2D                 - jne victoria3.exe+122A786
victoria3.exe+122A759 - 48 89 5D 20           - mov [rbp+20],rbx
victoria3.exe+122A75D - 48 C7 45 28 47000000  - mov qword ptr [rbp+28],00000047
victoria3.exe+122A765 - 48 8D 45 20           - lea rax,[rbp+20]
victoria3.exe+122A769 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122A76E - 48 8D 05 73266C04     - lea rax,[victoria3.exe+58ECDE8]
victoria3.exe+122A775 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+122A77A - E8 916E57FF           - call victoria3.exe+7A1610
victoria3.exe+122A77F - 48 8B 0D 92776C04     - mov rcx,[victoria3.exe+58F1F18]
victoria3.exe+122A786 - 48 8D 95 10010000     - lea rdx,[rbp+00000110]
victoria3.exe+122A78D - E8 9E739BFF           - call victoria3.exe+BE1B30
victoria3.exe+122A792 - 48 89 85 10010000     - mov [rbp+00000110],rax
victoria3.exe+122A799 - 48 8D 05 C0422503     - lea rax,[victoria3.exe+447EA60]
victoria3.exe+122A7A0 - 48 89 45 D8           - mov [rbp-28],rax
victoria3.exe+122A7A4 - C7 45 E0 1A000000     - mov [rbp-20],0000001A
victoria3.exe+122A7AB - C6 45 E4 00           - mov byte ptr [rbp-1C],00
victoria3.exe+122A7AF - 48 8D 85 28010000     - lea rax,[rbp+00000128]
victoria3.exe+122A7B6 - 48 89 44 24 60        - mov [rsp+60],rax
victoria3.exe+122A7BB - 48 8D 44 24 70        - lea rax,[rsp+70]
victoria3.exe+122A7C0 - 48 89 44 24 50        - mov [rsp+50],rax
victoria3.exe+122A7C5 - 48 8D 45 B0           - lea rax,[rbp-50]
victoria3.exe+122A7C9 - 48 89 44 24 40        - mov [rsp+40],rax
victoria3.exe+122A7CE - 48 8D 85 20010000     - lea rax,[rbp+00000120]
victoria3.exe+122A7D5 - 48 89 44 24 30        - mov [rsp+30],rax
victoria3.exe+122A7DA - 48 8D 85 10010000     - lea rax,[rbp+00000110]
victoria3.exe+122A7E1 - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+122A7E6 - 48 8D 55 D8           - lea rdx,[rbp-28]
victoria3.exe+122A7EA - 48 8D 4D 40           - lea rcx,[rbp+40]
victoria3.exe+122A7EE - E8 0DF90000           - call victoria3.exe+123A100
victoria3.exe+122A7F3 - 41 83 CF 01           - or r15d,01
victoria3.exe+122A7F7 - 44 89 BD 10010000     - mov [rbp+00000110],r15d
victoria3.exe+122A7FE - 48 8B D7              - mov rdx,rdi
victoria3.exe+122A801 - 49 8B CE              - mov rcx,r14
victoria3.exe+122A804 - E8 C7020000           - call victoria3.exe+122AAD0
victoria3.exe+122A809 - 48 8D 15 40422503     - lea rdx,[victoria3.exe+447EA50]
victoria3.exe+122A810 - 3C 01                 - cmp al,01
victoria3.exe+122A812 - 48 8D 05 3F422503     - lea rax,[victoria3.exe+447EA58]
victoria3.exe+122A819 - 48 0F44 D0            - cmove rdx,rax
victoria3.exe+122A81D - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+122A821 - C5F81145 B8           - vmovups [rbp-48],xmm0
victoria3.exe+122A826 - C5F1EFC9              - vpxor xmm1,xmm1,xmm1
victoria3.exe+122A82A - C5FA7F4D C8           - vmovdqu [rbp-38],xmm1
victoria3.exe+122A82F - 49 C7 C0 FFFFFFFF     - mov r8,FFFFFFFFFFFFFFFF
victoria3.exe+122A836 - 49 FF C0              - inc r8
victoria3.exe+122A839 - 42 80 3C 02  00       - cmp byte ptr [rdx+r8],00
victoria3.exe+122A83E - 75 F6                 - jne victoria3.exe+122A836
victoria3.exe+122A840 - 48 8D 4D B8           - lea rcx,[rbp-48]
victoria3.exe+122A844 - E8 F77C3EFF           - call victoria3.exe+612540
victoria3.exe+122A849 - 90                    - nop 
victoria3.exe+122A84A - 48 8D 05 3FFB1803     - lea rax,[victoria3.exe+43BA390]
victoria3.exe+122A851 - 48 89 45 E8           - mov [rbp-18],rax
victoria3.exe+122A855 - C7 45 F0 01000000     - mov [rbp-10],00000001
victoria3.exe+122A85C - C6 45 F4 00           - mov byte ptr [rbp-0C],00
victoria3.exe+122A860 - 48 8D 55 E8           - lea rdx,[rbp-18]
victoria3.exe+122A864 - 48 8B 8D 18010000     - mov rcx,[rbp+00000118]
victoria3.exe+122A86B - E8 40A18802           - call victoria3.exe+3AB49B0
victoria3.exe+122A870 - 48 8D 55 40           - lea rdx,[rbp+40]
victoria3.exe+122A874 - 48 8D 8D 80000000     - lea rcx,[rbp+00000080]
victoria3.exe+122A87B - E8 30F0A801           - call victoria3.exe+2CB98B0
victoria3.exe+122A880 - 48 8B D8              - mov rbx,rax
victoria3.exe+122A883 - 48 89 7C 24 78        - mov [rsp+78],rdi
victoria3.exe+122A888 - 48 C7 45 80 FFFFFFFF  - mov qword ptr [rbp-80],FFFFFFFFFFFFFFFF
victoria3.exe+122A890 - 48 8B 0D 314C6C04     - mov rcx,[victoria3.exe+58EF4C8]
victoria3.exe+122A897 - 48 89 4D 88           - mov [rbp-78],rcx
victoria3.exe+122A89B - 48 8B 0D 86766C04     - mov rcx,[victoria3.exe+58F1F28]
victoria3.exe+122A8A2 - 48 85 C9              - test rcx,rcx
victoria3.exe+122A8A5 - 75 34                 - jne victoria3.exe+122A8DB
victoria3.exe+122A8A7 - 48 8D 05 92AA1A03     - lea rax,[victoria3.exe+43D5340]
victoria3.exe+122A8AE - 48 89 45 30           - mov [rbp+30],rax
victoria3.exe+122A8B2 - 48 C7 45 38 47000000  - mov qword ptr [rbp+38],00000047
victoria3.exe+122A8BA - 48 8D 45 30           - lea rax,[rbp+30]
victoria3.exe+122A8BE - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122A8C3 - 48 8D 05 1E256C04     - lea rax,[victoria3.exe+58ECDE8]
victoria3.exe+122A8CA - 48 89 44 24 20        - mov [rsp+20],rax
victoria3.exe+122A8CF - E8 3C6D57FF           - call victoria3.exe+7A1610
victoria3.exe+122A8D4 - 48 8B 0D 4D766C04     - mov rcx,[victoria3.exe+58F1F28]
victoria3.exe+122A8DB - 48 8D 54 24 78        - lea rdx,[rsp+78]
victoria3.exe+122A8E0 - E8 FB6C9BFF           - call victoria3.exe+BE15E0
victoria3.exe+122A8E5 - 48 89 44 24 70        - mov [rsp+70],rax
victoria3.exe+122A8EA - C5F9EFC0              - vpxor xmm0,xmm0,xmm0
victoria3.exe+122A8EE - C5F81145 90           - vmovups [rbp-70],xmm0
victoria3.exe+122A8F3 - C5F1EFC9              - vpxor xmm1,xmm1,xmm1
victoria3.exe+122A8F7 - C5FA7F4D A0           - vmovdqu [rbp-60],xmm1
victoria3.exe+122A8FC - B9 20000000           - mov ecx,00000020
victoria3.exe+122A901 - E8 3AAA3EFF           - call victoria3.exe+615340
victoria3.exe+122A906 - 48 89 45 90           - mov [rbp-70],rax
victoria3.exe+122A90A - C5FA7F7D A0           - vmovdqu [rbp-60],xmm7
victoria3.exe+122A90F - C5F81005 21 412503    - vmovups xmm0,[victoria3.exe+447EA38]
victoria3.exe+122A917 - C5F81100              - vmovups [rax],xmm0
victoria3.exe+122A91B - 8B 0D 27412503        - mov ecx,[victoria3.exe+447EA48]
victoria3.exe+122A921 - 89 48 10              - mov [rax+10],ecx
victoria3.exe+122A924 - 0FB6 0D 21412503      - movzx ecx,byte ptr [victoria3.exe+447EA4C]
victoria3.exe+122A92B - 88 48 14              - mov [rax+14],cl
victoria3.exe+122A92E - C6 40 15 00           - mov byte ptr [rax+15],00
victoria3.exe+122A932 - 41 83 CF 02           - or r15d,02
victoria3.exe+122A936 - 44 89 BD 10010000     - mov [rbp+00000110],r15d
victoria3.exe+122A93D - 48 8D 55 B8           - lea rdx,[rbp-48]
victoria3.exe+122A941 - 48 83 7D D0 0F        - cmp qword ptr [rbp-30],0F
victoria3.exe+122A946 - 48 0F47 55 B8         - cmova rdx,[rbp-48]
victoria3.exe+122A94B - 4C 8B 45 C8           - mov r8,[rbp-38]
victoria3.exe+122A94F - 48 8D 4D 90           - lea rcx,[rbp-70]
victoria3.exe+122A953 - E8 98957001           - call victoria3.exe+2933EF0
victoria3.exe+122A958 - 48 8D 45 90           - lea rax,[rbp-70]
victoria3.exe+122A95C - 48 83 7D A8 0F        - cmp qword ptr [rbp-58],0F
victoria3.exe+122A961 - 48 0F47 45 90         - cmova rax,[rbp-70]
victoria3.exe+122A966 - 48 89 45 F8           - mov [rbp-08],rax
victoria3.exe+122A96A - 8B 45 A0              - mov eax,[rbp-60]
victoria3.exe+122A96D - 89 45 00              - mov [rbp+00],eax
victoria3.exe+122A970 - C6 45 04 00           - mov byte ptr [rbp+04],00
victoria3.exe+122A974 - 48 89 5C 24 48        - mov [rsp+48],rbx
victoria3.exe+122A979 - 48 8D 44 24 70        - lea rax,[rsp+70]
victoria3.exe+122A97E - 48 89 44 24 38        - mov [rsp+38],rax
victoria3.exe+122A983 - 48 8D 45 B0           - lea rax,[rbp-50]
victoria3.exe+122A987 - 48 89 44 24 28        - mov [rsp+28],rax
victoria3.exe+122A98C - 4C 8D 8D 20010000     - lea r9,[rbp+00000120]
victoria3.exe+122A993 - 48 8D 55 F8           - lea rdx,[rbp-08]
victoria3.exe+122A997 - 48 8D 4D 60           - lea rcx,[rbp+60]
victoria3.exe+122A99B - E8 60AB0000           - call victoria3.exe+1235500
victoria3.exe+122A9A0 - 90                    - nop 
victoria3.exe+122A9A1 - 4C 8B 40 10           - mov r8,[rax+10]
victoria3.exe+122A9A5 - 48 83 78 18 0F        - cmp qword ptr [rax+18],0F
victoria3.exe+122A9AA - 76 03                 - jna victoria3.exe+122A9AF
victoria3.exe+122A9AC - 48 8B 00              - mov rax,[rax]
victoria3.exe+122A9AF - 48 8B D0              - mov rdx,rax
victoria3.exe+122A9B2 - 48 8B 8D 18010000     - mov rcx,[rbp+00000118]
victoria3.exe+122A9B9 - E8 32957001           - call victoria3.exe+2933EF0
victoria3.exe+122A9BE - 90                    - nop 
victoria3.exe+122A9BF - 48 8D 4D 60           - lea rcx,[rbp+60]
victoria3.exe+122A9C3 - E8 18AE3EFF           - call victoria3.exe+6157E0
victoria3.exe+122A9C8 - 41 83 E7 FD           - and r15d,-03
victoria3.exe+122A9CC - 48 8B 45 A8           - mov rax,[rbp-58]
victoria3.exe+122A9D0 - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+122A9D4 - 76 31                 - jna victoria3.exe+122AA07
victoria3.exe+122A9D6 - 48 8B 4D 90           - mov rcx,[rbp-70]
victoria3.exe+122A9DA - 48 8B D1              - mov rdx,rcx
victoria3.exe+122A9DD - 48 FF C0              - inc rax
victoria3.exe+122A9E0 - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+122A9E6 - 72 15                 - jb victoria3.exe+122A9FD
victoria3.exe+122A9E8 - 48 8B 49 F8           - mov rcx,[rcx-08]
victoria3.exe+122A9EC - 48 2B D1              - sub rdx,rcx
victoria3.exe+122A9EF - 48 83 EA 08           - sub rdx,08
victoria3.exe+122A9F3 - 48 83 FA 1F           - cmp rdx,1F
victoria3.exe+122A9F7 - 0F87 97000000         - ja victoria3.exe+122AA94
victoria3.exe+122A9FD - 48 85 C9              - test rcx,rcx
victoria3.exe+122AA00 - 74 05                 - je victoria3.exe+122AA07
victoria3.exe+122AA02 - E8 2959EF02           - call victoria3.exe+4120330
victoria3.exe+122AA07 - C5FA7F75 A0           - vmovdqu [rbp-60],xmm6
victoria3.exe+122AA0C - C6 45 90 00           - mov byte ptr [rbp-70],00
victoria3.exe+122AA10 - 48 8D 8D 80000000     - lea rcx,[rbp+00000080]
victoria3.exe+122AA17 - E8 C4AD3EFF           - call victoria3.exe+6157E0
victoria3.exe+122AA1C - 90                    - nop 
victoria3.exe+122AA1D - 48 8B 45 D0           - mov rax,[rbp-30]
victoria3.exe+122AA21 - 48 83 F8 0F           - cmp rax,0F
victoria3.exe+122AA25 - 76 2E                 - jna victoria3.exe+122AA55
victoria3.exe+122AA27 - 48 8B 4D B8           - mov rcx,[rbp-48]
victoria3.exe+122AA2B - 48 8B D1              - mov rdx,rcx
victoria3.exe+122AA2E - 48 FF C0              - inc rax
victoria3.exe+122AA31 - 48 3D 00100000        - cmp rax,00001000
victoria3.exe+122AA37 - 72 11                 - jb victoria3.exe+122AA4A
victoria3.exe+122AA39 - 48 8B 49 F8           - mov rcx,[rcx-08]
victoria3.exe+122AA3D - 48 2B D1              - sub rdx,rcx
victoria3.exe+122AA40 - 48 83 EA 08           - sub rdx,08
victoria3.exe+122AA44 - 48 83 FA 1F           - cmp rdx,1F
victoria3.exe+122AA48 - 77 63                 - ja victoria3.exe+122AAAD
victoria3.exe+122AA4A - 48 85 C9              - test rcx,rcx
victoria3.exe+122AA4D - 74 06                 - je victoria3.exe+122AA55
victoria3.exe+122AA4F - E8 DC58EF02           - call victoria3.exe+4120330
victoria3.exe+122AA54 - 90                    - nop 
victoria3.exe+122AA55 - 48 8D 4D 40           - lea rcx,[rbp+40]
victoria3.exe+122AA59 - E8 82AD3EFF           - call victoria3.exe+6157E0
victoria3.exe+122AA5E - 48 83 C6 08           - add rsi,08
victoria3.exe+122AA62 - 49 3B F5              - cmp rsi,r13
victoria3.exe+122AA65 - 0F85 55FBFFFF         - jne victoria3.exe+122A5C0
victoria3.exe+122AA6B - 41 8B C4              - mov eax,r12d
victoria3.exe+122AA6E - C5F828B4 24 B0 010000 - vmovaps xmm6,[rsp+000001B0]
victoria3.exe+122AA77 - C5F828BC 24 A0 010000 - vmovaps xmm7,[rsp+000001A0]
victoria3.exe+122AA80 - 48 81 C4 C8010000     - add rsp,000001C8
victoria3.exe+122AA87 - 41 5F                 - pop r15
victoria3.exe+122AA89 - 41 5E                 - pop r14
victoria3.exe+122AA8B - 41 5D                 - pop r13
victoria3.exe+122AA8D - 41 5C                 - pop r12
victoria3.exe+122AA8F - 5F                    - pop rdi
victoria3.exe+122AA90 - 5E                    - pop rsi
victoria3.exe+122AA91 - 5B                    - pop rbx
victoria3.exe+122AA92 - 5D                    - pop rbp
victoria3.exe+122AA93 - C3                    - ret 

# victoria3.exe+11FD370
victoria3.exe+11FD370 - 48 89 5C 24 08        - mov [rsp+08],rbx
victoria3.exe+11FD375 - 48 89 6C 24 18        - mov [rsp+18],rbp
victoria3.exe+11FD37A - 48 89 74 24 20        - mov [rsp+20],rsi
victoria3.exe+11FD37F - 48 89 54 24 10        - mov [rsp+10],rdx
victoria3.exe+11FD384 - 57                    - push rdi
victoria3.exe+11FD385 - 41 56                 - push r14
victoria3.exe+11FD387 - 41 57                 - push r15
victoria3.exe+11FD389 - 48 83 EC 30           - sub rsp,30
victoria3.exe+11FD38D - 49 8B D9              - mov rbx,r9
victoria3.exe+11FD390 - 4D 8B F0              - mov r14,r8
victoria3.exe+11FD393 - 4C 8B FA              - mov r15,rdx
victoria3.exe+11FD396 - 48 8B F1              - mov rsi,rcx
victoria3.exe+11FD399 - C7 44 24 20 00000000  - mov [rsp+20],00000000
victoria3.exe+11FD3A1 - 48 8B CA              - mov rcx,rdx
victoria3.exe+11FD3A4 - E8 175EC3FF           - call victoria3.exe+E331C0
victoria3.exe+11FD3A9 - C7 44 24 20 01000000  - mov [rsp+20],00000001
victoria3.exe+11FD3B1 - 49 8D 8F 90010000     - lea rcx,[r15+00000190]
victoria3.exe+11FD3B8 - 48 8B 54 24 78        - mov rdx,[rsp+78]
victoria3.exe+11FD3BD - E8 9E31A1FF           - call victoria3.exe+C10560
victoria3.exe+11FD3C2 - 49 8D 8F 40010000     - lea rcx,[r15+00000140]
victoria3.exe+11FD3C9 - 48 8B 54 24 70        - mov rdx,[rsp+70]
victoria3.exe+11FD3CE - E8 8D31A1FF           - call victoria3.exe+C10560
victoria3.exe+11FD3D3 - 49 8D 8F E0010000     - lea rcx,[r15+000001E0]
victoria3.exe+11FD3DA - 48 8B 94 24 88000000  - mov rdx,[rsp+00000088]
victoria3.exe+11FD3E2 - E8 7931A1FF           - call victoria3.exe+C10560
victoria3.exe+11FD3E7 - 49 8D 8F 30020000     - lea rcx,[r15+00000230]
victoria3.exe+11FD3EE - 48 8B 94 24 80000000  - mov rdx,[rsp+00000080]
victoria3.exe+11FD3F6 - E8 6531A1FF           - call victoria3.exe+C10560
victoria3.exe+11FD3FB - 48 8D 56 60           - lea rdx,[rsi+60]
victoria3.exe+11FD3FF - 49 8B CF              - mov rcx,r15
victoria3.exe+11FD402 - E8 5931A1FF           - call victoria3.exe+C10560
victoria3.exe+11FD407 - 49 8D 4F 50           - lea rcx,[r15+50]
victoria3.exe+11FD40B - 48 8D 56 10           - lea rdx,[rsi+10]
victoria3.exe+11FD40F - E8 4C31A1FF           - call victoria3.exe+C10560
victoria3.exe+11FD414 - 48 8B D3              - mov rdx,rbx
victoria3.exe+11FD417 - 49 8D 8F A0000000     - lea rcx,[r15+000000A0]
victoria3.exe+11FD41E - E8 3D31A1FF           - call victoria3.exe+C10560
victoria3.exe+11FD423 - 49 8B D6              - mov rdx,r14
victoria3.exe+11FD426 - 49 8D 8F F0000000     - lea rcx,[r15+000000F0]
victoria3.exe+11FD42D - E8 2E31A1FF           - call victoria3.exe+C10560
victoria3.exe+11FD432 - 48 8D 56 10           - lea rdx,[rsi+10]
victoria3.exe+11FD436 - 49 8D 8F A0000000     - lea rcx,[r15+000000A0]
victoria3.exe+11FD43D - E8 DEA9E2FF           - call victoria3.exe+1027E20
victoria3.exe+11FD442 - 48 8D 56 60           - lea rdx,[rsi+60]
victoria3.exe+11FD446 - 49 8D 8F F0000000     - lea rcx,[r15+000000F0]
victoria3.exe+11FD44D - E8 CEA9E2FF           - call victoria3.exe+1027E20
victoria3.exe+11FD452 - 49 8B C7              - mov rax,r15
victoria3.exe+11FD455 - 48 8B 5C 24 50        - mov rbx,[rsp+50]
victoria3.exe+11FD45A - 48 8B 6C 24 60        - mov rbp,[rsp+60]
victoria3.exe+11FD45F - 48 8B 74 24 68        - mov rsi,[rsp+68]
victoria3.exe+11FD464 - 48 83 C4 30           - add rsp,30
victoria3.exe+11FD468 - 41 5F                 - pop r15
victoria3.exe+11FD46A - 41 5E                 - pop r14
victoria3.exe+11FD46C - 5F                    - pop rdi
victoria3.exe+11FD46D - C3                    - ret 

# victoria3.exe+1027970
victoria3.exe+102796B - CC                    - int 3 
victoria3.exe+102796C - CC                    - int 3 
victoria3.exe+102796D - CC                    - int 3 
victoria3.exe+102796E - CC                    - int 3 
victoria3.exe+102796F - CC                    - int 3 
victoria3.exe+1027970 - 4D 85 C0              - test r8,r8
victoria3.exe+1027973 - 0F84 C5000000         - je victoria3.exe+1027A3E
victoria3.exe+1027979 - 53                    - push rbx
victoria3.exe+102797A - 57                    - push rdi
victoria3.exe+102797B - 48 83 EC 28           - sub rsp,28
victoria3.exe+102797F - 48 8B F9              - mov rdi,rcx
victoria3.exe+1027982 - 4C 89 7C 24 20        - mov [rsp+20],r15
victoria3.exe+1027987 - 4C 63 7A 10           - movsxd  r15,dword ptr [rdx+10]
victoria3.exe+102798B - 49 8B D8              - mov rbx,r8
victoria3.exe+102798E - 41 8B CF              - mov ecx,r15d
victoria3.exe+1027991 - E8 9AECFFFF           - call victoria3.exe+1026630
victoria3.exe+1027996 - 84 C0                 - test al,al
victoria3.exe+1027998 - 0F84 95000000         - je victoria3.exe+1027A33
victoria3.exe+102799E - 48 89 6C 24 40        - mov [rsp+40],rbp
victoria3.exe+10279A3 - 49 8B C7              - mov rax,r15
victoria3.exe+10279A6 - 48 C1 E8 06           - shr rax,06
victoria3.exe+10279AA - 41 0FB6 CF            - movzx ecx,r15b
victoria3.exe+10279AE - 48 89 74 24 48        - mov [rsp+48],rsi
victoria3.exe+10279B3 - BD 01000000           - mov ebp,00000001
victoria3.exe+10279B8 - 48 D3 E5              - shl rbp,cl
victoria3.exe+10279BB - 4C 8B C5              - mov r8,rbp
victoria3.exe+10279BE - 4C 89 74 24 50        - mov [rsp+50],r14
victoria3.exe+10279C3 - 48 8D 34 C7           - lea rsi,[rdi+rax*8]
victoria3.exe+10279C7 - 4E 8D 34 FD 00000000  - lea r14,[r15*8+00000000]
victoria3.exe+10279CF - 4C 23 46 20           - and r8,[rsi+20]
victoria3.exe+10279D3 - 74 0A                 - je victoria3.exe+10279DF
victoria3.exe+10279D5 - 48 8B 47 08           - mov rax,[rdi+08]
victoria3.exe+10279D9 - 49 8B 0C 06           - mov rcx,[r14+rax]
victoria3.exe+10279DD - EB 02                 - jmp victoria3.exe+10279E1
victoria3.exe+10279DF - 33 C9                 - xor ecx,ecx
victoria3.exe+10279E1 - 48 03 D9              - add rbx,rcx
victoria3.exe+10279E4 - 83 7F 48 00           - cmp dword ptr [rdi+48],00
victoria3.exe+10279E8 - 75 26                 - jne victoria3.exe+1027A10
victoria3.exe+10279EA - 48 85 DB              - test rbx,rbx
victoria3.exe+10279ED - 75 21                 - jne victoria3.exe+1027A10
victoria3.exe+10279EF - 4D 85 C0              - test r8,r8
victoria3.exe+10279F2 - 74 30                 - je victoria3.exe+1027A24
victoria3.exe+10279F4 - 48 8B 47 08           - mov rax,[rdi+08]
victoria3.exe+10279F8 - 48 F7 D5              - not rbp
victoria3.exe+10279FB - 41 8B D7              - mov edx,r15d
victoria3.exe+10279FE - 48 8B CF              - mov rcx,rdi
victoria3.exe+1027A01 - 49 89 1C 06           - mov [r14+rax],rbx
victoria3.exe+1027A05 - 48 21 6E 20           - and [rsi+20],rbp
victoria3.exe+1027A09 - E8 62EFFFFF           - call victoria3.exe+1026970
victoria3.exe+1027A0E - EB 14                 - jmp victoria3.exe+1027A24
victoria3.exe+1027A10 - 48 8B CF              - mov rcx,rdi
victoria3.exe+1027A13 - E8 E8ECFFFF           - call victoria3.exe+1026700
victoria3.exe+1027A18 - 48 8B 47 08           - mov rax,[rdi+08]
victoria3.exe+1027A1C - 49 89 1C 06           - mov [r14+rax],rbx
victoria3.exe+1027A20 - 48 09 6E 20           - or [rsi+20],rbp
victoria3.exe+1027A24 - 4C 8B 74 24 50        - mov r14,[rsp+50]
victoria3.exe+1027A29 - 48 8B 74 24 48        - mov rsi,[rsp+48]
victoria3.exe+1027A2E - 48 8B 6C 24 40        - mov rbp,[rsp+40]
victoria3.exe+1027A33 - 4C 8B 7C 24 20        - mov r15,[rsp+20]
victoria3.exe+1027A38 - 48 83 C4 28           - add rsp,28
victoria3.exe+1027A3C - 5F                    - pop rdi
victoria3.exe+1027A3D - 5B                    - pop rbx
victoria3.exe+1027A3E - C3                    - ret 

# victoria3.exe+122AB50
victoria3.exe+122AB46 - CC                    - int 3 
victoria3.exe+122AB47 - CC                    - int 3 
victoria3.exe+122AB48 - CC                    - int 3 
victoria3.exe+122AB49 - CC                    - int 3 
victoria3.exe+122AB4A - CC                    - int 3 
victoria3.exe+122AB4B - CC                    - int 3 
victoria3.exe+122AB4C - CC                    - int 3 
victoria3.exe+122AB4D - CC                    - int 3 
victoria3.exe+122AB4E - CC                    - int 3 
victoria3.exe+122AB4F - CC                    - int 3 
victoria3.exe+122AB50 - 48 89 5C 24 10        - mov [rsp+10],rbx
victoria3.exe+122AB55 - 57                    - push rdi
victoria3.exe+122AB56 - 48 83 EC 20           - sub rsp,20
victoria3.exe+122AB5A - 48 8B 89 B0180000     - mov rcx,[rcx+000018B0]
victoria3.exe+122AB61 - 48 8B FA              - mov rdi,rdx
victoria3.exe+122AB64 - 49 8B 58 50           - mov rbx,[r8+50]
victoria3.exe+122AB68 - 48 8D 54 24 30        - lea rdx,[rsp+30]
victoria3.exe+122AB6D - 44 0FB7 05 3BC4EA03   - movzx r8d,word ptr [victoria3.exe+50D6FB0]
victoria3.exe+122AB75 - 48 83 C1 10           - add rcx,10
victoria3.exe+122AB79 - E8 D29561FF           - call victoria3.exe+844150
victoria3.exe+122AB7E - 4C 8B 4C 24 30        - mov r9,[rsp+30]
victoria3.exe+122AB83 - B9 33F304B5           - mov ecx,B504F333
victoria3.exe+122AB88 - 49 81 C1 A0860100     - add r9,000186A0
victoria3.exe+122AB8F - 48 BA 66E6096A01000000 - mov rdx,000000016A09E666
victoria3.exe+122AB99 - 48 8D 04 0B           - lea rax,[rbx+rcx]
victoria3.exe+122AB9D - 48 3B C2              - cmp rax,rdx
victoria3.exe+122ABA0 - 77 2A                 - ja victoria3.exe+122ABCC
victoria3.exe+122ABA2 - 49 8D 04 09           - lea rax,[r9+rcx]
victoria3.exe+122ABA6 - 48 3B C2              - cmp rax,rdx
victoria3.exe+122ABA9 - 77 21                 - ja victoria3.exe+122ABCC
victoria3.exe+122ABAB - 4C 0FAF CB            - imul r9,rbx
victoria3.exe+122ABAF - 48 B8 09E1D1C6116BF129 - mov rax,29F16B11C6D1E109
victoria3.exe+122ABB9 - 49 F7 E9              - imul r9
victoria3.exe+122ABBC - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122ABC0 - 48 8B C2              - mov rax,rdx
victoria3.exe+122ABC3 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122ABC7 - 48 03 D0              - add rdx,rax
victoria3.exe+122ABCA - EB 58                 - jmp victoria3.exe+122AC24
victoria3.exe+122ABCC - 4C 3B CB              - cmp r9,rbx
victoria3.exe+122ABCF - 4D 8B C1              - mov r8,r9
victoria3.exe+122ABD2 - 49 BA 09E1D1C6116BF129 - mov r10,29F16B11C6D1E109
victoria3.exe+122ABDC - 4C 0F4C C3            - cmovl r8,rbx
victoria3.exe+122ABE0 - 4C 0F4F CB            - cmovg r9,rbx
victoria3.exe+122ABE4 - 49 8B C2              - mov rax,r10
victoria3.exe+122ABE7 - 49 F7 E8              - imul r8
victoria3.exe+122ABEA - 48 8B CA              - mov rcx,rdx
victoria3.exe+122ABED - 48 C1 F9 0E           - sar rcx,0E
victoria3.exe+122ABF1 - 48 8B C1              - mov rax,rcx
victoria3.exe+122ABF4 - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122ABF8 - 48 03 C8              - add rcx,rax
victoria3.exe+122ABFB - 48 69 C1 A0860100     - imul rax,rcx,000186A0
victoria3.exe+122AC02 - 49 0FAF C9            - imul rcx,r9
victoria3.exe+122AC06 - 4C 2B C0              - sub r8,rax
victoria3.exe+122AC09 - 49 8B C2              - mov rax,r10
victoria3.exe+122AC0C - 4D 0FAF C1            - imul r8,r9
victoria3.exe+122AC10 - 49 F7 E8              - imul r8
victoria3.exe+122AC13 - 48 C1 FA 0E           - sar rdx,0E
victoria3.exe+122AC17 - 48 8B C2              - mov rax,rdx
victoria3.exe+122AC1A - 48 C1 E8 3F           - shr rax,3F
victoria3.exe+122AC1E - 48 03 D0              - add rdx,rax
victoria3.exe+122AC21 - 48 03 D1              - add rdx,rcx
victoria3.exe+122AC24 - 48 8B 05 FDF16504     - mov rax,[victoria3.exe+5889E28]
victoria3.exe+122AC2B - 48 8B 5C 24 38        - mov rbx,[rsp+38]
victoria3.exe+122AC30 - 48 3B C2              - cmp rax,rdx
victoria3.exe+122AC33 - 48 0F4C C2            - cmovl rax,rdx
victoria3.exe+122AC37 - 48 89 07              - mov [rdi],rax
victoria3.exe+122AC3A - 48 8B C7              - mov rax,rdi
victoria3.exe+122AC3D - 48 83 C4 20           - add rsp,20
victoria3.exe+122AC41 - 5F                    - pop rdi
victoria3.exe+122AC42 - C3                    - ret 

# victoria3.exe+122BD40
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



+1229C50
    └─ 计算并返回 +1D58

+122A470
    ├─ 遍历 +1DD8/+1DE4 的对象列表
    ├─ 使用 +1DA8 位图、+1D90 指针表
    ├─ 调用 +122AB50 做定点分配
    └─ 返回并写入 +1D5C

+122BD40
    ├─ 遍历对象
    ├─ 调用 +122AC50 取得条目
    └─ 调用 +11FAF20 应用结果

+11FD370
    └─ 构造/填充路线或计算对象

+1027970
    └─ 更新位图缓存

目前最有价值的不是 +1027970，而是：
1. +122A470 的循环体；
2. +122AB50 的输入；
3. +11FAF20 的输出；
4. +1229C50 的返回值来源。


当前最合理的判断是：
- +1229C50：总容量/基础容量计算；
- +122A470：已用容量或容量占用聚合；
- +122AB50：容量分配的定点数插值/限制；
- +122BD40：把计算结果应用到各路线或对象；

很有价值了。因为我大概了解到，一定存在一个贸易容量的分配过程，他会将九州总的贸易容量（138）分配给各个商品。并且这个分配过程是迭代的，会在每周进行一次迭代更新，尝试对每个商品进行一次根据当前市场情况的贸易量重算。所以一定存在一个遍历函数，以及获取了贸易容量 32FDB11F8B8 或 32FDB11F8BC 之后，将其进行分配的函数。根据我新补充的信息，再思考一下，哪里是最有价值的

当前最强判断是：
+1229C50  = 计算九州总贸易容量 138
+122A470  = 遍历商品/路线并计算容量分配总量 （第一优先级）
+122AB50  = 单个商品/路线的容量份额计算 （第二优先级）
+122BD40  = 遍历对象并把结果应用到贸易路线
+11FAF20  = 可能的最终数量/状态写回