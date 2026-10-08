# Go Rules

## Contents

- [Scope](#scope)
- [Language Rules](#language-rules)
- [Web and Database](#web-and-database)
- [Verification](#verification)

## Scope

Load conditions include `.go`, `go.mod`, `go.work`, and Go CI configuration. Identify the Go version, module boundaries, generated code, and build tags.

## Language Rules

- `GO-ERROR-001`: Check whether errors are ignored, whether context is lost, whether error types are compared incorrectly, and whether the caller handles recoverable/non-recoverable failures.
- `GO-CONTEXT-001`: Requests, database, and external calls should propagate context; do not store context in long-lived objects, and do not use nil context.
- `GO-CONC-001`: Check goroutine startup, exit, cancellation, channel close, and backpressure; identify leaks and duplicate consumption.
- `GO-RACE-001`: Check shared maps/slices, lazy initialization, and closure variables; use the race detector to verify when conditions allow.
- `GO-RESOURCE-001`: Check the release of response bodies, files, rows, tickers, listeners, and locks, especially defer in loops.
- `GO-COR-001`: Check nil interfaces, slice/map semantics, partial writes after errors, integer overflow, and time handling.
- `GO-HTTP-001`: Clients and servers should have timeouts, size limits, cancellation, and status code handling.
- `GO-PERF-001`: Check in-loop IO, unbounded goroutines/caches, repeated encoding, and unnecessary copies; do not report issues based solely on "one extra allocation."
- `GO-BUILDER-001`: The main rule for in-loop string concatenation is `PERF-CONCAT-001`; in Go prefer `strings.Builder`/`bytes.Buffer`; do not report small-scale or constant concatenation.
- `GO-SLICE-001`: Check whether slices/maps preallocate capacity when the size is known, and whether allocations repeat inside loops; report only when the scale or hot path is clear.

## Web and Database

- `GO-HTTP-AUTH-001`: Verify middleware ordering, object-level authorization, request body limits, and sensitive logging.
- `GO-SQL-001`: Use parameterized queries; check rows/transaction lifetimes, N+1, and migration lock risks.

## Verification

Prefer `go test`, `go vet`, project-declared static analysis, and `-race` where necessary. When a command is unavailable or the environment does not support it, record that faithfully.
