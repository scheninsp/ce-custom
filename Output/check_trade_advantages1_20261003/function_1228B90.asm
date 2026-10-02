+1228B90 48895C2410                     mov [rsp+10],rbx
+1228B95 55                             push rbp
+1228B96 56                             push rsi
+1228B97 57                             push rdi
+1228B98 4154                           push r12
+1228B9A 4155                           push r13
+1228B9C 4156                           push r14
+1228B9E 4157                           push r15
+1228BA0 488DAC2480FEFFFF               lea rbp,[rsp-00000180]
+1228BA8 4881EC80020000                 sub rsp,00000280
+1228BAF C5F829B42470020000             vmovaps [rsp+00000270],xmm6
+1228BB8 4C8BFA                         mov r15,rdx
+1228BBB 4C8BE9                         mov r13,rcx
+1228BBE 4533E4                         xor r12d,r12d
+1228BC1 4489A5C0010000                 mov [rbp+000001C0],r12d
+1228BC8 488B99B0180000                 mov rbx,[rcx+000018B0]
+1228BCF 48895D50                       mov [rbp+50],rbx
+1228BD3 4885DB                         test rbx,rbx
+1228BD6 7404                           je 7FF777D18BDC
+1228BD8 F0FF4308                       lock inc [rbx+08]
+1228BDC C5F9EFC0                       vpxor xmm0,xmm0,xmm0
+1228BE0 C5F811442440                   vmovups [rsp+40],xmm0
+1228BE6 C5FA6F35D2D35D03               vmovdqu xmm6,[7FF77B2F5FC0]
+1228BEE C5FA7F742450                   vmovdqu [rsp+50],xmm6
+1228BF4 C644244000                     mov byte ptr [rsp+40],00
+1228BF9 488D442440                     lea rax,[rsp+40]
+1228BFE 4889442420                     mov [rsp+20],rax
+1228C03 440FB70D85E3EA03               movzx r9d,word ptr [7FF77BBC6F90]
+1228C0B 4C8D4550                       lea r8,[rbp+50]
+1228C0F BA02000000                     mov edx,00000002
+1228C14 498BCF                         mov rcx,r15
+1228C17 E894539CFF                     call 7FF7776DDFB0
+1228C1C 90                             nop 
+1228C1D 488B442458                     mov rax,[rsp+58]
+1228C22 4883F80F                       cmp rax,0F
+1228C26 7635                           jna 7FF777D18C5D
+1228C28 488B542440                     mov rdx,[rsp+40]
+1228C2D 488BCA                         mov rcx,rdx
+1228C30 48FFC0                         inc rax
+1228C33 483D00100000                   cmp rax,00001000
+1228C39 7215                           jb 7FF777D18C50
+1228C3B 488B52F8                       mov rdx,[rdx-08]
+1228C3F 482BCA                         sub rcx,rdx
+1228C42 4883E908                       sub rcx,08
+1228C46 4883F91F                       cmp rcx,1F
+1228C4A 0F8798080000                   ja 7FF777D194E8
+1228C50 4885D2                         test rdx,rdx
+1228C53 7408                           je 7FF777D18C5D
+1228C55 488BCA                         mov rcx,rdx
+1228C58 E8D376EF02                     call 7FF77AC10330
+1228C5D 498BCD                         mov rcx,r13
+1228C60 E8AB8E0000                     call 7FF777D21B10
+1228C65 488BF0                         mov rsi,rax
+1228C68 488D4808                       lea rcx,[rax+08]
+1228C6C 488B11                         mov rdx,[rcx]
+1228C6F FF5208                         call qword ptr [rdx+08]
+1228C72 41BE33F304B5                   mov r14d,B504F333
+1228C78 84C0                           test al,al
+1228C7A 0F8498050000                   je 7FF777D19218
+1228C80 83BEE800000000                 cmp dword ptr [rsi+000000E8],00
+1228C87 0F8E8B050000                   jng 7FF777D19218
+1228C8D E8DE3B58FF                     call 7FF77729C870
+1228C92 488BB8600F0000                 mov rdi,[rax+00000F60]
+1228C99 488BCE                         mov rcx,rsi
+1228C9C E89F6FC1FF                     call 7FF77792FC40
+1228CA1 4C8BC7                         mov r8,rdi
+1228CA4 488D95D8010000                 lea rdx,[rbp+000001D8]
+1228CAB 488BC8                         mov rcx,rax
+1228CAE E85DE7DFFF                     call 7FF777B17410
+1228CB3 488B85D8010000                 mov rax,[rbp+000001D8]
+1228CBA 4885C0                         test rax,rax
+1228CBD 0F8E55050000                   jng 7FF777D19218
+1228CC3 4C8B0DD6106604                 mov r9,[7FF77C379DA0]
+1228CCA 493BC6                         cmp rax,r14
+1228CCD 7F37                           jg 7FF777D18D06
+1228CCF 4B8D0C31                       lea rcx,[r9+r14]
+1228CD3 48BA66E6096A01000000           mov rdx,000000016A09E666
+1228CDD 483BCA                         cmp rcx,rdx
+1228CE0 7724                           ja 7FF777D18D06
+1228CE2 4C0FAFC8                       imul r9,rax
+1228CE6 48B809E1D1C6116BF129           mov rax,29F16B11C6D1E109
+1228CF0 49F7E9                         imul r9
+1228CF3 488BFA                         mov rdi,rdx
+1228CF6 48C1FF0E                       sar rdi,0E
+1228CFA 488BC7                         mov rax,rdi
+1228CFD 48C1E83F                       shr rax,3F
+1228D01 4803F8                         add rdi,rax
+1228D04 EB5B                           jmp 7FF777D18D61
+1228D06 4D8BC1                         mov r8,r9
+1228D09 4C3BC8                         cmp r9,rax
+1228D0C 4C0F4CC0                       cmovl r8,rax
+1228D10 4C0F4FC8                       cmovg r9,rax
+1228D14 49BA09E1D1C6116BF129           mov r10,29F16B11C6D1E109
+1228D1E 498BC2                         mov rax,r10
+1228D21 49F7E8                         imul r8
+1228D24 488BCA                         mov rcx,rdx
+1228D27 48C1F90E                       sar rcx,0E
+1228D2B 488BC1                         mov rax,rcx
+1228D2E 48C1E83F                       shr rax,3F
+1228D32 4803C8                         add rcx,rax
+1228D35 4869C1A0860100                 imul rax,rcx,000186A0
+1228D3C 4C2BC0                         sub r8,rax
+1228D3F 4D0FAFC1                       imul r8,r9
+1228D43 498BC2                         mov rax,r10
+1228D46 49F7E8                         imul r8
+1228D49 488BFA                         mov rdi,rdx
+1228D4C 48C1FF0E                       sar rdi,0E
+1228D50 488BC7                         mov rax,rdi
+1228D53 48C1E83F                       shr rax,3F
+1228D57 4803F8                         add rdi,rax
+1228D5A 490FAFC9                       imul rcx,r9
+1228D5E 4803F9                         add rdi,rcx
+1228D61 48897D58                       mov [rbp+58],rdi
+1228D65 C5F9EFC0                       vpxor xmm0,xmm0,xmm0
+1228D69 C5F81145B0                     vmovups [rbp-50],xmm0
+1228D6E C5FA7F75C0                     vmovdqu [rbp-40],xmm6
+1228D73 C645B000                       mov byte ptr [rbp-50],00
+1228D77 488D05AA4B2503                 lea rax,[7FF77AF6D928]
+1228D7E 48894570                       mov [rbp+70],rax
+1228D82 488D4558                       lea rax,[rbp+58]
+1228D86 48894578                       mov [rbp+78],rax
+1228D8A 488D85D8010000                 lea rax,[rbp+000001D8]
+1228D91 48898580000000                 mov [rbp+00000080],rax
+1228D98 488D4D70                       lea rcx,[rbp+70]
+1228D9C 48898DA8000000                 mov [rbp+000000A8],rcx
+1228DA3 488D0586B12003                 lea rax,[7FF77AF23F30]
+1228DAA 488985F0000000                 mov [rbp+000000F0],rax
+1228DB1 488D45B0                       lea rax,[rbp-50]
+1228DB5 488985F8000000                 mov [rbp+000000F8],rax
+1228DBC 4C8D85F0000000                 lea r8,[rbp+000000F0]
+1228DC3 4C898528010000                 mov [rbp+00000128],r8
+1228DCA 48897D80                       mov [rbp-80],rdi
+1228DCE 49017F10                       add [r15+10],rdi
+1228DD2 41807F3101                     cmp byte ptr [r15+31],01
+1228DD7 0F85BF030000                   jne 7FF777D1919C
+1228DDD 4D8B7738                       mov r14,[r15+38]
+1228DE1 4180BEAC01000000               cmp byte ptr [r14+000001AC],00
+1228DE9 7409                           je 7FF777D18DF4
+1228DEB 4885FF                         test rdi,rdi
+1228DEE 0F84A2030000                   je 7FF777D19196
+1228DF4 488D55F0                       lea rdx,[rbp-10]
+1228DF8 488D4D70                       lea rcx,[rbp+70]
+1228DFC E8EF570100                     call 7FF777D2E5F0
+1228E01 90                             nop 
+1228E02 48837D0000                     cmp qword ptr [rbp+00],00
+1228E07 7509                           jne 7FF777D18E12
+1228E09 4885FF                         test rdi,rdi
+1228E0C 0F846D030000                   je 7FF777D1917F
+1228E12 498D8E50010000                 lea rcx,[r14+00000150]
+1228E19 E80240A2FF                     call 7FF77773CE20
+1228E1E 488BF0                         mov rsi,rax
+1228E21 C7402802000000                 mov [rax+28],00000002
+1228E28 48897820                       mov [rax+20],rdi
+1228E2C 488B8D28010000                 mov rcx,[rbp+00000128]
+1228E33 4885C9                         test rcx,rcx
+1228E36 0F84C1060000                   je 7FF777D194FD
+1228E3C 488B01                         mov rax,[rcx]
+1228E3F 488D5530                       lea rdx,[rbp+30]
+1228E43 FF5010                         call qword ptr [rax+10]
+1228E46 C785C001000003000000           mov [rbp+000001C0],00000003
+1228E50 48837D4000                     cmp qword ptr [rbp+40],00
+1228E55 0F84E5020000                   je 7FF777D19140
+1228E5B 418BBEB0010000                 mov edi,[r14+000001B0]
+1228E62 488BCE                         mov rcx,rsi
+1228E65 48837D0000                     cmp qword ptr [rbp+00],00
+1228E6A 0F85A4000000                   jne 7FF777D18F14
+1228E70 E88B383FFF                     call 7FF77710C700
+1228E75 498BD6                         mov rdx,r14
+1228E78 488BCE                         mov rcx,rsi
+1228E7B E8209A1900                     call 7FF777EB28A0
+1228E80 897C2420                       mov [rsp+20],edi
+1228E84 4533C9                         xor r9d,r9d
+1228E87 41B802000000                   mov r8d,00000002
+1228E8D 488D542440                     lea rdx,[rsp+40]
+1228E92 498BCF                         mov rcx,r15
+1228E95 E806649CFF                     call 7FF7776DF2A0
+1228E9A 90                             nop 
+1228E9B 488D442440                     lea rax,[rsp+40]
+1228EA0 48837C24580F                   cmp qword ptr [rsp+58],0F
+1228EA6 480F47442440                   cmova rax,[rsp+40]
+1228EAC 4889442460                     mov [rsp+60],rax
+1228EB1 8B442450                       mov eax,[rsp+50]
+1228EB5 89442468                       mov [rsp+68],eax
+1228EB9 C644246C00                     mov byte ptr [rsp+6C],00
+1228EBE 488D4530                       lea rax,[rbp+30]
+1228EC2 4889442428                     mov [rsp+28],rax
+1228EC7 4C8D4D80                       lea r9,[rbp-80]
+1228ECB 488D542460                     lea rdx,[rsp+60]
+1228ED0 488D4D90                       lea rcx,[rbp-70]
+1228ED4 E8D71BA2FF                     call 7FF77773AAB0
+1228ED9 90                             nop 
+1228EDA 4C8B4010                       mov r8,[rax+10]
+1228EDE 488378180F                     cmp qword ptr [rax+18],0F
+1228EE3 7603                           jna 7FF777D18EE8
+1228EE5 488B00                         mov rax,[rax]
+1228EE8 488BD0                         mov rdx,rax
+1228EEB 488BCE                         mov rcx,rsi
+1228EEE E8FDAF7001                     call 7FF779423EF0
+1228EF3 90                             nop 
+1228EF4 488D4D90                       lea rcx,[rbp-70]
+1228EF8 E8E3C83EFF                     call 7FF7771057E0
+1228EFD 90                             nop 
+1228EFE 488D4C2440                     lea rcx,[rsp+40]
+1228F03 E8D8C83EFF                     call 7FF7771057E0
+1228F08 4589A6B0010000                 mov [r14+000001B0],r12d
+1228F0F E961020000                     jmp 7FF777D19175
+1228F14 E8E7373FFF                     call 7FF77710C700
+1228F19 498BD6                         mov rdx,r14
+1228F1C 488BCE                         mov rcx,rsi
+1228F1F E87C991900                     call 7FF777EB28A0
+1228F24 41807F3101                     cmp byte ptr [r15+31],01
+1228F29 7417                           je 7FF777D18F42
+1228F2B C5F9EFC0                       vpxor xmm0,xmm0,xmm0
+1228F2F C5F81145D0                     vmovups [rbp-30],xmm0
+1228F34 C5FA7F75E0                     vmovdqu [rbp-20],xmm6
+1228F39 C645D000                       mov byte ptr [rbp-30],00
+1228F3D E96B010000                     jmp 7FF777D190AD
+1228F42 C5F1EFC9                       vpxor xmm1,xmm1,xmm1
+1228F46 C5F8114C2460                   vmovups [rsp+60],xmm1
+1228F4C C5FA7F742470                   vmovdqu [rsp+70],xmm6
+1228F52 C644246000                     mov byte ptr [rsp+60],00
+1228F57 41B804000000                   mov r8d,00000004
+1228F5D 488D15308C2003                 lea rdx,[7FF77AF21B94]
+1228F64 488D4C2460                     lea rcx,[rsp+60]
+1228F69 E8A2C23EFF                     call 7FF777105210
+1228F6E 498B5738                       mov rdx,[r15+38]
+1228F72 4881C288010000                 add rdx,00000188
+1228F79 488D4D10                       lea rcx,[rbp+10]
+1228F7D E89E963EFF                     call 7FF777102620
+1228F82 C785C00100000B000000           mov [rbp+000001C0],0000000B
+1228F8C 41B811000000                   mov r8d,00000011
+1228F92 488D15278C2003                 lea rdx,[7FF77AF21BC0]
+1228F99 488D4D10                       lea rcx,[rbp+10]
+1228F9D E84EAF7001                     call 7FF779423EF0
+1228FA2 90                             nop 
+1228FA3 C5FC104510                     vmovups ymm0,[rbp+10]
+1228FA8 C5FC114590                     vmovups [rbp-70],ymm0
+1228FAD C5FA7F7520                     vmovdqu [rbp+20],xmm6
+1228FB2 C6451000                       mov byte ptr [rbp+10],00
+1228FB6 C785C00100001B000000           mov [rbp+000001C0],0000001B
+1228FC0 488D542460                     lea rdx,[rsp+60]
+1228FC5 48837C24780F                   cmp qword ptr [rsp+78],0F
+1228FCB 480F47542460                   cmova rdx,[rsp+60]
+1228FD1 4C8B442470                     mov r8,[rsp+70]
+1228FD6 488D4D90                       lea rcx,[rbp-70]
+1228FDA C5F877                         vzeroupper 
+1228FDD E80EAF7001                     call 7FF779423EF0
+1228FE2 4C8D05EB8B2003                 lea r8,[7FF77AF21BD4]
+1228FE9 488D5590                       lea rdx,[rbp-70]
+1228FED 488D4C2440                     lea rcx,[rsp+40]
+1228FF2 E8097E58FF                     call 7FF7772A0E00
+1228FF7 90                             nop 
+1228FF8 4C8B45A8                       mov r8,[rbp-58]
+1228FFC 4983F80F                       cmp r8,0F
+1229000 760D                           jna 7FF777D1900F
+1229002 488B5590                       mov rdx,[rbp-70]
+1229006 488D4D90                       lea rcx,[rbp-70]
+122900A E851CC3EFF                     call 7FF777105C60
+122900F C5FA7F75A0                     vmovdqu [rbp-60],xmm6
+1229014 C6459000                       mov byte ptr [rbp-70],00
+1229018 4C8B4528                       mov r8,[rbp+28]
+122901C 4983F80F                       cmp r8,0F
+1229020 760D                           jna 7FF777D1902F
+1229022 488B5510                       mov rdx,[rbp+10]
+1229026 488D4D10                       lea rcx,[rbp+10]
+122902A E831CC3EFF                     call 7FF777105C60
+122902F C5FA7F7520                     vmovdqu [rbp+20],xmm6
+1229034 C6451000                       mov byte ptr [rbp+10],00
+1229038 41B811000000                   mov r8d,00000011
+122903E 488D15AB8B2003                 lea rdx,[7FF77AF21BF0]
+1229045 488D4C2440                     lea rcx,[rsp+40]
+122904A E8A1AE7001                     call 7FF779423EF0
+122904F 83FF01                         cmp edi,01
+1229052 7509                           jne 7FF777D1905D
+1229054 488D15858B2003                 lea rdx,[7FF77AF21BE0]
+122905B EB0C                           jmp 7FF777D19069
+122905D 83FF02                         cmp edi,02
+1229060 7517                           jne 7FF777D19079
+1229062 488D15BF8C2003                 lea rdx,[7FF77AF21D28]
+1229069 41B809000000                   mov r8d,00000009
+122906F 488D4C2440                     lea rcx,[rsp+40]
+1229074 E877AE7001                     call 7FF779423EF0
+1229079 C5FC10442440                   vmovups ymm0,[rsp+40]
+122907F C5FC1145D0                     vmovups [rbp-30],ymm0
+1229084 C5FA7F742450                   vmovdqu [rsp+50],xmm6
+122908A C644244000                     mov byte ptr [rsp+40],00
+122908F 4C8B442478                     mov r8,[rsp+78]
+1229094 4983F80F                       cmp r8,0F
+1229098 7613                           jna 7FF777D190AD
+122909A 488B542460                     mov rdx,[rsp+60]
+122909F 488D4C2460                     lea rcx,[rsp+60]
+12290A4 C5F877                         vzeroupper 
+12290A7 E8B4CB3EFF                     call 7FF777105C60
+12290AC 90                             nop 
+12290AD 488D55F0                       lea rdx,[rbp-10]
+12290B1 488D4D90                       lea rcx,[rbp-70]
+12290B5 C5F877                         vzeroupper 
+12290B8 E8F307A901                     call 7FF7797A98B0
+12290BD 90                             nop 
+12290BE 488D4DD0                       lea rcx,[rbp-30]
+12290C2 48837DE80F                     cmp qword ptr [rbp-18],0F
+12290C7 480F474DD0                     cmova rcx,[rbp-30]
+12290CC 48894C2460                     mov [rsp+60],rcx
+12290D1 8B4DE0                         mov ecx,[rbp-20]
+12290D4 894C2468                       mov [rsp+68],ecx
+12290D8 C644246C00                     mov byte ptr [rsp+6C],00
+12290DD 4889442438                     mov [rsp+38],rax
+12290E2 488D4530                       lea rax,[rbp+30]
+12290E6 4889442428                     mov [rsp+28],rax
+12290EB 4C8D4D80                       lea r9,[rbp-80]
+12290EF 488D542460                     lea rdx,[rsp+60]
+12290F4 488D4C2440                     lea rcx,[rsp+40]
+12290F9 E8723EA2FF                     call 7FF77773CF70
+12290FE 90                             nop 
+12290FF 488BD0                         mov rdx,rax
+1229102 488BCE                         mov rcx,rsi
+1229105 E886A98802                     call 7FF77A5A3A90
+122910A 90                             nop 
+122910B 488D4C2440                     lea rcx,[rsp+40]
+1229110 E8CBC63EFF                     call 7FF7771057E0
+1229115 90                             nop 
+1229116 488D4D90                       lea rcx,[rbp-70]
+122911A E8C1C63EFF                     call 7FF7771057E0
+122911F 90                             nop 
+1229120 4C8B45E8                       mov r8,[rbp-18]
+1229124 4983F80F                       cmp r8,0F
+1229128 760D                           jna 7FF777D19137
+122912A 488B55D0                       mov rdx,[rbp-30]
+122912E 488D4DD0                       lea rcx,[rbp-30]
+1229132 E829CB3EFF                     call 7FF777105C60
+1229137 4589A6B0010000                 mov [r14+000001B0],r12d
+122913E EB35                           jmp 7FF777D19175
+1229140 48837D0000                     cmp qword ptr [rbp+00],00
+1229145 742E                           je 7FF777D19175
+1229147 488BCE                         mov rcx,rsi
+122914A E8B1353FFF                     call 7FF77710C700
+122914F 498BD6                         mov rdx,r14
+1229152 488BCE                         mov rcx,rsi
+1229155 E846971900                     call 7FF777EB28A0
+122915A 488D55F0                       lea rdx,[rbp-10]
+122915E 48837D080F                     cmp qword ptr [rbp+08],0F
+1229163 480F4755F0                     cmova rdx,[rbp-10]
+1229168 4C8B4500                       mov r8,[rbp+00]
+122916C 488BCE                         mov rcx,rsi
+122916F E87CAD7001                     call 7FF779423EF0
+1229174 90                             nop 
+1229175 488D4D30                       lea rcx,[rbp+30]
+1229179 E862C63EFF                     call 7FF7771057E0
+122917E 90                             nop 
+122917F 488D4DF0                       lea rcx,[rbp-10]
+1229183 E858C63EFF                     call 7FF7771057E0
+1229188 4C8B8528010000                 mov r8,[rbp+00000128]
+122918F 488B8DA8000000                 mov rcx,[rbp+000000A8]
+1229196 41BE33F304B5                   mov r14d,B504F333
+122919C 4D85C0                         test r8,r8
+122919F 741D                           je 7FF777D191BE
+12291A1 488D85F0000000                 lea rax,[rbp+000000F0]
+12291A8 4C3BC0                         cmp r8,rax
+12291AB 0F95C2                         setne dl
+12291AE 498B00                         mov rax,[r8]
+12291B1 498BC8                         mov rcx,r8
+12291B4 FF5020                         call qword ptr [rax+20]
+12291B7 488B8DA8000000                 mov rcx,[rbp+000000A8]
+12291BE 4885C9                         test rcx,rcx
+12291C1 7417                           je 7FF777D191DA
+12291C3 488D4570                       lea rax,[rbp+70]
+12291C7 483BC8                         cmp rcx,rax
+12291CA 0F95C2                         setne dl
+12291CD 488B01                         mov rax,[rcx]
+12291D0 FF5020                         call qword ptr [rax+20]
+12291D3 4C89A5A8000000                 mov [rbp+000000A8],r12
+12291DA 488B45C8                       mov rax,[rbp-38]
+12291DE 4883F80F                       cmp rax,0F
+12291E2 7634                           jna 7FF777D19218
+12291E4 488B55B0                       mov rdx,[rbp-50]
+12291E8 488BCA                         mov rcx,rdx
+12291EB 48FFC0                         inc rax
+12291EE 483D00100000                   cmp rax,00001000
+12291F4 7215                           jb 7FF777D1920B
+12291F6 488B52F8                       mov rdx,[rdx-08]
+12291FA 482BCA                         sub rcx,rdx
+12291FD 4883E908                       sub rcx,08
+1229201 4883F91F                       cmp rcx,1F
+1229205 0F87F8020000                   ja 7FF777D19503
+122920B 4885D2                         test rdx,rdx
+122920E 7408                           je 7FF777D19218
+1229210 488BCA                         mov rcx,rdx
+1229213 E81871EF02                     call 7FF77AC10330
+1229218 496385581D0000                 movsxd  rax,dword ptr [r13+00001D58]
+122921F 4869F8A0860100                 imul rdi,rax,000186A0
+1229226 48897D60                       mov [rbp+60],rdi
+122922A 440FB70562DDEA03               movzx r8d,word ptr [7FF77BBC6F94]
+1229232 488D95C0010000                 lea rdx,[rbp+000001C0]
+1229239 488D4B10                       lea rcx,[rbx+10]
+122923D E80EAF61FF                     call 7FF777334150
+1229242 4C8B8DC0010000                 mov r9,[rbp+000001C0]
+1229249 4A8D0C37                       lea rcx,[rdi+r14]
+122924D 48B866E6096A01000000           mov rax,000000016A09E666
+1229257 483BC8                         cmp rcx,rax
+122925A 772D                           ja 7FF777D19289
+122925C 4B8D0C31                       lea rcx,[r9+r14]
+1229260 483BC8                         cmp rcx,rax
+1229263 7724                           ja 7FF777D19289
+1229265 4C0FAFCF                       imul r9,rdi
+1229269 48B809E1D1C6116BF129           mov rax,29F16B11C6D1E109
+1229273 49F7E9                         imul r9
+1229276 488BFA                         mov rdi,rdx
+1229279 48C1FF0E                       sar rdi,0E
+122927D 488BC7                         mov rax,rdi
+1229280 48C1E83F                       shr rax,3F
+1229284 4803F8                         add rdi,rax
+1229287 EB5B                           jmp 7FF777D192E4
+1229289 498BC9                         mov rcx,r9
+122928C 4C3BCF                         cmp r9,rdi
+122928F 480F4CCF                       cmovl rcx,rdi
+1229293 4C0F4FCF                       cmovg r9,rdi
+1229297 49BA09E1D1C6116BF129           mov r10,29F16B11C6D1E109
+12292A1 498BC2                         mov rax,r10
+12292A4 48F7E9                         imul rcx
+12292A7 4C8BC2                         mov r8,rdx
+12292AA 49C1F80E                       sar r8,0E
+12292AE 498BC0                         mov rax,r8
+12292B1 48C1E83F                       shr rax,3F
+12292B5 4C03C0                         add r8,rax
+12292B8 4969C0A0860100                 imul rax,r8,000186A0
+12292BF 482BC8                         sub rcx,rax
+12292C2 490FAFC9                       imul rcx,r9
+12292C6 498BC2                         mov rax,r10
+12292C9 48F7E9                         imul rcx
+12292CC 488BFA                         mov rdi,rdx
+12292CF 48C1FF0E                       sar rdi,0E
+12292D3 488BC7                         mov rax,rdi
+12292D6 48C1E83F                       shr rax,3F
+12292DA 4803F8                         add rdi,rax
+12292DD 4D0FAFC1                       imul r8,r9
+12292E1 4903F8                         add rdi,r8
+12292E4 48897D88                       mov [rbp-78],rdi
+12292E8 440FB705A8DCEA03               movzx r8d,word ptr [7FF77BBC6F98]
+12292F0 488D95D0010000                 lea rdx,[rbp+000001D0]
+12292F7 488D4B10                       lea rcx,[rbx+10]
+12292FB E850AE61FF                     call 7FF777334150
+1229300 C5F9EFC0                       vpxor xmm0,xmm0,xmm0
+1229304 C5F8114530                     vmovups [rbp+30],xmm0
+1229309 C5FA7F7540                     vmovdqu [rbp+40],xmm6
+122930E C6453000                       mov byte ptr [rbp+30],00
+1229312 488D0547462503                 lea rax,[7FF77AF6D960]
+1229319 488985B0000000                 mov [rbp+000000B0],rax
+1229320 488D4588                       lea rax,[rbp-78]
+1229324 488985B8000000                 mov [rbp+000000B8],rax
+122932B 488D85D0010000                 lea rax,[rbp+000001D0]
+1229332 488985C0000000                 mov [rbp+000000C0],rax
+1229339 488D4560                       lea rax,[rbp+60]
+122933D 488985C8000000                 mov [rbp+000000C8],rax
+1229344 488D85B0000000                 lea rax,[rbp+000000B0]
+122934B 488985E8000000                 mov [rbp+000000E8],rax
+1229352 488D5588                       lea rdx,[rbp-78]
+1229356 488D85D0010000                 lea rax,[rbp+000001D0]
+122935D 483BBDD0010000                 cmp rdi,[rbp+000001D0]
+1229364 480F4DD0                       cmovge rdx,rax
+1229368 4C8D4D30                       lea r9,[rbp+30]
+122936C 4C8D85B0000000                 lea r8,[rbp+000000B0]
+1229373 488B12                         mov rdx,[rdx]
+1229376 498BCF                         mov rcx,r15
+1229379 E8F250AEFF                     call 7FF7777FE470
+122937E 90                             nop 
+122937F 488B8DE8000000                 mov rcx,[rbp+000000E8]
+1229386 4885C9                         test rcx,rcx
+1229389 741A                           je 7FF777D193A5
+122938B 488D85B0000000                 lea rax,[rbp+000000B0]
+1229392 483BC8                         cmp rcx,rax
+1229395 0F95C2                         setne dl
+1229398 488B01                         mov rax,[rcx]
+122939B FF5020                         call qword ptr [rax+20]
+122939E 4C89A5E8000000                 mov [rbp+000000E8],r12
+12293A5 488D4D30                       lea rcx,[rbp+30]
+12293A9 E832C43EFF                     call 7FF7771057E0
+12293AE 498B5568                       mov rdx,[r13+68]
+12293B2 48895568                       mov [rbp+68],rdx
+12293B6 4881FAA0860100                 cmp rdx,000186A0
+12293BD 0F8DAE000000                   jnl 7FF777D19471
+12293C3 C5F9EFC0                       vpxor xmm0,xmm0,xmm0
+12293C7 C5F81145B0                     vmovups [rbp-50],xmm0
+12293CC C5FA7F75C0                     vmovdqu [rbp-40],xmm6
+12293D1 C645B000                       mov byte ptr [rbp-50],00
+12293D5 488D05D4462503                 lea rax,[7FF77AF6DAB0]
+12293DC 48898530010000                 mov [rbp+00000130],rax
+12293E3 488D4568                       lea rax,[rbp+68]
+12293E7 48898538010000                 mov [rbp+00000138],rax
+12293EE 488D8530010000                 lea rax,[rbp+00000130]
+12293F5 48898568010000                 mov [rbp+00000168],rax
+12293FC 4C8D4DB0                       lea r9,[rbp-50]
+1229400 4C8D8530010000                 lea r8,[rbp+00000130]
+1229407 498BCF                         mov rcx,r15
+122940A E8A1589CFF                     call 7FF7776DECB0
+122940F 90                             nop 
+1229410 488B8D68010000                 mov rcx,[rbp+00000168]
+1229417 4885C9                         test rcx,rcx
+122941A 741A                           je 7FF777D19436
+122941C 488D8530010000                 lea rax,[rbp+00000130]
+1229423 483BC8                         cmp rcx,rax
+1229426 0F95C2                         setne dl
+1229429 488B01                         mov rax,[rcx]
+122942C FF5020                         call qword ptr [rax+20]
+122942F 4C89A568010000                 mov [rbp+00000168],r12
+1229436 488B45C8                       mov rax,[rbp-38]
+122943A 4883F80F                       cmp rax,0F
+122943E 7631                           jna 7FF777D19471
+1229440 488B55B0                       mov rdx,[rbp-50]
+1229444 488BCA                         mov rcx,rdx
+1229447 48FFC0                         inc rax
+122944A 483D00100000                   cmp rax,00001000
+1229450 7211                           jb 7FF777D19463
+1229452 488B52F8                       mov rdx,[rdx-08]
+1229456 482BCA                         sub rcx,rdx
+1229459 4883E908                       sub rcx,08
+122945D 4883F91F                       cmp rcx,1F
+1229461 7770                           ja 7FF777D194D3
+1229463 4885D2                         test rdx,rdx
+1229466 7409                           je 7FF777D19471
+1229468 488BCA                         mov rcx,rdx
+122946B E8C06EEF02                     call 7FF77AC10330
+1229470 90                             nop 
+1229471 4885DB                         test rbx,rbx
+1229474 7439                           je 7FF777D194AF
+1229476 B8FFFFFFFF                     mov eax,FFFFFFFF
+122947B F00FC14308                     lock xadd [rbx+08],eax
+1229480 83F801                         cmp eax,01
+1229483 752A                           jne 7FF777D194AF
+1229485 33D2                           xor edx,edx
+1229487 488BCB                         mov rcx,rbx
+122948A E8C18D58FF                     call 7FF7772A2250
+122948F 488B050A5DEB03                 mov rax,[7FF77BBCF1A0]
+1229496 488B7810                       mov rdi,[rax+10]
+122949A 488BCB                         mov rcx,rbx
+122949D E8E6E5F002                     call 7FF77AC27A88
+12294A2 488BD0                         mov rdx,rax
+12294A5 488D0DF45CEB03                 lea rcx,[7FF77BBCF1A0]
+12294AC FFD7                           call rdi
+12294AE 90                             nop 
+12294AF 488B9C24C8020000               mov rbx,[rsp+000002C8]
+12294B7 C5F828B42470020000             vmovaps xmm6,[rsp+00000270]
+12294C0 4881C480020000                 add rsp,00000280
+12294C7 415F                           pop r15
+12294C9 415E                           pop r14
+12294CB 415D                           pop r13
+12294CD 415C                           pop r12
+12294CF 5F                             pop rdi
+12294D0 5E                             pop rsi
+12294D1 5D                             pop rbp
+12294D2 C3                             ret 
+12294D3 4C89642420                     mov [rsp+20],r12
+12294D8 4533C9                         xor r9d,r9d
+12294DB 4533C0                         xor r8d,r8d
+12294DE 33D2                           xor edx,edx
+12294E0 33C9                           xor ecx,ecx
+12294E2 E875BCF102                     call 7FF77AC3515C
+12294E7 CC                             int 3 
+12294E8 4C89642420                     mov [rsp+20],r12
+12294ED 4533C9                         xor r9d,r9d
+12294F0 4533C0                         xor r8d,r8d
+12294F3 33D2                           xor edx,edx
+12294F5 33C9                           xor ecx,ecx
+12294F7 E860BCF102                     call 7FF77AC3515C
+12294FC 90                             nop 
+12294FD E8C63CF002                     call 7FF77AC1D1C8
+1229502 90                             nop 
+1229503 4C89642420                     mov [rsp+20],r12
+1229508 4533C9                         xor r9d,r9d
+122950B 4533C0                         xor r8d,r8d
+122950E 33D2                           xor edx,edx
+1229510 33C9                           xor ecx,ecx
+1229512 E845BCF102                     call 7FF77AC3515C
+1229517 CC                             int 3 
