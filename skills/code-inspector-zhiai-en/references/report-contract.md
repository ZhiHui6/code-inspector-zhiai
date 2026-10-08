# Report Contract

## Contents

- [Report Structure](#report-structure)
- [Finding Fields](#finding-fields)
- [Fix Output](#fix-output)
- [Verification Record](#verification-record)
- [Optional Scoring](#optional-scoring)

## Report Structure

Output an English Markdown report in the following order:

1. **Scope and assumptions**: target, mode, language/version, framework, file statistics, exclusions.
2. **Executive summary**: P0-P3 counts, highest risk, main uncovered items, and overall recommendations.
3. **Verification status**: commands run, exit codes, key results; commands not run and the reasons.
4. **Issue list**: sorted by severity, then by file location.
5. **Specialized coverage**: which rule packs were loaded, which are inapplicable, which languages/tools were unrecognized.
6. **Remediation order**: minimal fix, regression tests, follow-up refactoring, and optional optimization.

## Finding Fields

Each finding uses a globally incrementing `ISSUE-001` number and fills in:

```text
ISSUE-001: short title
- rule_id: SEC-TAINT-001
- severity: P0 | P1 | P2 | P3
- confidence: high | medium | low
- location: absolute-or-repository-relative/path:line[:symbol]
- evidence: the minimal necessary code fact or redacted fragment
- impact: observable consequences, affected boundaries, and trigger conditions
- recommendation: the minimal viable fix direction
- verification: test, static check, or manual review steps
```

When one pattern appears in multiple locations it may be consolidated, but all affected locations must be listed or the representative scope made explicit. Do not write only unverifiable conclusions such as "code quality is poor" or "potential issues exist".

## Fix Output

Review and Audit do not output fully rewritten files. When the user explicitly enters Fix mode:

- Use a GitHub unified diff or an actual file patch, preserving unrelated user changes.
- Modify only the authorized scope; do not opportunistically format the whole repository, update lock files, or upgrade dependencies.
- Associate modified locations with diff context and `ISSUE-xxx`; do not hard-code comments into production code.
- Behavior changes must include test changes; when testing is impossible, explain the reason and the remaining risk.
- After fixing, re-run the minimal relevant commands and report failures or skips.

## Verification Record

Record the command, working directory, tool version (when available), exit code, and result summary. When a command was not run due to missing dependencies, timeout, permissions, network, or environmental uncertainty, state the reason and do not claim "passed".

## Optional Scoring

By default, do not output a composite A-F score, to avoid mixing inapplicable dimensions and style issues into the release judgment. Score only when the user explicitly requests it:

1. Compute only over the actually applicable core dimensions, each starting at 100.
2. Use fixed deductions (P0/P1/P2/P3 = 30/15/5/1); the same root cause is deducted only once within the same dimension.
3. The score floor is 0; the composite score is the weighted average of applicable dimensions, with the weights and deduction table disclosed.
4. P0/P1 still stand alone as the release gate and cannot be offset by a high score.
