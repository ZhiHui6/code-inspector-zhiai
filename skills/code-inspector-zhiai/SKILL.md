---
name: code-inspector-zhiai
description: 对源代码、配置、依赖或变更集进行代码审查、安全审计、性能分析与整改规划。用于明确的 Code Review、代码质量或技术安全请求；不用于审计 agent 指令、Skill 规范、提示词或 Codex 配置。默认只读，只有用户明确要求修复或重构时才修改文件。
---

# Code Inspector

按项目上下文选择通用规则和语言/框架规则，先报告可证实的风险，再给出可验证的整改路径。保持范围明确、证据可追溯、结论与置信度一致。

## 工作模式

- **Review（默认）**：只读检查，输出问题、证据、影响、建议和验证命令；不修改文件。
- **Audit**：在 Review 之外检查依赖、秘密、配置、迁移、部署和供应链风险。
- **Refactor plan**：只输出重构方案、拆分顺序、兼容性风险和测试计划。
- **Fix**：仅在用户明确要求时修改文件；优先提供最小 unified diff，并在修改后重新验证。

## 总体流程

1. **确定目标**：读取用户范围、任务意图、只读/修改授权、运行环境和项目级 `AGENTS.md`；未指定范围时以当前变更集为首选，只有用户要求或问题确实跨越边界时才扩大到整个仓库。Agent 指令、Skill 规范、提示词和 Codex 配置审计不适用此技能。
2. **建立项目清单**：使用 `rg --files` 和 `scripts/detect_stack.py`（若可运行）识别语言、版本、框架、清单文件、测试目录、CI 配置和现有命令。不要读取或输出秘密值。
3. **选择规则包**：始终加载适用的通用规则；根据扩展名、shebang、依赖清单、导入和配置选择语言/框架/制品规则；仅当用户显式要求格式/风格/可读性审查时才加载 `style-readability.md`。规则包选择与门控见 [references/routing.md](references/routing.md)。
4. **先查高风险路径**：按正确性、数据契约、安全、可靠性/并发、性能、测试、可维护性和风格的顺序检查。跨文件问题要追踪输入、状态、存储和输出，不把孤立的风格差异当成缺陷。
5. **验证现状**：优先运行项目已经声明且与范围相关的 lint、类型检查、测试、构建或审计命令。不得为了运行检查而自动安装依赖、联网、部署或执行破坏性迁移；未运行的命令必须记录原因。
6. **生成报告**：遵循 [references/report-contract.md](references/report-contract.md)，每个发现都要有路径、行号或可定位符号、代码证据、影响、严重度、置信度和验证方式。报告写入文件时运行 `scripts/validate_report.py <report.md>`；直接回复时按同一字段人工核对。没有证据就不要创建问题。
7. **执行整改（仅 Fix 模式）**：保留用户已有改动，使用最小补丁；不要强制重写完整文件，不要在源代码中插入跨语言不兼容的 `//` 标记。行为变化需要补充或更新针对性测试。
8. **复查**：重新运行相关检查，比较修改前后行为，并说明仍未覆盖的风险。

## 范围与安全边界

- 默认检查用户指定文件、当前 diff 及其直接依赖；扩大范围前说明范围变化。
- 默认跳过生成文件、构建产物、缓存、供应商目录和二进制文件。锁文件可用于依赖审计，但默认不改写。
- 不执行发布、删除、数据库破坏性迁移、远程写操作或未经授权的凭据操作。
- 在报告和日志中脱敏密钥、令牌、Cookie、个人数据和完整连接串；只保留变量名、位置和必要的指纹信息。
- 遵循项目已有的 formatter、linter、类型配置和命名约定；无法确认版本或约定时标记假设，不强行套用单一语言风格。

## 发现分类

使用稳定的规则编号，不把规则编号和本次报告的问题编号混用：

| 分类 | 关注内容 |
|---|---|
| `COR` | 功能正确性、边界条件、需求符合度、不变量 |
| `SEC` | 注入、认证授权、秘密、危险反序列化、供应链 |
| `REL` | 异常、超时、重试、资源释放、失败恢复 |
| `CON` | 并发、竞态、事务、幂等性和数据一致性 |
| `API` | API/Schema、序列化、兼容性、迁移 |
| `PERF` | 算法、查询、IO、内存、缓存、渲染和资源上限 |
| `TEST` | 回归、契约、集成、属性测试和断言有效性 |
| `MAINT` | 耦合、复杂度、重复、模块边界和可读性 |
| `OPS` | 日志、指标、追踪、配置、部署和可观测性 |
| `STYLE` | 格式和惯用法；默认仅在有一致性或维护收益时报告，用户显式要求风格维度时按门控加载 `style-readability.md` |

## 严重度与置信度

- `P0`：可直接导致远程利用、重大数据泄露/损坏、生产不可用或发布阻断。
- `P1`：高概率功能错误、权限绕过、数据不一致、资源耗尽或明显回归。
- `P2`：中等风险、测试缺口、可维护性问题或有条件触发的性能问题。
- `P3`：低风险的风格、局部简化或可选优化。

为每个问题标记 `high`、`medium` 或 `low` 置信度。低置信度结论必须写出待确认假设，不能直接标为“必须修复”。默认以 P0/P1 为发布门槛，不强制计算 A-F 分数；用户要求评分时，按适用维度归一化并公开计算方法，避免对不适用维度扣分。

## 规则包导航

| 发现到的内容 | 读取的参考 |
|---|---|
| 所有项目 | [references/core-rules.md](references/core-rules.md)、[references/routing.md](references/routing.md)、[references/report-contract.md](references/report-contract.md) |
| JavaScript/TypeScript、Node、浏览器 | [references/language-js-ts.md](references/language-js-ts.md) |
| Python | [references/language-python.md](references/language-python.md) |
| Java/Kotlin、Spring | [references/language-jvm.md](references/language-jvm.md) |
| Go | [references/language-go.md](references/language-go.md) |
| Rust | [references/language-rust.md](references/language-rust.md) |
| C/C++ | [references/language-c-cpp.md](references/language-c-cpp.md) |
| C#/.NET | [references/language-csharp-dotnet.md](references/language-csharp-dotnet.md) |
| PHP、Ruby、Swift、Dart | [references/language-other.md](references/language-other.md) |
| HTML/CSS、SQL、GraphQL、OpenAPI、配置、脚本、容器和 IaC | [references/artifacts.md](references/artifacts.md) |
| 用户显式要求格式/风格/可读性审查，或要求含风格维度的评级 | [references/style-readability.md](references/style-readability.md)（默认不加载，见门控） |

只读取与当前项目相关的规则包。一个仓库包含多种语言时，对每个边界分别应用规则，并额外检查 API、数据和构建契约。无法识别的语言仍执行通用检查，并在报告中明确标记“未加载专项规则”，不得臆造语法结论。风格/可读性规则包默认不加载，仅在用户显式要求风格/可读性维度时启用，且以其默认较低严重度处理。

## 完成检查

- [ ] 范围、模式、语言/版本和排除项已记录。
- [ ] 通用规则与适用专项规则均已检查；不适用项注明原因。
- [ ] 若用户显式要求风格/可读性审查，已按门控加载 `style-readability.md`，并区分“参考阈值”与硬性缺陷。
- [ ] 每个问题都有真实位置、证据、影响、严重度、置信度和验证方式。
- [ ] 已运行的命令、退出结果和未运行原因已列出。
- [ ] Review 模式未修改文件；Fix 模式只改授权范围并完成复查。
