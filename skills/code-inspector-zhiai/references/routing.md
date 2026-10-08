# Rule Routing and Project Detection

## 目录

- [检测优先级](#检测优先级)
- [项目信号](#项目信号)
- [规则选择](#规则选择)
- [命令发现](#命令发现)
- [置信度和降级](#置信度和降级)
- [边界](#边界)

## 检测优先级

按以下优先级确定规则适用性，冲突时保留较高优先级结论：

1. 用户明确指定的语言、框架、版本和检查范围。
2. 仓库内的 `AGENTS.md`、贡献指南、构建配置、formatter/linter 配置和 CI 定义。
3. 依赖清单、锁文件、构建文件和框架入口。
4. 文件扩展名、shebang、目录约定和导入语句。
5. 代码内容启发式识别。

不要因为一个文件的扩展名就断定框架或运行时。发现多个版本或多个构建系统时，分别记录并说明假设。

## 项目信号

| 信号 | 常见例子 | 路由动作 |
|---|---|---|
| JS/TS | `package.json`、`tsconfig*.json`、lockfile | 识别运行时、模块系统、TypeScript 配置和 scripts；再按 Node、SSR、React/Vue/Angular、数据层特征细化 |
| Python | `pyproject.toml`、`requirements*.txt`、`poetry.lock` | 加载 Python 包；按 Django/FastAPI/Flask、async 和数据处理特征细化 |
| JVM | `pom.xml`、`build.gradle*`、wrapper/toolchain | 识别 JDK release、模块和插件；再按 Spring MVC/WebFlux、JPA/Hibernate、Android、Kotlin coroutine 特征细化 |
| Go | `go.mod`、`go.sum` | 加载 Go 包；检查 HTTP、数据库、goroutine 和 context 边界 |
| Rust | `Cargo.toml`、`Cargo.lock` | 加载 Rust 包；检查 ownership、unsafe、async 和 FFI |
| C/C++ | `CMakeLists.txt`、`Makefile`、`.vcxproj` | 加载 C/C++ 包；检查生命周期、未定义行为和构建变体 |
| .NET | `*.sln`、`*.csproj`、`global.json` | 加载 C#/.NET 包；按 ASP.NET、EF Core、worker 或桌面应用细化 |
| 数据/API | `*.sql`、OpenAPI/GraphQL schema、迁移目录 | 加载制品包，并检查跨服务契约和迁移风险 |
| 运维 | `Dockerfile`、`*.yaml`、Helm、Terraform、CI 文件 | 加载制品包；检查秘密、权限、资源限制和可回滚性 |

## 规则选择

对每个目标文件建立规则集合：

```text
通用核心规则
  + 语言规则（按文件和运行时）
  + 框架规则（仅在依赖/入口证据充分时）
  + 制品规则（SQL、API、配置、容器、IaC、CI）
  + 风格/可读性规则（仅用户显式要求时，见下）
```

同一问题只保留一个主规则编号，并在报告中注明受影响的跨边界组件。测试、迁移、schema 和配置文件不能因“不像业务代码”而跳过。

### 风格与可读性门控

[style-readability.md](style-readability.md) 默认不加载，不得仅因项目“看起来没有风格工具”就自行启用。仅在用户明确要求格式/风格/可读性审查，或明确要求含风格维度的评级时才加载。项目已有风格工具时以工具输出为准，风格类问题默认 P3，不得单独作为发布阻断。

## 命令发现

先读取项目已声明的命令，再选择与风险相关的最小集合。常见映射如下，仅在命令实际存在且依赖可用时执行：

| 生态 | 优先检查 |
|---|---|
| JS/TS | 项目 scripts 中的 lint、typecheck/`tsc`、单元/集成/浏览器测试、构建；核对 Node、TS 和模块配置 |
| Python | `ruff`/`flake8`、`mypy`/`pyright`、`pytest` |
| JVM | 仓库 wrapper 的 Maven `test`/`verify` 或 Gradle `test`/`check`、编译、静态分析；核对实际 JDK toolchain/profile |
| Go | `go test`、`go vet`，必要时 race 测试 |
| Rust | `cargo test`、`cargo check`、`cargo clippy`、格式检查 |
| C/C++ | 项目构建、clang-tidy 或编译器警告、可用时 Sanitizer |
| .NET | `dotnet test`、编译、分析器/格式检查 |
| PHP/Ruby | PHPUnit/RSpec、静态分析、风格检查 |

优先使用现有 CI 命令和脚本，设置合理超时；不为了“绿灯”修改配置或跳过失败。命令、版本、退出码和截断后的关键输出写入报告。

## 置信度和降级

- `high`：规则、版本和代码证据均明确，或工具直接报告。
- `medium`：代码证据明确，但运行时、调用方或配置尚不完整。
- `low`：仅启发式迹象；列为待确认项，不作为发布阻断。

无法识别的语言执行通用核心规则、依赖和契约检查，并输出未覆盖项。不要将别的语言的语法偏好套用到未知语言。

## 边界

默认排除生成目录、构建产物、缓存、供应商源码、二进制和大文件。锁文件只读用于依赖审计；秘密文件只做存在性和引用关系检查，不输出内容。若用户明确把这些路径纳入范围，先说明潜在噪声和风险。
