# 贸易中心硬木数量的运行时追踪

## 当前状态

使用 Cheat Engine 7.6 对运行中的 `victoria3.exe` 设置断点。目标是贸易中心硬木数量；曾在 UI 中看到约 465、487.5。关闭 UI 后候选地址清零，所以目前追到的字段**可能是 UI 临时对象或缓存**，尚未证实为模拟层持久数据。绝对内存地址仅适用于本次运行。

本次对象基址为 `RCX=33131CD9100`：

| 地址 | 偏移 | 已观察到的作用 |
|---|---:|---|
| `33131CD9528` | `+0x428` | 最终写入的 Float 值 |
| `33131CD952C` | `+0x42C` | 比较用 Float 值 |
| `33131CD9530` | `+0x430` | `min` 的一个输入 |

## 已确认的代码

`victoria3.exe+3665EA0` 读取 `+0x42C`、`+0x430`，最终写入 `+0x428`。核心指令为：

```asm
vmovss xmm2,[rcx+0000042C]
vcomiss xmm2,xmm1
vmovss xmm3,[rcx+00000430]
jna victoria3.exe+3665EC0
vmovaps xmm0,xmm2
jmp victoria3.exe+3665EC4
vminss xmm0,xmm3,xmm1
vmovss [rcx+00000428],xmm0
```

忽略 NaN 等特殊情况时，近似为：`[+0x428] = ([+0x42C] <= XMM1) ? min([+0x430], XMM1) : [+0x42C]`。

直接调用者始于 `victoria3.exe+36663C0`。它先用相同条件算出候选值，再与当前 `+0x428` 比较；若值不同，会根据 `+0x44A`、`+0x44B` 状态决定是否先调用 `+3665FA0`，随后可能调用 `+3665EA0` 写入。`XMM1` 是从更上层传入的输入，其含义尚未确定。

在 `+3665EA0` 断下得到的调用栈开头：

```text
victoria3.exe+3665EA0  → 返回 +3666420
victoria3.exe+3666420  → 返回 +34E4D53
victoria3.exe+34E4D53  → 返回 +366671A
victoria3.exe+366671A  → 返回 +35939CA
```

`+3666420` 正是 `+36663C0` 函数里调用 `+3665EA0` 后的返回地址。早先还捕捉到 `victoria3.exe+6122AB` 使用 `mov [rcx],rax` 清零旧候选地址；这只是清零操作，不是贸易数量公式。

## 后续追踪与走偏原因

在 `+36663C0` 函数入口设置执行断点，得到直接调用者的返回地址 `victoria3.exe+34E4D53`。调用位置实际为 `+34E4D51: call rax`，属于间接调用；在这次命中时，`RAX` 指向 `+36663C0`。调用前 `+34E4D3A: vmovss xmm1,[rsp+40]`，而 `[rsp+40]` 由 `+34E4D31: call +202DA80` 写入。

`+202DA80` 的反汇编显示它是通用取值/类型转换函数，不是已识别的贸易公式。类型匹配时，它在 `+202DAC1: mov eax,[rax]` 读取 4 字节，再写入输出地址；其他类型走间接转换调用。一次单步进入后，读取地址为 `33093950EC0`，原始 4 字节按整数显示为 `1088421888`（十六进制 `0x40E00000`），按 Float 为 `7.0`。

随后在 `+34E4D51` 确认 `RAX=7FF7ED4E63C0`，确实指向 `+36663C0`；但这次接收对象的 `RCX=33093806E00`，**不同于先前硬木候选对象的 `RCX=33131CD9100`**。因此，虽然调用链相同，`7.0` 属于另一个对象；不能把它认作硬木数量或贸易公式输入。`+36663C0` 可服务多个对象，不能只按函数地址筛选。

## 新进展：稳定地址与对象基址（2026-09-30）

九州贸易容量的稳定地址 `32FDB11F8B8`，数值不受 UI 开关影响。UI 打开（显示硬木贸易量）时，两个 getter 持续被调用：

- `victoria3.exe+19D323D`（函数入口 `+19D3230`）：`mov eax,[rax+1D58]`
- `victoria3.exe+19D325D`（函数入口 `+19D3250`）：`mov eax,[rax+1D5C]`

两函数结构相同：`add rcx,10` → `call +7C96A0`（句柄解析：`rcx` 指向 4 字节句柄，返回对象指针）→ 读字段返回 `eax`。

断点实测：两次命中时 `RAX` 均为 `32FDB11DB60`（同一对象）。

```text
32FDB11DB60 + 0x1D58 = 32FDB11F8B8   ← 稳定地址所在字段
32FDB11DB60 + 0x1D5C = 32FDB11F8BC   ← 相邻 4 字节字段
```

即稳定值是对象 `+0x1D58` 的 4 字节字段，两个 getter 读同一对象的两个相邻字段。对象基址内存中 `[rcx]`（getter 传入的句柄）待记录。

## 下一步

1. 当前若仍停在 `+34E4D51`，先在 `Breakpointlist`（Ctrl+B）移除本轮旧断点，再按 F9 继续；无需重启游戏。
2. 重新确认当前硬木数量对应的 Float 地址。UI 重建后旧绝对地址可能失效。
3. 对**该地址**设置写入监视，命中时记录 `RCX` 对象基址，再只追踪同一对象的调用；不要把其他对象的 `+36663C0` 命中混入。
4. 对比 UI 开关状态和周结算时机，寻找关 UI 后仍存在的模拟层数据。当前只确认了一个通用数值限制/写入路径，**尚未找到贸易中心选择进口商品的算法**。


## Memory View 地址 victoria3.exe+3666420 附近内容
```
victoria3.exe+3666420


victoria3.exe+36663C0 - 40 53                 - push rbx
victoria3.exe+36663C2 - 48 83 EC 30           - sub rsp,30
victoria3.exe+36663C6 - C5F82974 24 20        - vmovaps [rsp+20],xmm6
victoria3.exe+36663CC - C5FA10B1 2C 040000    - vmovss xmm6,[rcx+0000042C]
victoria3.exe+36663D4 - C5F82FF1              - vcomiss xmm6,xmm1
victoria3.exe+36663D8 - 48 8B D9              - mov rbx,rcx
victoria3.exe+36663DB - 77 0C                 - ja victoria3.exe+36663E9
victoria3.exe+36663DD - C5FA1081 30 040000    - vmovss xmm0,[rcx+00000430]
victoria3.exe+36663E5 - C5FA5DF1              - vminss xmm6,xmm0,xmm1
victoria3.exe+36663E9 - C5F82EB1 28 040000    - vucomiss xmm6,[rcx+00000428]
victoria3.exe+36663F1 - 7A 02                 - jp victoria3.exe+36663F5
victoria3.exe+36663F3 - 74 32                 - je victoria3.exe+3666427
victoria3.exe+36663F5 - 80 B9 4A040000 00     - cmp byte ptr [rcx+0000044A],00
victoria3.exe+36663FC - 74 09                 - je victoria3.exe+3666407
victoria3.exe+36663FE - 80 B9 4B040000 00     - cmp byte ptr [rcx+0000044B],00
victoria3.exe+3666405 - 75 0D                 - jne victoria3.exe+3666414
victoria3.exe+3666407 - C5F828CE              - vmovaps xmm1,xmm6
victoria3.exe+366640B - E8 90FBFFFF           - call victoria3.exe+3665FA0
victoria3.exe+3666410 - 84 C0                 - test al,al
victoria3.exe+3666412 - 75 0C                 - jne victoria3.exe+3666420
victoria3.exe+3666414 - C5F828CE              - vmovaps xmm1,xmm6
victoria3.exe+3666418 - 48 8B CB              - mov rcx,rbx
victoria3.exe+366641B - E8 80FAFFFF           - call victoria3.exe+3665EA0
victoria3.exe+3666420 - C6 83 4B040000 00     - mov byte ptr [rbx+0000044B],00
victoria3.exe+3666427 - C5F82874 24 20        - vmovaps xmm6,[rsp+20]
victoria3.exe+366642D - 48 83 C4 30           - add rsp,30
victoria3.exe+3666431 - 5B                    - pop rbx
victoria3.exe+3666432 - C3                    - ret
```



## victoria3.exe+3666420 地址附近伪代码

```
float old_limit = *(float*)(rcx + 0x42C);
float candidate;


if (old_limit > xmm1) {
    candidate = old_limit;
} else {
    float other = *(float*)(rcx + 0x430);
    candidate = min(other, xmm1);
}


if (candidate == *(float*)(rcx + 0x428)) {
    return;
}


if (*(byte*)(rcx + 0x44A) != 0 &&
    *(byte*)(rcx + 0x44B) != 0) {
    update_value(candidate);
} else {
    bool blocked = helper_3665FA0(candidate);


    if (!blocked) {
        update_value(candidate);
    }
}
```


# 7FF7EB85323D 断点到 RSP = AE695FC3A0 时, Memory Viewer 跳转 RSP+28 是
AE695FC3C8 - CB                    - ret   但是为什么到这里开始我一向上滚动 MemoryViewer，AE695FC3C8 这个地址就会消失，剩下的内容是 “AE695FC3A4 - AE                    - scasb&#x20;
AE695FC3A5 - 00 00                 - add [rax],al
AE695FC3A7 - 00 83 AF66EBF7        - add [rbx-08149951],al
AE695FC3AD - 7F 00                 - jg AE695FC3AF
AE695FC3AF - 00 50 E2              - add [rax-1E],dl
AE695FC3B2 - 5F                    - pop rdi
AE695FC3B3 - 69 AE 000000E8 CA5F69AE - imul ebp,[rsi-18000000],AE695FCA
AE695FC3BD - 00 00                 - add [rax],al
AE695FC3BF - 00 30                 - add [rax],dh
AE695FC3C1 - 32 85 EBF77F00        - xor al,[rbp+007FF7EB]
AE695FC3C7 - 00 CB                 - add bl,cl
AE695FC3C9 - 60                    - pushad (invalid)&#x20;
AE695FC3CA - E3 EA                 - jecxz AE695FC3B6
AE695FC3CC - F7 7F 00              - idiv [rdi+00]
AE695FC3CF - 00 F0                 - add al,dh
AE695FC3D1 - C3                    - ret “


你这次已经拿到关键证据了：`AE695FC3C8` 是“保存返回地址的栈槽地址”，不是返回地址本身。Memory Viewer 把栈里的原始字节当成机器码反汇编，所以看起来像一串乱码；要读取该位置的 8 字节指针，再把这个指针当作代码地址跳转。你看到的现象是正常的，关键在于区分：

```text
RSP+28                 栈槽地址
[RSP+28]               栈槽中保存的 8 字节返回地址
```

你现在看到：

```text
AE695FC3C8 - CB - ret
```

其中 `AE695FC3C8` 只是栈地址。Memory Viewer 正在把栈上的数据当作代码反汇编，所以后面的内容看起来像：

```asm
scasb
add [rax],al
...
ret
```

这些并不是实际函数代码。

从你贴出的字节可以直接还原返回地址。相关位置是：

```text
AE695FC3C8: CB 60 E3 EA F7 7F 00 00
```

x64 使用小端序，因此这 8 个字节代表：

```text
0x00007FF7EAE360CB
```

这才是 getter 返回后要跳转到的调用者地址。

也就是说：

```text
RSP       = AE695FC3A0
RSP+28    = AE695FC3C8        ; 保存返回地址的栈位置
[RSP+28]  = 7FF7EAE360CB      ; 真正的代码地址
```

请在 Cheat Engine 中这样操作：

1. 断在：

   ```text
   7FF7EB85323D
   ```

2. 当前：

   ```text
   RSP = AE695FC3A0
   ```

3. 查看地址：

   ```text
   AE695FC3C8
   ```

4. 不要把 `AE695FC3C8` 当作代码地址，而是读取该地址处的 8 字节值：

   ```text
   CB 60 E3 EA F7 7F 00 00
   ```

5. 按小端序转换为：

   ```text
   7FF7EAE360CB
   ```

6. 在 Memory Viewer 中跳转到：

   ```text
   7FF7EAE360CB
   ```

这里应该就是 getter 执行完 `ret` 后返回到的调用者位置。

由于 `ret` 会跳到 `7FF7EAE360CB`，通常可以向前查看 5 到 10 个字节，寻找调用 getter 的 `call` 指令。例如：

```asm
7FF7EAE360C6 - E8 xx xx xx xx - call victoria3.exe+19D3230
7FF7EAE360CB - ...             ; call 返回后的下一条指令
```

x64 的近调用通常是 5 字节，所以返回地址前方大约 5 字节很可能就是：

```asm
call victoria3.exe+19D3230
```

然后重点查看返回地址之后的指令，例如：

```asm
7FF7EAE360CB - mov ebx,eax
7FF7EAE360CD - imul ebx,...
7FF7EAE360D2 - cvtsi2ss xmm0,ebx
7FF7EAE360D7 - divss xmm0,xmm1
```

如果出现这种数据流，就能判断 getter 返回值是否进入计算。

你说“向上滚动后 `AE695FC3C8` 消失”，原因也是因为那只是栈内存中的一个位置。Memory Viewer 在继续滚动时会重新按当前地址解释字节，而且栈数据不一定按指令边界排列，所以显示内容会变化；它没有消失，只是视图移动或重新解码了栈数据。不要继续分析 `AE695FC3A4` 附近那些伪指令，那里不是游戏函数。

你接下来需要对两个 getter 分别做同样的处理：

```text
+19D323D:
    RSP
    RSP+28
    [RSP+28] 的 8 字节值
    转换后的代码地址

+19D325D:
    RSP
    RSP+28
    [RSP+28] 的 8 字节值
    转换后的代码地址
```

建议记录成：

| getter | RSP | 返回地址栈槽 | `[RSP+28]` 解码后的代码地址 |
|---|---|---|---|
| `+19D323D` | `AE695FC3A0` | `AE695FC3C8` | `7FF7EAE360CB` |
| `+19D325D` | ... | ... | ... |

然后把这两个代码地址前后各读 30 到 50 条指令。尤其要看 getter 返回后有没有：

```asm
imul
idiv
mulss
divss
minss
maxss
cvtsi2ss
cvtsi2sd
```

以及是否又调用了商品、价格、供需、路线效率相关函数。

目前你已经确认了一条完整关系：

```text
贸易容量对象
  -> [对象+1D58] / [对象+1D5C]
  -> getter 返回 EAX
  -> 7FF7EAE360CB 之类的上层调用者
```

下一步就是查看 `7FF7EAE360CB` 附近的真实代码，而不是继续查看 `AE695FC3C8` 栈地址处的伪反汇编。


AE695FC3A0
# 7FF7EAE360CB 附近的真实代码

victoria3.exe+FB6090 - 48 89 5C 24 08        - mov [rsp+08],rbx
victoria3.exe+FB6095 - 48 89 6C 24 10        - mov [rsp+10],rbp
victoria3.exe+FB609A - 48 89 74 24 18        - mov [rsp+18],rsi
victoria3.exe+FB609F - 57                    - push rdi
victoria3.exe+FB60A0 - 48 81 EC 50050000     - sub rsp,00000550
victoria3.exe+FB60A7 - 49 8B F8              - mov rdi,r8
victoria3.exe+FB60AA - 48 8B DA              - mov rbx,rdx
victoria3.exe+FB60AD - 48 8B F1              - mov rsi,rcx
victoria3.exe+FB60B0 - 49 8B 11              - mov rdx,[r9]
victoria3.exe+FB60B3 - 8B 52 0C              - mov edx,[rdx+0C]
victoria3.exe+FB60B6 - 48 8D 4C 24 20        - lea rcx,[rsp+20]
victoria3.exe+FB60BB - E8 009777FF           - call victoria3.exe+72F7C0
victoria3.exe+FB60C0 - 90                    - nop
victoria3.exe+FB60C1 - 48 85 DB              - test rbx,rbx
victoria3.exe+FB60C4 - 74 21                 - je victoria3.exe+FB60E7
victoria3.exe+FB60C6 - 48 8B CB              - mov rcx,rbx
victoria3.exe+FB60C9 - FF D6                 - call rsi
victoria3.exe+FB60CB - 89 84 24 80050000     - mov [rsp+00000580],eax
victoria3.exe+FB60D2 - 48 8D 94 24 80050000  - lea rdx,[rsp+00000580]
victoria3.exe+FB60DA - 48 8B CF              - mov rcx,rdi
victoria3.exe+FB60DD - E8 5EC575FF           - call victoria3.exe+712640
victoria3.exe+FB60E2 - 40 B5 01              - mov bpl,01
victoria3.exe+FB60E5 - EB 03                 - jmp victoria3.exe+FB60EA
victoria3.exe+FB60E7 - 40 32 ED              - xor bpl,bpl
victoria3.exe+FB60EA - 48 8B 54 24 20        - mov rdx,[rsp+20]
victoria3.exe+FB60EF - 48 85 D2              - test rdx,rdx
victoria3.exe+FB60F2 - 74 4F                 - je victoria3.exe+FB6143
victoria3.exe+FB60F4 - 48 63 74 24 2C        - movsxd  rsi,dword ptr [rsp+2C]
victoria3.exe+FB60F9 - 48 85 F6              - test rsi,rsi
victoria3.exe+FB60FC - 7E 31                 - jle victoria3.exe+FB612F
victoria3.exe+FB60FE - 33 DB                 - xor ebx,ebx
victoria3.exe+FB6100 - 48 8D 3C 13           - lea rdi,[rbx+rdx]
victoria3.exe+FB6104 - 48 8B CF              - mov rcx,rdi
victoria3.exe+FB6107 - E8 14C97FFF           - call victoria3.exe+7B2A20
victoria3.exe+FB610C - F6 07 01              - test byte ptr [rdi],01
victoria3.exe+FB610F - 74 0F                 - je victoria3.exe+FB6120
victoria3.exe+FB6111 - 48 8B 4F 08           - mov rcx,[rdi+08]
victoria3.exe+FB6115 - 48 85 C9              - test rcx,rcx
victoria3.exe+FB6118 - 74 06                 - je victoria3.exe+FB6120
victoria3.exe+FB611A - E8 11A21603           - call victoria3.exe+4120330
victoria3.exe+FB611F - 90                    - nop
victoria3.exe+FB6120 - 48 83 C3 28           - add rbx,28
victoria3.exe+FB6124 - 48 83 EE 01           - sub rsi,01
victoria3.exe+FB6128 - 48 8B 54 24 20        - mov rdx,[rsp+20]
victoria3.exe+FB612D - 75 D1                 - jne victoria3.exe+FB6100
victoria3.exe+FB612F - C7 44 24 2C 00000000  - mov [rsp+2C],00000000
victoria3.exe+FB6137 - 48 8B 4C 24 30        - mov rcx,[rsp+30]
victoria3.exe+FB613C - 4C 8B 01              - mov r8,[rcx]
victoria3.exe+FB613F - 41 FF 50 10           - call qword ptr [r8+10]
victoria3.exe+FB6143 - 40 0FB6 C5            - movzx eax,bpl
victoria3.exe+FB6147 - 4C 8D 9C 24 50050000  - lea r11,[rsp+00000550]
victoria3.exe+FB614F - 49 8B 5B 10           - mov rbx,[r11+10]
victoria3.exe+FB6153 - 49 8B 6B 18           - mov rbp,[r11+18]
victoria3.exe+FB6157 - 49 8B 73 20           - mov rsi,[r11+20]
victoria3.exe+FB615B - 49 8B E3              - mov rsp,r11
victoria3.exe+FB615E - 5F                    - pop rdi
victoria3.exe+FB615F - C3                    - ret

这段反汇编已经能确定一件关键事实：7FF7EAE360CB 不是贸易容量公式，而是一个通用的“调用回调并处理结果”的函数。getter 返回地址正好落在 call rsi 之后，说明两个 getter 很可能是以函数指针形式传入这里的。接下来应追这个通用函数的上层调用者，以及它把 EAX 交给 +712640 后做了什么。这段代码非常有用。

这段函数本身不像硬木贸易量计算函数，原因有几个：
1. 没有读取贸易容量对象的固定字段。
2. 没有明显的乘法、除法、浮点转换、比较或 min/max。
3. 它在 FB6100 到 FB612D 之间遍历一个元素数组，每次执行：
   
因此它更像是一个通用的 UI 数据填充、集合遍历、条件检查或回调分发函数。

# 其他几个 7FF7EB85323D 断点时 RSP 为 AE695FC7C0，AE695FC8A0，AE695FC740，AE695FC3A0

AE695FC7E8 - 40 C9 5F 69 AE 00 00 00          
AE695FC8C8 - CB 60 E3 EA F7 7F 00 00               
AE695FC768 - 43 61 E3 EA F7 7F 00 00            
AE695FC3C8 - 33 F6 7C EB F7 7F 00 00   

| 栈槽地址 | 原始 8 字节 | 解码结果 | 判断 |
|---|---|---:|---|
| `AE695FC7E8` | `40 C9 5F 69 AE 00 00 00` | `000000AE695FC9C40` | 仍是栈地址，不是代码地址 |
| `AE695FC8C8` | `CB 60 E3 EA F7 7F 00 00` | `7FF7EAE360CB` | 代码地址 |
| `AE695FC768` | `43 61 E3 EA F7 7F 00 00` | `7FF7EAE36143` | 代码地址 |
| `AE695FC3C8` | `33 F6 7C EB F7 7F 00 00` | `7FF7EB7CF633` | 代码地址 |


# 7FF7EB7CF633 附近代码
```
victoria3.exe+194F39E - CC                    - int 3 
victoria3.exe+194F39F - CC                    - int 3 
victoria3.exe+194F3A0 - 48 89 5C 24 08        - mov [rsp+08],rbx
victoria3.exe+194F3A5 - 48 89 6C 24 18        - mov [rsp+18],rbp
victoria3.exe+194F3AA - 48 89 74 24 20        - mov [rsp+20],rsi
victoria3.exe+194F3AF - 48 89 54 24 10        - mov [rsp+10],rdx
victoria3.exe+194F3B4 - 57                    - push rdi
victoria3.exe+194F3B5 - 48 81 EC 80050000     - sub rsp,00000580
victoria3.exe+194F3BC - 49 8B F1              - mov rsi,r9
victoria3.exe+194F3BF - 49 8B E8              - mov rbp,r8
victoria3.exe+194F3C2 - 49 8B 11              - mov rdx,[r9]
victoria3.exe+194F3C5 - 8B 52 0C              - mov edx,[rdx+0C]
victoria3.exe+194F3C8 - 48 8D 4C 24 50        - lea rcx,[rsp+50]
victoria3.exe+194F3CD - E8 EE03DEFE           - call victoria3.exe+72F7C0
victoria3.exe+194F3D2 - 90                    - nop 
victoria3.exe+194F3D3 - 8B 46 08              - mov eax,[rsi+08]
victoria3.exe+194F3D6 - 48 8D 0C 80           - lea rcx,[rax+rax*4]
victoria3.exe+194F3DA - 48 8D 3C CD 00000000  - lea rdi,[rcx*8+00000000]
victoria3.exe+194F3E2 - 48 8B 06              - mov rax,[rsi]
victoria3.exe+194F3E5 - 48 8B 18              - mov rbx,[rax]
victoria3.exe+194F3E8 - 48 03 DF              - add rbx,rdi
victoria3.exe+194F3EB - 48 8B CB              - mov rcx,rbx
victoria3.exe+194F3EE - E8 BD6F6DFF           - call victoria3.exe+10263B0
victoria3.exe+194F3F3 - 84 C0                 - test al,al
victoria3.exe+194F3F5 - 0F84 05010000         - je victoria3.exe+194F500
victoria3.exe+194F3FB - 48 8D 54 24 20        - lea rdx,[rsp+20]
victoria3.exe+194F400 - 48 8B CB              - mov rcx,rbx
victoria3.exe+194F403 - E8 78CE0C02           - call victoria3.exe+3A1C280
victoria3.exe+194F408 - 90                    - nop 
victoria3.exe+194F409 - 48 8B 4C 24 50        - mov rcx,[rsp+50]
victoria3.exe+194F40E - 48 03 CF              - add rcx,rdi
victoria3.exe+194F411 - 48 8B D0              - mov rdx,rax
victoria3.exe+194F414 - E8 4758E4FE           - call victoria3.exe+794C60
victoria3.exe+194F419 - 90                    - nop 
victoria3.exe+194F41A - 48 8B 5C 24 20        - mov rbx,[rsp+20]
victoria3.exe+194F41F - 48 83 E3 FE           - and rbx,-02
victoria3.exe+194F423 - E8 9815CEFE           - call victoria3.exe+6309C0
victoria3.exe+194F428 - 48 3B D8              - cmp rbx,rax
victoria3.exe+194F42B - 74 37                 - je victoria3.exe+194F464
victoria3.exe+194F42D - 48 8B 54 24 20        - mov rdx,[rsp+20]
victoria3.exe+194F432 - 48 8B CA              - mov rcx,rdx
victoria3.exe+194F435 - 48 83 E1 FE           - and rcx,-02
victoria3.exe+194F439 - 48 8B 01              - mov rax,[rcx]
victoria3.exe+194F43C - F6 C2 01              - test dl,01
victoria3.exe+194F43F - 48 8D 54 24 28        - lea rdx,[rsp+28]
victoria3.exe+194F444 - 48 0F45 54 24 28      - cmovne rdx,[rsp+28]
victoria3.exe+194F44A - FF 50 18              - call qword ptr [rax+18]
victoria3.exe+194F44D - 0FB6 5C 24 20         - movzx ebx,byte ptr [rsp+20]
victoria3.exe+194F452 - 83 E3 01              - and ebx,01
victoria3.exe+194F455 - E8 6615CEFE           - call victoria3.exe+6309C0
victoria3.exe+194F45A - 48 0B D8              - or rbx,rax
victoria3.exe+194F45D - 48 89 5C 24 20        - mov [rsp+20],rbx
victoria3.exe+194F462 - EB 05                 - jmp victoria3.exe+194F469
victoria3.exe+194F464 - 48 8B 5C 24 20        - mov rbx,[rsp+20]
victoria3.exe+194F469 - F6 C3 01              - test bl,01
victoria3.exe+194F46C - 74 10                 - je victoria3.exe+194F47E
victoria3.exe+194F46E - 48 8B 4C 24 28        - mov rcx,[rsp+28]
victoria3.exe+194F473 - 48 85 C9              - test rcx,rcx
victoria3.exe+194F476 - 74 06                 - je victoria3.exe+194F47E
victoria3.exe+194F478 - E8 B30E7D02           - call victoria3.exe+4120330
victoria3.exe+194F47D - 90                    - nop 
victoria3.exe+194F47E - 48 8B 44 24 50        - mov rax,[rsp+50]
victoria3.exe+194F483 - 48 8B 1C 38           - mov rbx,[rax+rdi]
victoria3.exe+194F487 - 48 83 E3 FE           - and rbx,-02
victoria3.exe+194F48B - E8 A046CEFE           - call victoria3.exe+633B30
victoria3.exe+194F490 - 48 3B D8              - cmp rbx,rax
victoria3.exe+194F493 - 75 6B                 - jne victoria3.exe+194F500
victoria3.exe+194F495 - 8B 46 08              - mov eax,[rsi+08]
victoria3.exe+194F498 - 48 8D 0C 80           - lea rcx,[rax+rax*4]
victoria3.exe+194F49C - 48 8B 44 24 50        - mov rax,[rsp+50]
victoria3.exe+194F4A1 - 48 8D 3C C8           - lea rdi,[rax+rcx*8]
victoria3.exe+194F4A5 - 48 8B 1F              - mov rbx,[rdi]
victoria3.exe+194F4A8 - 48 83 E3 FE           - and rbx,-02
victoria3.exe+194F4AC - E8 5F706DFF           - call victoria3.exe+1026510
victoria3.exe+194F4B1 - 48 8B 37              - mov rsi,[rdi]
victoria3.exe+194F4B4 - 48 83 E6 FE           - and rsi,-02
victoria3.exe+194F4B8 - 48 3B D8              - cmp rbx,rax
victoria3.exe+194F4BB - 75 07                 - jne victoria3.exe+194F4C4
victoria3.exe+194F4BD - E8 4E706DFF           - call victoria3.exe+1026510
victoria3.exe+194F4C2 - EB 05                 - jmp victoria3.exe+194F4C9
victoria3.exe+194F4C4 - E8 6746CEFE           - call victoria3.exe+633B30
victoria3.exe+194F4C9 - 48 3B F0              - cmp rsi,rax
victoria3.exe+194F4CC - 74 04                 - je victoria3.exe+194F4D2
victoria3.exe+194F4CE - 33 C9                 - xor ecx,ecx
victoria3.exe+194F4D0 - EB 0C                 - jmp victoria3.exe+194F4DE
victoria3.exe+194F4D2 - F6 07 01              - test byte ptr [rdi],01
victoria3.exe+194F4D5 - 48 8D 4F 08           - lea rcx,[rdi+08]
victoria3.exe+194F4D9 - 74 03                 - je victoria3.exe+194F4DE
victoria3.exe+194F4DB - 48 8B 09              - mov rcx,[rcx]
victoria3.exe+194F4DE - E8 3DBBFDFF           - call victoria3.exe+192B020
victoria3.exe+194F4E3 - 48 89 84 24 98050000  - mov [rsp+00000598],rax
victoria3.exe+194F4EB - 48 8D 94 24 98050000  - lea rdx,[rsp+00000598]
victoria3.exe+194F4F3 - 48 8B CD              - mov rcx,rbp
victoria3.exe+194F4F6 - E8 A5D60000           - call victoria3.exe+195CBA0
victoria3.exe+194F4FB - 40 B5 01              - mov bpl,01
victoria3.exe+194F4FE - EB 03                 - jmp victoria3.exe+194F503
victoria3.exe+194F500 - 40 32 ED              - xor bpl,bpl
victoria3.exe+194F503 - 48 8B 54 24 50        - mov rdx,[rsp+50]
victoria3.exe+194F508 - 48 85 D2              - test rdx,rdx
victoria3.exe+194F50B - 74 56                 - je victoria3.exe+194F563
victoria3.exe+194F50D - 48 63 74 24 5C        - movsxd  rsi,dword ptr [rsp+5C]
victoria3.exe+194F512 - 48 85 F6              - test rsi,rsi
victoria3.exe+194F515 - 7E 38                 - jle victoria3.exe+194F54F
victoria3.exe+194F517 - 33 FF                 - xor edi,edi
victoria3.exe+194F519 - 0F1F 80 00000000      - nop dword ptr [rax+00000000]
victoria3.exe+194F520 - 48 8D 1C 17           - lea rbx,[rdi+rdx]
victoria3.exe+194F524 - 48 8B CB              - mov rcx,rbx
victoria3.exe+194F527 - E8 F434E6FE           - call victoria3.exe+7B2A20
victoria3.exe+194F52C - F6 03 01              - test byte ptr [rbx],01
victoria3.exe+194F52F - 74 0F                 - je victoria3.exe+194F540
victoria3.exe+194F531 - 48 8B 4B 08           - mov rcx,[rbx+08]
victoria3.exe+194F535 - 48 85 C9              - test rcx,rcx
victoria3.exe+194F538 - 74 06                 - je victoria3.exe+194F540
victoria3.exe+194F53A - E8 F10D7D02           - call victoria3.exe+4120330
victoria3.exe+194F53F - 90                    - nop 
victoria3.exe+194F540 - 48 83 C7 28           - add rdi,28
victoria3.exe+194F544 - 48 83 EE 01           - sub rsi,01
victoria3.exe+194F548 - 48 8B 54 24 50        - mov rdx,[rsp+50]
victoria3.exe+194F54D - 75 D1                 - jne victoria3.exe+194F520
victoria3.exe+194F54F - C7 44 24 5C 00000000  - mov [rsp+5C],00000000
victoria3.exe+194F557 - 48 8B 4C 24 60        - mov rcx,[rsp+60]
victoria3.exe+194F55C - 4C 8B 01              - mov r8,[rcx]
victoria3.exe+194F55F - 41 FF 50 10           - call qword ptr [r8+10]
victoria3.exe+194F563 - 40 0FB6 C5            - movzx eax,bpl
victoria3.exe+194F567 - 4C 8D 9C 24 80050000  - lea r11,[rsp+00000580]
victoria3.exe+194F56F - 49 8B 5B 10           - mov rbx,[r11+10]
victoria3.exe+194F573 - 49 8B 6B 20           - mov rbp,[r11+20]
victoria3.exe+194F577 - 49 8B 73 28           - mov rsi,[r11+28]
victoria3.exe+194F57B - 49 8B E3              - mov rsp,r11
victoria3.exe+194F57E - 5F                    - pop rdi
victoria3.exe+194F57F - C3                    - ret 
victoria3.exe+194F580 - 48 89 5C 24 08        - mov [rsp+08],rbx
victoria3.exe+194F585 - 48 89 6C 24 10        - mov [rsp+10],rbp
victoria3.exe+194F58A - 48 89 74 24 18        - mov [rsp+18],rsi
victoria3.exe+194F58F - 57                    - push rdi
victoria3.exe+194F590 - 48 81 EC 50050000     - sub rsp,00000550
victoria3.exe+194F597 - 49 8B F8              - mov rdi,r8
victoria3.exe+194F59A - 48 8B DA              - mov rbx,rdx
victoria3.exe+194F59D - 48 8B F1              - mov rsi,rcx
victoria3.exe+194F5A0 - 49 8B 11              - mov rdx,[r9]
victoria3.exe+194F5A3 - 8B 52 0C              - mov edx,[rdx+0C]
victoria3.exe+194F5A6 - 48 8D 4C 24 20        - lea rcx,[rsp+20]
victoria3.exe+194F5AB - E8 1002DEFE           - call victoria3.exe+72F7C0
victoria3.exe+194F5B0 - 90                    - nop 
victoria3.exe+194F5B1 - 48 85 DB              - test rbx,rbx
victoria3.exe+194F5B4 - 74 1D                 - je victoria3.exe+194F5D3
victoria3.exe+194F5B6 - 48 8D 94 24 78050000  - lea rdx,[rsp+00000578]
victoria3.exe+194F5BE - 48 8B CB              - mov rcx,rbx
victoria3.exe+194F5C1 - FF D6                 - call rsi
victoria3.exe+194F5C3 - 48 8B D0              - mov rdx,rax
victoria3.exe+194F5C6 - 48 8B CF              - mov rcx,rdi
victoria3.exe+194F5C9 - E8 02ADFDFF           - call victoria3.exe+192A2D0
victoria3.exe+194F5CE - 40 B5 01              - mov bpl,01
victoria3.exe+194F5D1 - EB 03                 - jmp victoria3.exe+194F5D6
victoria3.exe+194F5D3 - 40 32 ED              - xor bpl,bpl
victoria3.exe+194F5D6 - 48 8B 54 24 20        - mov rdx,[rsp+20]
victoria3.exe+194F5DB - 48 85 D2              - test rdx,rdx
victoria3.exe+194F5DE - 74 53                 - je victoria3.exe+194F633
victoria3.exe+194F5E0 - 48 63 74 24 2C        - movsxd  rsi,dword ptr [rsp+2C]
victoria3.exe+194F5E5 - 48 85 F6              - test rsi,rsi
victoria3.exe+194F5E8 - 7E 35                 - jle victoria3.exe+194F61F
victoria3.exe+194F5EA - 33 DB                 - xor ebx,ebx
victoria3.exe+194F5EC - 0F1F 40 00            - nop dword ptr [rax+00]
victoria3.exe+194F5F0 - 48 8D 3C 13           - lea rdi,[rbx+rdx]
victoria3.exe+194F5F4 - 48 8B CF              - mov rcx,rdi
victoria3.exe+194F5F7 - E8 2434E6FE           - call victoria3.exe+7B2A20
victoria3.exe+194F5FC - F6 07 01              - test byte ptr [rdi],01
victoria3.exe+194F5FF - 74 0F                 - je victoria3.exe+194F610
victoria3.exe+194F601 - 48 8B 4F 08           - mov rcx,[rdi+08]
victoria3.exe+194F605 - 48 85 C9              - test rcx,rcx
victoria3.exe+194F608 - 74 06                 - je victoria3.exe+194F610
victoria3.exe+194F60A - E8 210D7D02           - call victoria3.exe+4120330
victoria3.exe+194F60F - 90                    - nop 
victoria3.exe+194F610 - 48 83 C3 28           - add rbx,28
victoria3.exe+194F614 - 48 83 EE 01           - sub rsi,01
victoria3.exe+194F618 - 48 8B 54 24 20        - mov rdx,[rsp+20]
victoria3.exe+194F61D - 75 D1                 - jne victoria3.exe+194F5F0
victoria3.exe+194F61F - C7 44 24 2C 00000000  - mov [rsp+2C],00000000
victoria3.exe+194F627 - 48 8B 4C 24 30        - mov rcx,[rsp+30]
victoria3.exe+194F62C - 4C 8B 01              - mov r8,[rcx]
victoria3.exe+194F62F - 41 FF 50 10           - call qword ptr [r8+10]
victoria3.exe+194F633 - 40 0FB6 C5            - movzx eax,bpl
victoria3.exe+194F637 - 4C 8D 9C 24 50050000  - lea r11,[rsp+00000550]
victoria3.exe+194F63F - 49 8B 5B 10           - mov rbx,[r11+10]
victoria3.exe+194F643 - 49 8B 6B 18           - mov rbp,[r11+18]
victoria3.exe+194F647 - 49 8B 73 20           - mov rsi,[r11+20]
victoria3.exe+194F64B - 49 8B E3              - mov rsp,r11
victoria3.exe+194F64E - 5F                    - pop rdi
victoria3.exe+194F64F - C3                    - ret 

```


# victoria3.exe+FB6090 调用栈

PC	Stack	Frame	Return	Parameters
victoria3.exe+FB6090	AE695FCCC8	AE695FCCC0	victoria3.exe+19DBFE9	3F000000,00000000,00000000,695FE250,...
victoria3.exe+19DBFE9	AE695FCCD0	AE695FCD00	victoria3.exe+3A1BE70	E5952400,695FCD79,EE667458,695FCE18,...
victoria3.exe+3A1BE70	AE695FCD10	AE695FCDD0	victoria3.exe+3A1C36A	E5952400,695FE250,E5952400,695FCE80,...
victoria3.exe+3A1C36A	AE695FCDE0	AE695FCE50	victoria3.exe+17F4802	00000054,695FCE80,695FE270,EA614C3A,...
victoria3.exe+17F4802	AE695FCE60	AE695FD3E0	victoria3.exe+17F37AF	939C2650,695FD499,EEF3DDE38,695FD530,...
victoria3.exe+17F37AF	AE695FD3F0	AE695FD420	victoria3.exe+3A1BE70	939C2650,695FD499,EEF3DDC80,EF7FDE38,...
victoria3.exe+3A1BE70	AE695FD430	AE695FD4F0	victoria3.exe+3A1C613	EEF3DDC8,EEF3DDC8,EF7FDE38,939C2638,...
victoria3.exe+3A1C613	AE695FD500	AE695FD550	victoria3.exe+35939E0	FFFFFFFF,939C25E0,695FD619,B35E9000,...
victoria3.exe+35939E0	AE695FD560	AE695FD660	victoria3.exe+3594857	95206A40,00000FD3,95206A70,695FE250,...
victoria3.exe+3594857	AE695FD670	AE695FD6E0	victoria3.exe+3594A37	B1044800,00000000,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FD6F0	AE695FD760	victoria3.exe+3594A37	B1044800,00000000,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FD770	AE695FD7E0	victoria3.exe+3594A37	B1044800,00000000,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FD7F0	AE695FD860	victoria3.exe+3594A37	B1044800,00000000,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FD870	AE695FD8E0	victoria3.exe+3594A37	B1044800,00000000,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FD8F0	AE695FD960	victoria3.exe+3594A37	B1044800,00000000,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FD970	AE695FD9E0	victoria3.exe+3594A37	B1044800,ED3FE800,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FD9F0	AE695FDA60	victoria3.exe+3594A37	B1044800,ED3FE800,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDA70	AE695FDAE0	victoria3.exe+3594A37	B1044800,ED3FE800,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDAF0	AE695FDB60	victoria3.exe+3594A37	B1044800,ED3FE800,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDB70	AE695FDBE0	victoria3.exe+3594A37	B1044800,ED3FE800,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDBF0	AE695FDC60	victoria3.exe+3594A37	B1044800,ED3FE800,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDC70	AE695FDC00	victoria3.exe+3594A37	B1044800,ED3FE800,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDCF0	AE695FDD60	victoria3.exe+3594A37	B1044800,ED3FE800,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDD70	AE695FDDE0	victoria3.exe+3594A37	B1044800,43000FD3,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDDF0	AE695FDE60	victoria3.exe+3594A37	B1044800,00000000,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDE70	AE695FDEE0	victoria3.exe+3594A37	B1044800,00000000,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDEF0	AE695FDF60	victoria3.exe+3594A37	B1044800,43D98000,695FE250,00000FD3,...
victoria3.exe+3594A37	AE695FDF70	AE695FDFE0	victoria3.exe+3594CFC	B1044800,AC496D00,695FE250,3CA3A330,...
victoria3.exe+3594CFC	AE695FDF0	AE695FE7B0	victoria3.exe+358E42B	AC496DC0,00000000,89000FD3,AC496040,...
victoria3.exe+358E42B	AE695FE7C0	AE695FE880	victoria3.exe+200F38A	00000000,AC496DC0,DA602000,695FF0D0,...
victoria3.exe+200F38A	AE695FE890	AE695FE9D0	victoria3.exe+2045157	80000009,AC496DC0,AC496DC0,695FF0D0,...
victoria3.exe+2045157	AE695FE9E0	AE695FEAB0	victoria3.exe+335F6D6	8D0FF320,00000000,8D0FF320,ED2DF463,...
victoria3.exe+335F6D6	AE695FEAC0	AE695FEB00	victoria3.exe+64DC0B	AA502000,AA3B55C0,AA3B55C0,AA151800,...
victoria3.exe+64DC0B	AE695FEB10	AE695FEB50	victoria3.exe+34545D5	AA502000,AA3B55C0,00000000,00000000,...
victoria3.exe+34545D5	AE695FEB60	AE695FEBB0	victoria3.exe+344E8EC	AA3B55C0,EC6E0A17,695FED00,695FEC10,...
victoria3.exe+344E8EC	AE695FEBC0	AE695FEBF0	victoria3.exe+3B1AA1A	EF74D38C,695FED00,695FEC08,AAAB1150,...
victoria3.exe+3B1AA1A	AE695FEC00	AE695FF0A0	victoria3.exe+344D237	D85C5000,AAAB1110,695FF150,AAAB1118,...
victoria3.exe+344D237	AE695FF0B0	AE695FF100	victoria3.exe+61434B	D85C5000,AA9D4D80,695FF210,348F7A1C,...
victoria3.exe+61434B	AE695FF110	AE695FFA40	victoria3.exe+417CCD0	00000010,00000010,4E8EF53C,AA9D4D80,...
victoria3.exe+417CCD0	AE695FFA50	AE695FFAA0	victoria3.exe+41353C2	00000001,00063160,00000001,00000000,...
victoria3.exe+41353C2	AE695FFAB0	AE695FFAE0	KERNEL32.BaseThreadIn...	00000000,00000000,00000000,00000000,...
KERNEL32.BaseThreadIn...	AE695FFAF0	AE695FFB10	ntdll.RtlUserThreadStart...	00000000,00000000,FFFFFB30,FFFFFB30,...
ntdll.RtlUserThreadStart...	AE695FFB20	AE695FFB60	00000000	00000000,00000000,00000000,00000000,...

# victoria3.exe+FB6090 断点时寄存器情况

Registers:                Flags
RAX 00007FF7EB85BFD0    CF 0
RBX 00000330E5952400    PF 0
RCX 00007FF7EB853230    AF 0
RDX 00000330D4332800    ZF 0
RSI 000000AE695FCE18    SF 0
RDI 000000AE695FCE08    DF 0
RBP 000000AE695FCD79    OF 0
RSP 000000AE695FCCC8
R8  000000AE695FCE18
R9  000000AE695FCD80
R10 00000330939C2638
R11 000000AE695FCCE0
R12 000000AE695FE020
R13 0000000000000001
R14 000000AE695FE250
R15 0000000000000000
RIP 00007FF7EAE36090

Special
CS 0033
SS 002B
DS 002B
ES 002B
FS 0053
GS 002B
