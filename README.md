<div align="center">

# 🛡️ Code Inspector Zhiai

**面向 AI Agent 的跨语言代码审查技能**

*Reports provable risks first, then provides a verifiable remediation path.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Rules](https://img.shields.io/badge/rules-265-blue.svg)](#-规则编号速览)
[![Languages](https://img.shields.io/badge/languages-13-green.svg)](#-特性)
[![Modes](https://img.shields.io/badge/modes-4-8A2BE2.svg)](#-工作模式)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](skills/code-inspector-zhiai/scripts)
[![Type](https://img.shields.io/badge/type-Agent%20Skill-informational.svg)](#)

[📖 中文](#-中文) · [🌐 English](#-english)

</div>

---

## 📖 中文

### 🎯 简介

Code Inspector 是一个面向 AI Agent 的代码审查技能。它按项目上下文加载规则包，**先报告可证实的风险，再给出可验证的整改路径**，保持范围明确、证据可追溯、结论与置信度一致。

> 🔒 **默认只读**——只有用户明确要求修复或重构时才修改文件。

### ✨ 特性

| | 特性 | 说明 |
|:--:|---|---|
| 🧭 | **规则编号体系** | 265 条稳定编号（如 `SEC-TAINT-001`），可映射、可追踪、可引用 |
| 🗂️ | **10 类发现分类** | 正确性 / 安全 / 可靠性 / 并发 / 契约 / 性能 / 测试 / 可维护性 / 运维 / 风格 |
| 🎛️ | **4 种工作模式** | Review（只读）、Audit（含供应链）、Refactor plan（只出方案）、Fix（最小 diff） |
| 🌍 | **跨语言覆盖** | JS/TS、Python、Java/Kotlin、Go、Rust、C/C++、C#/.NET、PHP、Ruby、Swift、Dart、Scala、Elixir |
| 🧱 | **制品规则** | SQL 迁移、GraphQL/OpenAPI、HTML/CSS、Shell、配置、Docker、K8s/Helm、Terraform、CI/CD |
| 🔬 | **证据优先** | 每个发现都要求路径、行号或可定位符号、代码证据、影响、严重度、置信度与验证方式 |
| 🚫 | **误报控制** | 明确的 `false_positive_guard`，低置信度结论必须标注待确认假设 |
| 🙈 | **自动脱敏** | 报告与日志中脱敏密钥、令牌、Cookie、个人数据与完整连接串 |
| 🎚️ | **风格包门控** | 格式/可读性/结构阈值集中在独立规则包，默认不加载，仅显式要求时启用 |
| 🧰 | **可选脚本** | `detect_stack.py` 只读探测技术栈，`validate_report.py` 校验报告契约与密钥泄露 |

### 🧩 工作模式

| 模式 | 行为 | 是否改文件 |
|:--:|---|:--:|
| 🔍 **Review**（默认） | 只读检查，输出问题、证据、影响、建议和验证命令 | ❌ |
| 🔎 **Audit** | 在 Review 之外检查依赖、秘密、配置、迁移、部署与供应链风险 | ❌ |
| 📐 **Refactor plan** | 只输出重构方案、拆分顺序、兼容性风险与测试计划 | ❌ |
| 🛠️ **Fix** | 仅在用户明确要求时修改文件，优先最小 unified diff，改后复验 | ✅ |

### 🔄 执行流程

```text
🧭 确定范围 → 📋 建立项目清单 → 🎒 选择规则包 → 🔍 优先检查高风险路径
   → ✅ 验证现状 → 📝 生成报告 → 🛠️ 整改（仅 Fix 模式）→ 🔁 复查
```

### 📁 目录结构

```text
code-inspector-zhiai/
├── README.md
├── LICENSE
├── .gitignore
└── skills/
    ├── code-inspector-zhiai/          # 中文版
    │   ├── SKILL.md                   # 技能入口与总流程
    │   ├── agents/openai.yaml         # Agent 接口配置
    │   ├── references/                # 13 个规则文件
    │   │   ├── core-rules.md          # 跨语言核心规则
    │   │   ├── routing.md             # 规则路由与门控
    │   │   ├── report-contract.md     # 报告字段契约
    │   │   ├── style-readability.md   # 风格/可读性（门控）
    │   │   └── language-*.md          # 9 个语言规则包
    │   └── scripts/
    │       ├── detect_stack.py        # 技术栈探测
    │       └── validate_report.py     # 报告校验
    └── code-inspector-zhiai-en/       # English version
        └── （同结构 / same layout）
```

### 📦 安装

把 `skills/` 下对应语言的目录复制到你的 Agent 技能目录（目录名需与 `SKILL.md` 中的 `name` 一致）：

```bash
# 中文版
cp -r skills/code-inspector-zhiai ~/.your-agent/skills/

# English version
cp -r skills/code-inspector-zhiai-en ~/.your-agent/skills/
```

### 🧭 使用

在对话中直接提出代码审查请求即可：

| 你说 | 它做 |
|---|---|
| `检查这段代码` | 对当前文件执行全量检查 |
| `审查 src/ 目录` | 对指定目录递归检查 |
| `安全审计` | 聚焦安全维度与供应链风险 |
| `检查这个改动是否引入新问题` | 基于 diff 的增量检查 |

### 🧰 脚本

两个脚本均为**可选增强**：仅使用 Python 标准库，只读、无副作用。环境不可执行时，技能自动降级为人工核对。

```bash
# 🔎 探测仓库技术栈，输出 JSON 清单
python skills/code-inspector-zhiai/scripts/detect_stack.py [root] [--compact]

# ✅ 校验审查报告是否符合字段契约
python skills/code-inspector-zhiai/scripts/validate_report.py <report.md> [--json]
```

---

## 🌐 English

### 🎯 Overview

Code Inspector is a code review skill for AI agents. It loads rule packs based on project context, **reports provable risks first, then provides a verifiable remediation path**, keeping scope explicit, evidence traceable, and conclusions consistent with confidence.

> 🔒 **Read-only by default** — files are modified only when the user explicitly requests a fix or refactor.

### ✨ Features

| | Feature | Description |
|:--:|---|---|
| 🧭 | **Stable rule IDs** | 265 IDs (e.g. `SEC-TAINT-001`) — mappable, traceable, referenceable |
| 🗂️ | **10 finding categories** | Correctness / Security / Reliability / Concurrency / API / Performance / Testing / Maintainability / Operations / Style |
| 🎛️ | **4 working modes** | Review (read-only), Audit (incl. supply chain), Refactor plan, Fix (minimal diff) |
| 🌍 | **Cross-language** | JS/TS, Python, Java/Kotlin, Go, Rust, C/C++, C#/.NET, PHP, Ruby, Swift, Dart, Scala, Elixir |
| 🧱 | **Artifact rules** | SQL migrations, GraphQL/OpenAPI, HTML/CSS, Shell, config, Docker, K8s/Helm, Terraform, CI/CD |
| 🔬 | **Evidence first** | Every finding needs a path, line or locatable symbol, evidence, impact, severity, confidence, verification |
| 🚫 | **False-positive control** | Explicit `false_positive_guard`; low-confidence conclusions must state assumptions |
| 🙈 | **Redaction** | Secrets, tokens, cookies, personal data, and connection strings are redacted |
| 🎚️ | **Gated style pack** | Formatting/readability/threshold rules live in a separate pack, opt-in only |
| 🧰 | **Optional scripts** | `detect_stack.py` for stack detection, `validate_report.py` for report contract checks |

### 🧩 Working modes

| Mode | Behavior | Writes files |
|:--:|---|:--:|
| 🔍 **Review** (default) | Read-only inspection: issues, evidence, impact, recommendations, verification | ❌ |
| 🔎 **Audit** | Review plus dependencies, secrets, config, migrations, deployment, supply chain | ❌ |
| 📐 **Refactor plan** | Plan, split order, compatibility risks, test plan only | ❌ |
| 🛠️ **Fix** | Modifies files only on explicit request; minimal unified diff, re-verified | ✅ |

### 📦 Installation

```bash
cp -r skills/code-inspector-zhiai-en ~/.your-agent/skills/
```

### 🧭 Usage

```text
Review this code
Audit the src/ directory
Run a security audit
Check whether this change introduces new issues
```

### 🧰 Scripts

```bash
python skills/code-inspector-zhiai-en/scripts/detect_stack.py [root] [--compact]
python skills/code-inspector-zhiai-en/scripts/validate_report.py <report.md> [--json]
```

---

## 📊 规则编号速览

| 分类 | 关注内容 |
|:--:|---|
| `COR` | 功能正确性、边界条件、需求符合度、不变量 |
| `SEC` | 注入、认证授权、秘密、危险反序列化、供应链 |
| `REL` | 异常、超时、重试、资源释放、失败恢复 |
| `CON` | 并发、竞态、事务、幂等性、数据一致性 |
| `API` | API/Schema、序列化、兼容性、迁移 |
| `PERF` | 算法、查询、IO、内存、缓存、渲染、资源上限 |
| `TEST` | 回归、契约、集成、属性测试、断言有效性 |
| `MAINT` | 耦合、复杂度、重复、模块边界、可读性 |
| `OPS` | 日志、指标、追踪、配置、部署、可观测性 |
| `STYLE` | 格式与惯用法（🎚️ 门控加载） |

---

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源 · Licensed under the [MIT License](LICENSE).

<div align="center">

**⭐ 如果这个项目对你有帮助，欢迎 Star 支持一下**

</div>
