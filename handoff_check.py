#!/usr/bin/env python3
"""Check the Labs 01–02 Project Development Practicum student release."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LAB01 = ROOT / "lab_01"
LAB02 = ROOT / "lab_02"
TEXT_SUFFIXES = {".md", ".py", ".json", ".txt"}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def check_inventory(lab: Path, problems: list[str]) -> None:
    inventory = lab / "data" / "checksums.sha256"
    lab_source = lab / "lab.py"
    label = lab.name
    if not inventory.is_file() or not lab_source.is_file():
        problems.append(f"{label}: integrity files are missing")
        return
    match = re.search(
        r'EXPECTED_INVENTORY_SHA256\s*=\s*"([0-9a-f]{64})"',
        lab_source.read_text(encoding="utf-8"),
    )
    if match is None or match.group(1) != digest(inventory):
        problems.append(f"{label}: checksum inventory does not match lab.py")
    for number, line in enumerate(
        inventory.read_text(encoding="utf-8").splitlines(), start=1
    ):
        parts = line.split(maxsplit=1)
        if len(parts) != 2 or re.fullmatch(r"[0-9a-f]{64}", parts[0]) is None:
            problems.append(f"{label}: invalid checksum line {number}")
            continue
        target = lab / "data" / parts[1].strip()
        if not target.is_file() or digest(target) != parts[0]:
            relative = parts[1].strip()
            problems.append(f"{label}: missing or changed protected file data/{relative}")


def check_release_boundary(problems: list[str]) -> None:
    for number in range(3, 13):
        path = ROOT / f"lab_{number:02d}"
        if path.exists():
            problems.append(f"unreleased {path.name} is present")
    for name in ("course_data", "DATASET_PROVENANCE.md", "orientation"):
        if (ROOT / name).exists():
            problems.append(f"future or instructor-only material is present: {name}")
    for path in ROOT.glob("lab_*/.gitignore"):
        problems.append(f"duplicate nested ignore file is present: {path.relative_to(ROOT)}")


def required_files() -> tuple[Path, ...]:
    return (
        ROOT / ".gitattributes",
        ROOT / ".gitignore",
        ROOT / "README.md",
        ROOT / "course_integrity.py",
        ROOT / "handoff_check.py",
        LAB01 / "README.md",
        LAB01 / "lab.py",
        LAB01 / "project_brief.md",
        LAB01 / "requirements.txt",
        LAB01 / "data" / "README.md",
        LAB01 / "data" / "project_facts.json",
        LAB01 / "data" / "checksums.sha256",
        LAB02 / "README.md",
        LAB02 / "lab.py",
        LAB02 / "architecture_brief.md",
        LAB02 / "requirements.txt",
        LAB02 / "data" / "README.md",
        LAB02 / "data" / "architecture_requirements.json",
        LAB02 / "data" / "checksums.sha256",
    )


def check_output_directory(
    lab: Path, allowed_names: set[str], problems: list[str]
) -> None:
    output_dir = lab / "outputs"
    if output_dir.exists() and not output_dir.is_dir():
        problems.append(f"{lab.name}/outputs exists but is not a directory")
        return
    if not output_dir.is_dir():
        return
    unexpected = [
        path.name
        for path in output_dir.iterdir()
        if path.name not in allowed_names or not path.is_file()
    ]
    if unexpected:
        problems.append(f"{lab.name}/outputs contains an unexpected entry")


def check_source(problems: list[str]) -> None:
    for path in required_files():
        if not path.is_file():
            problems.append(f"missing {path.relative_to(ROOT)}")

    if (ROOT / "outputs").exists():
        problems.append("unexpected outputs directory at the repository root")
    check_output_directory(
        LAB01,
        {"lab_start_check.json", "project_brief_check.json"},
        problems,
    )
    check_output_directory(
        LAB02,
        {"architecture_start_check.json", "architecture_check.json"},
        problems,
    )

    local_patterns = (
        re.compile(r"/home/", re.IGNORECASE),
        re.compile(r"/Users/", re.IGNORECASE),
        re.compile(r"[A-Za-z]:\\"),
    )
    source_paths = (
        ROOT / "README.md",
        ROOT / "course_integrity.py",
        ROOT / "handoff_check.py",
        *LAB01.rglob("*"),
        *LAB02.rglob("*"),
    )
    for path in source_paths:
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".md" and text.count("```") % 2:
            problems.append(f"unbalanced Markdown fence: {path.relative_to(ROOT)}")
        if path.suffix.lower() != ".py" and any(
            pattern.search(text) for pattern in local_patterns
        ):
            problems.append(f"machine-specific path: {path.relative_to(ROOT)}")
        if path.suffix.lower() == ".py":
            try:
                compile(text, str(path), "exec")
            except SyntaxError as error:
                location = f"{path.relative_to(ROOT)}:{error.lineno}"
                problems.append(f"Python syntax error in {location}")
        elif path.suffix.lower() == ".json":
            try:
                json.loads(text)
            except json.JSONDecodeError as error:
                location = f"{path.relative_to(ROOT)}:{error.lineno}"
                problems.append(f"invalid JSON in {location}")


def check_lab01_contract(problems: list[str]) -> None:
    facts_path = LAB01 / "data" / "project_facts.json"
    brief_path = LAB01 / "project_brief.md"
    try:
        facts = json.loads(facts_path.read_text(encoding="utf-8"))
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


def check_lab02_contract(problems: list[str]) -> None:
    requirements_path = LAB02 / "data" / "architecture_requirements.json"
    brief_path = LAB02 / "architecture_brief.md"
    try:
        requirements = json.loads(requirements_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    expected_keys = {
        "workflow_parts",
        "case_ids",
        "fixed_rules",
        "dataset_images_required",
    }
    if set(requirements) != expected_keys:
        problems.append("Lab 02 protected requirements have an unexpected structure")
    if len(requirements.get("workflow_parts", [])) != 6:
        problems.append("Lab 02 must disclose six workflow parts")
    if len(requirements.get("case_ids", [])) != 5:
        problems.append("Lab 02 must disclose five case paths")
    if requirements.get("dataset_images_required") is not False:
        problems.append("Lab 02 must not require dataset images")
    if not brief_path.is_file():
        return
    brief = brief_path.read_text(encoding="utf-8")
    required_markers = (
        "ARCHITECTURE-GOAL:",
        "### INPUT",
        "### VALIDATION",
        "### PREPROCESSING",
        "### DETECTOR",
        "### RESULT",
        "### HUMAN-REVIEW",
        "VALID_IMAGE:",
        "MISSING_FILE:",
        "UNSUPPORTED_IMAGE:",
        "UNCERTAIN_RESULT:",
        "CONFIDENT_RESULT:",
        "VALIDATION-FIRST:",
        "REVIEW-BOUNDARY:",
        "TEAM-CHECK:",
    )
    missing = [marker for marker in required_markers if marker not in brief]
    if missing:
        problems.append("Lab 02 starter is missing required fields or headings")


def main() -> int:
    problems: list[str] = []
    if sys.version_info[:2] != (3, 12):
        actual = f"{sys.version_info.major}.{sys.version_info.minor}"
        problems.append(f"Python 3.12 is required; this command used Python {actual}")
    check_release_boundary(problems)
    check_source(problems)
    check_inventory(LAB01, problems)
    check_inventory(LAB02, problems)
    check_lab01_contract(problems)
    check_lab02_contract(problems)
    if problems:
        print("PDP_LAB02_HANDOFF_BLOCKED")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print("PDP_LAB02_HANDOFF_READY scope=labs01-02 future_labs=not_in_release")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
