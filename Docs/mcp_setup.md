我搞了一个新的 CE Mcp 到 McpExternals 中，请你告诉我如何部署







1:36 PM






Worked for 51s



当前仓库中已经放好了可部署包：
McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64
里面有：
- CheatEngine.Mcp.dll：CE 插件
- CheatEngine.Mcp.Gateway.exe：MCP stdio 网关
- README.md：原始英文说明
- LICENSE、THIRD-PARTY-NOTICES.md
部署步骤如下。
1. 安装运行环境
使用 Windows x64，并安装 .NET 10 的以下运行时：
- Microsoft.NETCore.App
- Microsoft.AspNetCore.App
- Microsoft.WindowsDesktop.App
你的 Cheat Engine 需要是 7.7 x64。
如果 CE 的 ce.runtimeconfig.json 没有选择 .NET 10，需要先备份并修改该文件，在 runtimeOptions.frameworks 中加入上述三个框架。
2. 安装 CE 插件
启动 Cheat Engine，打开：
Edit > Settings > Plugins
然后：
1. 点击 Add new
2. 选择：
   D:\cebuild\ce-custom\McpExternals\CheatEngine.Mcp-2.0.0-beta.2-win-x64\CheatEngine.Mcp.dll
3. 勾选启用插件
4. 关闭设置窗口
插件启用后会启动本地 MCP 后端，但不会自动附加游戏进程。
3. 配置 AI 客户端
把以下程序配置为 AI 客户端的 stdio MCP Server：
D:\cebuild\ce-custom\McpExternals\CheatEngine.Mcp-2.0.0-beta.2-win-x64\CheatEngine.Mcp.Gateway.exe
例如通用配置格式：
{
  "mcpServers": {
    "cheat-engine": {
      "command": "D:\\cebuild\\ce-custom\\McpExternals\\CheatEngine.Mcp-2.0.0-beta.2-win-x64\\CheatEngine.Mcp.Gateway.exe"
    }
  }
}
Gateway 和 Cheat Engine 必须使用同一个 Windows 用户运行。
4. 建立连接并调用工具
AI 客户端连接后，先调用：
instance_list
返回结果中会有当前 Cheat Engine 实例的 instanceId。之后调用其他 CE 工具时，都传入这个 instanceId。
5. 可选配置
默认配置可以直接使用。用户配置文件放在：
%APPDATA%\CheatEngine.Mcp\appsettings.json
也可以设置环境变量：
MCP_DATA_DIRECTORY
文件权限相关配置：
- Mcp:Files:AllowedRoots：允许 MCP 访问的文件根目录
- CheatEngineClient:AllowedTableRoots：允许加载和保存 CE Table 的目录
日志默认位于数据目录中：
CheatEngine.Mcp.<CE PID>.log
6. 更新部署
更新时按以下顺序操作：
1. 禁用 CE 插件
2. 关闭 Cheat Engine
3. 关闭 CheatEngine.Mcp.Gateway.exe
4. 替换新的 CheatEngine.Mcp.dll 和 CheatEngine.Mcp.Gateway.exe
5. 删除旧的文件夹型插件条目
6. 重新添加新的 DLL
7. 保留 %APPDATA%\CheatEngine.Mcp 中的个人配置
注意：当前包是 Windows x64 版本，不能直接用于 32 位 CE。详细说明也在 [mcp_deploy.md](D:/cebuild/ce-custom/McpExternals/mcp_deploy.md) 和随包的 README.md 中。


1:37 PM








使用 Windows x64，并安装 .NET 10 的以下运行时：
- Microsoft.NETCore.App
- Microsoft.AspNetCore.App
- Microsoft.WindowsDesktop.App  你能先检查一下我的环境满足这个吗







1:38 PM






Worked for 41s



检查结果如下：
项目	状态
Windows 架构	✅ 64 位
.NET Core 运行时	❌ 只有 6/7/8/9，没有 .NET 10
ASP.NET Core 运行时	❌ 未安装
Windows Desktop 运行时	✅ 已安装 6/8/9，但没有 10
Cheat Engine x64 文件	✅ 存在
ce.runtimeconfig.json	⚠️ 当前配置为 .NET 9


当前已安装的运行时是：
Microsoft.NETCore.App 6.0.36
Microsoft.NETCore.App 7.0.20
Microsoft.NETCore.App 8.0.8
Microsoft.NETCore.App 9.0.18

Microsoft.WindowsDesktop.App 6.0.36
Microsoft.WindowsDesktop.App 8.0.8
Microsoft.WindowsDesktop.App 9.0.18
因此目前还不能满足这个 MCP 包的要求。需要安装：
1. .NET 10 Desktop Runtime x64
   - 会提供 Microsoft.NETCore.App
   - 会提供 Microsoft.WindowsDesktop.App
2. ASP.NET Core Runtime 10 x64
   - 提供 Microsoft.AspNetCore.App
安装完成后，还需要把：
C:\Program Files\Cheat Engine\ce.runtimeconfig.json
从当前的：
"tfm": "net9.0"
调整为 .NET 10 配置。建议先备份该文件，再修改为：
{
  "runtimeOptions": {
    "tfm": "net10.0",
    "frameworks": [
      {
        "name": "Microsoft.NETCore.App",
        "version": "10.0.0",
        "rollForward": "latestMinor"
      },
      {
        "name": "Microsoft.AspNetCore.App",
        "version": "10.0.0",
        "rollForward": "latestMinor"
      },
      {
        "name": "Microsoft.WindowsDesktop.App",
        "version": "10.0.0",
        "rollForward": "latestMinor"
      }
    ]
  }
}
安装完成后可执行以下命令复查：
dotnet --list-runtimes
应至少看到：
Microsoft.NETCore.App 10.x
Microsoft.AspNetCore.App 10.x
Microsoft.WindowsDesktop.App 10.x


”Edit → Settings → Plugins 中添加并启用 CheatEngine.Mcp.dll  “ 会复制 dll 吗？如果后面我的当前项目文件夹的 dll 产生了修改，还要手动拷贝吗？

不会自动复制 DLL。 CE 添加插件时会记录所选文件的路径，并从该路径加载。因此，是否需要手动拷贝，取决于你修改的 DLL 是否就是添加时选择的那一个文件。
按 Docs\mcp_setup.md 的步骤，你选择的是：
D:\cebuild\ce-custom\McpExternals\CheatEngine.Mcp-2.0.0-beta.2-win-x64\CheatEngine.Mcp.dll

重启CE ，工具栏已经显示 MCP:Enabled
CheatEngine.Mcp: Enabled

Instance: Cheat Engine 45260
Listening at: http://127.0.0.1:53524

The CE backend is ready for MCP requests. Your AI client connects through CheatEngine.Mcp.Gateway.exe.

Log: CheatEngine.Mcp.45260.log

OK

请你测试连接，并根据 McpExternals\CheatEngine.Mcp-2.0.0-beta.2-win-x64 中文档，以及 它对应的源码文件夹 D:\cebuild\CheatEngine.Mcp 判定此 MCP 拥有的能力

连接测试成功。
- 网关：CheatEngine.Mcp.Gateway 2.0.0.0
- MCP 协议：2025-06-18
- CE 实例：Cheat Engine 45260
- CE PID：45260
- 插件版本：2.0.0.0
- 实例 ID：ce-45260-220efd1ea3de43a7821a9df5017e8cd2
- instance_list 返回正常，discoveryIncomplete=false
该 MCP 目前公开：
- 191 个工具
- 33 个静态资源
- 26 个实例资源模板
- 43 个工作流提示词
主要能力包括：
- 进程枚举、附加、暂停、线程管理
- 内存读取、写入、批量操作、分配、释放、保护属性
- 数值扫描、未知值扫描、AOB 扫描、快照比较
- 指针扫描、指针路径、指针映射
- 模块、导入导出表、符号解析与注册
- 反汇编、代码搜索、函数识别、函数图、引用查找
- 调试器：断点、寄存器、单步、运行到、写入/访问捕获、跟踪
- Auto Assembler 汇编、注入、API Hook、代码补丁
- Cheat Engine 地址列表记录的创建、修改、冻结、脚本管理
- Lua 执行和 Lua API 查找
- Mono、Unity Mono、.NET、IL2CPP 检查与方法调用
- 远程函数调用、C 编译、DLL 注入、.NET 注入
- 内核 DBVM、物理内存读写、地址转换、监视
- 结构体创建、自动猜测、读写、比较、C 头文件生成
- Cheat Table 加载、保存、文件枚举
- Speedhack
- 内存转储、文件读写、哈希、快照
- 工具计算与数值转换
资源内容包括 CE 教程、工作流、扫描、指针、调试器、AOB、Auto Assembler、Lua、Mono/.NET、Unity/IL2CPP、Unreal、内核、安全和错误恢复等文档。
需要特别注意：
1. 每次调用 instance_list 以外的工具都必须传入上述 instanceId。
2. 当前 MCP 只证明 CE 插件和网关连接正常，尚未附加任何目标进程。
3. 文档建议后续顺序为：
   runtime_get_info → runtime_get_overview → process_list → process_attach
4. asm_*、内存写入、Lua、远程调用、内核访问等属于有副作用或高权限能力，实际使用前应确认目标和操作。
5. 53524 是 CE 后端的本地 HTTP 监听端口；AI 客户端应通过 CheatEngine.Mcp.Gateway.exe 的 stdio MCP 接口连接，而不是直接访问该端口。
依据文档和源码，该 MCP 是一个功能完整的 Cheat Engine 控制层，覆盖从目标进程选择、内存扫描和分析，到修改、调试、脚本、注入、Mono/.NET 检查以及内核操作的完整链路。

