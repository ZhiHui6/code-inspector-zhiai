# Python Rules

## Contents

- [Scope](#scope)
- [Language Rules](#language-rules)
- [Web and Data Frameworks](#web-and-data-frameworks)
- [Verification](#verification)

## Scope

Load conditions include `.py`, `pyproject.toml`, `setup.cfg`, `requirements*.txt`, `Pipfile`, or `poetry.lock`. Read the Python version, async usage, type-checking configuration, and test entry points.

## Language Rules

- `PY-COR-001`: Check mutable default arguments, shallow/deep copies, one-shot iterator consumption, time zones, and mixing `Decimal`/floats. Only report a mutable default when the argument or state is genuinely shared across calls.
- `PY-REL-001`: Check `except:`/overly broad exceptions, empty `except`, lost exception context, and mixing in error return values. Intentional catches in tests must be judged together with the assertions.
- `PY-RESOURCE-001`: Files, locks, connections, temporary directories, and generator resources should use a context manager or an equivalent `finally` lifecycle.
- `PY-SEC-001`: Check `eval`/`exec`, untrusted `pickle`/yaml, `subprocess` shell concatenation, and path and SQL interpolation; state the input source and sink.
- `PY-TYPE-001`: Check `Any` spread, unannotated public boundaries, `cast` misuse, and missing runtime validation. Data-parsing boundaries may use `TypedDict`, dataclasses, or validation libraries, but do not rewrite internal code just for annotations.
- `PY-ASYNC-001`: In async functions, look for blocking IO, synchronous locks, un-awaited coroutines, and task leaks; confirm the event loop lifecycle.
- `PY-GIL-001`: Check CPU-bound tasks mistakenly using threads (limited by the GIL) where multiprocessing or native extensions are needed, and blocking calls mixed into async; report only when a concurrency scenario genuinely exists.
- `PY-PERF-001`: Check queries/HTTP inside loops, reading large files in full, repeated regex compilation, and unnecessary object copies; list comprehensions are not uniformly better than `map`/generators.
- `PY-COMPREHENSION-001`: Check whether the choice between list comprehensions/generators and `map`/`filter` affects readability or peak memory; list comprehensions are not an unconditional defect, and neither form is uniformly better or worse.
- `PY-PACKAGE-001`: Check dependency ranges, import side effects, external operations performed at startup, and configuration defaults.
- `PY-STYLE-001`: Check modern idioms (`f-string`, `dataclasses`, `@property`) and consistency with type annotations; f-strings and formatting style must not be treated as unconditional defects, and only when the user explicitly requests a style dimension should you give a preference hint under gating.

## Web and Data Frameworks

- `DJANGO-SEC-001`: Check CSRF, object-level authorization, template auto-escaping, ORM parameterization, file uploads, and admin exposure.
- `DJANGO-PERF-001`: Check queryset N+1, unpaginated lists, transaction scope, and signal side effects.
- `FASTAPI-CONTRACT-001`: Check Pydantic input/output models, authentication dependencies, exception responses, and async/sync route boundaries.
- `DATA-RESOURCE-001`: Check database cursors, connection pools, transactions, bulk writes, and pandas/NumPy peak memory.

## Verification

Prefer running the project's existing pytest, ruff/flake8, mypy/pyright, bandit, or build commands. Do not treat f-strings, list comprehensions, or any particular formatting style as unconditional defects.
