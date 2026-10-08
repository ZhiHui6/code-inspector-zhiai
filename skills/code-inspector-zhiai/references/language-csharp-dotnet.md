# C# and .NET Rules

## 目录

- [适用范围](#适用范围)
- [语言与运行时](#语言与运行时)
- [ASP.NET 与 EF Core](#aspnet-与-ef-core)
- [验证](#验证)

## 适用范围

加载条件包括 `.cs`、`.csproj`、`.sln`、`global.json` 和 .NET 配置。识别目标框架、nullable、分析器、ASP.NET/worker/桌面类型。

## 语言与运行时

- `CS-NULL-001`：检查 nullable 警告、`!`、默认值和外部输入的运行时验证。
- `CS-ASYNC-001`：检查未 await 的任务、`async void`（事件处理器例外）、同步阻塞 async 和取消 token 传播。
- `CS-RESOURCE-001`：检查 `IDisposable`/`IAsyncDisposable`、HttpClient 生命周期、流和锁释放。
- `CS-SEC-001`：检查反射/反序列化、命令/路径/SQL 注入、日志 PII 和授权边界。
- `CS-CON-001`：检查共享状态、线程安全、Channel/后台任务关闭和重试幂等性。

## ASP.NET 与 EF Core

- `ASP-AUTH-001`：核对 endpoint、policy、resource authorization 和默认拒绝。
- `ASP-CONTRACT-001`：检查模型绑定、验证、错误响应、版本和文件上传限制。
- `EF-PERF-001`：检查 N+1、tracking、分页、投影、事务和并发 token。

## 验证

优先运行 `dotnet test`、编译、项目分析器和声明的格式检查。不要在没有项目上下文时机械要求某个 `ConfigureAwait` 或命名风格。
