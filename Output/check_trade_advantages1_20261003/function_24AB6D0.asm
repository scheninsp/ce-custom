+24AB6D0 48895C2408                     mov [rsp+08],rbx
+24AB6D5 57                             push rdi
+24AB6D6 4881EC80000000                 sub rsp,00000080
+24AB6DD 488BFA                         mov rdi,rdx
+24AB6E0 498B10                         mov rdx,[r8]
+24AB6E3 488D4C2430                     lea rcx,[rsp+30]
+24AB6E8 E8231E2B00                     call 7FF77924D510
+24AB6ED 8B442430                       mov eax,[rsp+30]
+24AB6F1 89842498000000                 mov [rsp+00000098],eax
+24AB6F8 488D8C2498000000               lea rcx,[rsp+00000098]
+24AB700 E89BDF31FE                     call 7FF7772B96A0
+24AB705 488BD8                         mov rbx,rax
+24AB708 833D313EC30200                 cmp dword ptr [7FF77BBCF540],00
+24AB70F 7518                           jne 7FF778F9B729
+24AB711 488D056E674403                 lea rax,[7FF77C3E1E86]
+24AB718 4889442428                     mov [rsp+28],rax
+24AB71D 488D0DAC04F301                 lea rcx,[7FF77AECBBD0]
+24AB724 E897705F01                     call 7FF77A5927C0
+24AB729 48C70700000000                 mov qword ptr [rdi],00000000
+24AB730 33D2                           xor edx,edx
+24AB732 488D4C2440                     lea rcx,[rsp+40]
+24AB737 E8D462F1FE                     call 7FF777EB1A10
+24AB73C 90                             nop 
+24AB73D 488D542440                     lea rdx,[rsp+40]
+24AB742 E839A9D7FE                     call 7FF777D16080
+24AB747 41B101                         mov r9b,01
+24AB74A 4C8B442438                     mov r8,[rsp+38]
+24AB74F 488D542440                     lea rdx,[rsp+40]
+24AB754 488BCB                         mov rcx,rbx
+24AB757 E804AAD7FE                     call 7FF777D16160
+24AB75C 488D542440                     lea rdx,[rsp+40]
+24AB761 488BCB                         mov rcx,rbx
+24AB764 E827D4D7FE                     call 7FF777D18B90
+24AB769 488D9424A0000000               lea rdx,[rsp+000000A0]
+24AB771 488D4C2440                     lea rcx,[rsp+40]
+24AB776 E8D56BF1FE                     call 7FF777EB2350
+24AB77B 48C7842498000000A0860100       mov qword ptr [rsp+00000098],000186A0
+24AB787 488D8C2498000000               lea rcx,[rsp+00000098]
+24AB78F 488138A0860100                 cmp qword ptr [rax],000186A0
+24AB796 480F4FC8                       cmovg rcx,rax
+24AB79A 488B19                         mov rbx,[rcx]
+24AB79D 488D4C2478                     lea rcx,[rsp+78]
+24AB7A2 E869D579FE                     call 7FF777738D10
+24AB7A7 48891F                         mov [rdi],rbx
+24AB7AA 488BC7                         mov rax,rdi
+24AB7AD 488B9C2490000000               mov rbx,[rsp+00000090]
+24AB7B5 4881C480000000                 add rsp,00000080
+24AB7BC 5F                             pop rdi
+24AB7BD C3                             ret 
