#!/usr/bin/env python3
"""Check the Lab 01-only Project Development Practicum student release."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LAB = ROOT / "lab_01"
TEXT_SUFFIXES = {".md", ".py", ".json", ".txt"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def check_inventory(problems: list[str]) -> None:
    inventory = LAB / "data" / "checksums.sha256"
    lab_source = LAB / "lab.py"
    if not inventory.is_file() or not lab_source.is_file():
        problems.append("Lab 01 integrity files are missing")
        return
    match = re.search(
        r'EXPECTED_INVENTORY_SHA256\s*=\s*"([0-9a-f]{64})"',
        lab_source.read_text(encoding="utf-8"),
    )
    if match is None or match.group(1) != digest(inventory):
        problems.append("lab_01: checksum inventory identity does not match lab.py")
    for number, line in enumerate(inventory.read_text(encoding="utf-8").splitlines(), start=1):
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or re.fullmatch(r"[0-9a-f]{64}", parts[0]) is None:
            problems.append(f"lab_01: invalid checksum line {number}")
            continue
        target = LAB / "data" / parts[1].strip()
        if not target.is_file() or digest(target) != parts[0]:
            problems.append(f"lab_01: missing or changed protected file data/{parts[1].strip()}")


def check_release_boundary(problems: list[str]) -> None:
    for number in range(2, 13):
        if (ROOT / f"lab_{number:02d}").exists():
            problems.append(f"unreleased lab_{number:02d} is present")
    for name in ("course_data", "DATASET_PROVENANCE.md", "orientation"):
        if (ROOT / name).exists():
            problems.append(f"future or delivery-only material is present: {name}")


def check_source(problems: list[str]) -> None:
    required = (
        ROOT / ".gitattributes",
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "course_integrity.py",
        ROOT / "handoff_check.py",
        LAB / "README.md",
        LAB / "lab.py",
        LAB / "project_brief.md",
        LAB / "requirements.txt",
        LAB / "data" / "README.md",
        LAB / "data" / "project_facts.json",
        LAB / "data" / "checksums.sha256",
    )
    for path in required:
        if not path.is_file():
            problems.append(f"missing {path.relative_to(ROOT)}")

    root_outputs = ROOT / "outputs"
    if root_outputs.exists():
        problems.append("unexpected outputs directory at the repository root")
    lab_outputs = LAB / "outputs"
    if lab_outputs.exists() and not lab_outputs.is_dir():
        problems.append("lab_01/outputs exists but is not a directory")
    elif lab_outputs.is_dir():
        allowed_outputs = {"lab_start_check.json", "project_brief_check.json"}
        unexpected = [
            path.name
            for path in lab_outputs.iterdir()
            if path.name not in allowed_outputs or not path.is_file()
        ]
        if unexpected:
            problems.append("lab_01/outputs contains an unexpected entry")

    local_patterns = (
        re.compile(r"/home/", re.IGNORECASE),
        re.compile(r"/Users/", re.IGNORECASE),
        re.compile(r"[A-Za-z]:\\"),
    )
    source_paths = (
        ROOT / "README.md",
        ROOT / "course_integrity.py",
        ROOT / "handoff_check.py",
        *LAB.rglob("*"),
    )
    for path in source_paths:
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".md" and text.count("```") % 2:
            problems.append(f"unbalanced Markdown fence: {path.relative_to(ROOT)}")
        if path.suffix.lower() != ".py" and any(pattern.search(text) for pattern in local_patterns):
            relative = path.relative_to(ROOT)
            problems.append(f"machine-specific path or internal folder name: {relative}")
        if path.suffix.lower() == ".py":
            try:
                compile(text, str(path), "exec")
            except SyntaxError as error:
                problems.append(f"Python syntax error in {path.relative_to(ROOT)}:{error.lineno}")
        elif path.suffix.lower() == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as error:
                problems.append(f"invalid JSON in {path.relative_to(ROOT)}:{error.lineno}")


def check_lab01_contract(problems: list[str]) -> None:
    try:
        facts = json.loads((LAB / "data" / "project_facts.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    expected_fact_keys = {
        "project",
        "dataset_page",
        "license",
        "input",
        "labels",
        "notumor_images",
        "result",
        "full_dataset_needed_from",
        "use",
    }
    if set(facts) != expected_fact_keys:
        problems.append("Lab 01 protected facts have an unexpected structure")

    brief_path = LAB / "project_brief.md"
    if not brief_path.is_file():
        return
    brief = brief_path.read_text(encoding="utf-8")
    required_fields = (
        "TEAM-NAME:",
        "MEMBER-LABELS:",
        "TEAM-WORK:",
        "SYSTEM-DOES:",
        "SYSTEM-DOES-NOT:",
        "REVIEWER:",
        "RISK:",
        "RESPONSE:",
        "TESTABLE-BEHAVIOUR:",
        "INITIAL-CONTRIBUTIONS:",
    )
    missing = [field for field in required_fields if field not in brief]
    if missing:
        problems.append("Lab 01 starter is missing fields: " + ", ".join(missing))


def main() -> int:
    problems: list[str] = []
    if sys.version_info[:2] != (3, 12):
        actual = f"{sys.version_info.major}.{sys.version_info.minor}"
        problems.append(f"Python 3.12 is required; this command used Python {actual}")
    check_release_boundary(problems)
    check_source(problems)
    check_inventory(problems)
    check_lab01_contract(problems)
    if problems:
        print("PDP_LAB01_HANDOFF_BLOCKED")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("PDP_LAB01_HANDOFF_READY scope=lab01 future_labs=not_in_release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
