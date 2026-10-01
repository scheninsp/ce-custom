CheatEngine.Mcp 2.0.0-beta.2
Windows x64 beta for Cheat Engine 7.7, built from c51a0ec.
Windows x64 版本의 Cheat Engine 7.7 测试版，基于 c51a0ec 版本构建。

Downloads  下载量
Download CheatEngine.Mcp-2.0.0-beta.2-win-x64.zip and extract it into a permanent folder. This is the complete distribution:
下载 CheatEngine.Mcp-2.0.0-beta.2-win-x64.zip 文件，然后将其解压到指定的文件夹中。这就是完整的分发包：

CheatEngine.Mcp.dll: the single Cheat Engine plugin DLL, containing its managed dependencies and native Lua bridge.
CheatEngine.Mcp.dll：这是 Cheat Engine 唯一的插件 DLL 文件，包含了其管理的依赖库以及原生 Lua 接口。
CheatEngine.Mcp.Gateway.exe: the separate, standalone stdio MCP gateway.
CheatEngine.Mcp.Gateway.exe：这是一个独立的、独立的 stdio MCP 网关程序。
README.md: installation, configuration, updating, and connection instructions.
README.md：安装、配置、更新以及连接使用的说明。
LICENSE and THIRD-PARTY-NOTICES.md: licenses for the project and bundled dependencies.
许可证和第三方通知文件：关于该项目的许可证以及所依赖库的许可证信息。
SHA256SUMS.txt contains the ZIP's SHA-256 checksum. GitHub's automatically generated source archives are for building from source.
SHA256SUMS.txt 文件中包含了 ZIP 压缩包的 SHA-256 校验和。GitHub 自动生成的源代码档案可用于从源代码构建该软件。

Install and connect  安装并连接好设备。
Install the Windows x64 .NET 10 frameworks required by Cheat Engine's managed host and the plugin: Microsoft.NETCore.App, Microsoft.AspNetCore.App, and Microsoft.WindowsDesktop.App. Follow the included README to configure Cheat Engine's ce.runtimeconfig.json.
请安装 Cheat Engine 管理主机所需的 Windows x64 .NET 10 框架，以及插件 Microsoft.NETCore.App 、 Microsoft.AspNetCore.App 和 Microsoft.WindowsDesktop.App 。请参照随附的 README 文件来配置 Cheat Engine 的 ce.runtimeconfig.json 功能。
In Cheat Engine, open Edit > Settings > Plugins, add CheatEngine.Mcp.dll from the extracted folder, and enable it.
在 Cheat Engine 中，打开“编辑”>“设置”>“插件”，将从提取的文件夹中复制的 CheatEngine.Mcp.dll 添加到列表中，然后启用它。
Configure your AI application's stdio MCP server command to the full path of CheatEngine.Mcp.Gateway.exe.
请配置你的 AI 应用程序的 stdio MCP 服务器命令，使其指向 CheatEngine.Mcp.Gateway.exe 的完整路径。
Call instance_list, then use the returned instanceId for calls to that Cheat Engine instance. One gateway supports multiple enabled Cheat Engine instances.
请调用 instance_list ，然后使用返回的 instanceId 来调用该 Cheat Engine 实例。一个网关可以支持多个启用的 Cheat Engine 实例。
The gateway is a standalone Native AOT executable. The plugin requires the installed .NET frameworks. Costura extracts its embedded native Lua bridge into a per-user cache when loading it.
该网关是一个独立的原生 AOT 可执行文件。该插件需要安装.NET 框架。在加载时，Costura 会将内置的原生 Lua 桥接层提取到每个用户的缓存中。

Operator guidance is provided through MCP resources and workflow prompts. No separate skill installation is required. Defaults are built in; the included README explains optional JSON settings and file-access roots.
操作指南通过 MCP 资源和工作流程提示来提供。无需安装单独的技能组件。默认设置已经包含在内；附带的 README 文件详细说明了可选的 JSON 配置和文件访问权限设置。

To update an earlier installation, close Cheat Engine and the gateway before replacing the files. Add the new DLL plugin entry and preserve personal configuration in the user data directory.
如果要更新之前的安装程序，请先关闭 Cheat Engine 软件以及相关工具，然后再替换文件。请添加新的 DLL 插件条目，并保留用户数据目录中的个人配置设置。

Packaging improvements  包装方面的改进
Install the plugin as one DLL, with the gateway kept as its own executable.
将该插件作为单个 DLL 进行安装，同时让网关保持为独立的可执行文件。
Releases use one complete ZIP and a checksum file, produced and verified by eng/Release.ps1.
这些发布文件包含了一个完整的 ZIP 文件以及一个校验和文件，这些文件均由 eng/Release.ps1 生成并进行了验证。
Bundled dependencies remain isolated between plugin load contexts.
捆绑在一起的依赖项在插件加载上下文之间仍然保持隔离状态。
The regression probe compares the bundled plugin's reflected tools, schemas, resources, and prompts with the reviewed MCP contract.
该回归测试工具会对比打包的插件中包含的工具、模式、资源以及提示信息与已审核的 MCP 合同内容。
Validation  确认/验证
Debug and Release portable suites passed with 3,968 tests each, zero failures, and zero skips. The published DLL passed fresh-process loading, native bridge resolution, dependency isolation, and reflection checks in two load contexts. The Native AOT gateway passed its executable MCP smoke check.
那些经过调试和发布的可移植套件，每项都通过了 3,968 次测试。没有任何失败或遗漏的情况。所发布的 DLL 在两种加载环境中通过了新鲜进程加载、原生桥接解析、依赖项隔离以及反射检查等测试。而那个原生 AOT 网关则通过了其可执行文件的 MCP 烟雾测试。

Earlier live qualification exercised a focused two-instance Cheat Engine scenario. This beta does not claim live coverage of every exposed tool, every debugger backend, or DBVM. Use the plugin only with software you own or are authorized to inspect or modify.
在之前的实时资格测试中，采用了一种针对特定场景的测试方案。这个测试版并不保证能够覆盖所有可用的工具、所有的调试器后端以及数据库接口。请仅在您拥有权限或被允许检查、修改的软件中使用该插件。



CheatEngine.Mcp.dll 和 CheatEngine.Mcp.Gateway.exe 以及使用说明
已经下载到项目内 McpExternals/CheatEngine.Mcp-2.0.0-beta.2-win-x64 文件夹

