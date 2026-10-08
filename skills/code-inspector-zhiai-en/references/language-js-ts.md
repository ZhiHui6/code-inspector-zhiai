# JavaScript and TypeScript Rules

## Contents

- [Scope and Versions](#scope-and-versions)
- [Types and Contracts](#types-and-contracts)
- [Language Semantics](#language-semantics)
- [Async, Concurrency, and Resources](#async-concurrency-and-resources)
- [Security](#security)
- [Node.js and Server Frameworks](#nodejs-and-server-frameworks)
- [Browser and Frontend Frameworks](#browser-and-frontend-frameworks)
- [Modules, Dependencies, and Build](#modules-dependencies-and-build)
- [Testing and Verification](#testing-and-verification)

## Scope and Versions

Load conditions include `.js`, `.jsx`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.mts`, `.cts`, `package.json`, `tsconfig*.json`, or the corresponding build configuration. First identify the Node/browser/Bun/Deno runtime, module system, TypeScript version, package manager, framework version, and project lint/formatter rules. The same repository may contain server, client, SSR, worker, and build-script code at once; check their trust boundaries separately.

## Types and Contracts

- `TS-CONFIG-001`: Read the actually effective `extends` chain and project references, and verify `strict`, module resolution, JSX, lib, target, and emit settings. Only recommend tightening options when you can prove the configuration masks a defect; do not mechanically require enabling all strict flags at once.
- `TS-TYPE-001`: Check whether `any` spread, double assertions, non-null assertions, un-narrowed `unknown`, broad index signatures, and `@ts-ignore` cross a real boundary. Test fixtures and third-party type gaps may be local exceptions.
- `TS-CONTRACT-001`: Check whether discriminated unions, generic constraints, overloads, optional fields and `undefined`, readonly, and error types match runtime data; public functions and exported APIs should declare return types explicitly to avoid inference drift or accidental exposure of internal types; passing the type check does not mean external JSON, environment variables, or DOM data have been verified.
- `TS-BOUNDARY-001`: Perform runtime schema validation at HTTP, message, database, localStorage, file, and deserialization boundaries, and keep the rejection path; do not repeat validation on trusted internal objects.
- `TS-API-001`: Check whether exported types, declaration files, package exports, and generated clients remain backward compatible, with special attention to changes in enums, union types, and optional/nullable.

## Language Semantics

- `JS-COR-001`: Check `null`/`undefined`, NaN, negative zero, BigInt, floating-point precision, time zones, truthy/falsy, and implicit string/number conversion. Intentional forms such as `value == null` must be judged in light of lint and semantics.
- `JS-OBJECT-001`: Check object/array shallow copies, prototype inheritance, getter side effects, mutable keys, sparse arrays, in-place `sort` mutation, and mutation of a collection during iteration.
- `JS-CLOSURE-001`: Check closure capture, `this` binding, loop variables, module-level mutable state, and frontend stale closures; you must point to the actual async or lifecycle path.
- `JS-ERROR-001`: Check throwing non-Error values, lost error causes, mixing synchronous/asynchronous error channels, and business failures converted into successful returns.
- `JS-REGEX-001`: For untrusted long input, check catastrophic backtracking, unbounded matching, and incorrect Unicode assumptions; only report ReDoS when constructible input and complexity evidence exist.
- `JS-MODERN-001`: Check strict equality (`===`/`!==`) and redundant checks that modern syntax (optional chaining, nullish coalescing) could simplify; for mutability declaration preferences (`const`/`let`/`var`) see the gated `STYLE-CONST-001`; report only when the project does not uniformly enforce it via lint/formatter.
- `JS-ARRAY-001`: Check whether array/iteration methods match intent (`map`/`filter`/`reduce`/`forEach`/`for...of`), avoiding `map` used for side effects, `await` inside `forEach`, and ignoring the `reduce` initial value; do not make pure style judgments.
- `JS-PROMISE-001`: Check deep Promise chains, callback hell, and the error-channel fragmentation caused by mixing `then` with `async/await`; prefer unifying on `async/await` while preserving necessary concurrency semantics.
- `JS-OPTCHAIN-001`: Check whether optional chaining/nullish coalescing is misused and causes logic to fail silently (returning `undefined` when it should throw, `??` masking missing configuration); you must be able to point to the actual masked error path.

## Async, Concurrency, and Resources

- `JS-ASYNC-001`: Check whether Promises are awaited, returned, or explicitly handled, and whether floating promises, lost rejections, unawaited async callbacks, and lost error context exist. Do not mechanically convert all callbacks to `async/await`.
- `JS-CONC-001`: Check the fail-fast/partial-success semantics of `Promise.all`, unbounded concurrency, duplicate submissions, out-of-order responses overwriting newer state, and shared-cache races; evidence of idempotency, rate limiting, or version stamps is required.
- `JS-CANCEL-001`: Check whether AbortSignal propagates from the request/component to fetch, the database, streams, and subtasks, and whether state is still written or resources still consumed after cancellation.
- `JS-RESOURCE-001`: Check that event listeners, timers, subscriptions, WebSockets, MessagePorts, observers, file handles, and streams are cleaned up on success, exception, and unmount paths.
- `JS-STREAM-001`: Check Node/Web streams for error, backpressure, pipeline termination, Body size limits, and partial reads; do not make buffering the entire input the default implementation.

## Security

- `JS-XSS-001`: Trace data from URLs, forms, messages, and storage to `innerHTML`, templates, DOM URLs, scripts, and CSS sinks, and distinguish HTML/attribute/URL/JS context encoding; "contains a string" alone cannot prove XSS.
- `JS-INJECT-001`: Check SQL/NoSQL, command, path, template, header, log, and dynamic-import concatenation, preferring parameterization, fixed mappings, and allowlists.
- `JS-PROTOTYPE-001`: Check whether deep merge, dynamic property assignment, and object deserialization allow `__proto__`, `constructor`, or `prototype` pollution; confirm the library version and object creation method.
- `JS-SSRF-001`: Check the scheme, DNS/IP, redirects, proxies, and cloud metadata access of controllable URLs; you must prove the input is reachable to a server-side network request.
- `JS-AUTH-001`: Verify authentication, object-level authorization, tenant isolation, CSRF/CORS/Cookie attributes, and default-deny on routes/handlers; do not judge it safe merely because global middleware exists.
- `JS-SERIALIZE-001`: Check the schema, prototype, dates/large integers, circular references, and sensitive fields of untrusted objects; do not use `JSON.parse(JSON.stringify(...))` as a general deep copy or security filter.

## Node.js and Server Frameworks

- `NODE-TIMEOUT-001`: External HTTP, database, queue, DNS, subprocess, and stream calls must have explainable timeouts, cancellation, and concurrency and size limits.
- `NODE-ERROR-001`: Check Express/Nest/Fastify/Koa middleware error chains, stream `error`, background-task rejections, and process-level exception policy; a process-level handler cannot replace request-level recovery.
- `NODE-PROCESS-001`: Check graceful shutdown, stopping connection acceptance, task draining, exit codes, signals, and worker/child-process lifecycle.
- `NODE-API-001`: Check request schemas, status codes, error models, upload limits, pagination, idempotency keys, and sensitive fields in responses. Framework DTO types cannot replace runtime validation.
- `NODE-DATA-001`: In data layers such as Prisma/TypeORM/Sequelize/Mongoose, check N+1, unpaginated queries, transaction boundaries, bulk writes, mass assignment, and model hook side effects.
- `NODE-CACHE-001`: Check whether cache keys include tenant/permission/version, whether invalidation is consistent, whether value and key counts are bounded, and whether failures bypass security checks.

## Browser and Frontend Frameworks

- `UI-LIFECYCLE-001`: Check the dependencies, cleanup, cancellation, and races of effects/watches/subscriptions; do not assert functional errors based solely on lint warnings.
- `UI-STATE-001`: Check updates based on stale values, direct mutation, duplicated derived state, stable keys, controlled form state, and async results overwriting state.
- `UI-SSR-001`: Check server/client initial values, browser-only APIs, randomness/time, authentication state, and data caching that cause hydration issues or cross-request leakage.
- `UI-ACCESS-001`: Check semantics, keyboard, focus, labels, error messaging, loading/empty states, and dynamic-update announcements; apply only to real interactive code.
- `UI-RENDER-001`: Check large lists, duplicate requests, expensive computations, and context/store broadcasts; you must combine profiler, dependency path, or input scale, and must not mechanically add memo.
- `UI-PERF-001`: Check debounce/throttle of high-frequency events, and lazy loading and compression of images/static assets; for long lists, expensive computations, and caching see `UI-RENDER-001`; combine real interaction frequency and input scale, and do not mechanically add memo/debounce.
- `REACT-HOOK-001`: Check Hook call order, effect dependencies/cleanup, side effects under concurrent rendering, Suspense/transition failure states, and the server/client component boundary.
- `VUE-REACTIVITY-001`: Check ref/reactive unwrapping, watch flush/cleanup, computed side effects, component-scoped resources, and SSR state isolation.
- `ANGULAR-RX-001`: Check Observable subscription disposal, error channels, switch/merge/concat semantics, change detection, DI scope, and the fact that route guards cannot replace server-side authorization.

## Modules, Dependencies, and Build

- `JS-MODULE-001`: Check ESM/CJS, conditional exports, default/named imports, circular dependencies, side-effect imports, top-level await, and dynamic-import error boundaries.
- `JS-BUILD-001`: Check browser/server environment-variable isolation, source map exposure, tree-shaking side effects, SSR bundles, and polyfill/target compatibility.
- `JS-DEP-001`: Verify the lockfile and package manager, direct dependency sources, script lifecycle, and workspace boundaries; for the general determination of unused dependencies see `MAINT-UNUSED-001`; vulnerability conclusions must come from actual versions and audit evidence.

## Testing and Verification

- `JS-TEST-001`: Check whether async assertions are awaited, whether fake timers/microtasks are advanced correctly, whether mocks are reset, whether snapshots mask behavior, and the differences between jsdom and real browsers.
- `JS-TEST-002`: For security, concurrency, SSR, routing, and database issues, prefer adding boundary or integration tests; mocks that only test implementation details cannot prove the real contract.

Prefer reading project scripts and CI, then run the existing lint, `tsc --noEmit`/typecheck, unit tests, browser tests, and build. Record the Node, TypeScript, package manager, module system, and actual configuration; when there is no configuration, do not treat a tool's default rules as the project standard.
