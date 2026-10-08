# Data, API, Script, Configuration, and Infrastructure Rules

## Contents

- [SQL and Migrations](#sql-and-migrations)
- [GraphQL and OpenAPI](#graphql-and-openapi)
- [HTML/CSS and Web Markup](#htmlcss-and-web-markup)
- [Schema and Serialization](#schema-and-serialization)
- [Shell and PowerShell](#shell-and-powershell)
- [Configuration Files](#configuration-files)
- [Docker](#docker)
- [Kubernetes and Helm](#kubernetes-and-helm)
- [Terraform](#terraform)
- [CI/CD](#cicd)
- [Verification](#verification)

## SQL and Migrations

- `SQL-SEC-001`: Confirm that application input uses parameterized queries and that dynamic identifiers use an allowlist; if only string concatenation is visible, keep tracing the input source.
- `SQL-COR-001`: Check NULL, time zone, precision, sort stability, duplicate rows, and JOIN cardinality semantics.
- `SQL-TX-001`: Check transaction isolation, lock ordering, partial commits, retries, and external side effects.
- `SQL-PERF-001`: Use execution plans, indexes, row estimates, and real access patterns to judge full table scans, N+1, inefficient pagination, and duplicate aggregation.
- `SQL-MIG-001`: Check migration reversibility, table locks, long transactions, non-null column defaults, online index creation, backfill, and compatibility across multiple application versions.
- `SQL-DATA-001`: Prefer relying on database constraints to maintain uniqueness, foreign keys, and range invariants; check whether application validation conflicts with database constraints.

Do not assert that a given syntax or index strategy is available under an unknown database dialect and version.

## GraphQL and OpenAPI

- `OPENAPI-SCHEMA-001`: Check the compatibility of deleted/renamed fields, newly required fields, enum expansion, defaults, and error responses.
- `GRAPHQL-SEC-001`: Check field-level authorization, depth/complexity limits, batched queries, and introspection exposure policy.
- `GRAPHQL-PERF-001`: Check resolver N+1, DataLoader lifecycle, cache keys, and pagination.
- `OPENAPI-CONTRACT-001`: Verify that the implementation matches the schema for status codes, content type, nullable, format, pagination, and error model.
- `API-GEN-001`: Generated client/server code is usually read-only; prefer fixing the schema or the generation configuration.

## HTML/CSS and Web Markup

- `WEB-SEC-001`: Check output encoding, dangerous URL schemes, inline scripts, CSP/security headers, and template context; do not misjudge static copy as injection.
- `WEB-ACCESS-001`: Check semantic elements, form labels, keyboard focus, error messaging, contrast, and dynamic content announcements.
- `WEB-CSS-001`: Check layout overflow, breakpoints, stacking contexts, selector conflicts, and `prefers-reduced-motion`; visual suggestions must have an observable interaction or usability impact.
- `WEB-COMPAT-001`: Check browser APIs, polyfills, SSR hydration, and fallback paths for resource loading failures.

## Schema and Serialization

- `SCHEMA-COMPAT-001`: Changes to protobuf/Avro/JSON Schema etc. must not reuse published field numbers or break unknown-field handling.
- `SCHEMA-VALIDATION-001`: Check whether schema validation is actually applied at the trust boundary, and whether errors are returned stably without leaking internal information.

## Shell and PowerShell

- `SHELL-QUOTE-001`: Check variable references, array arguments, paths with spaces, globbing, and command substitution to avoid argument injection and word splitting.
- `SHELL-ERROR-001`: Check exit codes, pipeline errors, trap/finally, temporary file cleanup, and partial success. Do not mechanically add `set -e`; first confirm the script's control flow.
- `SHELL-SECRET-001`: Do not expose credentials in arguments, logs, the process list, or debug output.
- `SHELL-PATH-001`: Use resolved, explicit paths for delete, move, and recursive operations; check symlink, root directory, and empty variable risks.
- `PS-ERROR-001`: Check PowerShell terminating/non-terminating errors, `-LiteralPath`, `$ErrorActionPreference`, and external command exit codes.

## Configuration Files

- `CONFIG-SECRET-001`: Identify hardcoded secrets, default passwords, and sensitive logs, but the values must be redacted.
- `CONFIG-DEFAULT-001`: Check missing keys, types, environment overrides, feature flag defaults, and development/production differences.
- `CONFIG-SCHEMA-001`: Validate YAML/JSON/TOML with a schema or official tool; watch for YAML implicit types, anchors, and duplicate keys.
- `CONFIG-COMPAT-001`: Check compatibility between old and new versions during configuration renames, deprecations, and rolling upgrades.

## Docker

- `DOCKER-BASE-001`: Check base image provenance, immutable tag/digest, support lifecycle, and build context.
- `DOCKER-SEC-001`: Check non-root user, capabilities, secret mounts, sensitive layers, file permissions, and network exposure.
- `DOCKER-SIZE-001`: Check multi-stage builds, cache ordering, and unnecessary files; image size optimization must not sacrifice reproducibility.
- `DOCKER-RUNTIME-001`: Check entrypoint signals, health checks, read-only filesystem, resource/temp directories, and shutdown.

## Kubernetes and Helm

- `K8S-SEC-001`: Check service account, RBAC, privileged, hostPath, capability, secret, and network policy.
- `K8S-REL-001`: Check readiness/liveness/startup probes, rollout strategy, PDB, resource requests/limits, and graceful shutdown.
- `K8S-CONFIG-001`: Check selector/label, namespace, service port, configuration mounts, and Helm values defaults.
- `K8S-DATA-001`: Check persistent volumes, StatefulSet identity, backups, and irreversible changes.

## Terraform

- `TF-STATE-001`: Check state backend, locking, sensitive outputs, and resource import/move plans.
- `TF-SEC-001`: Check public networks, overly broad IAM, unencrypted storage, secret variables, and provider credentials.
- `TF-LIFE-001`: Check `prevent_destroy`, replace, dependencies, drift, and the destruction risk of production resources.
- `TF-VERSION-001`: Pin compatible Terraform/provider/module versions and retain the lock file; do not upgrade without a request.

## CI/CD

- `CI-SEC-001`: Check third-party action/image pinning, pull request secret boundaries, script injection, and least token privilege.
- `CI-COR-001`: Check cache keys, matrix coverage, conditional expressions, failure propagation, and artifact provenance.
- `CI-DEPLOY-001`: Check environment approvals, concurrent deployments, rollback, immutable artifacts, and production variable isolation.

## Verification

Prefer database explain/migration dry-run, schema validators, ShellCheck/PSScriptAnalyzer, Docker/Compose checks, Kubernetes/Helm dry-run, Terraform fmt/validate/plan, and official CI validation. Any plan, migration, or cluster command must be confirmed not to write to remote or production state.
