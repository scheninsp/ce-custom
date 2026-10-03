+1944400 48895C2410                     mov [rsp+10],rbx
+1944405 55                             push rbp
+1944406 56                             push rsi
+1944407 57                             push rdi
+1944408 4883EC60                       sub rsp,60
+194440C 410FB6E8                       movzx ebp,r8b
+1944410 488BF2                         mov rsi,rdx
+1944413 488BD9                         mov rbx,rcx
+1944416 8B4118                         mov eax,[rcx+18]
+1944419 83F8FF                         cmp eax,-01
+194441C 750C                           jne 7FF77843442A
+194441E 48C70200000000                 mov qword ptr [rdx],00000000
+1944425 E9B6000000                     jmp 7FF7784344E0
+194442A 89842480000000                 mov [rsp+00000080],eax
+1944431 488D8C2480000000               lea rcx,[rsp+00000080]
+1944439 E86252E8FE                     call 7FF7772B96A0
+194443E 488BC8                         mov rcx,rax
+1944441 E84AA429FF                     call 7FF7776CE890
+1944446 8B4810                         mov ecx,[rax+10]
+1944449 898C2480000000                 mov [rsp+00000080],ecx
+1944450 488D8C2480000000               lea rcx,[rsp+00000080]
+1944458 E84352E8FE                     call 7FF7772B96A0
+194445D 488BF8                         mov rdi,rax
+1944460 488B5B10                       mov rbx,[rbx+10]
+1944464 33D2                           xor edx,edx
+1944466 488D4C2420                     lea rcx,[rsp+20]
+194446B E8A0D5A7FF                     call 7FF777EB1A10
+1944470 90                             nop 
+1944471 488D542420                     lea rdx,[rsp+20]
+1944476 E8051C8EFF                     call 7FF777D16080
+194447B 440FB6CD                       movzx r9d,bpl
+194447F 4C8BC3                         mov r8,rbx
+1944482 488D542420                     lea rdx,[rsp+20]
+1944487 488BCF                         mov rcx,rdi
+194448A E8D11C8EFF                     call 7FF777D16160
+194448F 488D542420                     lea rdx,[rsp+20]
+1944494 488BCF                         mov rcx,rdi
+1944497 E8F4468EFF                     call 7FF777D18B90
+194449C 488D942498000000               lea rdx,[rsp+00000098]
+19444A4 488D4C2420                     lea rcx,[rsp+20]
+19444A9 E8A2DEA7FF                     call 7FF777EB2350
+19444AE 488BC8                         mov rcx,rax
+19444B1 48C7842480000000A0860100       mov qword ptr [rsp+00000080],000186A0
+19444BD 488D842480000000               lea rax,[rsp+00000080]
+19444C5 488139A0860100                 cmp qword ptr [rcx],000186A0
+19444CC 480F4FC1                       cmovg rax,rcx
+19444D0 488B00                         mov rax,[rax]
+19444D3 488906                         mov [rsi],rax
+19444D6 488D4C2458                     lea rcx,[rsp+58]
+19444DB E8304830FF                     call 7FF777738D10
+19444E0 488BC6                         mov rax,rsi
+19444E3 488B9C2488000000               mov rbx,[rsp+00000088]
+19444EB 4883C460                       add rsp,60
+19444EF 5F                             pop rdi
+19444F0 5E                             pop rsi
+19444F1 5D                             pop rbp
+19444F2 C3                             ret 
