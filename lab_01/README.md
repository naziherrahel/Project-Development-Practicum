# Lab 01 — Define the project boundary

## Goal

Write a short project brief that another student can understand and check.
Your brief will state what the project does, what it must not claim, one risk
and response, one testable behaviour, and each member's first contribution.

For Lab 01, you do **not** download images, train a model, select an
architecture, write deployment plans, or complete work from a later lab.

## What you edit and submit

Edit only `project_brief.md`, using a plain-text editor such as VS Code. Do not
convert it to Word or rename it.

At the end, submit exactly these two files:

1. `project_brief.md` — your team's writing;
2. `outputs/project_brief_check.json` — evidence created by the checker.

Do not edit the generated JSON file. If you change the brief after checking
it, run the check again so the evidence matches the latest brief.

## Fixed course facts

Every team uses:

- the public [Labeled MRI brain Tumor dataset](https://www.kaggle.com/datasets/ammarahmed310/labeled-mri-brain-tumor-dataset), listed as CC0 Public Domain;
- RGB brain-MRI images and bounding-box annotations;
- the annotation categories `glioma`, `meningioma`, and `pituitary`;
- `notumor` images as valid negative examples with no boxes, not as a fourth
  detection category;
- zero or more labeled boxes that always go to human review;
- non-clinical wording: the output is not a diagnosis and cannot authorize an
  automatic medical action.

The phrase **annotated as** describes the label supplied with the dataset. It
does not claim that a model prediction establishes medical truth. Lab 01 does
not ask you to medically define or validate the three category names.

These are supplied facts, not research questions. The dataset link records the
common public source for all teams. You may open the page, but you do not need
a Kaggle account or a dataset download for Lab 01. The checked download and
data-preparation instructions will be supplied when the dataset is first
needed.

## Team names and member labels

- **Team name:** a short name your team chooses, such as `MRI-Team-3`.
- **Member label:** a first name or short initials, such as `Salma`, `Elina`,
  or `Emanuel`.

Use the same member label in later released labs.

For this lab, choose one person to type, one to check the project boundary,
and one to check the risk and behaviour. A small team may combine these jobs.
Rotate who controls the keyboard at least once. Report a blocker—a problem
that stops progress—to the whole team.

## Start the lab

First open a terminal in the repository root. Change into the Lab 01 folder:

```text
cd lab_01
```

Then run one of these commands:

- Ubuntu: `python3.12 lab.py start`
- Windows PowerShell: `py -3.12 lab.py start`

The expected final line is:

`ASE01_START_PASS project_facts=checked dataset_images=not_required brief_file=project_brief.md`

The command checks the supplied facts and creates
`outputs/lab_start_check.json`. It does not download data and does not
overwrite your brief. Running `start` again is safe.

If you see `can't open file 'lab.py'`, your terminal is in the wrong folder.
Change into `lab_01` and try again.

No package installation is required. `requirements.txt` is included only to
record that Lab 01 uses Python's standard library.

## Why the lab creates JSON evidence

JSON stores information using names and values. For example:

```json
{
  "status": "ready_to_write_brief",
  "dataset_images_loaded": false
}
```

Here, `status` and `dataset_images_loaded` are field names. The value `false`
confirms that the command did not load dataset images.

- `data/project_facts.json` is a protected input supplied with the lab.
- `outputs/lab_start_check.json` records which protected input was read.
- `outputs/project_brief_check.json` records that your completed brief passed
  the structural checks.

A long string of letters and numbers ending in `_hash` is a digital
fingerprint used to notice accidental file changes. You do not type,
calculate, or edit it. None of these JSON files contains MRI images.

## Complete the project brief

Open `project_brief.md`. Replace every instruction inside square brackets,
including the brackets themselves. Keep each uppercase field name and its
colon. An answer may continue on the following line. Do not rewrite the
**Fixed Course Facts**.

Use this guide:

| Field | Question your answer must resolve |
| --- | --- |
| `TEAM-NAME` | What short name did your team choose? |
| `MEMBER-LABELS` | Which first names or initials identify the members? |
| `TEAM-WORK` | Who runs commands, who checks decisions, and how are problems that stop progress reported? |
| `SYSTEM-DOES` | What MRI image enters, what object-detection action occurs, and what result is returned? |
| `SYSTEM-DOES-NOT` | Which medical claim or automatic decision is outside the boundary? |
| `REVIEWER` | From the workflow's perspective, who receives and reviews every model output? |
| `RISK` | What one specific failure could occur? |
| `RESPONSE` | What will the team or workflow do if that failure occurs? |
| `TESTABLE-BEHAVIOUR` | Given a condition, when an action occurs, what observable result follows? |
| `INITIAL-CONTRIBUTIONS` | What did each listed member first contribute to this lab? |

For this project, `REVIEWER` means the designated human reviewer who receives
the workflow's output. It does not mean a student proofreading the brief or
the instructor grading it. The reviewer checks the output but does not use it
to make a diagnosis or automatic medical decision.

A good risk is specific enough that its response can address it. “The project
might fail” is too broad.

Do not describe a complete architecture. That is not part of Lab 01.

## Complete worked example — a different project

This manufacturing-panel example shows the required format for every editable
field. It is not an answer to the brain-MRI task. Do not copy its domain,
categories, risk, or decisions into your brief.

```text
TEAM-NAME: Panel-Team-2
MEMBER-LABELS: Salma, Elina, Emanuel
TEAM-WORK: Salma runs the first command, Elina checks the recorded decisions,
Emanuel records blockers in the team log, and the members rotate these jobs
after the first check.

SYSTEM-DOES: The inspection workflow receives one panel photograph, locates
regions annotated as scratches, dents, or cracks, and returns labeled boxes.

SYSTEM-DOES-NOT: It does not certify that a product is safe or decide whether
the product may be shipped.

REVIEWER: A quality engineer receives and reviews every result.

RISK: A reflection on the panel could be marked as a defect.

RESPONSE: The workflow flags uncertain results for review and never triggers
an automatic production decision.

TESTABLE-BEHAVIOUR: Given a missing panel image, when the workflow is started,
then it reports the missing input and returns no defect boxes.

INITIAL-CONTRIBUTIONS: Salma ran the start command; Elina checked the project
boundary; Emanuel drafted the risk and response.
```

Notice that the response directly addresses the stated risk, and the
Given–When–Then result can be observed by another person.

## Check your work

Save `project_brief.md`, remain inside `lab_01`, and run:

- Ubuntu: `python3.12 lab.py check project_brief.md`
- Windows PowerShell: `py -3.12 lab.py check project_brief.md`

You are finished when the final line is:

`ASE01_PROJECT_CHECK_PASS status=brief_complete risk=recorded behaviour=testable`

The checker confirms that required ideas and fields are present. It cannot
judge whether your writing is thoughtful, so your team must read the brief
once more before submission.

## If something fails

| Message or question | What to do |
| --- | --- |
| `unfinished square-bracket prompt` | Replace every `[instruction]` with your team's answer and remove the brackets. |
| `invalid team name` | Use 2–32 letters, numbers, hyphens, or underscores with no spaces. |
| `invalid member label` | Use a 2–24 character first name or initials without spaces. |
| `missing project-boundary idea` | Check the four `SYSTEM-DOES` questions in the field guide. |
| `missing Given–When–Then term` | Include the words **Given**, **When**, and **Then** in that one field. |
| `missing contribution` | Name every member label and one contribution for each person. |
| `changed project facts` | Restore the original `project_brief.md` facts and the complete `data/` folder. |
| “Do we need the MRI images?” | No. Do not download them for Lab 01. |
| “Do we edit JSON or checksum files?” | No. The commands create or verify them. |
| “Do we build or train anything?” | No. This lab defines the project boundary only. |

To remove generated JSON and start the checks again without deleting your
brief, run `python3.12 lab.py reset` on Ubuntu or `py -3.12 lab.py reset` in
Windows PowerShell. Do not run `reset` after your final check unless you plan
to regenerate the required submission evidence.
