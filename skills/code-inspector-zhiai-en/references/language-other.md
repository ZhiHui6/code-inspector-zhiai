# Additional Language Rules

## Contents

- [PHP](#php)
- [Ruby](#ruby)
- [Swift and Objective-C](#swift-and-objective-c)
- [Dart and Flutter](#dart-and-flutter)
- [Scala and Elixir](#scala-and-elixir)
- [Verification](#verification)

## PHP

- `PHP-SEC-001`: Check SQL/command/path injection, output encoding, CSRF, session cookies, file uploads, and deserialization.
- `PHP-TYPE-001`: Check `strict_types`, external input validation, implicit type conversion, and null semantics.
- `LARAVEL-PERF-001`: In Laravel, check mass assignment, policy authorization, ORM N+1, queue idempotency, and configuration cache boundaries.

## Ruby

- `RUBY-SEC-001`: Check SQL/template/command injection, strong parameters, deserialization, and secret logging.
- `RUBY-REL-001`: Check exception boundaries, transactions, background job retries, and resource release.
- `RAILS-PERF-001`: Check ActiveRecord N+1, unpaginated queries, callback side effects, and migration locks.

## Swift and Objective-C

- `SWIFT-LIFE-001`: Check force unwrapping, optional boundaries, retain cycles, delegate deregistration, and resource lifecycle.
- `SWIFT-CON-001`: Check MainActor/UI thread, actor isolation, Task cancellation, and shared state.
- `OBJC-MEM-001`: Check manual memory management, block captures, pointers, and Objective-C exception/error boundaries.

## Dart and Flutter

- `DART-ASYNC-001`: Check unhandled Futures, cancellation, stream subscriptions, and isolate boundaries.
- `FLUTTER-LIFE-001`: Check the `dispose` of controllers, focus, animations, and subscriptions.
- `FLUTTER-RENDER-001`: Check side effects in build, large lists, stable keys, and UI thread blocking.

## Scala and Elixir

- `SCALA-COR-001`: Check the error paths of `Option`/`Either`/`Try`, Future execution contexts, mutable collections, and implicit conversion boundaries.
- `SCALA-PERF-001`: Check whether collection laziness/materialization, parallel collections, and Spark transformations match the data scale and execution plan.
- `ELIXIR-CON-001`: Check process/supervision lifecycle, message backlog, state isolation, and unhandled messages in the mailbox.
- `ELIXIR-DATA-001`: Check whether pattern matching, Ecto changeset, transactions, and SQL parameterization cover exception paths.

For Lua, R, and other unlisted languages, first apply the general rules and artifact rules; propose language-specific conclusions only after finding explicit syntactic evidence and loading the corresponding extension pack.

## Verification

Run Composer/PHPUnit/PHPStan, Bundler/RSpec/RuboCop/Brakeman, Swift test/Xcode build, or Dart/Flutter test/analyzer as declared by the project. When tools are missing, report only static evidence and unverified items.
