+12289D0 48895C2410                     mov [rsp+10],rbx
+12289D5 4889742418                     mov [rsp+18],rsi
+12289DA 55                             push rbp
+12289DB 57                             push rdi
+12289DC 4156                           push r14
+12289DE 488DAC2470FEFFFF               lea rbp,[rsp-00000190]
+12289E6 4881EC90020000                 sub rsp,00000290
+12289ED 498BD8                         mov rbx,r8
+12289F0 488BFA                         mov rdi,rdx
+12289F3 488BF1                         mov rsi,rcx
+12289F6 4533F6                         xor r14d,r14d
+12289F9 4489B5B0010000                 mov [rbp+000001B0],r14d
+1228A00 4C634210                       movsxd  r8,dword ptr [rdx+10]
+1228A04 4585C0                         test r8d,r8d
+1228A07 7436                           je 7FF777D18A3F
+1228A09 488BC2                         mov rax,rdx
+1228A0C 488B5218                       mov rdx,[rdx+18]
+1228A10 4883FA0F                       cmp rdx,0F
+1228A14 7603                           jna 7FF777D18A19
+1228A16 488B00                         mov rax,[rax]
+1228A19 41807C00FF0A                   cmp byte ptr [r8+rax-01],0A
+1228A1F 741E                           je 7FF777D18A3F
+1228A21 488BC7                         mov rax,rdi
+1228A24 4883FA0F                       cmp rdx,0F
+1228A28 7603                           jna 7FF777D18A2D
+1228A2A 488B07                         mov rax,[rdi]
+1228A2D 41807C00FF20                   cmp byte ptr [r8+rax-01],20
+1228A33 740A                           je 7FF777D18A3F
+1228A35 B220                           mov dl,20
+1228A37 488BCF                         mov rcx,rdi
+1228A3A E851456401                     call 7FF77935CF90
+1228A3F 488B06                         mov rax,[rsi]
+1228A42 488D153F5C2503                 lea rdx,[7FF77AF6E688]
+1228A49 488D0D185C2503                 lea rcx,[7FF77AF6E668]
+1228A50 443830                         cmp [rax],r14b
+1228A53 480F44CA                       cmove rcx,rdx
+1228A57 48894C2430                     mov [rsp+30],rcx
+1228A5C 48C7C0FFFFFFFF                 mov rax,FFFFFFFFFFFFFFFF
+1228A63 48FFC0                         inc rax
+1228A66 44383401                       cmp [rcx+rax],r14b
+1228A6A 75F7                           jne 7FF777D18A63
+1228A6C 89442438                       mov [rsp+38],eax
+1228A70 448874243C                     mov [rsp+3C],r14b
+1228A75 488D35C44758FF                 lea rsi,[7FF77729D240]
+1228A7C 4889742420                     mov [rsp+20],rsi
+1228A81 4C8D0DF8684AFF                 lea r9,[7FF7771BF380]
+1228A88 BA78000000                     mov edx,00000078
+1228A8D 41B801000000                   mov r8d,00000001
+1228A93 488D4C2460                     lea rcx,[rsp+60]
+1228A98 E8CBC6F002                     call 7FF77AC25168
+1228A9D 90                             nop 
+1228A9E 488D4DE0                       lea rcx,[rbp-20]
+1228AA2 E8099B58FF                     call 7FF7772A25B0
+1228AA7 90                             nop 
+1228AA8 488D05F95B2503                 lea rax,[7FF77AF6E6A8]
+1228AAF 48894588                       mov [rbp-78],rax
+1228AB3 C745900E000000                 mov [rbp-70],0000000E
+1228ABA C6459400                       mov byte ptr [rbp-6C],00
+1228ABE 0FB744243D                     movzx eax,word ptr [rsp+3D]
+1228AC3 66894595                       mov [rbp-6B],ax
+1228AC7 0FB644243F                     movzx eax,byte ptr [rsp+3F]
+1228ACC 884597                         mov [rbp-69],al
+1228ACF C744246007000000               mov [rsp+60],00000007
+1228AD7 48895DB8                       mov [rbp-48],rbx
+1228ADB 4C89742428                     mov [rsp+28],r14
+1228AE0 488D45E0                       lea rax,[rbp-20]
+1228AE4 4889442420                     mov [rsp+20],rax
+1228AE9 41B901000000                   mov r9d,00000001
+1228AEF 4C8D442460                     lea r8,[rsp+60]
+1228AF4 488D542430                     lea rdx,[rsp+30]
+1228AF9 488D4C2440                     lea rcx,[rsp+40]
+1228AFE E89DE47F02                     call 7FF77A516FA0
+1228B03 C785B001000002000000           mov [rbp+000001B0],00000002
+1228B0D 48837DE000                     cmp qword ptr [rbp-20],00
+1228B12 741F                           je 7FF777D18B33
+1228B14 488D4DE0                       lea rcx,[rbp-20]
+1228B18 E8F39B58FF                     call 7FF7772A2710
+1228B1D 488B4DF0                       mov rcx,[rbp-10]
+1228B21 488B01                         mov rax,[rcx]
+1228B24 488B55E0                       mov rdx,[rbp-20]
+1228B28 FF5010                         call qword ptr [rax+10]
+1228B2B 4C8975E0                       mov [rbp-20],r14
+1228B2F 448975E8                       mov [rbp-18],r14d
+1228B33 4C8BCE                         mov r9,rsi
+1228B36 BA78000000                     mov edx,00000078
+1228B3B 41B801000000                   mov r8d,00000001
+1228B41 488D4C2460                     lea rcx,[rsp+60]
+1228B46 E8E9C2F002                     call 7FF77AC24E34
+1228B4B 90                             nop 
+1228B4C 488D542440                     lea rdx,[rsp+40]
+1228B51 48837C24580F                   cmp qword ptr [rsp+58],0F
+1228B57 480F47542440                   cmova rdx,[rsp+40]
+1228B5D 4C8B442450                     mov r8,[rsp+50]
+1228B62 488BCF                         mov rcx,rdi
+1228B65 E886B37001                     call 7FF779423EF0
+1228B6A 90                             nop 
+1228B6B 488D4C2440                     lea rcx,[rsp+40]
+1228B70 E86BCC3EFF                     call 7FF7771057E0
+1228B75 4C8D9C2490020000               lea r11,[rsp+00000290]
+1228B7D 498B5B28                       mov rbx,[r11+28]
+1228B81 498B7330                       mov rsi,[r11+30]
+1228B85 498BE3                         mov rsp,r11
+1228B88 415E                           pop r14
+1228B8A 5F                             pop rdi
+1228B8B 5D                             pop rbp
+1228B8C C3                             ret 
