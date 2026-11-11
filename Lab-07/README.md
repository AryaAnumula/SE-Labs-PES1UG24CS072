# Lab 07: Fuzz Testing - Library Fines

Student: PES1UG24CS072

## Source and filenames

Assigned repository: [SETAPESU26/L6_L7_14_library_fines](https://github.com/SETAPESU26/L6_L7_14_library_fines/tree/main/Lab%207).

The assigned Lab 7 application is named `library_fines.py` upstream. It is
submitted here as `processor.py`, and the tests as `test_processor.py`, to match
the filenames required by the handout and submission instructions. The folder
name follows this repository's `Lab-01` through `Lab-06` convention.

The original application and initial completed tests are preserved in commit
`19e0306` (`Add Lab-07 original application and Hypothesis fuzz tests`). The
original application's upstream Git blob is
`6b645f56bdde64ace19b67cc6e22c154d91d0178`.

The current application includes the validation fixes. Verification on Python
3.13.12, pytest 9.2.0, and Hypothesis 6.170.15:

- Original checkpoint: **10 failed, 3 passed**.
- Corrected application: **15 passed** (the original 13 properties plus two
  numeric-validation properties).
- Valid, malformed, and blank interactive input sequences all exit successfully.

## Files

- `processor.py`: the assigned application, with three functions and an interactive main program.
- `test_processor.py`: Hypothesis properties for all three functions.
- `requirements.txt`: test dependencies.
- `README.md`: provenance, input policy, and execution instructions.
- `screenshots/`: eight screenshots documenting original execution, fuzz-test
  failures, corrected execution, and the passing final tests.

## Input behavior

The application handles unexpected inputs without crashing using this policy:

| Function | Valid input and result | Invalid input policy |
| --- | --- | --- |
| `parse_member_id` | A letter prefix and a nonnegative decimal number separated by one `-`; trim surrounding field whitespace and return the uppercase prefix and integer number. | Return `None` for malformed IDs or non-string input. |
| `total_fine` | A CSV of nonnegative decimal whole days; allow surrounding field whitespace and sum `2 * max(days - 14, 0)` for each book. | Return `None` for malformed CSV or non-string input; reject the entire list rather than calculating a partial fine. |
| `shelf_code` | Uppercase initials from the first two words; a one-word title uses one initial. | Return `""` for blank or non-string input. |

The properties cover arbitrary Unicode text, `None`, valid generated values,
missing separators, malformed CSV fields, whitespace-only and one-word titles,
and generated integers, floats, booleans, bytes, lists, and dictionaries.
Numeric validation rejects signed numbers, fractions, exponents, underscores,
and digit-like characters that are not decimal digits. If Python's integer
conversion limit rejects an excessively long number, the function returns
`None`. Explicit examples replay missing values, empty strings, a short title,
and 5,000-digit numbers.

## Bugs fixed

| Original defect | Correction |
| --- | --- |
| Calling `.split()` on `None` or other non-string values raised errors. | Check the input type before parsing. |
| Missing/extra member-ID separators, invalid prefixes, or malformed numbers were not validated. | Validate the complete ID and return `None` on invalid input. |
| Empty, malformed, or negative CSV fields crashed or were silently accepted. | Validate every field and reject the entire list on an invalid value. |
| Empty and one-word titles raised `IndexError`. | Take initials from the available first two words safely. |
| Invalid CLI input stopped the application before later prompts. | Display a useful message and continue to the next operation. |

## Setup

Use PowerShell in the repository root. A local `.venv` has already been created;
the following commands also allow recreating it on another machine:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\Lab-07\requirements.txt
cd .\Lab-07
```

Calling the virtual environment's Python directly avoids activation-policy issues.

## Saved original screenshots

The two original user-provided screenshots are saved as:

- `screenshots/01_original_application.png`: original execution with valid inputs.
- `screenshots/02_original_test_results.png`: the original test outcome list.

The second image shows the test outcomes but does not show exception details
or minimized failing inputs. Capture those details as described below for the
report. All commands below run from `Lab-07`.

## Capture original failure details

A local, ignored copy of the original application and original tests is stored
in `evidence/original/`. Its test file is named `original_fuzz_checks.py` to keep
it out of ordinary test discovery. It is unchanged from the first checkpoint
apart from that filename. This local snapshot is for reproducing report evidence;
the committed original is always available at `19e0306`.

Run each command individually. Capture the exception and Hypothesis's minimized
failing input for that function. Scroll or take additional screenshots as needed.

```powershell
..\.venv\Scripts\python.exe -m pytest evidence/original/original_fuzz_checks.py::test_parse_member_id_no_crash -q --tb=short
..\.venv\Scripts\python.exe -m pytest evidence/original/original_fuzz_checks.py::test_total_fine_no_crash -q --tb=short
..\.venv\Scripts\python.exe -m pytest evidence/original/original_fuzz_checks.py::test_shelf_code_no_crash -q --tb=short
```

Save as `screenshots/03_member_id_failure.png`,
`screenshots/04_total_fine_failure.png`, and
`screenshots/05_shelf_code_failure.png`.
These tests must fail because they target the original code. The verified full
baseline log is also saved in `evidence/original_test_failures.txt`.

## Capture corrected execution and final tests

Run the corrected application:

```powershell
..\.venv\Scripts\python.exe processor.py
```

Enter `STU-1023`, `10,20,30`, and `Clean Code` to confirm the original valid
results remain `('STU', 1023)`, `44`, and `CC`.
Save the screenshot as `screenshots/06_corrected_application.png`.

Run it again with `STU-`, `10,,30`, and `Clean`. It should display validation
messages for the first two values, continue running, and show `Shelf Code: C`.
Save the screenshot as `screenshots/07_corrected_invalid_inputs.png`.

Finally, run the corrected test suite:

```powershell
..\.venv\Scripts\python.exe -m pytest test_processor.py -v --tb=short
```

Capture all test results and the **15 passed** summary in
`screenshots/08_final_tests_passed.png`.

Include the `screenshots/` folder in the Git submission and reuse its eight
images in the consolidated PDF. The original replay copies and optional logs
in `evidence/` remain local and ignored by Git, along with the virtual
environment, Python caches, Hypothesis database, handouts, and reference checkout.

The final submission still requires one consolidated PDF containing the required
screenshots and both Python source files. Commit and push the corrected code
before submitting that PDF through the provided Google Form.
