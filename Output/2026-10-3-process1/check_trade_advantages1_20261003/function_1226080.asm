+1226080 4C8BDC                         mov r11,rsp
+1226083 4881EC98000000                 sub rsp,00000098
+122608A 488BC2                         mov rax,rdx
+122608D C5F9EFC0                       vpxor xmm0,xmm0,xmm0
+1226091 C5F811442430                   vmovups [rsp+30],xmm0
+1226097 C5FA6F0D21FF5D03               vmovdqu xmm1,[7FF77B2F5FC0]
+122609F C5FA7F4C2440                   vmovdqu [rsp+40],xmm1
+12260A5 C644243000                     mov byte ptr [rsp+30],00
+12260AA 488D0DCF772503                 lea rcx,[7FF77AF6D880]
+12260B1 49894BB8                       mov [r11-48],rcx
+12260B5 498D4BB8                       lea rcx,[r11-48]
+12260B9 49894BF0                       mov [r11-10],rcx
+12260BD 4D8D4B98                       lea r9,[r11-68]
+12260C1 4D8D43B8                       lea r8,[r11-48]
+12260C5 488B153C3D6604                 mov rdx,[7FF77C379E08]
+12260CC 488BC8                         mov rcx,rax
+12260CF E87C869CFF                     call 7FF7776DE750
+12260D4 90                             nop 
+12260D5 488B8C2488000000               mov rcx,[rsp+00000088]
+12260DD 4885C9                         test rcx,rcx
+12260E0 741D                           je 7FF777D160FF
+12260E2 488D442450                     lea rax,[rsp+50]
+12260E7 483BC8                         cmp rcx,rax
+12260EA 0F95C2                         setne dl
+12260ED 488B01                         mov rax,[rcx]
+12260F0 FF5020                         call qword ptr [rax+20]
+12260F3 48C784248800000000000000       mov qword ptr [rsp+00000088],00000000
+12260FF 488B442448                     mov rax,[rsp+48]
+1226104 4883F80F                       cmp rax,0F
+1226108 7631                           jna 7FF777D1613B
+122610A 488B542430                     mov rdx,[rsp+30]
+122610F 488BCA                         mov rcx,rdx
+1226112 48FFC0                         inc rax
+1226115 483D00100000                   cmp rax,00001000
+122611B 7211                           jb 7FF777D1612E
+122611D 488B52F8                       mov rdx,[rdx-08]
+1226121 482BCA                         sub rcx,rdx
+1226124 4883E908                       sub rcx,08
+1226128 4883F91F                       cmp rcx,1F
+122612C 7715                           ja 7FF777D16143
+122612E 4885D2                         test rdx,rdx
+1226131 7408                           je 7FF777D1613B
+1226133 488BCA                         mov rcx,rdx
+1226136 E8F5A1EF02                     call 7FF77AC10330
+122613B 4881C498000000                 add rsp,00000098
+1226142 C3                             ret 
+1226143 48C744242000000000             mov qword ptr [rsp+20],00000000
+122614C 4533C9                         xor r9d,r9d
+122614F 4533C0                         xor r8d,r8d
+1226152 33D2                           xor edx,edx
+1226154 33C9                           xor ecx,ecx
+1226156 E801F0F102                     call 7FF77AC3515C
+122615B CC                             int 3 
