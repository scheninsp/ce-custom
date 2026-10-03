+1943300 48895C2410                     mov [rsp+10],rbx
+1943305 4488442418                     mov [rsp+18],r8b
+194330A 55                             push rbp
+194330B 56                             push rsi
+194330C 57                             push rdi
+194330D 4883EC70                       sub rsp,70
+1943311 488BF2                         mov rsi,rdx
+1943314 488BD9                         mov rbx,rcx
+1943317 837918FF                       cmp dword ptr [rcx+18],-01
+194331B 7510                           jne 7FF77843332D
+194331D 83791CFF                       cmp dword ptr [rcx+1C],-01
+1943321 750A                           jne 7FF77843332D
+1943323 33C0                           xor eax,eax
+1943325 488902                         mov [rdx],rax
+1943328 E9DA010000                     jmp 7FF778433507
+194332D 33C0                           xor eax,eax
+194332F 48898424A8000000               mov [rsp+000000A8],rax
+1943337 4889842490000000               mov [rsp+00000090],rax
+194333F E8CCB4FFFF                     call 7FF77842E810
+1943344 488D4810                       lea rcx,[rax+10]
+1943348 E833D0E7FE                     call 7FF7772B0380
+194334D 488BF8                         mov rdi,rax
+1943350 488B6B10                       mov rbp,[rbx+10]
+1943354 48896C2430                     mov [rsp+30],rbp
+1943359 488D8424A0000000               lea rax,[rsp+000000A0]
+1943361 4889442438                     mov [rsp+38],rax
+1943366 488D842490000000               lea rax,[rsp+00000090]
+194336E 4889442440                     mov [rsp+40],rax
+1943373 488D8424A8000000               lea rax,[rsp+000000A8]
+194337B 4889442448                     mov [rsp+48],rax
+1943380 488D542430                     lea rdx,[rsp+30]
+1943385 488BCF                         mov rcx,rdi
+1943388 E893AF0000                     call 7FF77843E320
+194338D 488B8C2490000000               mov rcx,[rsp+00000090]
+1943395 4885C9                         test rcx,rcx
+1943398 0F8F97000000                   jg 7FF778433435
+194339E 488D8F48080000                 lea rcx,[rdi+00000848]
+19433A5 E806D7E6FE                     call 7FF7772A0AB0
+19433AA 488BC8                         mov rcx,rax
+19433AD E8DEDF2BFF                     call 7FF7776F1390
+19433B2 488BF8                         mov rdi,rax
+19433B5 0FB69C24A0000000               movzx ebx,byte ptr [rsp+000000A0]
+19433BD 33D2                           xor edx,edx
+19433BF 488D4C2430                     lea rcx,[rsp+30]
+19433C4 E847E6A7FF                     call 7FF777EB1A10
+19433C9 90                             nop 
+19433CA 488D542430                     lea rdx,[rsp+30]
+19433CF E8AC2C8EFF                     call 7FF777D16080
+19433D4 440FB6CB                       movzx r9d,bl
+19433D8 4C8BC5                         mov r8,rbp
+19433DB 488D542430                     lea rdx,[rsp+30]
+19433E0 488BCF                         mov rcx,rdi
+19433E3 E8782D8EFF                     call 7FF777D16160
+19433E8 488D542430                     lea rdx,[rsp+30]
+19433ED 488BCF                         mov rcx,rdi
+19433F0 E89B578EFF                     call 7FF777D18B90
+19433F5 488D542428                     lea rdx,[rsp+28]
+19433FA 488D4C2430                     lea rcx,[rsp+30]
+19433FF E84CEFA7FF                     call 7FF777EB2350
+1943404 488BC8                         mov rcx,rax
+1943407 48C7442420A0860100             mov qword ptr [rsp+20],000186A0
+1943410 488D442420                     lea rax,[rsp+20]
+1943415 488139A0860100                 cmp qword ptr [rcx],000186A0
+194341C 480F4FC1                       cmovg rax,rcx
+1943420 488B00                         mov rax,[rax]
+1943423 488906                         mov [rsi],rax
+1943426 488D4C2468                     lea rcx,[rsp+68]
+194342B E8E05830FF                     call 7FF777738D10
+1943430 E9D2000000                     jmp 7FF778433507
+1943435 4C8B8C24A8000000               mov r9,[rsp+000000A8]
+194343D 48B8A38D23D6E2530000           mov rax,000053E2D6238DA3
+1943447 4903C1                         add rax,r9
+194344A 48BA461B47ACC5A70000           mov rdx,0000A7C5AC471B46
+1943454 483BC2                         cmp rax,rdx
+1943457 7714                           ja 7FF77843346D
+1943459 4969C1A0860100                 imul rax,r9,000186A0
+1943460 4899                           cqo 
+1943462 48F7F9                         idiv rcx
+1943465 4C8BD0                         mov r10,rax
+1943468 E997000000                     jmp 7FF778433504
+194346D 488BD1                         mov rdx,rcx
+1943470 48F7DA                         neg rdx
+1943473 480F48D1                       cmovs rdx,rcx
+1943477 48B800E40B5402000000           mov rax,00000002540BE400
+1943481 483BD0                         cmp rdx,rax
+1943484 48B809E1D1C6116BF129           mov rax,29F16B11C6D1E109
+194348E 7C21                           jl 7FF7784334B1
+1943490 48F7E9                         imul rcx
+1943493 4C8BC2                         mov r8,rdx
+1943496 49C1F80E                       sar r8,0E
+194349A 498BC8                         mov rcx,r8
+194349D 48C1E93F                       shr rcx,3F
+19434A1 4C03C1                         add r8,rcx
+19434A4 498BC1                         mov rax,r9
+19434A7 4899                           cqo 
+19434A9 49F7F8                         idiv r8
+19434AC 4C8BD0                         mov r10,rax
+19434AF EB53                           jmp 7FF778433504
+19434B1 49F7E9                         imul r9
+19434B4 48C1FA0E                       sar rdx,0E
+19434B8 488BC2                         mov rax,rdx
+19434BB 48C1E83F                       shr rax,3F
+19434BF 4803D0                         add rdx,rax
+19434C2 4C69C2A0860100                 imul r8,rdx,000186A0
+19434C9 498BC0                         mov rax,r8
+19434CC 4899                           cqo 
+19434CE 48F7F9                         idiv rcx
+19434D1 4869C2A0860100                 imul rax,rdx,000186A0
+19434D8 4899                           cqo 
+19434DA 48F7F9                         idiv rcx
+19434DD 4C8BD0                         mov r10,rax
+19434E0 4D2BC8                         sub r9,r8
+19434E3 4969C1A0860100                 imul rax,r9,000186A0
+19434EA 4899                           cqo 
+19434EC 48F7F9                         idiv rcx
+19434EF 4C03D0                         add r10,rax
+19434F2 498BC0                         mov rax,r8
+19434F5 4899                           cqo 
+19434F7 48F7F9                         idiv rcx
+19434FA 4869C8A0860100                 imul rcx,rax,000186A0
+1943501 4C03D1                         add r10,rcx
+1943504 4C8916                         mov [rsi],r10
+1943507 488BC6                         mov rax,rsi
+194350A 488B9C2498000000               mov rbx,[rsp+00000098]
+1943512 4883C470                       add rsp,70
+1943516 5F                             pop rdi
+1943517 5E                             pop rsi
+1943518 5D                             pop rbp
+1943519 C3                             ret 
