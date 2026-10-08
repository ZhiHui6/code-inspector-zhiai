# Style, Readability, and Structural Heuristics

## Contents

- [Scope and Gating](#scope-and-gating)
- [Formatting and Style](#formatting-and-style)
- [Readability](#readability)
- [Structural Heuristic Thresholds](#structural-heuristic-thresholds)
- [Verification](#verification)

## Scope and Gating

This rule pack is **not loaded by default**, to preserve code-inspector's evidence-first, low-noise default behavior. Enable it only when the following conditions hold:

1. The user explicitly requests format checking, code style, readability, or naming conventions, or explicitly requests a "code health check that includes the style dimension".
2. The report needs to align with checklist-style tools (A–F rating per dimension), and the user explicitly requests coverage of the formatting and readability dimensions.

Do not load this pack on your own merely because a project "looks like it has no style tooling". When a project already configures tools such as Prettier/ESLint/Black/Ruff/clang-format/Checkstyle/Spotless, **the tool output prevails**; this pack serves only as supplementary explanation, does not override the tool's conclusions, and does not block a release over style issues. Style issues default to `P3`, and structural readability issues default to `P2`; escalate the severity only when the user explicitly includes style in the gate.

## Formatting and Style

- `STYLE-NAMING-001`: Check whether naming conforms to language/project conventions (camelCase / snake_case / PascalCase) and stays consistent; when it conflicts with existing code, the project prevails.
- `STYLE-INDENT-001`: Check whether indentation is uniform (Tab / 2 spaces / 4 spaces), whether brace style is consistent (K&R / Allman), and whether blank-line grouping is reasonable.
- `STYLE-LINEWIDTH-001`: Check whether line width exceeds the project convention (refer to ≤120 characters when there is none) or clearly hurts readability.
- `STYLE-WHITESPACE-001`: Check operator/comma spacing consistency, trailing whitespace, and the final newline at end of file.
- `STYLE-IMPORT-001`: Check whether import/use statements are grouped and ordered (standard library → third-party → local), and whether any are out of order or ungrouped.
- `STYLE-CONST-001`: Check mutability declaration preferences (e.g. JS `const` > `let` > `var`, Java `final`, C++ `const`, Go zero-value use); report only when the project has no tool constraint, and on the JS side `JS-MODERN-001` references this number.

## Readability

- `READ-MAGIC-001`: Check whether magic numbers/strings should be extracted into named constants; explain the semantic benefit of extraction, and do not report pure configuration constants.
- `READ-NAMING-001`: Check whether variable/function/type names accurately express intent (avoid `data`/`info`/`tmp`/`handle2`), and whether booleans use the `is/has/can/should` prefix.
- `READ-COMMENT-001`: Check whether complex logic lacks a "why" comment and whether public APIs lack JSDoc/docstring; do not require comments on self-evident code.
- `READ-GUARD-001`: Check whether deeply nested conditions can be simplified with guard clauses (early return/continue).
- `READ-TERNARY-001`: Check whether nested ternary expressions or complex logical operators hurt readability.
- `READ-DEBUG-001`: Check for leftover commented-out code blocks, temporary debug output (`console.log`/`print`/`fmt.Println`), and stale TODOs; this echoes `MAINT-DEAD-001`, with the emphasis here on readability presentation.

## Structural Heuristic Thresholds

The following thresholds are **reference signals** used to locate places that "may need splitting or simplification"; they must **not be used for mechanical deduction**; whether to report depends on cognitive load and change risk (consistent with `MAINT-COMPLEXITY-001`). When citing a threshold in a report, you must also state the actual size and the benefit of splitting.

- `STRUCT-FUNC-001`: Function length reference ≤50 lines; when exceeded, explain whether it is genuinely hard to understand, test, or reuse.
- `STRUCT-FILE-001`: Single file reference ≤300 lines; when exceeded, check whether multiple responsibilities are mixed together.
- `STRUCT-COMPLEXITY-001`: Cyclomatic complexity reference ≤10; when exceeded, locate the specific source of branching and give a split point.
- `STRUCT-NEST-001`: Nesting depth reference ≤4 levels; when exceeded, prefer guard clauses or extracting a function.
- `STRUCT-PARAM-001`: Parameter count reference ≤4; when exceeded, consider an object parameter or configuration object, and confirm caller compatibility; this number is the primary number for "too many parameters".
- `STRUCT-GOD-001`: Identify God Class / God Function (overloaded responsibilities, too many methods, overly broad state coupling).

## Verification

Prefer running the project's existing formatter/linter (Prettier, ESLint, Black/Ruff, gofmt, clang-format, Checkstyle/Spotless, etc.) and let its results prevail. When no corresponding tool exists, manually verify the items above and note in the report "manual baseline based on the project having no style tooling", to avoid presenting a manual preference as a hard defect.
