# C and C++ Rules

## Contents

- [Scope](#scope)
- [Memory and Undefined Behavior](#memory-and-undefined-behavior)
- [Boundaries and Concurrency](#boundaries-and-concurrency)
- [Build and Verification](#build-and-verification)

## Scope

Load conditions include `.c`, `.h`, `.cc`, `.cpp`, `.hpp`, CMake, Make, Meson, or Visual Studio projects. First distinguish the C/C++ standard, compiler, platform, and build configuration.

## Memory and Undefined Behavior

- `CPP-LIFE-001`: Check use-after-free, double free, dangling references, out-of-bounds, uninitialized reads, and unclear ownership.
- `CPP-RAII-001`: For C++, prioritize RAII, smart pointers, exception safety, and container boundaries; for C projects, check all return paths of explicit cleanup.
- `CPP-UB-001`: Check signed overflow, shifts, alignment, strict aliasing, formatting, and integer/pointer conversions.
- `CPP-FFI-001`: Check ABI, struct layout, string termination, calling conventions, and cross-language resource release.
- `CPP-HEADER-001`: Check whether headers use include guards or `#pragma once`, whether they expose implementation details, and whether there are risks of duplicate inclusion or macro pollution; judge together with the build configuration.

## Boundaries and Concurrency

- `CPP-INPUT-001`: Trace lengths, indices, files, network, and formatted input into memory/command/API sinks.
- `CPP-CON-001`: Check data races, lock ordering, atomic memory ordering, thread lifetimes, and callback unregistration.
- `CPP-EXCEPTION-001`: Check exception safety levels, error codes, and destructor behavior; do not require all projects to use exceptions uniformly.

## Build and Verification

Prefer project build commands, compiler warnings, clang-tidy, static analysis, and Sanitizers. Do not write performance guesses as defects without a reproduction or tool evidence; preserve platform/compilation option differences.
