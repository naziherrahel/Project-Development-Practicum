# Lab 02 — Design the workflow architecture

## Goal

Turn the checked Lab 01 project boundary into a clear architecture. Your team
will describe six workflow parts, show what each part receives and returns,
state what happens when each part fails, and trace five important cases.

This is a design lab. You do not download the MRI dataset, write workflow
code, choose a model, train a model, create an API, or plan deployment.

## What you edit and submit

Edit only `architecture_brief.md` using a plain-text editor.

At the end, submit exactly these two files:

1. `architecture_brief.md` — your team's architecture;
2. `outputs/architecture_check.json` — evidence created by the checker.

Do not edit the generated JSON. If you change the architecture brief after
checking it, run the check again.

## Before you start

Lab 02 must remain in the same repository as your completed Lab 01. Confirm
that these files exist:

- `lab_01/project_brief.md`;
- `lab_01/outputs/project_brief_check.json`.

If the Lab 01 evidence is missing, enter `lab_01` and run its final check
again. If you changed the Lab 01 brief, its final check must be rerun before
Lab 02 can start.

The Lab 02 checker reads your Lab 01 member labels and brief fingerprint. It
does not copy your Lab 01 answers into the architecture brief.

## Fixed workflow map

Every team uses the same six-part path:

```text
INPUT -> VALIDATION -> PREPROCESSING -> DETECTOR -> RESULT -> HUMAN-REVIEW
```

The first five parts are software responsibilities. `HUMAN-REVIEW` is the
required person at the end of the workflow, not another software component.

| Workflow part | Main responsibility |
| --- | --- |
| `INPUT` | Receive the requested MRI input. |
| `VALIDATION` | Accept supported input or reject it before later processing. |
| `PREPROCESSING` | Prepare accepted input for object detection. |
| `DETECTOR` | Produce zero or more labeled boxes. |
| `RESULT` | Form one complete result for review. |
| `HUMAN-REVIEW` | Review the result without automatic medical action. |

If a requested file cannot be found, `INPUT` may pass a missing-input state.
`VALIDATION` remains the boundary that rejects it before preprocessing or
detection.

Your task is not to invent different parts. Your task is to define the
interfaces and failure behaviour clearly enough that another student could
implement the same design later.

## Start the lab

Open a terminal in the repository root and enter the Lab 02 folder:

```text
cd lab_02
```

Then run:

- Ubuntu: `python3.12 lab.py start`
- Windows PowerShell: `py -3.12 lab.py start`

The expected final line is:

`ASE02_START_PASS parts=6 cases=5 lab01=linked dataset_images=not_required`

The command checks the supplied Lab 02 requirements, confirms that the Lab 01
brief still matches its evidence, and creates
`outputs/architecture_start_check.json`. It does not load dataset images or
overwrite your architecture brief.

No package installation is required. `requirements.txt` records that Lab 02
uses only Python's standard library.

## Complete the workflow parts

Open `architecture_brief.md`. Replace every square-bracket prompt while
keeping all headings and uppercase field names.

For every workflow part, complete:

- `INTERFACE` — what crosses into the part and what crosses out when it
  succeeds;
- `FAILURE` — the observable stopped, rejected, recorded, or review-pending
  result when the part cannot finish normally.

Do not write only “fix the error.” State what the workflow does with the input
or result. Do not include computer-specific file paths, libraries, model names,
or version numbers.

For `HUMAN-REVIEW`, describe the designated reviewer from the workflow's
perspective. This is not a student proofreading the document or the instructor
grading it.

## Trace the five cases

Use the fixed uppercase workflow-part names and `->` to make each path easy to
follow.

| Case | Required outcome |
| --- | --- |
| `VALID_IMAGE` | Pass through all six workflow parts. |
| `MISSING_FILE` | Stop at validation before preprocessing or detection. |
| `UNSUPPORTED_IMAGE` | Stop at validation before preprocessing or detection. |
| `UNCERTAIN_RESULT` | Reach human review with no automatic action. |
| `CONFIDENT_RESULT` | Still reach human review with no automatic action. |

Confidence changes what the reviewer sees; it does not remove the review
boundary.

## Record the two boundary decisions

- `VALIDATION-FIRST` explains why preprocessing and detection cannot run until
  validation accepts the input.
- `REVIEW-BOUNDARY` explains why both uncertain and confident results require
  human review and no automatic action.

In `TEAM-CHECK`, list every Lab 01 member label and one workflow part or case
that each person checked.

## Worked example — a different project

The following factory-inspection example demonstrates the format. It is not an
answer to the brain-MRI architecture.

```text
### VALIDATION

INTERFACE: Receives one factory-panel photograph from INPUT and returns an
accepted photograph with its basic image information.
FAILURE: A missing or unreadable photograph is rejected before inspection.

MISSING_PHOTO: INPUT -> VALIDATION -> rejected before DEFECT-DETECTOR.

VALIDATION-FIRST: Validation prevents an unreadable factory photograph from
reaching preparation or defect detection.
```

The example states an interface, an observable failure, and an ordered path.
Do not copy its factory domain or component names into your MRI brief.

## Check your work

Save `architecture_brief.md`, remain inside `lab_02`, and run:

- Ubuntu: `python3.12 lab.py check architecture_brief.md`
- Windows PowerShell: `py -3.12 lab.py check architecture_brief.md`

You are finished when the final line is:

`ASE02_ARCHITECTURE_CHECK_PASS parts=6 cases=5 lab01=linked`

The generated `outputs/architecture_check.json` records the Lab 01 brief
fingerprint, the architecture brief fingerprint, the six workflow-part names,
the five case names, and the checks that passed.

## If something fails

| Message or question | What to do |
| --- | --- |
| Lab 01 evidence is missing | Run the Lab 01 final check, then return to Lab 02. |
| Lab 01 brief changed after its check | Rerun the Lab 01 final check so its evidence matches. |
| square-bracket prompt remains | Replace every `[instruction]` and remove the brackets. |
| missing heading or field | Restore the supplied heading or uppercase field name. |
| answer is too short | State the actual input, output, failure, or path rather than a vague phrase. |
| invalid case path | Use the fixed workflow-part names and the required outcome table. |
| member missing from `TEAM-CHECK` | Add that Lab 01 member label and what the person checked. |
| changed requirements | Restore the complete supplied `data/` folder. |
| “Do we need MRI images?” | No. Lab 02 uses architecture descriptions only. |
| “Do we write Python workflow code?” | No. Only `architecture_brief.md` is edited. |
| “Do we choose a model?” | No. Model selection is outside Lab 02. |

To remove generated Lab 02 JSON without changing your architecture or Lab 01
work, run `python3.12 lab.py reset` on Ubuntu or `py -3.12 lab.py reset` in
Windows PowerShell. Do not reset after your final check unless you plan to
regenerate the submission evidence.
