# Java and Kotlin Rules

## Contents

- [Scope and Versions](#scope-and-versions)
- [Java Semantics and Types](#java-semantics-and-types)
- [Exceptions and Resources](#exceptions-and-resources)
- [Concurrency and Modern Runtime](#concurrency-and-modern-runtime)
- [Security and Serialization](#security-and-serialization)
- [Spring and Service Boundaries](#spring-and-service-boundaries)
- [JPA/Hibernate and Data](#jpahibernate-and-data)
- [Performance](#performance)
- [Kotlin Interop](#kotlin-interop)
- [Build, Testing, and Verification](#build-testing-and-verification)

## Scope and Versions

Load conditions include `.java`, `.kt`, `.kts`, `pom.xml`, Gradle files, Maven/Gradle wrapper, Android build files, or JVM configuration. Identify the actual JDK release/toolchain, Kotlin/JVM target, Spring/Jakarta generation, module boundaries, annotation processors, and static-analysis configuration. When the version is unknown, do not suggest APIs available only on newer JDKs; for multi-module repositories, confirm each module's settings separately.

## Java Semantics and Types

- `JAVA-EQUALITY-001`: Verify `equals`/`hashCode`/`compareTo` consistency, array comparison, BigDecimal value/scale semantics, entity identity, and mutable map/set keys. Report only when they actually enter a comparison or a hash-based container.
- `JAVA-NULL-001`: Check nullable boundaries, autounboxing, reflection/framework injection, empty-collection semantics, and misuse of Optional in returns/fields/parameters; do not mechanically spread Optional across all models.
- `JAVA-GENERIC-001`: Check contract gaps caused by raw types, unchecked casts, heap pollution, generic arrays, wildcard bounds, and reflective type erasure.
- `JAVA-MUTABLE-001`: Check leakage of internal mutable collections, defensive copying, mutable fields in immutable objects, record members, and builder reuse.
- `JAVA-COR-001`: Check integer overflow, precision, time zones/locale, charset, regex, string parsing, and the unknown-value paths of switch/enum.
- `JAVA-API-001`: Check the binary/source/data compatibility of public APIs, records/DTOs, enums, serialized fields, and exception types.

## Exceptions and Resources

- `JAVA-ERROR-001`: Check overly broad catches, empty catches, lost cause on rethrow, checked/unchecked boundaries, exceptions overwritten by finally, and business failures returned as success.
- `JAVA-RESOURCE-001`: Check all paths of files, streams, JDBC, locks, executors, HTTP bodies, and temporary resources; prefer try-with-resources, and pay attention to suppressed exceptions.
- `JAVA-INTERRUPT-001`: After catching `InterruptedException`, the interrupt status should be restored or the task explicitly ended; do not silently swallow the cancellation signal.
- `JAVA-RETRY-001`: Check retry limits, backoff, exception filtering, idempotency, transactions, and duplicate external side effects.

## Concurrency and Modern Runtime

- `JAVA-JMM-001`: Check safe publication of shared mutable state, volatile/atomic/lock semantics, compound operations, and happens-before; thread-safe collections cannot automatically guarantee cross-operation atomicity.
- `JAVA-EXECUTOR-001`: Check thread-pool/queue limits, rejection policy, exception visibility, shutdown waiting, and task cancellation. Do not use the common pool without justification in library code.
- `JAVA-FUTURE-001`: Check the executor, exception chain, timeouts, cancellation, composition order, and blocking join/get of CompletableFuture; an async return cannot mask failure.
- `JAVA-LOCK-001`: Check lock ordering, IO while holding a lock, read-write lock upgrade, condition loops, and release after a failed resource acquisition.
- `JAVA-SYNC-001`: Check for overuse of `synchronized` (which atomic classes/concurrent collections/explicit locks from `java.util.concurrent` could replace) and whether lock granularity is too coarse; do not make pure style judgments, and require concurrency semantics or hotspot evidence.
- `JAVA-VTHREAD-001`: Only when the target JDK supports it, check virtual threads for unbounded external resources, synchronized/native pinning, ThreadLocal cost, and structured lifecycle; do not mechanically convert all executors to virtual threads.
- `JAVA-CONTEXT-001`: Check the propagation and cleanup of MDC, security context, transaction, and tenant information across thread pools, async callbacks, and virtual threads.

## Security and Serialization

- `JAVA-INJECT-001`: Trace input to SQL/JPQL, commands, templates, logs, LDAP, SpEL/expressions, and script engines, preferring parameterization and fixed mappings.
- `JAVA-SSRF-001`: Check URL scheme, redirects, DNS/IP, proxies, and cloud metadata access, and prove that untrusted input is reachable to a network sink.
- `JAVA-PATH-001`: Check path normalization, zip slip, upload filenames, temporary file permissions, and symlink boundaries.
- `JAVA-XML-001`: Check the XML parser's external entities, DOCTYPE, schema, and resource limits; combine the specific parser/JDK defaults to avoid version false positives.
- `JAVA-DESER-001`: Check native serialization, Jackson polymorphic typing, the allowed type ranges of XStream/Kryo, and gadget exposure; do not judge it insecure merely because Jackson is used.
- `JAVA-AUTH-001`: Verify endpoint/method/object-level authorization, tenant isolation, CSRF/CORS/session/token, and default-deny.
- `JAVA-DATA-001`: Logs, exceptions, traces, and serialization output must not leak tokens, personal data, connection strings, or full request bodies.

## Spring and Service Boundaries

- `SPRING-TX-001`: Check the proxy visibility, self-invocation, propagation, read-only semantics, rollback exceptions, async boundaries, and external side effects of `@Transactional`.
- `SPRING-PROXY-001`: Check whether proxy annotations such as `@Async`, `@Cacheable`, and `@Secured` are defeated by final/private/self-invocation or the object creation method.
- `SPRING-CONTRACT-001`: Check DTO/entity isolation, whether Bean Validation actually triggers, error responses, pagination, file uploads, idempotency keys, and API version compatibility.
- `SPRING-ERROR-001`: Check controller advice, status codes, exception mapping, sensitive details, and trace IDs; do not return all exceptions uniformly as 200.
- `SPRING-WEBFLUX-001`: Only in WebFlux/reactive paths, check blocking JDBC/IO, subscribe calls, backpressure, context, and error recovery; do not apply reactive rules to MVC projects.
- `SPRING-CONFIG-001`: Check profiles, property precedence, secrets, defaults, actuator exposure, and configuration compatibility during rolling upgrades.
- `SPRING-RESILIENCE-001`: Check timeouts, connection pools, retries, circuit breaking, bulkheads, and duplicate-consumption idempotency for HTTP/messaging calls.

## JPA/Hibernate and Data

- `JPA-IDENTITY-001`: Check entity equals/hashCode against persistence identity, proxies, lifecycle, and collection membership, avoiding semantic changes before and after ID assignment.
- `JPA-PERF-001`: Check N+1, lazy loading out of bounds, incorrect fetch joins, entity graphs, unpaginated queries, and queries triggered by serialization; corroborate with SQL/statistics or call paths.
- `JPA-TX-001`: Check transaction scope, flush timing, optimistic locking/version, pessimistic locking, isolation, and database constraints, avoiding read-then-write relying only on the application layer.
- `JPA-BATCH-001`: Check the batch configuration, flush/clear, memory growth, and partial failures of bulk writes; do not force batching on small data volumes.
- `JPA-CASCADE-001`: Check cascade, orphanRemoval, bidirectional relationship maintenance, and deletion scope to prevent unexpected cascades or orphaned data.
- `JPA-PAGE-001`: Check sort stability, offset/keyset selection, collection fetch join pagination, and count query cost.
- `JDBC-RESOURCE-001`: Check parameterized queries, statement/result set lifecycle, transaction commit/rollback, and connection pool leaks.

## Performance

- `JAVA-PERF-001`: Check hot-path boxing, repeated allocation, string concatenation inside loops (see `PERF-CONCAT-001`), regex compilation, reflection, and repeated serialization; input scale, profile, or benchmark evidence is required.
- `JAVA-STREAM-001`: Check stream reuse, side effects, short-circuiting, collector concurrency characteristics, and `parallelStream` common pool; do not make pure style judgments between plain loops and streams.
- `JAVA-CACHE-001`: Check cache keys, tenant/permission, expiration, maximum capacity, stampede, and failure caching; do not treat caching as a default optimization without measurement.
- `JAVA-COLLECTION-001`: Report collection initial capacity, implementation type, and concurrent structures only when scale or semantics are clear; do not mechanically require pre-allocation.

## Kotlin Interop

- `KOTLIN-NULL-001`: Check whether `!!`, platform types, nullable chains, and default values mask the Java nullable contract.
- `KOTLIN-COROUTINE-001`: Check coroutine scope, structured concurrency, cancellation propagation, blocking-call dispatchers, and Java future interop.
- `KOTLIN-STATE-001`: Check data classes, immutable collections, shared state, default parameters, and Java serialization/framework proxy compatibility.

## Build, Testing, and Verification

- `JVM-BUILD-001`: Check the Maven/Gradle wrapper, toolchain/release, dependency scope/configuration, BOM/convergence, plugin/annotation-processor versions, and reproducible builds; do not upgrade dependencies unrequested.
- `JAVA-TEST-001`: Check JUnit exception/async assertions, time and randomness, Mockito over-mocking, Spring slice boundaries, database cleanup, and whether concurrency tests genuinely fail.
- `JAVA-TEST-002`: For transaction, authorization, serialization, migration, and messaging issues, prefer integration/contract tests; use tools such as Testcontainers only when the project already has the dependency or the user authorizes it.

Prefer the repository wrapper and the Maven/Gradle test, compile/check, static-analysis, and format commands in CI; common tools include Error Prone, SpotBugs, PMD, Checkstyle, JaCoCo, and dependency auditing. Record the JDK, toolchain, profiles, modules, and test selection; when there is no version or configuration basis, do not apply specific Spring/JDK rules.
