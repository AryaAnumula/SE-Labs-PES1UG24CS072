# Lab 07: Fuzz Testing - Library Fines

Student: PES1UG24CS072

## Source and filenames

Assigned repository: [SETAPESU26/L6_L7_14_library_fines](https://github.com/SETAPESU26/L6_L7_14_library_fines/tree/main/Lab%207).

The assigned Lab 7 application is named `library_fines.py` upstream. It is
submitted here as `processor.py`, and the tests as `test_processor.py`, to match
the filenames required by the handout and submission instructions. The folder
name follows this repository's `Lab-01` through `Lab-06` convention.

At this first checkpoint, `processor.py` is byte-for-byte identical to the
upstream application (Git blob `6b645f56bdde64ace19b67cc6e22c154d91d0178`).
The tests are complete, but the application has not yet been fixed. This
checkpoint records the original behavior and failing fuzz tests before fixes.
It is not the final submission state.

## Files

- `processor.py`: the assigned application, with three functions and an interactive main program.
- `test_processor.py`: Hypothesis properties for all three functions.
- `requirements.txt`: test dependencies.
- `README.md`: provenance, input policy, and execution instructions.

## Expected behavior for hardening

The handout requires handling unexpected inputs without crashing. These tests
use the following policy, to be implemented in the correction checkpoint:

| Function | Valid input and result | Invalid input policy |
| --- | --- | --- |
| `parse_member_id` | A member prefix and a nonnegative number separated by `-`; return the uppercase prefix and integer number. | Return `None` for malformed IDs or non-string input. |
| `total_fine` | A CSV of nonnegative whole days; sum `2 * max(days - 14, 0)` for each book. | Return `None` for malformed CSV or non-string input; reject the entire list rather than calculating a partial fine. |
| `shelf_code` | Uppercase initials from the first two words; a one-word title uses one initial. | Return `""` for blank or non-string input. |

The properties cover arbitrary Unicode text, `None`, valid generated values,
missing separators, malformed CSV fields, whitespace-only and one-word titles,
and generated integers, floats, booleans, bytes, lists, and dictionaries.

## Setup

Use PowerShell in the repository root. A local `.venv` has already been created;
the following commands also allow recreating it on another machine:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\Lab-07\requirements.txt
cd .\Lab-07
```

Calling the virtual environment's Python directly avoids activation-policy issues.

## Capture evidence before the correction checkpoint

Run commands below from `Lab-07`.

1. Run the original application:

   ```powershell
   ..\.venv\Scripts\python.exe processor.py
   ```

   Enter `STU-1023`, `10,20,30`, and `Clean Code` at the three prompts.
   Take a screenshot showing the command, inputs, and all output: member
   `('STU', 1023)`, fine `44`, and shelf code `CC`.
   Save it as `screenshots/01_original_application.png`.

2. Run the complete tests:

   ```powershell
   ..\.venv\Scripts\python.exe -m pytest test_processor.py -v --tb=short
   ```

   Take a screenshot of the final summary. The verified baseline is
   **10 failed, 3 passed**. These failures are expected for the original code.
   Save it as `screenshots/02_original_test_summary.png`.

3. Capture the failing inputs for each of the three functions. Run these
   commands individually, and screenshot the error and Hypothesis's minimized
   failing example for each. Scroll or take additional screenshots as needed.

   ```powershell
   ..\.venv\Scripts\python.exe -m pytest test_processor.py::test_parse_member_id_no_crash -q --tb=short
   ..\.venv\Scripts\python.exe -m pytest test_processor.py::test_total_fine_no_crash -q --tb=short
   ..\.venv\Scripts\python.exe -m pytest test_processor.py::test_shelf_code_no_crash -q --tb=short
   ```

   Save as `screenshots/03_member_id_failure.png`,
   `screenshots/04_total_fine_failure.png`, and
   `screenshots/05_shelf_code_failure.png`.
   Hypothesis may report multiple distinct failures; generated examples and
   timings can vary. Empty strings and `None` expose crashes in all three functions.

Screenshots and optional logs in `evidence/` are local report material and are
ignored by Git, along with the virtual environment, Python caches, Hypothesis
database, handouts, and reference checkout. Keep the screenshots for the later
consolidated PDF.

After this checkpoint is committed and pushed, the next checkpoint will fix
`processor.py`, rerun the same tests, and capture the corrected application and
passing test results. The consolidated PDF and Google Form submission follow
after the final code is on GitHub.
