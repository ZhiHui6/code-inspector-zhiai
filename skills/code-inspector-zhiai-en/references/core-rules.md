# Cross-Language Core Rules

## Contents

- [Rule Record Format](#rule-record-format)
- [Correctness](#correctness)
- [Security and Privacy](#security-and-privacy)
- [Reliability](#reliability)
- [Concurrency and Consistency](#concurrency-and-consistency)
- [Contracts and Compatibility](#contracts-and-compatibility)
- [Performance and Resources](#performance-and-resources)
- [Testing](#testing)
- [Maintainability and Operations](#maintainability-and-operations)
- [False-Positive Control](#false-positive-control)

## Rule Record Format

Every specialized or general rule should map to the following fields:

```text
rule_id: stable and unique, e.g. COR-BOUNDARY-001
applies_when: applicable conditions and exclusion conditions
inspect: the code/configuration facts to observe
evidence: the locatable form of evidence
severity: default P0-P3; adjust based on actual impact
false_positive_guard: when not to report
verify: the recommended safe verification command or test
```

Rules are inspection prompts, not unconditional refactoring instructions. Project conventions, versions, and business invariants take precedence over general preferences.

## Correctness

- `COR-CONTRACT-001`: Verify that inputs, outputs, errors, and state transitions conform to requirements, types/schema, and caller assumptions.
- `COR-BOUNDARY-001`: Check null values, empty collections, boundary values, timeouts, duplicate requests, partial failures, and reentrancy.
- `COR-STATE-001`: Check whether state initialization, update ordering, cache invalidation, and post-failure recovery preserve invariants.
- `COR-RESOURCE-001`: Confirm that files, connections, locks, temporary objects, subscriptions, and tasks are terminated on both success and exception paths.

Report only when a violated contract or a reproducible path can be identified; "looks unusual" is not evidence.

## Security and Privacy

- `SEC-TAINT-001`: Trace unvalidated data from requests, files, messages, environment variables, or user input to SQL, HTML, commands, paths, templates, and deserialization points.
- `SEC-AUTH-001`: Verify authentication, authorization, tenant isolation, object-level permissions, and default deny; do not merely check whether login middleware exists.
- `SEC-SECRET-001`: Identify hard-coded keys, log leakage, error echo, and insecure default configuration; report the location but redact the value.
- `SEC-DATA-001`: Check the collection, storage, transmission, retention, encryption, and log minimization of personal data.
- `SEC-DEP-001`: Check direct dependencies, lock files, provenance, version ranges, and declared audit commands; do not assert without basis that a dependency "has a vulnerability".

Incorporate exploitability, exposure surface, and impact into severity; the mere presence of a variable named `password` does not by itself prove a secret.

## Reliability

- `REL-ERROR-001`: Errors must be handled, transformed, or propagated with context; empty catch blocks, silently returning success, and losing the original error are forbidden.
- `REL-TIMEOUT-001`: External networks, databases, queues, and subprocesses must have explainable timeout and cancellation boundaries.
- `REL-RETRY-001`: Retries should have limits, backoff, idempotency, and observability; do not blindly retry non-retryable errors.
- `REL-FALLBACK-001`: Fallback, circuit-breaking, and partial-success paths must not bypass authorization, data validation, or consistency constraints.
- `REL-RESOURCE-001`: Check resource release, connection pools, file handles, listeners, tasks, and temporary file lifecycles.

## Concurrency and Consistency

- `CON-RACE-001`: Identify shared mutable state, check-to-use gaps, duplicate consumption, and out-of-order writes.
- `CON-CANCEL-001`: Async tasks, goroutines, threads, futures, and queue consumers must have lifecycle, cancellation, and exit strategies.
- `CON-TRANSACTION-001`: Confirm that transaction boundaries cover all related writes, and handle commit failures, retries, and external side effects.
- `CON-IDEMPOTENCY-001`: Check idempotency keys and duplicate-request handling for webhooks, messages, payments, batch processing, and retry entry points.

When there is no concurrency or transaction evidence, mark as "not applicable"; do not demand locking or opening a transaction out of nowhere.

## Contracts and Compatibility

- `API-SCHEMA-001`: Check schema, serialization, default values, enums, error codes, and backward compatibility.
- `API-CONSUMER-001`: Trace field usage, version negotiation, pagination, and null semantics from the caller side.
- `API-MIGRATION-001`: Migrations must consider old versions, rollback, lock time, data backfill, and dual-write/dual-read windows.
- `API-CONFIG-001`: The default values, types, secrets, and change compatibility of configuration keys, environment variables, and feature flags must be explicit.

## Performance and Resources

- `PERF-COMPLEXITY-001`: Identify complexity degradation as input size grows, repeated traversals, and unbounded recursion.
- `PERF-LOOP-001`: Check loop-invariant computations that can be hoisted out of loops, condition ordering that can be optimized by probability or short-circuiting, and unnecessary collection/type round-trips; report only when there is scale or hot-path evidence.
- `PERF-CONCAT-001`: Identify repeated string concatenation (`+`/`+=`) inside loops or repeated construction of large objects; recommend language-appropriate aggregation such as builder/join/StringIO, and do not report small-scale or constant concatenation. Language-specific rules (such as Go `GO-BUILDER-001`) reference this number rather than establishing a separate primary number.
- `PERF-IO-001`: Identify network/database/disk IO inside loops, N+1, repeated serialization, and unnecessary full reads.
- `PERF-BOUND-001`: Check whether pagination, batch size, cache limits, concurrency degree, request bodies, and queue backlogs are bounded.
- `PERF-MEASURE-001`: Without benchmarks, execution plans, or metrics, use "may" and provide a verification method; do not write guesses as facts.

## Testing

- `TEST-BEHAVIOR-001`: Tests should verify user-observable behavior, errors, and boundaries, not merely cover lines.
- `TEST-ASSERT-001`: Check whether assertions actually fail, whether they only verify truthy, and whether mocks are misused to bypass core logic.
- `TEST-REGRESSION-001`: Every P0/P1 behavioral defect should have a targeted regression test or an explicit explanation of why one cannot be added.
- `TEST-CONTRACT-001`: Cross-service, schema, migration, and serialization changes should consider contract/integration tests.

## Maintainability and Operations

- `MAINT-BOUNDARY-001`: Check module responsibilities, dependency direction, public interfaces, and cross-layer leakage.
- `MAINT-COMPLEXITY-001`: Address overly long functions and deep nesting based on cognitive load and change risk, not mechanical deduction by fixed line counts or parameter counts; for duplicate code see `MAINT-DUP-001`, and for fixed thresholds of function/file length, cyclomatic complexity, nesting, and parameters see the gated [style-readability.md](style-readability.md).
- `MAINT-DEAD-001`: Identify commented-out dead code, unreachable branches, always-false conditions, leftover switches, and unreferenced private symbols; confirm there is no framework/reflection/external call dependency before recommending deletion, and let version control bear the history.
- `MAINT-DUP-001`: Identify extractable duplicate code blocks, mergeable similar conditional branches, constants defined repeatedly in multiple places, and wrapper functions with no real logic; confirm before merging whether the difference is intentional or coincidental similarity.
- `MAINT-UNUSED-001`: Check unused imports/dependencies, variables, functions, types, and parameters; conclusions about unused dependencies in language-specific rules (such as `JS-DEP-001`) reference this number; note false positives caused by exported symbols, dynamic references, reflection, serialization, and framework conventions.
- `MAINT-SIMPLICITY-001`: Check DRY/KISS/YAGNI violations and over-engineering (premature abstraction for a hypothetical future, unnecessary configuration layers/interface layers); report only when it adds real cognitive load, and do not treat "looks flexible" as a defect.
- `MAINT-TESTABILITY-001`: Check hard-to-test designs (implicit global dependencies, non-injectable external clients, directly inlined time/randomness/IO); recommend dependency injection, pure functions, or port abstraction, but must align with the project's existing architecture.
- `OPS-LOG-001`: Logs must have events, correlation IDs, levels, and actionable context, and must not leak secrets/personal data.
- `OPS-HEALTH-001`: Services should have reasonable health checks, timeouts, metrics, and failure alerts; do not mistake log volume for observability quality.
- `STYLE-CONFIG-001`: Formatting and idioms are low priority by default, reported only when the project has no contrary configuration and it can reduce maintenance cost; when systematic style/readability/structure checks are needed, load [style-readability.md](style-readability.md) per the gating conditions.

## False-Positive Control

Confirm each item before reporting: the code path is truly reachable; the impact is not purely theoretical; the rule applies to the current version; the project configuration does not explicitly allow the pattern; the issue is not intentional behavior in generated code or test fixtures. When confirmation is impossible, downgrade to `low` confidence and list it as an item to be confirmed.
