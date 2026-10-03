+13A39A0 48895C2408                     mov [rsp+08],rbx
+13A39A5 4889742410                     mov [rsp+10],rsi
+13A39AA 57                             push rdi
+13A39AB 4883EC20                       sub rsp,20
+13A39AF 49637010                       movsxd  rsi,dword ptr [r8+10]
+13A39B3 488DB930020000                 lea rdi,[rcx+00000230]
+13A39BA 8BCE                           mov ecx,esi
+13A39BC 488BDA                         mov rbx,rdx
+13A39BF E86C2CC8FF                     call 7FF777B16630
+13A39C4 84C0                           test al,al
+13A39C6 7425                           je 7FF777E939ED
+13A39C8 400FB6C6                       movzx eax,sil
+13A39CC 243F                           and al,3F
+13A39CE 0FB6D0                         movzx edx,al
+13A39D1 488BC6                         mov rax,rsi
+13A39D4 48C1E806                       shr rax,06
+13A39D8 488B4CC720                     mov rcx,[rdi+rax*8+20]
+13A39DD 480FA3D1                       bt rcx,rdx
+13A39E1 730A                           jae 7FF777E939ED
+13A39E3 488B4708                       mov rax,[rdi+08]
+13A39E7 4C8B0CF0                       mov r9,[rax+rsi*8]
+13A39EB EB03                           jmp 7FF777E939F0
+13A39ED 4533C9                         xor r9d,r9d
+13A39F0 488B05895D4E04                 mov rax,[7FF77C379780]
+13A39F7 4C3BC8                         cmp r9,rax
+13A39FA 7F1A                           jg 7FF777E93A16
+13A39FC 48C70300000000                 mov qword ptr [rbx],00000000
+13A3A03 488BC3                         mov rax,rbx
+13A3A06 488B5C2430                     mov rbx,[rsp+30]
+13A3A0B 488B742438                     mov rsi,[rsp+38]
+13A3A10 4883C420                       add rsp,20
+13A3A14 5F                             pop rdi
+13A3A15 C3                             ret 
+13A3A16 4C2BC8                         sub r9,rax
+13A3A19 41BAA0860100                   mov r10d,000186A0
+13A3A1F 4C2BD0                         sub r10,rax
+13A3A22 750A                           jne 7FF777E93A2E
+13A3A24 B8FFFFFFFF                     mov eax,FFFFFFFF
+13A3A29 E9C1000000                     jmp 7FF777E93AEF
+13A3A2E 48B8A38D23D6E2530000           mov rax,000053E2D6238DA3
+13A3A38 48B9461B47ACC5A70000           mov rcx,0000A7C5AC471B46
+13A3A42 4903C1                         add rax,r9
+13A3A45 483BC1                         cmp rax,rcx
+13A3A48 7711                           ja 7FF777E93A5B
+13A3A4A 4969C1A0860100                 imul rax,r9,000186A0
+13A3A51 4899                           cqo 
+13A3A53 49F7FA                         idiv r10
+13A3A56 E994000000                     jmp 7FF777E93AEF
+13A3A5B 48B800E40B5402000000           mov rax,00000002540BE400
+13A3A65 498BCA                         mov rcx,r10
+13A3A68 48F7D9                         neg rcx
+13A3A6B 490F48CA                       cmovs rcx,r10
+13A3A6F 483BC8                         cmp rcx,rax
+13A3A72 48B809E1D1C6116BF129           mov rax,29F16B11C6D1E109
+13A3A7C 7C1E                           jl 7FF777E93A9C
+13A3A7E 49F7EA                         imul r10
+13A3A81 498BC1                         mov rax,r9
+13A3A84 4C8BC2                         mov r8,rdx
+13A3A87 4899                           cqo 
+13A3A89 49C1F80E                       sar r8,0E
+13A3A8D 498BC8                         mov rcx,r8
+13A3A90 48C1E93F                       shr rcx,3F
+13A3A94 4C03C1                         add r8,rcx
+13A3A97 49F7F8                         idiv r8
+13A3A9A EB53                           jmp 7FF777E93AEF
+13A3A9C 49F7E9                         imul r9
+13A3A9F 48C1FA0E                       sar rdx,0E
+13A3AA3 488BC2                         mov rax,rdx
+13A3AA6 48C1E83F                       shr rax,3F
+13A3AAA 4803D0                         add rdx,rax
+13A3AAD 4869CAA0860100                 imul rcx,rdx,000186A0
+13A3AB4 4C2BC9                         sub r9,rcx
+13A3AB7 4969C1A0860100                 imul rax,r9,000186A0
+13A3ABE 4899                           cqo 
+13A3AC0 49F7FA                         idiv r10
+13A3AC3 4C8BC0                         mov r8,rax
+13A3AC6 488BC1                         mov rax,rcx
+13A3AC9 4899                           cqo 
+13A3ACB 49F7FA                         idiv r10
+13A3ACE 4869C2A0860100                 imul rax,rdx,000186A0
+13A3AD5 4899                           cqo 
+13A3AD7 49F7FA                         idiv r10
+13A3ADA 4C03C0                         add r8,rax
+13A3ADD 488BC1                         mov rax,rcx
+13A3AE0 4899                           cqo 
+13A3AE2 49F7FA                         idiv r10
+13A3AE5 4869C0A0860100                 imul rax,rax,000186A0
+13A3AEC 4903C0                         add rax,r8
+13A3AEF 488B742438                     mov rsi,[rsp+38]
+13A3AF4 488903                         mov [rbx],rax
+13A3AF7 488BC3                         mov rax,rbx
+13A3AFA 488B5C2430                     mov rbx,[rsp+30]
+13A3AFF 4883C420                       add rsp,20
+13A3B03 5F                             pop rdi
+13A3B04 C3                             ret 
