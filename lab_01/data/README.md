# Lab 01 protected data

This folder contains no MRI images and no sample dataset.

- `project_facts.json` is a short machine-readable description of the fixed
  project, public dataset page, license, labels, result, and dataset timing.
- `checksums.sha256` protects that facts file from accidental changes.

In machine learning operations (MLOps), a checked input artifact lets people
and automated checks read the same facts. Running `lab.py start` creates a
different JSON file, `outputs/lab_start_check.json`. That output records that
the facts file was readable and which exact file hash was used. It is evidence
of a completed check, not a duplicate dataset.

Students do not edit files in this folder. The full image dataset first becomes
necessary in Lab 04.
