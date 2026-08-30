# Project Development Practicum — Project Brief

Read `README.md` before editing this file. Replace only the prompts in square
brackets, including the brackets. Keep every uppercase field name and colon.
An answer may continue on the following line.

Use the same member labels in later labs. A member label is a first name or
short initials.

## Team

TEAM-NAME: [Choose a 2–32 character team name.]
MEMBER-LABELS: [List each member's first name or initials, separated by commas.]
TEAM-WORK: [Explain how the team will rotate commands, review decisions, and report problems that stop progress.]

## Fixed Course Facts

- The project is a brain-MRI object-detection workflow.
- The input is one RGB brain-MRI image.
- The provided dataset annotates regions as `glioma`, `meningioma`, or
  `pituitary`. A `notumor` image is a valid negative example with no boxes.
- The result is zero or more labeled boxes for human review.
- This is non-clinical coursework and not a diagnosis.
- The full dataset is introduced in Lab 04. Do not download it for Lab 01.

These are supplied facts, not questions. Do not rewrite them.

## Project Boundary

SYSTEM-DOES: [In one sentence, describe the MRI input, object-detection action, and returned result.]
SYSTEM-DOES-NOT: [In one sentence, state one medical or automatic-decision claim the workflow must not make.]
REVIEWER: [State that a designated human reviewer receives and reviews every model output.]

## Risk And Testable Behaviour

RISK: [Describe one specific thing that could go wrong.]
RESPONSE: [State what the team or workflow will do when that risk occurs.]
TESTABLE-BEHAVIOUR: [Write one Given–When–Then example with an observable result.]

## Initial Contributions

INITIAL-CONTRIBUTIONS: [List every member label and one first contribution for this lab.]
