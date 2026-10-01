我在用 CheatEngine 尝试反编译出贸易中心硬木数量计算公式。Docs\trace_capcity1.md 是之前的操作。之前走不通了，我尝试通过九州贸易容量再进行公式查找，因为我相信贸易容量一定是硬木数量的计算函数的参数之一。目前我通过CheatEngine找到九州贸易容量的稳定内存地址：32FDB11F8B8
该地址数值不受UI开关影响。
当打开九州贸易中心界面，此界面带有硬木贸易量显示时。
会有两个 access 一直增加 count，关闭贸易中心界面后就不会增加 count 了
两个地址是
7FF7EB85323D - 8B 80 581D0000  - mov eax,[rax+00001D58]
7FF7EB85325D - 8B 80 5C1D0000  - mov eax,[rax+00001D5C]
他们对应的 Memory View 分别是
7FF7EB85323D
victoria3.exe+19D3230 - 48 83 EC 28           - sub rsp,28
victoria3.exe+19D3234 - 48 83 C1 10           - add rcx,10
victoria3.exe+19D3238 - E8 6364DFFE           - call victoria3.exe+7C96A0
victoria3.exe+19D323D - 8B 80 581D0000        - mov eax,[rax+00001D58]
victoria3.exe+19D3243 - 48 83 C4 28           - add rsp,28
victoria3.exe+19D3247 - C3                    - ret 
7FF7EB85325D
victoria3.exe+19D3250 - 48 83 EC 28           - sub rsp,28
victoria3.exe+19D3254 - 48 83 C1 10           - add rcx,10
victoria3.exe+19D3258 - E8 4364DFFE           - call victoria3.exe+7C96A0
victoria3.exe+19D325D - 8B 80 5C1D0000        - mov eax,[rax+00001D5C]
victoria3.exe+19D3263 - 48 83 C4 28           - add rsp,28
victoria3.exe+19D3267 - C3                    - ret 
接下来要做什么？





Show more

Wednesday 10:35 PM






Worked for 3m 47s



 
下载图片


Wednesday 10:38 PM








你在干嘛？为什么给我生成图片了？我不是在问你一个公式反编译查找任务吗？







Wednesday 10:42 PM






你说得对，这是我的错误：我误触发了图片生成工具，与当前的 Cheat Engine 反编译任务无关。现在我会回到本地追踪文档和游戏文件，基于你给出的两个读取点，给出下一步可执行的定位流程。




Worked for 1m 1s







从现有信息看，两个地址是很短的字段读取包装函数。它们在 UI 打开时高频执行，只能说明界面刷新会读取同一对象的 +1D58 和 +1D5C；真正要找的是调用者，以及硬木贸易量结果的写入或返回位置。你说得对，刚才生成图片完全是误操作，与任务无关。下面回到反编译定位。
这两段代码的含义大致是：
; victoria3.exe+19D3230
sub rsp,28
add rcx,10
call victoria3.exe+7C96A0
mov eax,[rax+1D58]
add rsp,28
ret
; victoria3.exe+19D3250
sub rsp,28
add rcx,10
call victoria3.exe+7C96A0
mov eax,[rax+1D5C]
add rsp,28
ret
它们本身不是公式，而是两个 getter：
int GetValue1(void* object) {
    auto component = GetComponent((char*)object + 0x10);
    return *(int*)((char*)component + 0x1D58);
}

int GetValue2(void* object) {
    auto component = GetComponent((char*)object + 0x10);
    return *(int*)((char*)component + 0x1D5C);
}
+1D58 和 +1D5C 是同一对象内相邻的两个 int32 字段。它们可能是贸易容量的两个组成值，例如总容量、已使用容量、输入容量、输出容量等，但目前不能仅凭这两条指令确定哪个字段对应什么含义。
接下来建议按这个顺序做。
1. 在两个 getter 的入口断下，记录调用栈
在 Cheat Engine 的 Memory View 中分别对以下地址设置执行断点：
victoria3.exe+19D323D
victoria3.exe+19D325D
每次断下时记录：
RCX
RAX
[RAX+1D58]
[RAX+1D5C]
返回地址
完整调用栈
注意：
- 在执行 call victoria3.exe+7C96A0 之前，RCX 是传入的对象指针。
- 执行完 call 后，RAX 是被读取字段所在的对象。
- 实际访问地址分别是：
RAX + 1D58
RAX + 1D5C
先确认两条 getter 在断下时的 RAX 是否相同。如果相同，就基本可以确认它们是同一个贸易中心或贸易容量组件的两个字段。
2. 把调用者找出来
单步执行到 ret，观察返回到哪里。你需要找到调用这两个 getter 的上层函数，而不是停留在 getter 本身。
重点观察调用者中的指令是否类似：
call victoria3.exe+19D3230
...
imul ...
idiv ...
cvtsi2sd ...
divss ...
或者：
call victoria3.exe+19D323D
mov ...
add ...
如果返回值刚从 EAX 出来就被转换成浮点数、乘常数、除以容量或与其他字段相加，那就是很有价值的候选公式函数。
建议在这两个 getter 的 ret 指令上断下：
victoria3.exe+19D3247
victoria3.exe+19D3267
断下后检查返回地址所在的调用者，以及返回值离开 getter 后的后续几条指令。
3. 确认 +1D58 与 +1D5C 的语义
在贸易中心界面打开时，记录：
硬木贸易量
九州贸易容量稳定地址 32FDB11F8B8 的值
[RAX+1D58]
[RAX+1D5C]
然后只改变一个条件，重复记录：
- 改变贸易路线数量；
- 改变贸易中心等级或建筑数量；
- 改变可用贸易容量来源；
- 改变硬木价格或硬木供给；
- 改变路线的进口/出口方向。
可以用下面这种表格：
状态	硬木贸易量	稳定地址	+1D58	+1D5C
初始				
增加容量				
增加硬木路线				
改变价格				


如果硬木贸易量变化，但只有 +1D58 变化，则 +1D58 更可能是公式输入。如果容量变化时两个字段都变，则需要继续观察调用者如何使用这两个返回值。
4. 不要只追读取，必须追硬木结果的写入
你现在看到的是 UI 读取路径。UI 读取路径可能只是把游戏已经算好的结果显示出来，并不执行贸易量计算。
下一步应当对硬木贸易量对应的内存地址使用：
Find out what writes to this address
而不是只使用：
Find out what accesses this address
操作流程：
1. 找到硬木贸易量的稳定或临时地址。
2. 对该地址设置 Find out what writes to this address。
3. 打开贸易中心界面并等待数值更新。
4. 记录写入指令及其调用栈。
5. 找到写入前负责计算结果的函数。
6. 在该函数入口、返回处记录寄存器和参数。
如果硬木数值不是直接存储，而是每次由 UI 动态计算，那么写断点可能不会触发。这时就在硬木显示 getter 的返回点断下，沿调用栈向上追。
5. 判断容量是否真的参与硬木公式
找到候选函数后，在同一函数中检查是否出现以下行为：
call victoria3.exe+19D3230
call victoria3.exe+19D3250
或者间接使用：
mov eax,[某对象+1D58]
mov ecx,[某对象+1D5C]
然后观察返回值经过哪些运算。常见形式可能类似：
hardwood_amount =
    min(
        available_trade_capacity,
        market_demand,
        market_supply
    );
也可能是：
hardwood_amount =
    trade_capacity * price_factor * route_efficiency;
不能仅凭“容量字段和硬木显示同时变化”判定容量参与公式。必须看到容量字段的返回值进入同一个计算函数，并且改变容量会改变最终结果。
目前最有价值的下一批信息是：
+19D323D 断点时的 RCX、RAX、调用栈
+19D325D 断点时的 RCX、RAX、调用栈
两个 getter 的返回地址
改变容量前后 +1D58/+1D5C 的数值
硬木数量写断点捕获到的指令
有了这些内容，就可以继续判断这两个字段分别是什么，并进一步还原硬木贸易量公式。


Wednesday 10:43 PM








我刚想到。因为我刚才在内存中找不到硬木贸易量的稳定地址，只能找到一个临时地址，并且隔一段时间就会变。那么大概率这个硬木贸易量，是在UI打开的时候才会有一个计算并显示的过程。如果他使用了贸易容量进行计算，那么他的函数调用栈必然是要调到”victoria3.exe+19D323D victoria3.exe+19D325D” 这些 getter，我是不是只要在 getter 上打断点，然后看调用栈追踪上一级，再获取反编译opcode，就大概率能看到计算过程了







Wednesday 10:49 PM






Worked for 13s







你的判断方向是对的，而且这是目前最有希望的路线之一：如果硬木贸易量是在打开贸易中心界面后动态计算，并且计算确实使用贸易容量，那么执行路径中很可能会调用这两个 getter。对 getter 设置断点，再从调用栈向上追，通常可以找到显示值的计算链。
但有一个关键限制：getter 的调用者不一定就是公式函数。它可能经过几层：
UI刷新函数
  -> 硬木贸易量显示函数
      -> 格式化/单位换算函数
          -> 贸易容量 getter
也可能是：
UI刷新函数
  -> 同时读取多个字段
      -> 贸易容量 getter
所以不能只看 getter 的直接上一级就停止，需要沿调用链和寄存器数据流继续往上追。
建议这样操作。
第一步：断在实际读取指令
优先断在：
victoria3.exe+19D323D    mov eax,[rax+1D58]
victoria3.exe+19D325D    mov eax,[rax+1D5C]
不要只断在函数入口。实际读取指令断下后，可以确认：
RAX
[RAX+1D58]
[RAX+1D5C]
栈顶返回地址
调用栈
在 x64 Windows 调用约定下，调用者返回地址通常位于当前 RSP 指向的位置，因此可以查看：
[RSP]
它应该接近：
victoria3.exe+19D3243
或：
victoria3.exe+19D3263
这是 getter 自己的返回地址。继续向调用栈上一层看，才是实际调用 getter 的函数。
第二步：过滤调用来源
打开贸易中心界面后，断点可能会高频触发。记录每次调用的上一层返回地址，重点比较：
- 打开九州贸易中心时出现的调用者；
- 关闭界面后是否完全消失；
- 切换到其他贸易中心时调用者是否变化；
- 只改变硬木路线时，调用次数或参数是否变化。
如果同一个调用者只在包含硬木贸易量的界面出现，它就是高价值候选。
但是，两个 getter 也可能被同一界面用于多个数字，例如：
- 总贸易容量；
- 已使用容量；
- 可用容量；
- 进口容量；
- 出口容量；
- 进度条或百分比。
因此要同时观察 getter 返回值离开函数后的用途。
第三步：从返回值开始跟踪
在 getter 返回后，检查调用者接下来的指令。例如：
call victoria3.exe+19D3230
mov ebx,eax
...
imul eax,ebx
...
divss xmm0,xmm1
或者：
call victoria3.exe+19D325D
mov [rsp+...],eax
call ...
有价值的模式包括：
imul
idiv
divss
divsd
mulss
mulsd
minss
minsd
maxss
maxsd
cvtsi2ss
cvtsi2sd
如果返回值很快被传入浮点运算、整数除法、比较或 min/max，就可能接近公式核心。
如果 getter 返回值只是被放入 UI 文本对象、格式化函数或本地化函数，那么公式可能还在它的上游。此时要继续沿调用栈向上走，而不是把格式化函数当成计算函数。
第四步：确认硬木数量确实走过这条路径
你可以做一个非常有用的对照：
1. 打开九州贸易中心界面。
2. 只记录 getter 断点的调用栈。
3. 观察硬木贸易量文本是否变化。
4. 关闭界面，确认断点停止。
5. 改变硬木贸易路线或硬木市场条件。
6. 再次打开界面并比较调用栈、返回值和后续算术指令。
如果硬木贸易量变化时：
- 调用者相同；
- +1D58 或 +1D5C 的返回值变化；
- 返回值随后参与算术；
- 算术结果进入硬木文本显示路径；
那么基本可以确认你已经进入公式链。
反过来，如果 getter 每次都触发，但硬木贸易量改变时它们的值和调用者都不变，说明它们可能只是界面中的容量显示，与硬木数值计算无关。
第五步：注意调用栈的“上一级”可能仍然不够
实际可能看到类似：
victoria3.exe+19D323D
victoria3.exe+8A1234
victoria3.exe+8A5678
victoria3.exe+5C9012
其中：
- +19D323D 是 getter；
- +8A1234 可能只是 getter 的直接调用者；
- +8A5678 可能是贸易量计算或 UI 行项目生成函数；
- +5C9012 可能是整个贸易中心界面刷新函数。
你需要对这些地址逐个反汇编，寻找哪个函数同时读取：
- 贸易容量；
- 硬木对应的商品或路线对象；
- 价格、供需、路线效率等其他参数；
- 最终显示值或临时结果。
第六步：如果 getter 没有命中，不代表硬木公式不用容量
还要考虑三种情况：
1. 编译器已经把 getter 内联了，公式函数直接读取 [object+1D58]。
2. 硬木数量在更早的模拟更新阶段计算，UI 只读取缓存结果。
3. 硬木显示使用的是另一个容量对象，九州贸易容量 getter 只是同界面中的另一个数值。
因此可以对下面几种指令设置代码访问断点或搜索：
mov eax,[某对象+1D58]
mov eax,[某对象+1D5C]
mov ecx,[某对象+1D58]
mov edx,[某对象+1D5C]
如果发现直接字段访问而没有调用这两个 getter，说明存在内联或另一条实现路径。
所以，结论是：
可以从这两个 getter 追，而且很可能能找到相关计算过程；但要把它当作“入口线索”，不能假定直接调用者就是公式。 最可靠的判断标准是：容量 getter 的返回值是否在同一调用链中参与算术，并且最终影响硬木显示值。
下一次断点时，建议完整记录：
getter 地址
RAX
[RAX+1D58]
[RAX+1D5C]
[RSP] 返回地址
调用栈中前 5 到 8 层
getter 返回后调用者的 20 到 40 条指令
尤其是“getter 返回后调用者的指令”，通常比单独的调用栈更能判断公式在哪里。


Wednesday 10:50 PM








命中 7FF7EB85323D 和 7FF7EB85325D 时 RAX 都是 32FDB11DB60
7FF7EB85323D 断点时 RSP 为 AE695FC7C0 或 AE695FCD79，AE695FC8A0，AE695FC3A0
还有时是 AE695FC740
7FF7EB85325D 断点时 RSP 为稳定 AE695FC3A0
断点4次 7FF7EB85323D 之后会有一次 7FF7EB85325D， 然后再循环 7FF7EB85323D 4次 7FF7EB85325D 1次
AE695FC3A0 这个会不会是相关函数？但是为什么他的地址不是 7FF7EB85325D 这种前缀的？







Wednesday 11:00 PM






Worked for 22s







RAX = 32FDB11DB60 在两个断点都相同，这是有价值的结果：两个 getter 确实正在读取同一个对象的不同字段：
[32FDB11DB60 + 1D58]
[32FDB11DB60 + 1D5C]
不过 AE695FC3A0 不是相关函数地址。它看起来是 RSP 指向的栈地址，不是代码地址。
在命中这两条指令时，函数已经执行过：
sub rsp,28
因此调用者的返回地址不在 [RSP]，而通常在：
[RSP + 0x28]
原因是进入函数时，call 先把返回地址压入栈，然后函数又执行了 sub rsp,28：
进入 getter 前:
旧 RSP     -> 返回地址

执行 sub rsp,28 后:
当前 RSP   -> 预留的栈空间
当前 RSP+28 -> 返回地址
所以在 Cheat Engine 断点处应该查看：
RSP
[RSP]
[RSP+08]
[RSP+10]
[RSP+18]
[RSP+20]
[RSP+28]
其中 [RSP+28] 很可能是类似下面的代码地址：
7FF7xxxxxxxx
这个地址才是 getter 返回后的调用点。
你看到的这些值：
AE695FC7C0
AE695FCD79
AE695FC8A0
AE695FC3A0
AE695FC740
都有 AE... 前缀，符合当前线程栈内存地址的特征，而不是 victoria3.exe 的代码地址。它们之间相差不大，也说明断点发生在同一个线程的不同栈帧或不同调用路径中。AE695FC3A0 多次出现，可能表示某个稳定的调用路径或栈帧位置，但它本身仍然不是函数地址。
你可以按下面步骤确认：
1. 在 7FF7EB85323D 断下。
2. 记录当前 RSP。
3. 在内存窗口输入：
   RSP+28
4. 读取 8 字节值。
5. 检查这个值是否落在 7FF7... 的模块代码区。
6. 对 RSP+28 的值右键，选择跟随到反汇编。
对第二个 getter 也做同样操作。
如果 [RSP+28] 指向：
victoria3.exe+某偏移
那么这就是直接调用 getter 的上一级位置。查看它附近的反汇编，例如：
call victoria3.exe+19D3230
mov ...
imul ...
divss ...
或者：
call victoria3.exe+19D325D
mov ...
call ...
重点看 getter 返回后紧接着的 20 到 40 条指令。
关于你观察到的调用频率：
+1D58 命中 4 次
+1D5C 命中 1 次
这通常说明界面刷新时多次读取第一个字段，最后读取一次第二个字段。可能对应：
- 多个 UI 项目都需要容量总值；
- 一个字段用于多个显示文本或进度条；
- 第一个字段是总容量，第二个字段是已用/剩余容量；
- 两个 getter 被不同的 UI 控件调用。
这还不能直接证明硬木公式使用了它们。接下来要做的是比较每次命中时的 [RSP+28]：
getter	[RSP+28] 调用者	RAX	字段值
+19D323D	记录代码地址	32FDB11DB60	+[1D58]
+19D323D	记录代码地址	32FDB11DB60	+[1D58]
+19D325D	记录代码地址	32FDB11DB60	+[1D5C]


如果四次 +1D58 的 [RSP+28] 都相同，说明它们来自同一个上层函数。如果不同，则说明同一个 getter 被多个 UI 控件或多个计算函数复用。
还可以直接在 getter 的 ret 后一条指令所在位置下断点。也就是先得到 [RSP+28] 后，在该地址附近观察：
call victoria3.exe+19D3230
; 返回后从这里继续
此处是最关键的位置。若返回值进入：
imul
idiv
mulss
divss
minss
maxss
cvtsi2ss
cvtsi2sd
或者与其他市场、商品、路线数据进行比较，那么就可能接近硬木贸易量计算。
当前结论是：
- RAX 相同，说明两个字段属于同一个对象。
- AE695FC3A0 是栈地址，不是函数地址。
- 应读取 [RSP+28] 来取得 getter 的调用者返回地址。
- +1D58 四次、+1D5C 一次，说明 UI 刷新有不同读取频率，但还不能证明是硬木公式。
- 下一步最重要的是获取两个 getter 的 [RSP+28]，并查看返回后的调用者反汇编。


Wednesday 11:00 PM