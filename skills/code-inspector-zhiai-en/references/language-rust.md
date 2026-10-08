# Rust Rules

## Contents

- [Scope](#scope)
- [Ownership and Errors](#ownership-and-errors)
- [Concurrency and Async](#concurrency-and-async)
- [unsafe and FFI](#unsafe-and-ffi)
- [Verification](#verification)

## Scope

Load conditions include `.rs`, `Cargo.toml`, `Cargo.lock`, and workspace configuration. Identify edition, MSRV, features, unsafe/FFI, and async runtime.

## Ownership and Errors

- `RUST-PANIC-001`: Check whether `unwrap`/`expect`/index panics on production paths can be triggered by external input; tests, unreachable invariants, and hard failures at startup must retain context.
- `RUST-ERROR-001`: Check `Result`/`Option` error conversion, source chains, error messages, and caller handling.
- `RUST-CLONE-001`: Identify large object clones, implicit allocations, and in-lock clones produced to bypass borrows; requires scale or hot-path evidence.
- `RUST-COR-001`: Check integer overflow patterns, UTF-8/byte boundaries, drop order, and partial state on cancellation.
- `RUST-ITER-001`: Check whether imperative index loops can be safely converted to iterator/`iter()` chains; do not make purely stylistic judgments, and prioritize boundary and panic risks.
- `RUST-LIFETIME-001`: Check whether lifetime annotations can be elided (when the compiler can infer them) or cause unnecessary complexity due to over-borrowing; judge together with borrow checker output.
- `RUST-ERRORLIB-001`: Check whether error types are implemented by hand instead of reusing ecosystem conventions such as `thiserror`/`anyhow`; suggest only when the project already adopts or clearly needs unified error handling.

## Concurrency and Async

- `RUST-ASYNC-001`: Check blocking IO in async, runtime mixing, task cancellation, join errors, and backpressure.
- `RUST-CON-001`: Check mutex/RwLock hold time, lock ordering, channel close, and `Send`/`Sync` boundaries.
- `RUST-ARC-001`: Check whether `Arc<Mutex<>>`/`RwLock` granularity is too coarse and whether finer-grained locks or message passing could replace it; requires contention or hot-path evidence.

## unsafe and FFI

- `RUST-UNSAFE-001`: Every unsafe block must have verifiable invariants, minimal scope, and a safe wrapper; do not classify something as a vulnerability merely because unsafe exists.
- `RUST-FFI-001`: Check pointer lifetimes, layout, error codes, thread/exception boundaries, and resource release.

## Verification

Prefer running `cargo check`, `cargo test`, `cargo fmt --check`, `cargo clippy`, and project-declared audit tools. Follow the project MSRV and feature combinations; do not upgrade the toolchain on your own.
