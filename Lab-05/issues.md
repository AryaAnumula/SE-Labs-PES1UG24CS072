# Lab 5: Static Code Analysis

File analysed: recruitment_tracker.py (line numbers are from the original version)

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| SQL injection in addApplicant (Bandit B608) | Security, medium | 8 | The INSERT query was built with an f-string, so a name with a quote in it could break the query or change what gets stored. | Used a parameterized query with ? placeholders and passed the values separately. |
| eval() on the salary rule (Bandit B307) | Security, medium | 14 | eval will run whatever text is passed in as the rule, which means anyone controlling that input can run their own code. | Wrote a small parser using the ast module that only accepts numbers with +, - and *. Bandit suggests ast.literal_eval but that can't handle 500000 + 150000. |
| try/except/pass in updateStatus (Bandit B110, Pylint W0718) | Reliability, low | 26 to 29 | Any error got swallowed, so a failed update looked exactly like a successful one. | Now only catches sqlite3.Error and logs it with logging.exception. |
| shortlist returns two different types (Pylint R1710) | Bug | 12 to 21 | It returned a list when someone matched and None when nobody did, so the caller has to check for both. | It now always returns a list (empty if nobody matches) using a list comprehension. |
| Unused variable total_seen (Pylint W0612, Flake8 F841) | Code quality | 15 | The variable was calculated but never used anywhere. | Deleted it. |
| File opened without with (Pylint R1732, W1514) | Resource handling | 32 to 35 | exportReport opened the file and closed it by hand, so a failed write would leave it open. No encoding was given either. | Used with open(..., encoding="utf-8", newline="") and the csv module for writing rows. |
| Function names not in snake_case (Pylint C0103) | Style | 7, 24, 31, 38 | addApplicant, updateStatus, exportReport and countByStatus use camelCase instead of PEP 8 names. | Renamed them to add_applicant, update_status, export_report and count_by_status and fixed the calls in main. |
| Missing docstrings (Pylint C0114, C0116) | Documentation | 1, 7, 12, 24, 31, 38, 42 | Neither the module nor any function had a docstring. | Added a one line docstring to the module and to every function. |
| Lines too long (Flake8 E501, Pylint C0301) | Style | 4, 8, 13, 26, 39 | A few lines went past 79 characters, mostly the SQL strings. | Split the long strings and arguments over several lines. |
| Trailing whitespace (Flake8 W291, Pylint C0303) | Style | 15 | There were extra spaces at the end of a line. | Removed them. |
| Missing blank line (Flake8 E302) | Style | 31 | Only one blank line before exportReport instead of two. | Added the second blank line. |

## Results before and after

| Tool | Before | After |
| ---- | ------ | ----- |
| Pylint | 4.47/10 | 10.00/10 |
| Bandit | 3 issues (2 medium, 1 low) | 0 issues |
| Flake8 | 8 messages | 0 messages |

The program prints the same output as before the changes (['Nina'] and 2 in interview).