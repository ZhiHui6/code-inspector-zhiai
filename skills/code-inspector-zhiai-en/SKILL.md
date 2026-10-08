---
name: code-inspector-zhiai-en
description: Perform code review, security audit, performance analysis, and remediation planning on source code, configuration, dependencies, or changesets. Use for explicit Code Review, code quality, or technical security requests; do not use to audit agent instructions, Skill specifications, prompts, or Codex configuration. Read-only by default; modify files only when the user explicitly requests a fix or refactor.
---

# Code Inspector

Select general rules and language/framework rules based on project context, report provable risks first, then provide a verifiable remediation path. Keep scope explicit, evidence traceable, and conclusions consistent with confidence.

## Working Modes

- **Review (default)**: read-only inspection that outputs issues, evidence, impact, recommendations, and verification commands; does not modify files.
- **Audit**: beyond Review, inspect dependencies, secrets, configuration, migrations, deployment, and supply chain risks.
- **Refactor plan**: output only the refactoring plan, split order, compatibility risks, and test plan.
- **Fix**: modify files only when the user explicitly requests it; prefer providing a minimal unified diff and re-verify after the change.

## Overall Flow

1. **Determine the target**: read the user's scope, task intent, read-only/modify authorization, runtime environment, and project-level `AGENTS.md`; when no scope is specified, prefer the current changeset, and only expand to the whole repository when the user requests it or the issue truly crosses boundaries. Auditing agent instructions, Skill specifications, prompts, and Codex configuration is out of scope for this skill.
2. **Build a project inventory**: use `rg --files` and `scripts/detect_stack.py` (if runnable) to identify languages, versions, frameworks, manifest files, test directories, CI configuration, and existing commands. Do not read or output secret values.
3. **Select rule packs**: always load the applicable general rules; select language/framework/artifact rules based on extensions, shebangs, dependency manifests, imports, and configuration; load `style-readability.md` only when the user explicitly requests a format/style/readability review. Rule pack selection and gating are described in [references/routing.md](references/routing.md).
4. **Check high-risk paths first**: inspect in the order of correctness, data contracts, security, reliability/concurrency, performance, testing, maintainability, and style. For cross-file issues, trace inputs, state, storage, and outputs, and do not treat isolated style differences as defects.
5. **Verify the current state**: prefer running the lint, type check, test, build, or audit commands the project already declares and that are relevant to the scope. Do not automatically install dependencies, go online, deploy, or run destructive migrations in order to run checks; commands not run must have their reasons recorded.
6. **Generate the report**: follow [references/report-contract.md](references/report-contract.md); every finding must have a path, line number or locatable symbol, code evidence, impact, severity, confidence, and verification method. When the report is written to a file, run `scripts/validate_report.py <report.md>`; when replying directly, manually verify against the same fields. Do not create issues without evidence.
7. **Perform remediation (Fix mode only)**: preserve the user's existing changes and use minimal patches; do not force a full file rewrite, and do not insert cross-language-incompatible `//` markers into source code. Behavior changes require added or updated targeted tests.
8. **Re-inspect**: re-run the relevant checks, compare behavior before and after the change, and state risks that remain uncovered.

## Scope and Safety Boundaries

- By default, inspect the files the user specifies, the current diff, and their direct dependencies; explain scope changes before expanding scope.
- By default, skip generated files, build artifacts, caches, vendor directories, and binary files. Lock files may be used for dependency audits but are not rewritten by default.
- Do not perform releases, deletions, destructive database migrations, remote writes, or unauthorized credential operations.
- Redact secrets, tokens, cookies, personal data, and full connection strings in reports and logs; retain only variable names, locations, and necessary fingerprint information.
- Follow the project's existing formatter, linter, type configuration, and naming conventions; flag assumptions when versions or conventions cannot be confirmed, and do not force a single language style.

## Finding Categories

Use stable rule IDs, and do not conflate rule IDs with this report's issue numbers:

| Category | Focus |
|---|---|
| `COR` | Functional correctness, boundary conditions, requirement conformance, invariants |
| `SEC` | Injection, authentication/authorization, secrets, dangerous deserialization, supply chain |
| `REL` | Exceptions, timeouts, retries, resource release, failure recovery |
| `CON` | Concurrency, races, transactions, idempotency, and data consistency |
| `API` | API/Schema, serialization, compatibility, migration |
| `PERF` | Algorithms, queries, IO, memory, caching, rendering, and resource limits |
| `TEST` | Regression, contract, integration, property tests, and assertion validity |
| `MAINT` | Coupling, complexity, duplication, module boundaries, and readability |
| `OPS` | Logging, metrics, tracing, configuration, deployment, and observability |
| `STYLE` | Formatting and idioms; by default reported only when there is consistency or maintenance benefit, and load `style-readability.md` per gating when the user explicitly requests the style dimension |

## Severity and Confidence

- `P0`: can directly lead to remote exploitation, major data leakage/corruption, production unavailability, or release blocking.
- `P1`: high-probability functional errors, privilege bypass, data inconsistency, resource exhaustion, or obvious regression.
- `P2`: medium risk, test gaps, maintainability issues, or conditionally triggered performance problems.
- `P3`: low-risk style, local simplification, or optional optimization.

Mark each issue with `high`, `medium`, or `low` confidence. Low-confidence conclusions must state the assumptions to be confirmed and must not be directly labeled "must fix". By default, treat P0/P1 as the release gate, and do not force computation of an A-F score; when the user requests a score, normalize by applicable dimensions and disclose the calculation method, avoiding deductions for inapplicable dimensions.

## Rule Pack Navigation

| What is found | Reference to read |
|---|---|
| All projects | [references/core-rules.md](references/core-rules.md), [references/routing.md](references/routing.md), [references/report-contract.md](references/report-contract.md) |
| JavaScript/TypeScript, Node, browser | [references/language-js-ts.md](references/language-js-ts.md) |
| Python | [references/language-python.md](references/language-python.md) |
| Java/Kotlin, Spring | [references/language-jvm.md](references/language-jvm.md) |
| Go | [references/language-go.md](references/language-go.md) |
| Rust | [references/language-rust.md](references/language-rust.md) |
| C/C++ | [references/language-c-cpp.md](references/language-c-cpp.md) |
| C#/.NET | [references/language-csharp-dotnet.md](references/language-csharp-dotnet.md) |
| PHP, Ruby, Swift, Dart | [references/language-other.md](references/language-other.md) |
| HTML/CSS, SQL, GraphQL, OpenAPI, configuration, scripts, containers, and IaC | [references/artifacts.md](references/artifacts.md) |
| The user explicitly requests a format/style/readability review, or a rating that includes the style dimension | [references/style-readability.md](references/style-readability.md) (not loaded by default, see gating) |

Read only the rule packs relevant to the current project. When a repository contains multiple languages, apply rules separately to each boundary and additionally check API, data, and build contracts. For unrecognized languages, still run the general checks and explicitly mark "no specialized rules loaded" in the report; do not fabricate syntax conclusions. The style/readability rule pack is not loaded by default and is enabled only when the user explicitly requests the style/readability dimension, and is handled at its default lower severity.

## Completion Checklist

- [ ] Scope, mode, language/version, and exclusions are recorded.
- [ ] Both general rules and applicable specialized rules have been checked; inapplicable items are noted with reasons.
- [ ] If the user explicitly requests a style/readability review, `style-readability.md` has been loaded per gating, and "reference thresholds" are distinguished from hard defects.
- [ ] Every issue has a real location, evidence, impact, severity, confidence, and verification method.
- [ ] Commands run, exit results, and reasons for not running are listed.
- [ ] Review mode did not modify files; Fix mode changed only the authorized scope and completed re-inspection.
