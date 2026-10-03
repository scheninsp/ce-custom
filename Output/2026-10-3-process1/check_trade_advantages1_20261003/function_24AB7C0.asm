+24AB7C0 48895C2408                     mov [rsp+08],rbx
+24AB7C5 57                             push rdi
+24AB7C6 4881EC80000000                 sub rsp,00000080
+24AB7CD 488BFA                         mov rdi,rdx
+24AB7D0 498B10                         mov rdx,[r8]
+24AB7D3 488D4C2430                     lea rcx,[rsp+30]
+24AB7D8 E8331D2B00                     call 7FF77924D510
+24AB7DD 8B442430                       mov eax,[rsp+30]
+24AB7E1 89842498000000                 mov [rsp+00000098],eax
+24AB7E8 488D8C2498000000               lea rcx,[rsp+00000098]
+24AB7F0 E8ABDE31FE                     call 7FF7772B96A0
+24AB7F5 488BD8                         mov rbx,rax
+24AB7F8 833D413DC30200                 cmp dword ptr [7FF77BBCF540],00
+24AB7FF 7518                           jne 7FF778F9B819
+24AB801 488D057E664403                 lea rax,[7FF77C3E1E86]
+24AB808 4889442428                     mov [rsp+28],rax
+24AB80D 488D0DBC03F301                 lea rcx,[7FF77AECBBD0]
+24AB814 E8A76F5F01                     call 7FF77A5927C0
+24AB819 48C70700000000                 mov qword ptr [rdi],00000000
+24AB820 33D2                           xor edx,edx
+24AB822 488D4C2440                     lea rcx,[rsp+40]
+24AB827 E8E461F1FE                     call 7FF777EB1A10
+24AB82C 90                             nop 
+24AB82D 488D542440                     lea rdx,[rsp+40]
+24AB832 E849A8D7FE                     call 7FF777D16080
+24AB837 4533C9                         xor r9d,r9d
+24AB83A 4C8B442438                     mov r8,[rsp+38]
+24AB83F 488D542440                     lea rdx,[rsp+40]
+24AB844 488BCB                         mov rcx,rbx
+24AB847 E814A9D7FE                     call 7FF777D16160
+24AB84C 488D542440                     lea rdx,[rsp+40]
+24AB851 488BCB                         mov rcx,rbx
+24AB854 E837D3D7FE                     call 7FF777D18B90
+24AB859 488D9424A0000000               lea rdx,[rsp+000000A0]
+24AB861 488D4C2440                     lea rcx,[rsp+40]
+24AB866 E8E56AF1FE                     call 7FF777EB2350
+24AB86B 48C7842498000000A0860100       mov qword ptr [rsp+00000098],000186A0
+24AB877 488D8C2498000000               lea rcx,[rsp+00000098]
+24AB87F 488138A0860100                 cmp qword ptr [rax],000186A0
+24AB886 480F4FC8                       cmovg rcx,rax
+24AB88A 488B19                         mov rbx,[rcx]
+24AB88D 488D4C2478                     lea rcx,[rsp+78]
+24AB892 E879D479FE                     call 7FF777738D10
+24AB897 48891F                         mov [rdi],rbx
+24AB89A 488BC7                         mov rax,rdi
+24AB89D 488B9C2490000000               mov rbx,[rsp+00000090]
+24AB8A5 4881C480000000                 add rsp,00000080
+24AB8AC 5F                             pop rdi
+24AB8AD C3                             ret 
