# Project Development Practicum

AI Systems Engineering — Semester 7

## Current student release: Lab 01 only

This repository contains the opening lab. Labs 02–12 and instructor materials
are not included. You do not need any future lab to complete Lab 01.

## Get the course files

If you use Git, run:

```text
git clone https://github.com/naziherrahel/Project-Development-Practicum.git
cd Project-Development-Practicum
```

Because the repository is private, GitHub may ask you to sign in. If GitHub
says **Repository not found**, confirm that you are signed in with the account
to which your instructor granted access.

If your instructor gives you a ZIP file instead, extract it first. Do not run
the lab from inside the ZIP preview. Open a terminal in the extracted
`Project-Development-Practicum` folder.

## Check that you are in the right folder

From the repository root, run:

- Ubuntu: `python3.12 handoff_check.py`
- Windows PowerShell: `py -3.12 handoff_check.py`

The expected final line is:

`PDP_LAB01_HANDOFF_READY scope=lab01 future_labs=not_in_release`

If your computer says that Python 3.12 cannot be found, stop here and ask your
instructor for the course Python setup instructions. Do not use `sudo` to run
the lab.

## What is in this release?

```text
Project-Development-Practicum/
├── README.md                 ← start here
├── handoff_check.py          ← checks that the release is complete
├── course_integrity.py       ← support code used by the lab checker
└── lab_01/
    ├── README.md             ← complete Lab 01 instructions
    ├── project_brief.md      ← the only supplied file your team edits
    ├── lab.py                ← starts, checks, and resets the lab
    ├── requirements.txt      ← confirms that no extra packages are needed
    └── data/                 ← small protected facts; no MRI images
```

Running the lab creates `lab_01/outputs/`. Do not create that folder yourself.

Do not edit the Python checkers, the files under `lab_01/data/`, or hidden Git
setup files. They are supplied so every team starts with the same facts and
the same automated checks.

## Project direction

Across the semester, your team will develop a reviewable object-detection
workflow for brain-MRI images. The supplied dataset uses three annotation
categories: `glioma`, `meningioma`, and `pituitary`. A `notumor` image is a
valid negative example with no boxes.

This is non-clinical coursework. A result is not a diagnosis, does not
authorize medical action, and always requires human review.

## What Lab 01 produces

Your team will submit:

- `lab_01/project_brief.md`;
- `lab_01/outputs/project_brief_check.json`.

The brief records the project boundary, one risk and response, one testable
behaviour, and each member's first contribution. It does not require the full
dataset, architecture, model training, deployment planning, or future lab
work.

Continue with [the Lab 01 instructions](lab_01/README.md).
