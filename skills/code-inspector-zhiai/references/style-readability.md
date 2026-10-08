# Style, Readability, and Structural Heuristics

## 目录

- [适用范围与门控](#适用范围与门控)
- [格式与风格](#格式与风格)
- [可读性](#可读性)
- [结构启发式阈值](#结构启发式阈值)
- [验证](#验证)

## 适用范围与门控

本规则包默认**不加载**，以保持 code-inspector 证据优先、低噪声的默认行为。仅在以下条件成立时启用：

1. 用户明确要求格式检查、代码风格、可读性、命名规范，或明确要求“含风格维度的代码体检”。
2. 报告需要与清单式工具（A–F 逐维度评级）对齐，且用户明确要求覆盖格式与可读性维度。

不得仅因项目“看起来没有风格工具”就自行加载本包。项目已配置 Prettier/ESLint/Black/Ruff/clang-format/Checkstyle/Spotless 等工具时，**以工具输出为准**，本包只作补充说明，不覆盖工具结论，也不因风格问题阻断发布。风格类问题默认 `P3`，可读性结构问题默认 `P2`，仅当用户明确把风格纳入门槛时才升级严重度。

## 格式与风格

- `STYLE-NAMING-001`：检查命名是否符合语言/项目约定（camelCase / snake_case / PascalCase）并保持一致性；与既有代码冲突时以项目为准。
- `STYLE-INDENT-001`：检查缩进是否统一（Tab / 2 空格 / 4 空格）、大括号风格是否一致（K&R / Allman）、空行分组是否合理。
- `STYLE-LINEWIDTH-001`：检查行宽是否超出项目约定（无约定时参考 ≤120 字符）或明显影响阅读。
- `STYLE-WHITESPACE-001`：检查运算符/逗号空格一致性、尾随空格和文件末尾换行。
- `STYLE-IMPORT-001`：检查 import/use 是否分组有序（标准库 → 第三方 → 本地）、是否存在乱序或未分组。
- `STYLE-CONST-001`：检查可变性声明偏好（如 JS `const` > `let` > `var`、Java `final`、C++ `const`、Go 零值使用）；仅在项目无工具约束时报告，JS 侧由 `JS-MODERN-001` 引用本编号。

## 可读性

- `READ-MAGIC-001`：检查魔法数字/字符串是否应提取为命名常量；说明提取后的语义收益，纯配置常量不报。
- `READ-NAMING-001`：检查变量/函数/类型命名是否准确表达意图（避免 `data`/`info`/`tmp`/`handle2`），布尔量是否使用 `is/has/can/should` 前缀。
- `READ-COMMENT-001`：检查复杂逻辑是否缺少“为什么”的注释、公共 API 是否缺少 JSDoc/docstring；不要求给显而易见代码加注释。
- `READ-GUARD-001`：检查深嵌套条件是否可用卫语句（early return/continue）简化。
- `READ-TERNARY-001`：检查嵌套三元表达式或复杂逻辑运算符是否影响可读性。
- `READ-DEBUG-001`：检查遗留的注释掉代码块、临时调试输出（`console.log`/`print`/`fmt.Println`）和过期 TODO；与 `MAINT-DEAD-001` 呼应，此处侧重可读性呈现。

## 结构启发式阈值

以下阈值为**参考信号**，用于定位“可能需要拆分或简化”的位置，**不得机械扣分**；是否报告取决于认知负担与变更风险（与 `MAINT-COMPLEXITY-001` 一致）。在报告中引用阈值时必须同时说明实际规模与拆分收益。

- `STRUCT-FUNC-001`：函数长度参考 ≤50 行；超出时说明是否真的难以理解、测试或复用。
- `STRUCT-FILE-001`：单文件参考 ≤300 行；超出时检查是否混合了多个职责。
- `STRUCT-COMPLEXITY-001`：圈复杂度参考 ≤10；超出时定位具体分支来源并给出拆分点。
- `STRUCT-NEST-001`：嵌套层级参考 ≤4 层；超出时优先考虑卫语句或抽取函数。
- `STRUCT-PARAM-001`：参数个数参考 ≤4；超出时考虑对象参数或配置对象，并确认调用方兼容性；本编号是“参数过多”的主编号。
- `STRUCT-GOD-001`：识别 God Class / God Function（职责过载、方法过多、状态耦合过广）。

## 验证

优先运行项目已有的 formatter/linter（Prettier、ESLint、Black/Ruff、gofmt、clang-format、Checkstyle/Spotless 等）并以其结果为准。没有对应工具时，人工核对上述条目，并在报告中标注“基于项目无风格工具的人工基线”，避免把人工偏好表述为硬性缺陷。
