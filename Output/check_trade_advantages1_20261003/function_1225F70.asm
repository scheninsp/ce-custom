+1225F70 48895C2408                     mov [rsp+08],rbx
+1225F75 48896C2418                     mov [rsp+18],rbp
+1225F7A 56                             push rsi
+1225F7B 57                             push rdi
+1225F7C 4156                           push r14
+1225F7E 4883EC70                       sub rsp,70
+1225F82 410FB6D9                       movzx ebx,r9b
+1225F86 498BF8                         mov rdi,r8
+1225F89 4C8BF2                         mov r14,rdx
+1225F8C 488BF1                         mov rsi,rcx
+1225F8F 488BAC24B0000000               mov rbp,[rsp+000000B0]
+1225F97 4885ED                         test rbp,rbp
+1225F9A 0F95C2                         setne dl
+1225F9D 488D4C2430                     lea rcx,[rsp+30]
+1225FA2 E869BA1900                     call 7FF777EB1A10
+1225FA7 90                             nop 
+1225FA8 488D542430                     lea rdx,[rsp+30]
+1225FAD E8CE000000                     call 7FF777D16080
+1225FB2 440FB6CB                       movzx r9d,bl
+1225FB6 4C8BC7                         mov r8,rdi
+1225FB9 488D542430                     lea rdx,[rsp+30]
+1225FBE 488BCE                         mov rcx,rsi
+1225FC1 E89A010000                     call 7FF777D16160
+1225FC6 488D542430                     lea rdx,[rsp+30]
+1225FCB 488BCE                         mov rcx,rsi
+1225FCE E8BD2B0000                     call 7FF777D18B90
+1225FD3 4885ED                         test rbp,rbp
+1225FD6 7449                           je 7FF777D16021
+1225FD8 488D05B1431903                 lea rax,[7FF77AEAA390]
+1225FDF 4889442420                     mov [rsp+20],rax
+1225FE4 C744242801000000               mov [rsp+28],00000001
+1225FEC C644242C00                     mov byte ptr [rsp+2C],00
+1225FF1 488D542420                     lea rdx,[rsp+20]
+1225FF6 488BCD                         mov rcx,rbp
+1225FF9 E8B2E98802                     call 7FF77A5A49B0
+1225FFE 488D4C2430                     lea rcx,[rsp+30]
+1226003 E8B8C51900                     call 7FF777EB25C0
+1226008 4C8B4010                       mov r8,[rax+10]
+122600C 488378180F                     cmp qword ptr [rax+18],0F
+1226011 7603                           jna 7FF777D16016
+1226013 488B00                         mov rax,[rax]
+1226016 488BD0                         mov rdx,rax
+1226019 488BCD                         mov rcx,rbp
+122601C E8CFDE7001                     call 7FF779423EF0
+1226021 488D942498000000               lea rdx,[rsp+00000098]
+1226029 488D4C2430                     lea rcx,[rsp+30]
+122602E E81DC31900                     call 7FF777EB2350
+1226033 488BC8                         mov rcx,rax
+1226036 48C78424B0000000A0860100       mov qword ptr [rsp+000000B0],000186A0
+1226042 488D8424B0000000               lea rax,[rsp+000000B0]
+122604A 488139A0860100                 cmp qword ptr [rcx],000186A0
+1226051 480F4FC1                       cmovg rax,rcx
+1226055 488B00                         mov rax,[rax]
+1226058 498906                         mov [r14],rax
+122605B 488D4C2468                     lea rcx,[rsp+68]
+1226060 E8AB2CA2FF                     call 7FF777738D10
+1226065 498BC6                         mov rax,r14
+1226068 4C8D5C2470                     lea r11,[rsp+70]
+122606D 498B5B20                       mov rbx,[r11+20]
+1226071 498B6B30                       mov rbp,[r11+30]
+1226075 498BE3                         mov rsp,r11
+1226078 415E                           pop r14
+122607A 5F                             pop rdi
+122607B 5E                             pop rsi
+122607C C3                             ret 
