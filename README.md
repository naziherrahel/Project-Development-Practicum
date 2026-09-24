# Project Development Practicum

AI Systems Engineering — Semester 7

## Current student release: Lab 02

This repository contains Labs 01 and 02. Labs 03–12 and instructor materials
are not included. Complete and check Lab 01 before starting Lab 02.

## Get or update the course files

If you already used Git for Lab 01, open a terminal in your existing
`Project-Development-Practicum` folder and run:

```text
git pull --ff-only
```

This adds Lab 02 without replacing your completed Lab 01 brief or generated
Lab 01 evidence. If Git refuses to update, do not delete your work; keep the
message visible and ask for help.

For a new Git clone, run:

```text
git clone https://github.com/naziherrahel/Project-Development-Practicum.git
cd Project-Development-Practicum
```

Because the repository is private, GitHub may ask you to sign in. If GitHub
says **Repository not found**, confirm that you are using the GitHub account
that has course access.

If you receive a ZIP file, extract it before running commands. A student who
completed Lab 01 in an older ZIP must copy these two completed files into the
new extracted repository:

- `lab_01/project_brief.md`;
- `lab_01/outputs/project_brief_check.json`.

## Check the release

From the repository root, run:

- Ubuntu: `python3.12 handoff_check.py`
- Windows PowerShell: `py -3.12 handoff_check.py`

The expected final line is:

`PDP_LAB02_HANDOFF_READY scope=labs01-02 future_labs=not_in_release`

If Python 3.12 cannot be found, stop and use the course Python setup before
continuing. Do not use `sudo` or administrator mode to run the labs.

## Repository structure

```text
Project-Development-Practicum/
├── README.md
├── handoff_check.py
├── course_integrity.py
├── lab_01/
│   ├── README.md
│   ├── project_brief.md
│   └── data/
└── lab_02/
    ├── README.md                 ← start here for the current lab
    ├── architecture_brief.md     ← the only supplied Lab 02 file you edit
    ├── lab.py
    ├── requirements.txt
    └── data/                     ← protected requirements; no MRI images
```

The lab commands create `outputs/` inside the corresponding lab folder. Do
not create or edit generated evidence by hand.

## Project direction

Across the semester, your team will develop a reviewable object-detection
workflow for brain-MRI images. The supplied dataset uses three annotation
categories: `glioma`, `meningioma`, and `pituitary`. A `notumor` image is a
valid negative example with no boxes.

This is non-clinical coursework. A result is not a diagnosis, does not
authorize medical action, and always requires human review.

## What Lab 02 produces

Lab 02 turns the checked project boundary from Lab 01 into a six-part workflow
architecture with five traced cases. It does not require the dataset, model
selection, model training, API development, or deployment planning.

Your team will submit:

- `lab_02/architecture_brief.md`;
- `lab_02/outputs/architecture_check.json`.

Continue with [the Lab 02 instructions](lab_02/README.md).
