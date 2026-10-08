#!/usr/bin/env python3
"""Detect a repository's languages, frameworks, manifests, and safe checks.

The script is read-only, uses only the Python standard library, skips symlinks,
and avoids reading secret files. It prints a JSON inventory to stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:  # pragma: no cover - Python < 3.11
    tomllib = None


SCHEMA_VERSION = 1
MAX_MANIFEST_BYTES = 2_000_000
EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".cache",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    "coverage",
    ".next",
    ".nuxt",
    ".terraform",
    "DerivedData",
    "Pods",
}

SECRET_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    "credentials",
    "credentials.json",
    "secrets.yml",
    "secrets.yaml",
    ".npmrc",
    ".pypirc",
}

EXTENSION_LANGUAGES = {
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".mts": "TypeScript",
    ".cts": "TypeScript",
    ".py": "Python",
    ".pyi": "Python",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".go": "Go",
    ".rs": "Rust",
    ".c": "C",
    ".h": "C/C++ Header",
    ".cc": "C++",
    ".cpp": "C++",
    ".cxx": "C++",
    ".hpp": "C++",
    ".hh": "C++",
    ".cs": "C#",
    ".fs": "F#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".m": "Objective-C",
    ".mm": "Objective-C++",
    ".dart": "Dart",
    ".sql": "SQL",
    ".graphql": "GraphQL",
    ".gql": "GraphQL",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".fish": "Shell",
    ".ps1": "PowerShell",
    ".psm1": "PowerShell",
    ".psd1": "PowerShell",
    ".tf": "Terraform",
    ".tfvars": "Terraform",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".proto": "Protocol Buffers",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",
    ".xml": "XML",
    ".scala": "Scala",
    ".sc": "Scala",
    ".sbt": "Scala",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".lua": "Lua",
    ".r": "R",
}

SPECIAL_LANGUAGES = {
    "dockerfile": "Dockerfile",
    "containerfile": "Dockerfile",
    "makefile": "Make",
    "cmakelists.txt": "CMake",
    "gemfile": "Ruby",
    "rakefile": "Ruby",
    "vagrantfile": "Ruby",
}

MANIFEST_NAMES = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
    "tsconfig.json",
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
    "requirements.txt",
    "pipfile",
    "poetry.lock",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "settings.gradle.kts",
    "go.mod",
    "go.work",
    "go.sum",
    "cargo.toml",
    "cargo.lock",
    "composer.json",
    "composer.lock",
    "gemfile",
    "gemfile.lock",
    "pubspec.yaml",
    "pubspec.lock",
    "package.swift",
    "build.sbt",
    "mix.exs",
    "mix.lock",
    "renv.lock",
    "cmakelists.txt",
    "makefile",
    "terraform.lock.hcl",
}

TEST_DIR_NAMES = {"test", "tests", "spec", "specs", "__tests__"}
TEST_FILE_RE = re.compile(r"(^test_|_test\.|\.test\.|\.spec\.|^spec_)", re.IGNORECASE)


def read_text(path: Path, limit: int = MAX_MANIFEST_BYTES) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except (OSError, UnicodeError):
        return ""


def is_secret_named_file(path: Path) -> bool:
    name = path.name.lower()
    return name in SECRET_FILE_NAMES or name.startswith(".env")


def read_json(path: Path) -> dict[str, Any]:
    text = read_text(path)
    if not text:
        return {}
    try:
        value = json.loads(text)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def detect_shebang(path: Path) -> str | None:
    if path.suffix or is_secret_named_file(path):
        return None
    try:
        with path.open("rb") as handle:
            first_line = handle.readline(256).decode("utf-8", errors="ignore").lower()
    except OSError:
        return None
    if not first_line.startswith("#!"):
        return None
    if "python" in first_line:
        return "Python"
    if any(shell in first_line for shell in ("bash", "zsh", "sh", "fish")):
        return "Shell"
    if "ruby" in first_line:
        return "Ruby"
    if "node" in first_line or "deno" in first_line or "bun" in first_line:
        return "JavaScript"
    if "pwsh" in first_line or "powershell" in first_line:
        return "PowerShell"
    return None


def classify_language(path: Path) -> str | None:
    lower_name = path.name.lower()
    if lower_name.startswith("dockerfile") or lower_name.startswith("containerfile"):
        return "Dockerfile"
    special = SPECIAL_LANGUAGES.get(lower_name)
    if special:
        return special
    language = EXTENSION_LANGUAGES.get(path.suffix.lower())
    return language or detect_shebang(path)


def is_test_file(relative: Path) -> bool:
    lower_parts = {part.lower() for part in relative.parts[:-1]}
    return bool(lower_parts & TEST_DIR_NAMES) or bool(TEST_FILE_RE.search(relative.name))


def is_ci_file(relative: Path) -> bool:
    normalized = "/".join(part.lower() for part in relative.parts)
    name = relative.name.lower()
    return (
        normalized.startswith(".github/workflows/")
        or name in {".gitlab-ci.yml", "azure-pipelines.yml", "jenkinsfile"}
        or "/.circleci/" in f"/{normalized}"
    )


def walk_repository(root: Path, max_files: int) -> tuple[list[Path], bool]:
    files: list[Path] = []
    truncated = False
    for current, dirs, names in os.walk(root, followlinks=False):
        current_path = Path(current)
        dirs[:] = sorted(
            directory
            for directory in dirs
            if directory not in EXCLUDED_DIRS
            and not (current_path / directory).is_symlink()
        )
        for name in sorted(names):
            path = current_path / name
            if path.is_symlink() or is_secret_named_file(path):
                continue
            files.append(path)
            if len(files) >= max_files:
                truncated = True
                return files, truncated
    return files, truncated


def add_framework(frameworks: set[str], dependency: str, ecosystem: str) -> None:
    normalized = dependency.lower()
    substring_rules = {
        "python": {
            "django": "Django",
            "fastapi": "FastAPI",
            "flask": "Flask",
            "sqlalchemy": "SQLAlchemy",
        },
        "jvm": {
            "spring-boot": "Spring Boot",
            "org.springframework": "Spring Framework",
            "spring-boot-starter-data-jpa": "JPA",
            "jakarta.persistence": "JPA",
            "javax.persistence": "JPA",
            "org.hibernate.orm": "Hibernate",
            "hibernate-core": "Hibernate",
            "hibernate-entitymanager": "Hibernate",
            "io.quarkus": "Quarkus",
            "io.micronaut": "Micronaut",
            "io.vertx": "Vert.x",
            "com.android.application": "Android",
            "com.android.library": "Android",
        },
        "php": {
            "laravel/framework": "Laravel",
            "symfony/framework-bundle": "Symfony",
        },
        "ruby": {"rails": "Rails"},
        "dart": {"flutter": "Flutter"},
    }
    javascript_rules = {
        "react-native": "React Native",
        "react": "React",
        "react-dom": "React",
        "next": "Next.js",
        "astro": "Astro",
        "vue": "Vue",
        "nuxt": "Nuxt",
        "svelte": "Svelte",
        "electron": "Electron",
        "express": "Express",
        "@nestjs/core": "NestJS",
        "fastify": "Fastify",
        "koa": "Koa",
        "hono": "Hono",
        "prisma": "Prisma",
        "@prisma/client": "Prisma",
        "typeorm": "TypeORM",
        "sequelize": "Sequelize",
        "mongoose": "Mongoose",
        "vitest": "Vitest",
        "@playwright/test": "Playwright",
    }
    if ecosystem == "javascript":
        label = javascript_rules.get(normalized)
        if label:
            frameworks.add(label)
        if normalized.startswith("@remix-run/"):
            frameworks.add("Remix")
        if normalized.startswith("@angular/"):
            frameworks.add("Angular")
        return
    for needle, label in substring_rules.get(ecosystem, {}).items():
        if needle in normalized:
            frameworks.add(label)


def inspect_manifests(root: Path, files: list[Path]) -> dict[str, Any]:
    frameworks: set[str] = set()
    manifests: list[str] = []
    runtime_hints: dict[str, str] = {}
    script_commands: list[dict[str, str]] = []
    file_by_name: dict[str, list[Path]] = {}

    for path in files:
        file_by_name.setdefault(path.name.lower(), []).append(path)
        lower_name = path.name.lower()
        if (
            lower_name in MANIFEST_NAMES
            or (lower_name.startswith("requirements") and lower_name.endswith(".txt"))
            or path.suffix.lower() in {".csproj", ".sln"}
        ):
            manifests.append(path.relative_to(root).as_posix())

    package_files = file_by_name.get("package.json", [])
    for package_file in package_files:
        data = read_json(package_file)
        dependencies: set[str] = set()
        for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            section = data.get(key, {})
            if isinstance(section, dict):
                dependencies.update(str(name) for name in section)
        for dependency in dependencies:
            add_framework(frameworks, dependency, "javascript")
        engines = data.get("engines", {})
        prefer_package = package_file.parent == root
        if (
            isinstance(engines, dict)
            and isinstance(engines.get("node"), str)
            and (prefer_package or "node" not in runtime_hints)
        ):
            runtime_hints["node"] = engines["node"]
        if isinstance(data.get("packageManager"), str) and (
            prefer_package or "package_manager" not in runtime_hints
        ):
            runtime_hints["package_manager"] = data["packageManager"]
        if data.get("type") in {"module", "commonjs"} and (
            prefer_package or "javascript_module" not in runtime_hints
        ):
            runtime_hints["javascript_module"] = str(data["type"])
        scripts = data.get("scripts", {})
        if isinstance(scripts, dict):
            base = package_file.parent
            manager = detect_package_manager(base, root)
            for name in (
                "lint",
                "lint:ci",
                "typecheck",
                "check:types",
                "check",
                "format:check",
                "test",
                "test:unit",
                "test:integration",
                "test:e2e",
                "build",
                "audit",
            ):
                if name in scripts:
                    script_commands.append(
                        {
                            "purpose": name,
                            "command": package_script_command(manager, name),
                            "source": package_file.relative_to(root).as_posix(),
                        }
                    )

    for path in files:
        name = path.name.lower()
        if name == "pyproject.toml":
            inspect_pyproject(path, frameworks, runtime_hints, script_commands, root)
        elif (name.startswith("requirements") and name.endswith(".txt")) or name == "pipfile":
            for line in read_text(path).splitlines():
                add_framework(frameworks, line.split("=", 1)[0].strip(), "python")
        elif name in {"pom.xml", "build.gradle", "build.gradle.kts"}:
            text = read_text(path)
            add_framework(frameworks, text, "jvm")
            java_version = detect_java_version(text)
            if java_version and "java" not in runtime_hints:
                runtime_hints["java"] = java_version
        elif name == "tsconfig.json" and path.parent == root:
            runtime_hints.update(detect_typescript_config(read_text(path)))
        elif name == "go.mod":
            match = re.search(r"^go\s+([0-9.]+)", read_text(path), re.MULTILINE)
            if match:
                runtime_hints["go"] = match.group(1)
        elif name == "cargo.toml":
            text = read_text(path)
            edition = re.search(r'^edition\s*=\s*["\']([^"\']+)', text, re.MULTILINE)
            rust_version = re.search(r'^rust-version\s*=\s*["\']([^"\']+)', text, re.MULTILINE)
            if edition:
                runtime_hints["rust_edition"] = edition.group(1)
            if rust_version:
                runtime_hints["rust_version"] = rust_version.group(1)
        elif path.suffix.lower() == ".csproj":
            text = read_text(path)
            target = re.search(r"<TargetFrameworks?>([^<]+)</TargetFrameworks?>", text)
            if target:
                runtime_hints["dotnet"] = target.group(1).strip()
            if "Microsoft.AspNetCore" in text:
                frameworks.add("ASP.NET Core")
            if "EntityFrameworkCore" in text:
                frameworks.add("Entity Framework Core")
        elif name == "composer.json":
            data = read_json(path)
            dependencies = data.get("require", {})
            if isinstance(dependencies, dict):
                for dependency in dependencies:
                    add_framework(frameworks, str(dependency), "php")
            scripts = data.get("scripts", {})
            if isinstance(scripts, dict):
                source = path.relative_to(root).as_posix()
                for script_name in ("lint", "analyse", "analyze", "test", "audit"):
                    if script_name in scripts:
                        script_commands.append(
                            {
                                "purpose": script_name,
                                "command": f"composer {script_name}",
                                "source": source,
                            }
                        )
        elif name == "gemfile":
            add_framework(frameworks, read_text(path), "ruby")
        elif name == "pubspec.yaml":
            add_framework(frameworks, read_text(path), "dart")

    return {
        "manifests": sorted(set(manifests)),
        "frameworks": sorted(frameworks),
        "runtime_hints": dict(sorted(runtime_hints.items())),
        "script_commands": deduplicate_commands(script_commands),
        "file_by_name": file_by_name,
    }


def inspect_pyproject(
    path: Path,
    frameworks: set[str],
    runtime_hints: dict[str, str],
    commands: list[dict[str, str]],
    root: Path,
) -> None:
    text = read_text(path)
    lowered = text.lower()
    for dependency in ("django", "fastapi", "flask", "sqlalchemy"):
        if dependency in lowered:
            add_framework(frameworks, dependency, "python")
    if tomllib is not None and text:
        try:
            data = tomllib.loads(text)
            project = data.get("project", {})
            if isinstance(project, dict) and isinstance(project.get("requires-python"), str):
                runtime_hints["python"] = project["requires-python"]
        except (ValueError, TypeError):
            pass
    source = path.relative_to(root).as_posix()
    tool_checks = {
        "[tool.ruff]": ("lint", "ruff check ."),
        "[tool.mypy]": ("typecheck", "mypy ."),
        "[tool.pyright]": ("typecheck", "pyright"),
        "[tool.pytest": ("test", "pytest"),
    }
    for marker, (purpose, command) in tool_checks.items():
        if marker in lowered:
            commands.append({"purpose": purpose, "command": command, "source": source})


def detect_java_version(text: str) -> str | None:
    patterns = (
        r"<maven\.compiler\.release>\s*([^<]+)\s*</maven\.compiler\.release>",
        r"<java\.version>\s*([^<]+)\s*</java\.version>",
        r"<maven\.compiler\.source>\s*([^<]+)\s*</maven\.compiler\.source>",
        r"JavaLanguageVersion\.of\(\s*([0-9]+)\s*\)",
        r"JavaVersion\.VERSION_([0-9_]+)",
        r"sourceCompatibility\s*=\s*['\"]?([0-9.]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            version = match.group(1).replace("_", ".").strip()
            if "$" not in version:
                return version
    return None


def strip_jsonc_comments(text: str) -> str:
    result: list[str] = []
    index = 0
    quote: str | None = None
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if quote:
            result.append(char)
            if char == "\\" and next_char:
                result.append(next_char)
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char in {'"', "'"}:
            quote = char
            result.append(char)
            index += 1
            continue
        if char == "/" and next_char == "/":
            result.extend("  ")
            index += 2
            while index < len(text) and text[index] not in "\r\n":
                result.append(" ")
                index += 1
            continue
        if char == "/" and next_char == "*":
            result.extend("  ")
            index += 2
            while index < len(text):
                if text[index] == "*" and index + 1 < len(text) and text[index + 1] == "/":
                    result.extend("  ")
                    index += 2
                    break
                result.append(text[index] if text[index] in "\r\n" else " ")
                index += 1
            continue
        result.append(char)
        index += 1
    return "".join(result)


def detect_typescript_config(text: str) -> dict[str, str]:
    hints: dict[str, str] = {}
    active_text = strip_jsonc_comments(text)
    fields = {
        "typescript_target": r'["\']target["\']\s*:\s*["\']([^"\']+)',
        "typescript_module": r'["\']module["\']\s*:\s*["\']([^"\']+)',
        "typescript_module_resolution": r'["\']moduleResolution["\']\s*:\s*["\']([^"\']+)',
        "typescript_strict": r'["\']strict["\']\s*:\s*(true|false)',
    }
    for key, pattern in fields.items():
        match = re.search(pattern, active_text, re.IGNORECASE)
        if match:
            hints[key] = match.group(1)
    return hints


def detect_package_manager(package_dir: Path, root: Path) -> str:
    candidates = (
        ("pnpm-lock.yaml", "pnpm"),
        ("yarn.lock", "yarn"),
        ("bun.lockb", "bun"),
        ("bun.lock", "bun"),
        ("package-lock.json", "npm"),
    )
    for base in (package_dir, root):
        for filename, manager in candidates:
            if (base / filename).exists():
                return manager
    return "npm"


def package_script_command(manager: str, name: str) -> str:
    if manager == "yarn":
        return f"yarn {name}"
    return f"{manager} run {name}"


def deduplicate_commands(commands: list[dict[str, str]]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for command in commands:
        key = (command["command"], command["source"])
        if key not in seen:
            seen.add(key)
            result.append(command)
    return sorted(result, key=lambda item: (item["purpose"], item["command"], item["source"]))


def ecosystem_commands(
    root: Path,
    file_by_name: dict[str, list[Path]],
    languages: Counter[str],
    frameworks: list[str],
) -> list[dict[str, str]]:
    commands: list[dict[str, str]] = []

    def add(purpose: str, command: str, source: str) -> None:
        commands.append({"purpose": purpose, "command": command, "source": source})

    if "go.mod" in file_by_name:
        add("test", "go test ./...", "go.mod")
        add("static-analysis", "go vet ./...", "go.mod")
    if "cargo.toml" in file_by_name:
        add("compile", "cargo check --workspace", "Cargo.toml")
        add("test", "cargo test --workspace", "Cargo.toml")
        add("static-analysis", "cargo clippy --workspace --all-targets", "Cargo.toml")
    if "pom.xml" in file_by_name:
        wrapper = ".\\mvnw.cmd" if (root / "mvnw.cmd").exists() else "mvn"
        add("test", f"{wrapper} test", "pom.xml")
        add("verification", f"{wrapper} verify", "pom.xml")
    if "build.gradle" in file_by_name or "build.gradle.kts" in file_by_name:
        wrapper = ".\\gradlew.bat" if (root / "gradlew.bat").exists() else "gradle"
        add("test", f"{wrapper} test", "Gradle build")
        add("verification", f"{wrapper} check", "Gradle build")
    if any(name.endswith(".csproj") for name in file_by_name) or any(name.endswith(".sln") for name in file_by_name):
        add("test", "dotnet test", ".NET project")
    if "gemfile" in file_by_name:
        gemfile_text = read_text(file_by_name["gemfile"][0]).lower()
        if "rspec" in gemfile_text:
            add("test", "bundle exec rspec", "Gemfile")
        elif "minitest" in gemfile_text:
            add("test", "bundle exec rake test", "Gemfile")
    if "pubspec.yaml" in file_by_name:
        command = "flutter test" if "Flutter" in frameworks else "dart test"
        add("test", command, "pubspec.yaml")
    if "package.swift" in file_by_name:
        add("test", "swift test", "Package.swift")
    if "build.sbt" in file_by_name:
        add("test", "sbt test", "build.sbt")
    if "mix.exs" in file_by_name:
        add("test", "mix test", "mix.exs")
    if "Terraform" in languages:
        add("format", "terraform fmt -check -recursive", "*.tf")
        add("validate", "terraform validate", "*.tf (may require initialized providers)")
    return deduplicate_commands(commands)


def build_inventory(root: Path, max_files: int) -> dict[str, Any]:
    files, truncated = walk_repository(root, max_files)
    languages: Counter[str] = Counter()
    tests: list[str] = []
    ci_files: list[str] = []

    for path in files:
        relative = path.relative_to(root)
        language = classify_language(path)
        if language:
            languages[language] += 1
        if is_test_file(relative):
            tests.append(relative.as_posix())
        if is_ci_file(relative):
            ci_files.append(relative.as_posix())

    manifest_data = inspect_manifests(root, files)
    commands = manifest_data["script_commands"] + ecosystem_commands(
        root,
        manifest_data["file_by_name"],
        languages,
        manifest_data["frameworks"],
    )
    commands = deduplicate_commands(commands)

    return {
        "schema_version": SCHEMA_VERSION,
        "root": str(root),
        "scanned_files": len(files),
        "truncated": truncated,
        "languages": [
            {"name": name, "files": count}
            for name, count in sorted(languages.items(), key=lambda item: (-item[1], item[0]))
        ],
        "manifests": manifest_data["manifests"],
        "frameworks": manifest_data["frameworks"],
        "runtime_hints": manifest_data["runtime_hints"],
        "tests": {"count": len(tests), "samples": sorted(tests)[:20]},
        "ci_files": sorted(ci_files),
        "command_candidates": commands,
        "notes": [
            "Command candidates are not executed by this script.",
            "Generated, vendor, cache, secret-named files, and symlinks are skipped by default.",
        ],
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root (default: current directory)")
    parser.add_argument("--max-files", type=int, default=50_000, help="Stop after this many files")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    if args.max_files < 1:
        print("error: --max-files must be positive", file=sys.stderr)
        return 2
    inventory = build_inventory(root, args.max_files)
    if args.compact:
        print(json.dumps(inventory, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(inventory, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
