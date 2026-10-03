+C48D10 4053                           push rbx
+C48D12 4883EC20                       sub rsp,20
+C48D16 488B19                         mov rbx,[rcx]
+C48D19 4885DB                         test rbx,rbx
+C48D1C 745C                           je 7FF777738D7A
+C48D1E 488D8B88010000                 lea rcx,[rbx+00000188]
+C48D25 48897C2430                     mov [rsp+30],rdi
+C48D2A E8B1CA9CFF                     call 7FF7771057E0
+C48D2F 488D8B68010000                 lea rcx,[rbx+00000168]
+C48D36 E8A5CA9CFF                     call 7FF7771057E0
+C48D3B 488DBB50010000                 lea rdi,[rbx+00000150]
+C48D42 48833F00                       cmp qword ptr [rdi],00
+C48D46 741D                           je 7FF777738D65
+C48D48 488BCF                         mov rcx,rdi
+C48D4B E8C099B6FF                     call 7FF7772A2710
+C48D50 488B4F10                       mov rcx,[rdi+10]
+C48D54 488B17                         mov rdx,[rdi]
+C48D57 488B01                         mov rax,[rcx]
+C48D5A FF5010                         call qword ptr [rax+10]
+C48D5D 33C0                           xor eax,eax
+C48D5F 488907                         mov [rdi],rax
+C48D62 894708                         mov [rdi+08],eax
+C48D65 488BCB                         mov rcx,rbx
+C48D68 E8731B0400                     call 7FF77777A8E0
+C48D6D 488BCB                         mov rcx,rbx
+C48D70 E8BB754D03                     call 7FF77AC10330
+C48D75 488B7C2430                     mov rdi,[rsp+30]
+C48D7A 4883C420                       add rsp,20
+C48D7E 5B                             pop rbx
+C48D7F C3                             ret 
