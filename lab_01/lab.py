#!/usr/bin/env python3
"""Start, check, or reset the Lab 01 project brief task."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_integrity import IntegrityError, sha256, verify_inventory

LAB_ROOT = Path(__file__).resolve().parent
EXPECTED_INVENTORY_SHA256 = "d149bd0a6f359714b7f188ebf2a61e82e8c3791021a2dad067464c79b81937a5"
FACTS_PATH = LAB_ROOT / "data" / "project_facts.json"
OUTPUT_DIR = LAB_ROOT / "outputs"
START_CHECK_PATH = OUTPUT_DIR / "lab_start_check.json"
CHECK_PATH = OUTPUT_DIR / "project_brief_check.json"
BRIEF_PATH = LAB_ROOT / "project_brief.md"
REQUIRED_HEADINGS = (
    "Team",
    "Fixed Course Facts",
    "Project Boundary",
    "Risk And Testable Behaviour",
    "Initial Contributions",
)


class LabError(Exception):
    pass


def ensure_runtime() -> None:
    if sys.version_info[:2] != (3, 12):
        actual = f"{sys.version_info.major}.{sys.version_info.minor}"
        raise LabError(f"Python 3.12 is required; this command used Python {actual}.")


def load_project_facts() -> dict[str, object]:
    try:
        content = json.loads(FACTS_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LabError(
            "data/project_facts.json is missing or invalid. Restore the lab copy."
        ) from error
    if (
        content.get("project") != "Brain MRI object detection"
        or content.get("labels") != ["glioma", "meningioma", "pituitary"]
        or content.get("full_dataset_needed_from") != "Lab 04"
        or content.get("use") != "education only; not a medical diagnosis"
    ):
        raise LabError("The protected project facts were changed. Restore the lab copy.")
    return content


def write_json(path: Path, content: object) -> None:
    rendered = json.dumps(content, ensure_ascii=False, indent=2, sort_keys=True)
    path.write_text(rendered + "\n", encoding="utf-8")


def ensure_brief_file() -> None:
    if not BRIEF_PATH.is_file():
        raise LabError(
            "project_brief.md is missing; restore it from the original student package."
        )


def parse_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1).strip().casefold()] = text[match.end():end].strip()
    missing = [heading for heading in REQUIRED_HEADINGS if heading.casefold() not in sections]
    if missing:
        raise LabError("project_brief.md is missing: " + ", ".join(missing))
    return sections


def check_brief() -> dict[str, object]:
    load_project_facts()
    if not BRIEF_PATH.is_file():
        raise LabError("Run python lab.py start first, then complete project_brief.md.")
    text = BRIEF_PATH.read_text(encoding="utf-8-sig")
    placeholder = re.search(r"(?m)^\s*[A-Z0-9-]+:\s*\[[^\]\n]+\]\s*$", text)
    if placeholder is not None:
        raise LabError("project_brief.md still contains an unfinished square-bracket prompt.")
    parse_sections(text)

    def field(label: str, minimum: int) -> str:
        match = re.search(
            rf"(?ims)^{re.escape(label)}:\s*(.*?)"
            rf"(?=^\s*[A-Z][A-Z0-9-]*:\s|^#{{1,6}}\s|\Z)",
            text,
        )
        if match is None:
            raise LabError(f"Complete {label}: with a concrete answer.")
        value = match.group(1).strip()
        if sum(character.isalnum() for character in value) < minimum:
            raise LabError(f"Complete {label}: with a concrete answer.")
        return value

    folded = text.casefold()
    team_match = re.search(r"(?im)^TEAM-NAME:\s*(\S+)\s*$", text)
    team_name = team_match.group(1) if team_match is not None else ""
    if not (
        2 <= len(team_name) <= 32
        and team_name[0].isalnum()
        and all(character.isalnum() or character in "_-" for character in team_name)
    ):
        raise LabError(
            "TEAM-NAME must be a 2–32 character name using letters, numbers, "
            "hyphens, or underscores."
        )
    labels_match = re.search(r"(?im)^MEMBER-LABELS:\s*(.+?)\s*$", text)
    if labels_match is None:
        raise LabError(
            "List comma-separated first names or initials after MEMBER-LABELS:."
        )
    member_labels = [label.strip() for label in labels_match.group(1).split(",")]
    if not member_labels or any(
        not (2 <= len(label) <= 24)
        or not any(character.isalpha() for character in label)
        or not all(character.isalnum() or character in "._-" for character in label)
        for label in member_labels
    ):
        raise LabError(
            "Each MEMBER-LABELS value must be a 2–24 character first name or "
            "initials without spaces."
        )
    if len({label.casefold() for label in member_labels}) != len(member_labels):
        raise LabError("MEMBER-LABELS contains a duplicate label.")
    field("TEAM-WORK", 20)
    system_does = field("SYSTEM-DOES", 40).casefold()
    system_does_not = field("SYSTEM-DOES-NOT", 20).casefold()
    reviewer = field("REVIEWER", 8).casefold()
    field("RISK", 12)
    field("RESPONSE", 12)
    testable = field("TESTABLE-BEHAVIOUR", 25).casefold()
    contributions = field("INITIAL-CONTRIBUTIONS", 12).casefold()

    if "mri" not in system_does:
        raise LabError("SYSTEM-DOES must identify the MRI input.")
    detection_terms = (
        "locate",
        "localize",
        "localise",
        "localization",
        "localisation",
        "detect",
    )
    if not any(term in system_does for term in detection_terms):
        raise LabError("SYSTEM-DOES must describe locating or detecting regions.")
    if "box" not in system_does:
        raise LabError("SYSTEM-DOES must describe the labeled boxes returned.")
    if not any(
        term in system_does_not
        for term in (
            "diagnos",
            "medical",
            "clinical",
            "treat",
            "doctor",
            "clinician",
            "automatic decision",
        )
    ):
        raise LabError(
            "SYSTEM-DOES-NOT must exclude diagnosis, treatment, a medical "
            "decision, or replacing a clinician."
        )
    if "review" not in reviewer:
        raise LabError("REVIEWER must state who performs human review.")
    if not all(term in testable for term in ("given", "when", "then")):
        raise LabError("TESTABLE-BEHAVIOUR must contain Given, When, and Then.")
    missing_contributions = [
        label for label in member_labels if label.casefold() not in contributions
    ]
    if missing_contributions:
        missing_text = ", ".join(missing_contributions)
        raise LabError(
            "INITIAL-CONTRIBUTIONS must name every member label: " + missing_text
        )
    fixed_terms = (
        "glioma",
        "meningioma",
        "pituitary",
        "notumor",
        "human review",
        "non-clinical",
        "not a diagnosis",
    )
    if not all(term in folded for term in fixed_terms):
        raise LabError("Restore the supplied Fixed Course Facts section.")
    result = {
        "status": "brief_complete",
        "team_name": team_name,
        "member_labels": member_labels,
        "project_brief_sha256": sha256(BRIEF_PATH),
        "task_type": "object_detection",
        "risk_count": 1,
        "checks": [
            "project boundary stated",
            "human-output review stated",
            "one risk and response recorded",
            "Given-When-Then behaviour recorded",
            "initial contributions recorded for every member",
        ],
        "note": (
            "This automated check verifies the project brief structure. It does "
            "not measure model accuracy or approve clinical use."
        ),
    }
    return result


def command_start() -> int:
    ensure_runtime()
    facts = load_project_facts()
    OUTPUT_DIR.mkdir(exist_ok=True)
    write_json(
        START_CHECK_PATH,
        {
            "status": "ready_to_write_brief",
            "project": facts["project"],
            "project_facts_file_hash": sha256(FACTS_PATH),
            "dataset_images_loaded": False,
            "full_dataset_needed_from": facts["full_dataset_needed_from"],
        },
    )
    ensure_brief_file()
    print(
        "ASE01_START_PASS project_facts=checked dataset_images=not_required "
        "brief_file=project_brief.md"
    )
    return 0


def command_check(argument: str) -> int:
    ensure_runtime()
    if argument != "project_brief.md":
        raise LabError("Run the check with: python lab.py check project_brief.md")
    result = check_brief()
    OUTPUT_DIR.mkdir(exist_ok=True)
    write_json(CHECK_PATH, {"project_facts_file_hash": sha256(FACTS_PATH), **result})
    print("Created outputs/project_brief_check.json")
    print("ASE01_PROJECT_CHECK_PASS status=brief_complete risk=recorded behaviour=testable")
    return 0


def command_reset() -> int:
    ensure_runtime()
    before = sha256(BRIEF_PATH) if BRIEF_PATH.is_file() else None
    removed = 0
    if OUTPUT_DIR.exists():
        if any(path.is_dir() for path in OUTPUT_DIR.iterdir()):
            raise LabError("Refusing reset because outputs contains a nested directory.")
        for path in OUTPUT_DIR.iterdir():
            path.unlink()
            removed += 1
        OUTPUT_DIR.rmdir()
    after = sha256(BRIEF_PATH) if BRIEF_PATH.is_file() else None
    if before != after:
        raise LabError("Reset changed project_brief.md.")
    print(f"ASE01_RESET_PASS outputs_removed={removed} brief=preserved")
    return 0


def main() -> int:
    try:
        verify_inventory(LAB_ROOT, EXPECTED_INVENTORY_SHA256)
        if sys.argv[1:] == ["start"]:
            return command_start()
        if sys.argv[1:] == ["reset"]:
            return command_reset()
        if len(sys.argv) == 3 and sys.argv[1] == "check":
            return command_check(sys.argv[2])
        print("Usage: python lab.py start | check project_brief.md | reset", file=sys.stderr)
        return 2
    except PermissionError:
        print(
            "ASE01_ERROR: This lab folder is not writable. Copy it into a folder "
            "you own; do not use sudo.",
            file=sys.stderr,
        )
        return 2
    except (LabError, IntegrityError, OSError, json.JSONDecodeError) as error:
        print(f"ASE01_ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
