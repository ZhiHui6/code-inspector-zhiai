# Code Inspector Zhiai

> 面向 AI Agent 的跨语言代码审查技能 · A cross-language code review skill for AI agents
>
> [中文](#中文) · [English](#english)

---

## 中文

### 简介

Code Inspector 是一个面向 AI Agent 的代码审查 Skill。它按项目上下文加载规则包，**先报告可证实的风险，再给出可验证的整改路径**，保持范围明确、证据可追溯、结论与置信度一致。

默认只读：只有用户明确要求修复或重构时才修改文件。

### 特性

- **265 条稳定规则编号**：如 `SEC-TAINT-001`、`PERF-CONCAT-001`、`MAINT-DUP-001`，可映射、可追踪、可引用。
- **10 类发现分类**：`COR` 正确性、`SEC` 安全、`REL` 可靠性、`CON` 并发、`API` 契约、`PERF` 性能、`TEST` 测试、`MAINT` 可维护性、`OPS` 运维、`STYLE` 风格。
- **4 种工作模式**：Review（默认只读）、Audit（含依赖/秘密/供应链）、Refactor plan（只出方案）、Fix（最小 diff 改文件）。
- **跨语言覆盖**：JavaScript/TypeScript、Python、Java/Kotlin/Spring、Go、Rust、C/C++、C#/.NET、PHP、Ruby、Swift、Dart/Flutter、Scala、Elixir。
- **制品规则**：SQL 与迁移、GraphQL/OpenAPI、HTML/CSS、Shell/PowerShell、配置文件、Docker、Kubernetes/Helm、Terraform、CI/CD。
- **证据优先**：每个发现都要求路径、行号或可定位符号、代码证据、影响、严重度、置信度和验证方式。
- **误报控制与脱敏**：报告与日志中脱敏密钥、令牌、Cookie、个人数据与完整连接串。
- **风格包门控**：格式/可读性/结构阈值集中在独立规则包，默认不加载，仅在用户显式要求时启用。
- **可选脚本**：`detect_stack.py` 只读探测技术栈，`validate_report.py` 校验报告字段契约与密钥泄露。

### 目录结构

```text
code-inspector-zhiai/
├── README.md
├── LICENSE
├── .gitignore
└── skills/
    ├── code-inspector-zhiai/          # 中文版
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── references/                # 13 个规则文件
    │   │   ├── core-rules.md
    │   │   ├── routing.md
    │   │   ├── report-contract.md
    │   │   ├── style-readability.md
    │   │   └── language-*.md          # 9 个语言规则包
    │   └── scripts/
    │       ├── detect_stack.py
    │       └── validate_report.py
    └── code-inspector-zhiai-en/       # English version
        └── （同结构 / same layout）
```

### 安装

把 `skills/` 下对应语言的目录复制到你的 Agent 技能目录即可（目录名需与 `SKILL.md` 中的 `name` 一致）：

```bash
# 中文版
cp -r skills/code-inspector-zhiai ~/.your-agent/skills/

# English version
cp -r skills/code-inspector-zhiai-en ~/.your-agent/skills/
```

### 使用

在对话中直接提出代码审查请求即可，例如：

```text
检查这段代码
审查 src/ 目录
安全审计
检查这个改动是否引入新问题
```

技能会按 `SKILL.md` 的流程执行：确定范围 → 建立项目清单 → 选择规则包 → 优先检查高风险路径 → 验证现状 → 生成报告 → （可选）整改 → 复查。

### 脚本

两个脚本均为**可选增强**，仅使用 Python 标准库，只读、无副作用；环境不可执行时技能会自动降级为人工核对。

```bash
# 探测仓库技术栈，输出 JSON 清单
python skills/code-inspector-zhiai/scripts/detect_stack.py [root] [--compact]

# 校验审查报告是否符合字段契约
python skills/code-inspector-zhiai/scripts/validate_report.py <report.md> [--json]
```

---

## English

### Overview

Code Inspector is a code review skill for AI agents. It loads rule packs based on project context, **reports provable risks first, then provides a verifiable remediation path**, keeping scope explicit, evidence traceable, and conclusions consistent with confidence.

Read-only by default: files are modified only when the user explicitly requests a fix or refactor.

### Features

- **265 stable rule IDs** such as `SEC-TAINT-001`, `PERF-CONCAT-001`, `MAINT-DUP-001` — mappable, traceable, and referenceable.
- **10 finding categories**: `COR` correctness, `SEC` security, `REL` reliability, `CON` concurrency, `API` contracts, `PERF` performance, `TEST` testing, `MAINT` maintainability, `OPS` operations, `STYLE` style.
- **4 working modes**: Review (read-only, default), Audit (dependencies/secrets/supply chain), Refactor plan (plan only), Fix (minimal diff).
- **Cross-language coverage**: JavaScript/TypeScript, Python, Java/Kotlin/Spring, Go, Rust, C/C++, C#/.NET, PHP, Ruby, Swift, Dart/Flutter, Scala, Elixir.
- **Artifact rules**: SQL and migrations, GraphQL/OpenAPI, HTML/CSS, Shell/PowerShell, configuration files, Docker, Kubernetes/Helm, Terraform, CI/CD.
- **Evidence first**: every finding requires a path, line number or locatable symbol, code evidence, impact, severity, confidence, and verification method.
- **False-positive control and redaction**: secrets, tokens, cookies, personal data, and full connection strings are redacted in reports and logs.
- **Gated style pack**: formatting/readability/structural thresholds live in a separate rule pack, not loaded by default, enabled only on explicit request.
- **Optional scripts**: `detect_stack.py` performs read-only stack detection; `validate_report.py` validates report field contracts and secret leakage.

### Installation

Copy the language folder you need from `skills/` into your agent's skills directory (the folder name must match the `name` field in `SKILL.md`):

```bash
cp -r skills/code-inspector-zhiai-en ~/.your-agent/skills/
```

### Usage

Simply ask for a code review in conversation, for example:

```text
Review this code
Audit the src/ directory
Run a security audit
Check whether this change introduces new issues
```

### Scripts

Both scripts are **optional enhancements**. They use only the Python standard library, are read-only and side-effect free; when the environment cannot execute them, the skill degrades to manual verification.

```bash
python skills/code-inspector-zhiai-en/scripts/detect_stack.py [root] [--compact]
python skills/code-inspector-zhiai-en/scripts/validate_report.py <report.md> [--json]
```

---

## 规则编号速览 · Rule ID at a glance

| 分类 Category | 覆盖范围 Scope |
|---|---|
| `COR` | 功能正确性、边界条件、需求符合度、不变量 |
| `SEC` | 注入、认证授权、秘密、危险反序列化、供应链 |
| `REL` | 异常、超时、重试、资源释放、失败恢复 |
| `CON` | 并发、竞态、事务、幂等性、数据一致性 |
| `API` | API/Schema、序列化、兼容性、迁移 |
| `PERF` | 算法、查询、IO、内存、缓存、渲染、资源上限 |
| `TEST` | 回归、契约、集成、属性测试、断言有效性 |
| `MAINT` | 耦合、复杂度、重复、模块边界、可读性 |
| `OPS` | 日志、指标、追踪、配置、部署、可观测性 |
| `STYLE` | 格式与惯用法（门控加载） |

---

## 许可证 · License

本项目采用 [MIT License](LICENSE) 开源。
This project is licensed under the [MIT License](LICENSE).
