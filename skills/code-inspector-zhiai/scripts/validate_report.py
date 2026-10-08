#!/usr/bin/env python3
"""Validate Code Inspector Markdown finding records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


HEADING_RE = re.compile(
    r"^(?:#{2,6}\s+|\*\*)?(ISSUE-(\d{3,}))(?:\*\*)?\s*[:：-]?\s*(.*)$",
    re.IGNORECASE,
)
FIELD_RE = re.compile(
    r"^\s*[-*]\s*`?(rule_id|severity|confidence|location|evidence|impact|recommendation|verification)`?\s*[:：]\s*(.*)$",
    re.IGNORECASE,
)
REQUIRED_FIELDS = {
    "rule_id",
    "severity",
    "confidence",
    "location",
    "evidence",
    "impact",
    "recommendation",
    "verification",
}
VALID_SEVERITIES = {"P0", "P1", "P2", "P3"}
VALID_CONFIDENCE = {"high", "medium", "low"}
PLACEHOLDER_RE = re.compile(r"^(?:tbd|todo|n/?a|unknown|待补充|未知|\{.*\})$", re.IGNORECASE)
NO_FINDINGS_RE = re.compile(r"(?:未发现.*(?:问题|缺陷)|no\s+(?:actionable\s+)?findings)", re.IGNORECASE)
SECRET_PATTERNS = {
    "OpenAI-style API key": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key material": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def split_findings(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line_number, line in enumerate(text.splitlines(), start=1):
        heading = HEADING_RE.match(line.strip())
        if heading:
            current = {
                "id": heading.group(1).upper(),
                "number": int(heading.group(2)),
                "title": heading.group(3).strip(),
                "heading_line": line_number,
                "fields": {},
            }
            findings.append(current)
            continue
        if current is None:
            continue
        field = FIELD_RE.match(line)
        if field:
            current["fields"][field.group(1).lower()] = field.group(2).strip()
    return findings


def normalize_inline_code(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`") and value.count("`") == 2:
        return value[1:-1].strip()
    return value


def validate_finding(finding: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    issue_id = finding["id"]
    fields = finding["fields"]
    missing = sorted(REQUIRED_FIELDS - set(fields))
    if missing:
        errors.append(f"{issue_id}: missing fields: {', '.join(missing)}")
    if not finding["title"]:
        errors.append(f"{issue_id}: missing title")
    severity = normalize_inline_code(fields.get("severity", "")).upper()
    if "severity" in fields and severity not in VALID_SEVERITIES:
        errors.append(f"{issue_id}: invalid severity: {fields['severity']}")
    confidence = normalize_inline_code(fields.get("confidence", "")).lower()
    if "confidence" in fields and confidence not in VALID_CONFIDENCE:
        errors.append(f"{issue_id}: invalid confidence: {fields['confidence']}")
    location = fields.get("location", "")
    if location and not re.search(r":\d+(?::[A-Za-z_][A-Za-z0-9_.-]*)?", location):
        errors.append(f"{issue_id}: location must include :line or :line:symbol")
    rule_id = normalize_inline_code(fields.get("rule_id", ""))
    if rule_id and not re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+", rule_id):
        errors.append(f"{issue_id}: invalid rule_id: {rule_id}")
    for field_name, raw_value in fields.items():
        value = normalize_inline_code(raw_value)
        if not value or PLACEHOLDER_RE.fullmatch(value):
            errors.append(f"{issue_id}: field {field_name} is empty or a placeholder")
    return errors


def validate_report(text: str, allow_no_findings: bool) -> dict[str, Any]:
    findings = split_findings(text)
    errors: list[str] = []
    warnings: list[str] = []

    if not findings:
        if not allow_no_findings and not NO_FINDINGS_RE.search(text):
            errors.append("no findings found; state that no actionable findings were found or use --allow-no-findings")
    else:
        ids = [finding["id"] for finding in findings]
        if len(ids) != len(set(ids)):
            errors.append("finding IDs are not unique")
        numbers = [finding["number"] for finding in findings]
        expected = list(range(1, len(findings) + 1))
        if numbers != expected:
            errors.append(f"finding IDs must be sequential from ISSUE-001; got {numbers}")
        for finding in findings:
            errors.extend(validate_finding(finding))

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"report may expose {label}; redact the value")

    if "confidence" not in text.lower() and findings:
        warnings.append("report has findings but no confidence field text")

    return {
        "valid": not errors,
        "finding_count": len(findings),
        "errors": errors,
        "warnings": warnings,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="Markdown report path")
    parser.add_argument("--allow-no-findings", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    path = Path(args.report).expanduser().resolve()
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        print(f"error: cannot read report: {exc}", file=sys.stderr)
        return 2

    result = validate_report(text, args.allow_no_findings)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "valid" if result["valid"] else "invalid"
        print(f"{status}: {result['finding_count']} finding(s)")
        for error in result["errors"]:
            print(f"error: {error}")
        for warning in result["warnings"]:
            print(f"warning: {warning}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
