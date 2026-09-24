#!/usr/bin/env python3
"""Start, check, or reset the Lab 02 architecture task."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from course_integrity import IntegrityError, sha256, verify_inventory

LAB_ROOT = Path(__file__).resolve().parent
REQUIREMENTS_PATH = LAB_ROOT / "data" / "architecture_requirements.json"
BRIEF_PATH = LAB_ROOT / "architecture_brief.md"
OUTPUT_DIR = LAB_ROOT / "outputs"
START_CHECK_PATH = OUTPUT_DIR / "architecture_start_check.json"
CHECK_PATH = OUTPUT_DIR / "architecture_check.json"
LAB01_BRIEF_PATH = LAB_ROOT.parent / "lab_01" / "project_brief.md"
LAB01_CHECK_PATH = LAB_ROOT.parent / "lab_01" / "outputs" / "project_brief_check.json"
EXPECTED_INVENTORY_SHA256 = "e635d1b2ad7ce43e9bdcf37bb60ae9551f418afd590a0e53c2d2e85304efcf83"

WORKFLOW_PARTS = (
    "INPUT",
    "VALIDATION",
    "PREPROCESSING",
    "DETECTOR",
    "RESULT",
    "HUMAN-REVIEW",
)
CASE_IDS = (
    "VALID_IMAGE",
    "MISSING_FILE",
    "UNSUPPORTED_IMAGE",
    "UNCERTAIN_RESULT",
    "CONFIDENT_RESULT",
)
REQUIRED_HEADINGS = (
    "Fixed Project Context",
    "Workflow Parts",
    *WORKFLOW_PARTS,
    "Case Paths",
    "Boundary Decisions",
    "Team Check",
)


class LabError(Exception):
    pass


def ensure_runtime() -> None:
    if sys.version_info[:2] != (3, 12):
        actual = f"{sys.version_info.major}.{sys.version_info.minor}"
        raise LabError(f"Python 3.12 is required; this command used Python {actual}.")


def load_json(path: Path, label: str) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LabError(f"{label} is missing or invalid JSON.") from error
    if not isinstance(value, dict):
        raise LabError(f"{label} must contain one JSON object.")
    return value


def load_requirements() -> dict[str, object]:
    requirements = load_json(
        REQUIREMENTS_PATH, "data/architecture_requirements.json"
    )
    expected_keys = {
        "workflow_parts",
        "case_ids",
        "fixed_rules",
        "dataset_images_required",
    }
    if set(requirements) != expected_keys:
        raise LabError("Restore the released Lab 02 requirements file.")
    if requirements.get("workflow_parts") != list(WORKFLOW_PARTS):
        raise LabError("Restore the released workflow-part names.")
    if requirements.get("case_ids") != list(CASE_IDS):
        raise LabError("Restore the released case names.")
    rules = requirements.get("fixed_rules")
    if not isinstance(rules, list) or len(rules) != 4:
        raise LabError("Restore the released boundary rules.")
    if requirements.get("dataset_images_required") is not False:
        raise LabError("Lab 02 must not require dataset images.")
    return requirements


def load_lab01_check() -> dict[str, object]:
    if not LAB01_BRIEF_PATH.is_file() or not LAB01_CHECK_PATH.is_file():
        raise LabError(
            "Complete Lab 01 and create lab_01/outputs/project_brief_check.json "
            "before starting Lab 02."
        )
    check = load_json(LAB01_CHECK_PATH, "Lab 01 project brief check")
    if check.get("status") != "brief_complete":
        raise LabError("Lab 01 has not passed its final check.")
    if check.get("project_brief_sha256") != sha256(LAB01_BRIEF_PATH):
        raise LabError(
            "The Lab 01 brief changed after its check. Rerun the Lab 01 final check."
        )
    member_labels = check.get("member_labels")
    if not isinstance(member_labels, list) or not member_labels or not all(
        isinstance(label, str) and label.strip() for label in member_labels
    ):
        raise LabError("The Lab 01 evidence does not contain valid member labels.")
    return check


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(exist_ok=True)
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)
    path.write_text(rendered + "\n", encoding="utf-8")


def ensure_brief_file() -> None:
    if not BRIEF_PATH.is_file():
        raise LabError("architecture_brief.md is missing; restore the Lab 02 copy.")


def parse_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1).strip().casefold()] = text[match.end() : end].strip()
    missing = [
        heading for heading in REQUIRED_HEADINGS if heading.casefold() not in sections
    ]
    if missing:
        raise LabError("architecture_brief.md is missing: " + ", ".join(missing))
    return sections


def field(section: str, label: str, minimum: int) -> str:
    match = re.search(
        rf"(?ims)^{re.escape(label)}:\s*(.*?)"
        rf"(?=^[A-Z][A-Z0-9-]*:\s|\Z)",
        section,
    )
    if match is None:
        raise LabError(f"Complete {label}: in architecture_brief.md.")
    value = match.group(1).strip()
    if sum(character.isalnum() for character in value) < minimum:
        raise LabError(f"Give a concrete answer after {label}:.")
    return value


def require_terms(label: str, value: str, terms: tuple[str, ...]) -> None:
    folded = value.casefold()
    missing = [term for term in terms if term.casefold() not in folded]
    if missing:
        raise LabError(f"{label} must mention: " + ", ".join(missing))


def require_no_automatic_action(label: str, value: str) -> None:
    folded = value.casefold()
    negative_terms = ("no", "not", "never", "without", "cannot", "doesn't")
    if "automatic action" not in folded or not any(
        term in folded for term in negative_terms
    ):
        raise LabError(f"{label} must state that automatic action is not allowed.")


def validate_brief(
    requirements: dict[str, object], member_labels: list[str]
) -> dict[str, object]:
    ensure_brief_file()
    text = BRIEF_PATH.read_text(encoding="utf-8-sig")
    if re.search(r"\[[^\]\n]+\]", text):
        raise LabError("architecture_brief.md still contains a square-bracket prompt.")
    sections = parse_sections(text)

    fixed_terms = (
        "brain-mri",
        "labeled boxes",
        "human reviewer",
        "does not make a diagnosis",
        "automatic medical decision",
        "no dataset images",
    )
    folded_text = text.casefold()
    if not all(term in folded_text for term in fixed_terms):
        raise LabError("Restore the supplied Fixed Project Context section.")

    context = sections["fixed project context"].casefold()
    goal = field(context, "ARCHITECTURE-GOAL", 30)
    require_terms("ARCHITECTURE-GOAL", goal, ("mri", "box", "review"))

    part_values: dict[str, dict[str, str]] = {}
    for part_id in requirements["workflow_parts"]:
        section = sections[str(part_id).casefold()]
        part_values[str(part_id)] = {
            "interface": field(section, "INTERFACE", 10),
            "failure": field(section, "FAILURE", 8),
        }

    require_terms(
        "DETECTOR INTERFACE",
        part_values["DETECTOR"]["interface"],
        ("box",),
    )
    validation_failure = part_values["VALIDATION"]["failure"].casefold()
    if not any(term in validation_failure for term in ("reject", "stop")):
        raise LabError("VALIDATION FAILURE must reject or stop invalid input.")
    require_terms(
        "HUMAN-REVIEW",
        " ".join(part_values["HUMAN-REVIEW"].values()),
        ("review",),
    )

    case_section = sections["case paths"]
    case_values = {
        case_id: field(case_section, case_id, 15)
        for case_id in requirements["case_ids"]
    }
    require_terms("VALID_IMAGE", case_values["VALID_IMAGE"], WORKFLOW_PARTS)
    for case_id in ("MISSING_FILE", "UNSUPPORTED_IMAGE"):
        require_terms(case_id, case_values[case_id], ("INPUT", "VALIDATION"))
        folded_case = case_values[case_id].casefold()
        if not any(term in folded_case for term in ("reject", "stop")):
            raise LabError(f"{case_id} must end in rejection or a stopped path.")
        if "before" not in folded_case or not any(
            term in folded_case for term in ("preprocessing", "detector", "detection")
        ):
            raise LabError(
                f"{case_id} must stop before preprocessing or detection."
            )
    for case_id, result_word in (
        ("UNCERTAIN_RESULT", "uncertain"),
        ("CONFIDENT_RESULT", "confident"),
    ):
        require_terms(
            case_id,
            case_values[case_id],
            (result_word, "DETECTOR", "RESULT", "HUMAN-REVIEW"),
        )
        require_no_automatic_action(case_id, case_values[case_id])

    boundary_section = sections["boundary decisions"]
    validation_first = field(boundary_section, "VALIDATION-FIRST", 25)
    require_terms(
        "VALIDATION-FIRST",
        validation_first,
        ("validation", "before", "preprocessing", "detect"),
    )
    review_boundary = field(boundary_section, "REVIEW-BOUNDARY", 25)
    require_terms(
        "REVIEW-BOUNDARY",
        review_boundary,
        ("uncertain", "confident", "human review"),
    )
    require_no_automatic_action("REVIEW-BOUNDARY", review_boundary)

    team_check = field(sections["team check"], "TEAM-CHECK", 20).casefold()
    missing_members = [
        label for label in member_labels if label.casefold() not in team_check
    ]
    if missing_members:
        raise LabError("TEAM-CHECK must name every Lab 01 member: " + ", ".join(missing_members))

    return {
        "part_count": len(part_values),
        "case_count": len(case_values),
    }


def command_start() -> int:
    ensure_runtime()
    requirements = load_requirements()
    lab01_check = load_lab01_check()
    ensure_brief_file()
    write_json(
        START_CHECK_PATH,
        {
            "status": "ready_to_design_architecture",
            "lab01_project_brief_sha256": lab01_check["project_brief_sha256"],
            "workflow_parts": requirements["workflow_parts"],
            "case_ids": requirements["case_ids"],
            "dataset_images_loaded": False,
        },
    )
    print(
        "ASE02_START_PASS parts=6 cases=5 lab01=linked "
        "dataset_images=not_required"
    )
    return 0


def command_check(argument: str) -> int:
    ensure_runtime()
    if argument != "architecture_brief.md":
        raise LabError("Run the check with: python lab.py check architecture_brief.md")
    requirements = load_requirements()
    lab01_check = load_lab01_check()
    counts = validate_brief(requirements, list(lab01_check["member_labels"]))
    write_json(
        CHECK_PATH,
        {
            "status": "architecture_complete",
            "lab01_project_brief_sha256": lab01_check["project_brief_sha256"],
            "architecture_brief_sha256": sha256(BRIEF_PATH),
            "requirements_sha256": sha256(REQUIREMENTS_PATH),
            "workflow_parts": requirements["workflow_parts"],
            "case_ids": requirements["case_ids"],
            **counts,
            "checks": [
                "six workflow parts described",
                "five case paths traced",
                "invalid input stopped before detection",
                "all model outputs end at human review",
                "no automatic medical action allowed",
                "every Lab 01 member recorded in the team check",
            ],
        },
    )
    print("ASE02_ARCHITECTURE_CHECK_PASS parts=6 cases=5 lab01=linked")
    return 0


def command_reset() -> int:
    ensure_runtime()
    protected_paths = (BRIEF_PATH, LAB01_BRIEF_PATH, LAB01_CHECK_PATH)
    before = {
        str(path): sha256(path) for path in protected_paths if path.is_file()
    }
    removed = 0
    if OUTPUT_DIR.exists():
        if any(path.is_dir() for path in OUTPUT_DIR.iterdir()):
            raise LabError("Refusing reset because outputs contains a nested directory.")
        for path in OUTPUT_DIR.iterdir():
            path.unlink()
            removed += 1
        OUTPUT_DIR.rmdir()
    after = {
        str(path): sha256(path) for path in protected_paths if path.is_file()
    }
    if before != after:
        raise LabError("Reset changed the architecture brief or Lab 01 evidence.")
    print(f"ASE02_RESET_PASS outputs_removed={removed} brief=preserved lab01=unchanged")
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
        print(
            "Usage: python lab.py start | check architecture_brief.md | reset",
            file=sys.stderr,
        )
        return 2
    except PermissionError:
        print(
            "ASE02_ERROR: This lab folder is not writable. Copy the repository "
            "into a folder you own; do not use administrator mode.",
            file=sys.stderr,
        )
        return 2
    except (LabError, IntegrityError, OSError, json.JSONDecodeError) as error:
        print(f"ASE02_ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
