# Rule Routing and Project Detection

## Contents

- [Detection Priority](#detection-priority)
- [Project Signals](#project-signals)
- [Rule Selection](#rule-selection)
- [Command Discovery](#command-discovery)
- [Confidence and Fallback](#confidence-and-fallback)
- [Boundaries](#boundaries)

## Detection Priority

Determine rule applicability in the following priority order, and when conflicts arise keep the higher-priority conclusion:

1. The language, framework, version, and inspection scope explicitly specified by the user.
2. The repository's `AGENTS.md`, contribution guidelines, build configuration, formatter/linter configuration, and CI definitions.
3. Dependency manifests, lock files, build files, and framework entry points.
4. File extensions, shebangs, directory conventions, and import statements.
5. Code content heuristics.

Do not conclude the framework or runtime from a single file's extension. When multiple versions or multiple build systems are found, record them separately and state the assumptions.

## Project Signals

| Signal | Common examples | Routing action |
|---|---|---|
| JS/TS | `package.json`, `tsconfig*.json`, lockfile | Identify runtime, module system, TypeScript configuration, and scripts; then refine by Node, SSR, React/Vue/Angular, and data-layer characteristics |
| Python | `pyproject.toml`, `requirements*.txt`, `poetry.lock` | Load the Python pack; refine by Django/FastAPI/Flask, async, and data-processing characteristics |
| JVM | `pom.xml`, `build.gradle*`, wrapper/toolchain | Identify JDK release, modules, and plugins; then refine by Spring MVC/WebFlux, JPA/Hibernate, Android, and Kotlin coroutine characteristics |
| Go | `go.mod`, `go.sum` | Load the Go pack; check HTTP, database, goroutine, and context boundaries |
| Rust | `Cargo.toml`, `Cargo.lock` | Load the Rust pack; check ownership, unsafe, async, and FFI |
| C/C++ | `CMakeLists.txt`, `Makefile`, `.vcxproj` | Load the C/C++ pack; check lifetimes, undefined behavior, and build variants |
| .NET | `*.sln`, `*.csproj`, `global.json` | Load the C#/.NET pack; refine by ASP.NET, EF Core, worker, or desktop application |
| Data/API | `*.sql`, OpenAPI/GraphQL schema, migration directories | Load the artifact pack and check cross-service contracts and migration risks |
| Operations | `Dockerfile`, `*.yaml`, Helm, Terraform, CI files | Load the artifact pack; check secrets, permissions, resource limits, and reversibility |

## Rule Selection

Build a rule set for each target file:

```text
General core rules
  + Language rules (by file and runtime)
  + Framework rules (only when dependency/entry-point evidence is sufficient)
  + Artifact rules (SQL, API, configuration, containers, IaC, CI)
  + Style/readability rules (only when the user explicitly requests, see below)
```

Keep only one primary rule number per issue, and note the affected cross-boundary components in the report. Tests, migrations, schemas, and configuration files must not be skipped because they "don't look like business code".

### Style and Readability Gating

[style-readability.md](style-readability.md) is not loaded by default, and must not be self-enabled merely because the project "looks like it has no style tooling". Load it only when the user explicitly requests a format/style/readability review or explicitly requests a rating that includes the style dimension. When the project already has style tooling, defer to the tool output; style issues default to P3 and must not alone block a release.

## Command Discovery

First read the commands the project already declares, then select the minimal set relevant to risk. Common mappings are as follows, executed only when the command actually exists and dependencies are available:

| Ecosystem | Prefer to check |
|---|---|
| JS/TS | lint, typecheck/`tsc`, unit/integration/browser tests, build in project scripts; verify Node, TS, and module configuration |
| Python | `ruff`/`flake8`, `mypy`/`pyright`, `pytest` |
| JVM | the repository wrapper's Maven `test`/`verify` or Gradle `test`/`check`, compilation, static analysis; verify the actual JDK toolchain/profile |
| Go | `go test`, `go vet`, and race tests when necessary |
| Rust | `cargo test`, `cargo check`, `cargo clippy`, format check |
| C/C++ | project build, clang-tidy or compiler warnings, Sanitizer when available |
| .NET | `dotnet test`, compilation, analyzers/format check |
| PHP/Ruby | PHPUnit/RSpec, static analysis, style check |

Prefer existing CI commands and scripts, set reasonable timeouts; do not modify configuration or skip failures just to "go green". Write the command, version, exit code, and truncated key output into the report.

## Confidence and Fallback

- `high`: the rule, version, and code evidence are all explicit, or the tool reports directly.
- `medium`: the code evidence is explicit, but the runtime, caller, or configuration is not yet complete.
- `low`: only heuristic signs; list as an item to be confirmed, and do not treat as a release blocker.

For unrecognized languages, run the general core rules, dependency, and contract checks, and output the uncovered items. Do not apply another language's syntax preferences to an unknown language.

## Boundaries

By default, exclude generated directories, build artifacts, caches, vendor source, binaries, and large files. Lock files are read-only for dependency audits; secret files are checked only for existence and reference relationships, without outputting contents. If the user explicitly includes these paths in scope, first explain the potential noise and risks.
