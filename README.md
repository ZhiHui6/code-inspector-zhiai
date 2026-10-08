# 🛡️ Code Inspector Zhiai

**A cross-language code review skill for AI agents**

*Reports provable risks first, then provides a verifiable remediation path.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Rules](https://img.shields.io/badge/rules-265-blue.svg)](#-rule-id-categories) [![Languages](https://img.shields.io/badge/languages-13-green.svg)](#-features) [![Modes](https://img.shields.io/badge/modes-4-8A2BE2.svg)](#-working-modes) [![Python](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](skills/code-inspector-zhiai-en/scripts) [![Type](https://img.shields.io/badge/type-Agent%20Skill-informational.svg)](#)

🌐 **English** · 📖 [中文](README.zh.md)

---

## 🎯 Overview

Code Inspector is a code review skill for AI agents. It loads rule packs based on project context, **reports provable risks first, then provides a verifiable remediation path**, keeping scope explicit, evidence traceable, and conclusions consistent with confidence.

> 🔒 **Read-only by default** — files are modified only when the user explicitly requests a fix or refactor.

## ✨ Features

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

## 🧩 Working modes

| Mode | Behavior | Writes files |
|:--:|---|:--:|
| 🔍 **Review** (default) | Read-only inspection: issues, evidence, impact, recommendations, verification | ❌ |
| 🔎 **Audit** | Review plus dependencies, secrets, config, migrations, deployment, supply chain | ❌ |
| 📐 **Refactor plan** | Plan, split order, compatibility risks, test plan only | ❌ |
| 🛠️ **Fix** | Modifies files only on explicit request; minimal unified diff, re-verified | ✅ |

## 🔄 Flow

```text
🧭 Determine scope → 📋 Build project inventory → 🎒 Select rule packs → 🔍 Check high-risk paths first
   → ✅ Verify current state → 📝 Generate report → 🛠️ Remediate (Fix mode only) → 🔁 Re-inspect
```

## 📁 Repository layout

```text
code-inspector-zhiai/
├── README.md                        # English (this file)
├── README.zh.md                     # 中文
├── LICENSE
├── .gitignore
└── skills/
    ├── code-inspector-zhiai/          # Chinese version
    │   ├── SKILL.md
    │   ├── agents/openai.yaml
    │   ├── references/                # 13 rule files
    │   │   ├── core-rules.md
    │   │   ├── routing.md
    │   │   ├── report-contract.md
    │   │   ├── style-readability.md
    │   │   └── language-*.md          # 9 language packs
    │   └── scripts/
    │       ├── detect_stack.py
    │       └── validate_report.py
    └── code-inspector-zhiai-en/       # English version (same layout)
```

## 📦 Installation

Copy the language folder you need from `skills/` into your agent's skills directory (the folder name must match the `name` field in `SKILL.md`):

```bash
# English version
cp -r skills/code-inspector-zhiai-en ~/.your-agent/skills/

# 中文版
cp -r skills/code-inspector-zhiai ~/.your-agent/skills/
```

## 🧭 Usage

Simply ask for a code review in conversation:

| You say | It does |
|---|---|
| `Review this code` | Full check on the current file |
| `Audit the src/ directory` | Recursive check on the given directory |
| `Run a security audit` | Focus on security and supply-chain risk |
| `Check whether this change introduces new issues` | Diff-based incremental check |

## 🧰 Scripts

Both scripts are **optional enhancements**: Python standard library only, read-only, side-effect free. When the environment cannot execute them, the skill degrades to manual verification.

```bash
# 🔎 Detect the repository stack, print a JSON inventory
python skills/code-inspector-zhiai-en/scripts/detect_stack.py [root] [--compact]

# ✅ Validate a review report against the field contract
python skills/code-inspector-zhiai-en/scripts/validate_report.py <report.md> [--json]
```

---

## 📊 Rule ID categories

| Category | Scope |
|:--:|---|
| `COR` | Functional correctness, boundary conditions, requirement conformance, invariants |
| `SEC` | Injection, authn/authz, secrets, dangerous deserialization, supply chain |
| `REL` | Exceptions, timeouts, retries, resource release, failure recovery |
| `CON` | Concurrency, races, transactions, idempotency, data consistency |
| `API` | API/schema, serialization, compatibility, migration |
| `PERF` | Algorithms, queries, IO, memory, caching, rendering, resource limits |
| `TEST` | Regression, contract, integration, property tests, assertion validity |
| `MAINT` | Coupling, complexity, duplication, module boundaries, readability |
| `OPS` | Logging, metrics, tracing, configuration, deployment, observability |
| `STYLE` | Formatting and idioms (🎚️ gated, opt-in) |

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

⭐ If this project helps you, a star would be appreciated
