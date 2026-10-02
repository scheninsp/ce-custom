+BEE750 48895C2408                     mov [rsp+08],rbx
+BEE755 55                             push rbp
+BEE756 56                             push rsi
+BEE757 57                             push rdi
+BEE758 4156                           push r14
+BEE75A 4157                           push r15
+BEE75C 488D6C24A0                     lea rbp,[rsp-60]
+BEE761 4881EC60010000                 sub rsp,00000160
+BEE768 488BDA                         mov rbx,rdx
+BEE76B 4C8BF1                         mov r14,rcx
+BEE76E 4533FF                         xor r15d,r15d
+BEE771 4489BD98000000                 mov [rbp+00000098],r15d
+BEE778 488D05B1578403                 lea rax,[7FF77AF23F30]
+BEE77F 48894520                       mov [rbp+20],rax
+BEE783 4C894D28                       mov [rbp+28],r9
+BEE787 488D4D20                       lea rcx,[rbp+20]
+BEE78B 48894D58                       mov [rbp+58],rcx
+BEE78F 488995A8000000                 mov [rbp+000000A8],rdx
+BEE796 49015608                       add [r14+08],rdx
+BEE79A 41807E3101                     cmp byte ptr [r14+31],01
+BEE79F 0F856C040000                   jne 7FF7776DEC11
+BEE7A5 498B7638                       mov rsi,[r14+38]
+BEE7A9 4438BEAC010000                 cmp [rsi+000001AC],r15b
+BEE7B0 7409                           je 7FF7776DE7BB
+BEE7B2 4885D2                         test rdx,rdx
+BEE7B5 0F8456040000                   je 7FF7776DEC11
+BEE7BB 498B4838                       mov rcx,[r8+38]
+BEE7BF 4885C9                         test rcx,rcx
+BEE7C2 0F848D040000                   je 7FF7776DEC55
+BEE7C8 488B01                         mov rax,[rcx]
+BEE7CB 488D55A0                       lea rdx,[rbp-60]
+BEE7CF FF5010                         call qword ptr [rax+10]
+BEE7D2 90                             nop 
+BEE7D3 48837DB000                     cmp qword ptr [rbp-50],00
+BEE7D8 7509                           jne 7FF7776DE7E3
+BEE7DA 4885DB                         test rbx,rbx
+BEE7DD 0F8421040000                   je 7FF7776DEC04
+BEE7E3 488D8E50010000                 lea rcx,[rsi+00000150]
+BEE7EA E831E60500                     call 7FF77773CE20
+BEE7EF 488BF8                         mov rdi,rax
+BEE7F2 C7402801000000                 mov [rax+28],00000001
+BEE7F9 48895820                       mov [rax+20],rbx
+BEE7FD 488B4D58                       mov rcx,[rbp+58]
+BEE801 4885C9                         test rcx,rcx
+BEE804 0F8451040000                   je 7FF7776DEC5B
+BEE80A 488B01                         mov rax,[rcx]
+BEE80D 488D5500                       lea rdx,[rbp+00]
+BEE811 FF5010                         call qword ptr [rax+10]
+BEE814 C7859800000003000000           mov [rbp+00000098],00000003
+BEE81E 48837D1000                     cmp qword ptr [rbp+10],00
+BEE823 0F849C030000                   je 7FF7776DEBC5
+BEE829 8B9EB0010000                   mov ebx,[rsi+000001B0]
+BEE82F 488BCF                         mov rcx,rdi
+BEE832 48837DB000                     cmp qword ptr [rbp-50],00
+BEE837 0F85A7000000                   jne 7FF7776DE8E4
+BEE83D E8BEDEA2FF                     call 7FF77710C700
+BEE842 488BD6                         mov rdx,rsi
+BEE845 488BCF                         mov rcx,rdi
+BEE848 E853407D00                     call 7FF777EB28A0
+BEE84D 895C2420                       mov [rsp+20],ebx
+BEE851 4533C9                         xor r9d,r9d
+BEE854 41B801000000                   mov r8d,00000001
+BEE85A 488D542460                     lea rdx,[rsp+60]
+BEE85F 498BCE                         mov rcx,r14
+BEE862 E8390A0000                     call 7FF7776DF2A0
+BEE867 90                             nop 
+BEE868 488D442460                     lea rax,[rsp+60]
+BEE86D 48837C24780F                   cmp qword ptr [rsp+78],0F
+BEE873 480F47442460                   cmova rax,[rsp+60]
+BEE879 4889442440                     mov [rsp+40],rax
+BEE87E 8B442470                       mov eax,[rsp+70]
+BEE882 89442448                       mov [rsp+48],eax
+BEE886 C644244C00                     mov byte ptr [rsp+4C],00
+BEE88B 488D4500                       lea rax,[rbp+00]
+BEE88F 4889442428                     mov [rsp+28],rax
+BEE894 4C8D8DA8000000                 lea r9,[rbp+000000A8]
+BEE89B 488D542440                     lea rdx,[rsp+40]
+BEE8A0 488D4DC0                       lea rcx,[rbp-40]
+BEE8A4 E807C20500                     call 7FF77773AAB0
+BEE8A9 90                             nop 
+BEE8AA 4C8B4010                       mov r8,[rax+10]
+BEE8AE 488378180F                     cmp qword ptr [rax+18],0F
+BEE8B3 7603                           jna 7FF7776DE8B8
+BEE8B5 488B00                         mov rax,[rax]
+BEE8B8 488BD0                         mov rdx,rax
+BEE8BB 488BCF                         mov rcx,rdi
+BEE8BE E82D56D401                     call 7FF779423EF0
+BEE8C3 90                             nop 
+BEE8C4 488D4DC0                       lea rcx,[rbp-40]
+BEE8C8 E8136FA2FF                     call 7FF7771057E0
+BEE8CD 90                             nop 
+BEE8CE 488D4C2460                     lea rcx,[rsp+60]
+BEE8D3 E8086FA2FF                     call 7FF7771057E0
+BEE8D8 4489BEB0010000                 mov [rsi+000001B0],r15d
+BEE8DF E916030000                     jmp 7FF7776DEBFA
+BEE8E4 E817DEA2FF                     call 7FF77710C700
+BEE8E9 488BD6                         mov rdx,rsi
+BEE8EC 488BCF                         mov rcx,rdi
+BEE8EF E8AC3F7D00                     call 7FF777EB28A0
+BEE8F4 C5F9EFC0                       vpxor xmm0,xmm0,xmm0
+BEE8F8 41807E3101                     cmp byte ptr [r14+31],01
+BEE8FD 741B                           je 7FF7776DE91A
+BEE8FF C5F8114580                     vmovups [rbp-80],xmm0
+BEE904 C5FA6F0DB476C103               vmovdqu xmm1,[7FF77B2F5FC0]
+BEE90C C5FA7F4D90                     vmovdqu [rbp-70],xmm1
+BEE911 C6458000                       mov byte ptr [rbp-80],00
+BEE915 E915020000                     jmp 7FF7776DEB2F
+BEE91A C5FA7F442450                   vmovdqu [rsp+50],xmm0
+BEE920 C5F1EFC9                       vpxor xmm1,xmm1,xmm1
+BEE924 C5F8114C2440                   vmovups [rsp+40],xmm1
+BEE92A 48C74424580F000000             mov qword ptr [rsp+58],0000000F
+BEE933 C644244000                     mov byte ptr [rsp+40],00
+BEE938 48C744245003000000             mov qword ptr [rsp+50],00000003
+BEE941 8B05C5328403                   mov eax,[7FF77AF21C0C]
+BEE947 6689442440                     mov [rsp+40],ax
+BEE94C 0FB605BB328403                 movzx eax,byte ptr [7FF77AF21C0E]
+BEE953 88442442                       mov [rsp+42],al
+BEE957 C644244300                     mov byte ptr [rsp+43],00
+BEE95C 498B5638                       mov rdx,[r14+38]
+BEE960 4881C288010000                 add rdx,00000188
+BEE967 488D4DE0                       lea rcx,[rbp-20]
+BEE96B E8B03CA2FF                     call 7FF777102620
+BEE970 C785980000000B000000           mov [rbp+00000098],0000000B
+BEE97A 41B811000000                   mov r8d,00000011
+BEE980 488D1539328403                 lea rdx,[7FF77AF21BC0]
+BEE987 488D4DE0                       lea rcx,[rbp-20]
+BEE98B E86055D401                     call 7FF779423EF0
+BEE990 90                             nop 
+BEE991 C5FC1045E0                     vmovups ymm0,[rbp-20]
+BEE996 C5FC1145C0                     vmovups [rbp-40],ymm0
+BEE99B C5FA6F0D1D76C103               vmovdqu xmm1,[7FF77B2F5FC0]
+BEE9A3 C5FA7F4DF0                     vmovdqu [rbp-10],xmm1
+BEE9A8 C645E000                       mov byte ptr [rbp-20],00
+BEE9AC C785980000001B000000           mov [rbp+00000098],0000001B
+BEE9B6 488D542440                     lea rdx,[rsp+40]
+BEE9BB 48837C24580F                   cmp qword ptr [rsp+58],0F
+BEE9C1 480F47542440                   cmova rdx,[rsp+40]
+BEE9C7 4C8B442450                     mov r8,[rsp+50]
+BEE9CC 488D4DC0                       lea rcx,[rbp-40]
+BEE9D0 C5F877                         vzeroupper 
+BEE9D3 E81855D401                     call 7FF779423EF0
+BEE9D8 4C8D05F5318403                 lea r8,[7FF77AF21BD4]
+BEE9DF 488D55C0                       lea rdx,[rbp-40]
+BEE9E3 488D4C2460                     lea rcx,[rsp+60]
+BEE9E8 E81324BCFF                     call 7FF7772A0E00
+BEE9ED 90                             nop 
+BEE9EE 488B45D8                       mov rax,[rbp-28]
+BEE9F2 4883F80F                       cmp rax,0F
+BEE9F6 7634                           jna 7FF7776DEA2C
+BEE9F8 488B55C0                       mov rdx,[rbp-40]
+BEE9FC 488BCA                         mov rcx,rdx
+BEE9FF 48FFC0                         inc rax
+BEEA02 483D00100000                   cmp rax,00001000
+BEEA08 7215                           jb 7FF7776DEA1F
+BEEA0A 488B52F8                       mov rdx,[rdx-08]
+BEEA0E 482BCA                         sub rcx,rdx
+BEEA11 4883E908                       sub rcx,08
+BEEA15 4883F91F                       cmp rcx,1F
+BEEA19 0F8742020000                   ja 7FF7776DEC61
+BEEA1F 4885D2                         test rdx,rdx
+BEEA22 7408                           je 7FF7776DEA2C
+BEEA24 488BCA                         mov rcx,rdx
+BEEA27 E804195303                     call 7FF77AC10330
+BEEA2C C5FA6F058C75C103               vmovdqu xmm0,[7FF77B2F5FC0]
+BEEA34 C5FA7F45D0                     vmovdqu [rbp-30],xmm0
+BEEA39 C645C000                       mov byte ptr [rbp-40],00
+BEEA3D 488B45F8                       mov rax,[rbp-08]
+BEEA41 4883F80F                       cmp rax,0F
+BEEA45 763C                           jna 7FF7776DEA83
+BEEA47 488B55E0                       mov rdx,[rbp-20]
+BEEA4B 488BCA                         mov rcx,rdx
+BEEA4E 48FFC0                         inc rax
+BEEA51 483D00100000                   cmp rax,00001000
+BEEA57 7215                           jb 7FF7776DEA6E
+BEEA59 488B52F8                       mov rdx,[rdx-08]
+BEEA5D 482BCA                         sub rcx,rdx
+BEEA60 4883E908                       sub rcx,08
+BEEA64 4883F91F                       cmp rcx,1F
+BEEA68 0F8708020000                   ja 7FF7776DEC76
+BEEA6E 4885D2                         test rdx,rdx
+BEEA71 7410                           je 7FF7776DEA83
+BEEA73 488BCA                         mov rcx,rdx
+BEEA76 E8B5185303                     call 7FF77AC10330
+BEEA7B C5FA6F053D75C103               vmovdqu xmm0,[7FF77B2F5FC0]
+BEEA83 C5FA7F45F0                     vmovdqu [rbp-10],xmm0
+BEEA88 C645E000                       mov byte ptr [rbp-20],00
+BEEA8C 41B811000000                   mov r8d,00000011
+BEEA92 488D1557318403                 lea rdx,[7FF77AF21BF0]
+BEEA99 488D4C2460                     lea rcx,[rsp+60]
+BEEA9E E84D54D401                     call 7FF779423EF0
+BEEAA3 83FB01                         cmp ebx,01
+BEEAA6 7509                           jne 7FF7776DEAB1
+BEEAA8 488D1531318403                 lea rdx,[7FF77AF21BE0]
+BEEAAF EB0C                           jmp 7FF7776DEABD
+BEEAB1 83FB02                         cmp ebx,02
+BEEAB4 7517                           jne 7FF7776DEACD
+BEEAB6 488D156B328403                 lea rdx,[7FF77AF21D28]
+BEEABD 41B809000000                   mov r8d,00000009
+BEEAC3 488D4C2460                     lea rcx,[rsp+60]
+BEEAC8 E82354D401                     call 7FF779423EF0
+BEEACD C5FC10442460                   vmovups ymm0,[rsp+60]
+BEEAD3 C5FC114580                     vmovups [rbp-80],ymm0
+BEEAD8 C5FA6F0DE074C103               vmovdqu xmm1,[7FF77B2F5FC0]
+BEEAE0 C5FA7F4C2470                   vmovdqu [rsp+70],xmm1
+BEEAE6 C644246000                     mov byte ptr [rsp+60],00
+BEEAEB 488B442458                     mov rax,[rsp+58]
+BEEAF0 4883F80F                       cmp rax,0F
+BEEAF4 7639                           jna 7FF7776DEB2F
+BEEAF6 488B542440                     mov rdx,[rsp+40]
+BEEAFB 488BCA                         mov rcx,rdx
+BEEAFE 48FFC0                         inc rax
+BEEB01 483D00100000                   cmp rax,00001000
+BEEB07 7215                           jb 7FF7776DEB1E
+BEEB09 488B52F8                       mov rdx,[rdx-08]
+BEEB0D 482BCA                         sub rcx,rdx
+BEEB10 4883E908                       sub rcx,08
+BEEB14 4883F91F                       cmp rcx,1F
+BEEB18 0F871F010000                   ja 7FF7776DEC3D
+BEEB1E 4885D2                         test rdx,rdx
+BEEB21 740C                           je 7FF7776DEB2F
+BEEB23 488BCA                         mov rcx,rdx
+BEEB26 C5F877                         vzeroupper 
+BEEB29 E802185303                     call 7FF77AC10330
+BEEB2E 90                             nop 
+BEEB2F 488D55A0                       lea rdx,[rbp-60]
+BEEB33 488D4DC0                       lea rcx,[rbp-40]
+BEEB37 C5F877                         vzeroupper 
+BEEB3A E871AD0C02                     call 7FF7797A98B0
+BEEB3F 90                             nop 
+BEEB40 488D4D80                       lea rcx,[rbp-80]
+BEEB44 48837D980F                     cmp qword ptr [rbp-68],0F
+BEEB49 480F474D80                     cmova rcx,[rbp-80]
+BEEB4E 48894C2440                     mov [rsp+40],rcx
+BEEB53 8B4D90                         mov ecx,[rbp-70]
+BEEB56 894C2448                       mov [rsp+48],ecx
+BEEB5A C644244C00                     mov byte ptr [rsp+4C],00
+BEEB5F 4889442438                     mov [rsp+38],rax
+BEEB64 488D4500                       lea rax,[rbp+00]
+BEEB68 4889442428                     mov [rsp+28],rax
+BEEB6D 4C8D8DA8000000                 lea r9,[rbp+000000A8]
+BEEB74 488D542440                     lea rdx,[rsp+40]
+BEEB79 488D4C2460                     lea rcx,[rsp+60]
+BEEB7E E8EDE30500                     call 7FF77773CF70
+BEEB83 90                             nop 
+BEEB84 488BD0                         mov rdx,rax
+BEEB87 488BCF                         mov rcx,rdi
+BEEB8A E8014FEC02                     call 7FF77A5A3A90
+BEEB8F 90                             nop 
+BEEB90 488D4C2460                     lea rcx,[rsp+60]
+BEEB95 E8466CA2FF                     call 7FF7771057E0
+BEEB9A 90                             nop 
+BEEB9B 488D4DC0                       lea rcx,[rbp-40]
+BEEB9F E83C6CA2FF                     call 7FF7771057E0
+BEEBA4 90                             nop 
+BEEBA5 4C8B4598                       mov r8,[rbp-68]
+BEEBA9 4983F80F                       cmp r8,0F
+BEEBAD 760D                           jna 7FF7776DEBBC
+BEEBAF 488B5580                       mov rdx,[rbp-80]
+BEEBB3 488D4D80                       lea rcx,[rbp-80]
+BEEBB7 E8A470A2FF                     call 7FF777105C60
+BEEBBC 4489BEB0010000                 mov [rsi+000001B0],r15d
+BEEBC3 EB35                           jmp 7FF7776DEBFA
+BEEBC5 48837DB000                     cmp qword ptr [rbp-50],00
+BEEBCA 742E                           je 7FF7776DEBFA
+BEEBCC 488BCF                         mov rcx,rdi
+BEEBCF E82CDBA2FF                     call 7FF77710C700
+BEEBD4 488BD6                         mov rdx,rsi
+BEEBD7 488BCF                         mov rcx,rdi
+BEEBDA E8C13C7D00                     call 7FF777EB28A0
+BEEBDF 488D55A0                       lea rdx,[rbp-60]
+BEEBE3 48837DB80F                     cmp qword ptr [rbp-48],0F
+BEEBE8 480F4755A0                     cmova rdx,[rbp-60]
+BEEBED 4C8B45B0                       mov r8,[rbp-50]
+BEEBF1 488BCF                         mov rcx,rdi
+BEEBF4 E8F752D401                     call 7FF779423EF0
+BEEBF9 90                             nop 
+BEEBFA 488D4D00                       lea rcx,[rbp+00]
+BEEBFE E8DD6BA2FF                     call 7FF7771057E0
+BEEC03 90                             nop 
+BEEC04 488D4DA0                       lea rcx,[rbp-60]
+BEEC08 E8D36BA2FF                     call 7FF7771057E0
+BEEC0D 488B4D58                       mov rcx,[rbp+58]
+BEEC11 4885C9                         test rcx,rcx
+BEEC14 7410                           je 7FF7776DEC26
+BEEC16 488D4520                       lea rax,[rbp+20]
+BEEC1A 483BC8                         cmp rcx,rax
+BEEC1D 0F95C2                         setne dl
+BEEC20 488B01                         mov rax,[rcx]
+BEEC23 FF5020                         call qword ptr [rax+20]
+BEEC26 488B9C2490010000               mov rbx,[rsp+00000190]
+BEEC2E 4881C460010000                 add rsp,00000160
+BEEC35 415F                           pop r15
+BEEC37 415E                           pop r14
+BEEC39 5F                             pop rdi
+BEEC3A 5E                             pop rsi
+BEEC3B 5D                             pop rbp
+BEEC3C C3                             ret 
+BEEC3D 4C897C2420                     mov [rsp+20],r15
+BEEC42 4533C9                         xor r9d,r9d
+BEEC45 4533C0                         xor r8d,r8d
+BEEC48 33D2                           xor edx,edx
+BEEC4A 33C9                           xor ecx,ecx
+BEEC4C C5F877                         vzeroupper 
+BEEC4F E808655503                     call 7FF77AC3515C
+BEEC54 90                             nop 
+BEEC55 E86EE55303                     call 7FF77AC1D1C8
+BEEC5A 90                             nop 
+BEEC5B E868E55303                     call 7FF77AC1D1C8
+BEEC60 90                             nop 
+BEEC61 4C897C2420                     mov [rsp+20],r15
+BEEC66 4533C9                         xor r9d,r9d
+BEEC69 4533C0                         xor r8d,r8d
+BEEC6C 33D2                           xor edx,edx
+BEEC6E 33C9                           xor ecx,ecx
+BEEC70 E8E7645503                     call 7FF77AC3515C
+BEEC75 90                             nop 
+BEEC76 4C897C2420                     mov [rsp+20],r15
+BEEC7B 4533C9                         xor r9d,r9d
+BEEC7E 4533C0                         xor r8d,r8d
+BEEC81 33D2                           xor edx,edx
+BEEC83 33C9                           xor ecx,ecx
+BEEC85 E8D2645503                     call 7FF77AC3515C
+BEEC8A CC                             int 3 
