# C# and .NET Rules

## Contents

- [Scope](#scope)
- [Language and Runtime](#language-and-runtime)
- [ASP.NET and EF Core](#aspnet-and-ef-core)
- [Verification](#verification)

## Scope

Load conditions include `.cs`, `.csproj`, `.sln`, `global.json`, and .NET configuration. Identify the target framework, nullable, analyzers, and ASP.NET/worker/desktop types.

## Language and Runtime

- `CS-NULL-001`: Check nullable warnings, `!`, default values, and runtime validation of external input.
- `CS-ASYNC-001`: Check un-awaited tasks, `async void` (event handlers excepted), synchronous blocking of async, and cancellation token propagation.
- `CS-RESOURCE-001`: Check `IDisposable`/`IAsyncDisposable`, HttpClient lifetimes, and stream and lock release.
- `CS-SEC-001`: Check reflection/deserialization, command/path/SQL injection, logging PII, and authorization boundaries.
- `CS-CON-001`: Check shared state, thread safety, Channel/background task shutdown, and retry idempotency.

## ASP.NET and EF Core

- `ASP-AUTH-001`: Verify endpoint, policy, resource authorization, and default deny.
- `ASP-CONTRACT-001`: Check model binding, validation, error responses, versioning, and file upload limits.
- `EF-PERF-001`: Check N+1, tracking, pagination, projection, transactions, and concurrency tokens.

## Verification

Prefer running `dotnet test`, compilation, project analyzers, and declared format checks. Do not mechanically require a particular `ConfigureAwait` or naming style without project context.
