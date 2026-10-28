# Lab 5: Reflection

**1. Which issues were the easiest and which were the hardest to fix?**

The easiest ones were the formatting and naming warnings. Things like long lines, missing blank lines, camelCase function names and missing docstrings are just tedious, and I could fix them without touching the logic. The hardest was the eval call. Bandit suggests ast.literal_eval as the safer option, but that doesn't work for a rule like 500000 + 150000, so I ended up writing a small evaluator with the ast module that only allows numbers and basic arithmetic.

**2. Did the tools report any false positives?**

Not really, since every warning pointed at something real in the code. But a few of them needed some thought before I applied the fix. The literal_eval suggestion from Bandit didn't fit this program, and Pylint and Flake8 disagree on line length (100 vs 79), so a line can pass one tool and still fail the other. A lot of the Pylint messages are also more about style than actual bugs.

**3. How would you use static analysis in a real project?**

I'd set Flake8 and Pylint up as pre-commit hooks so style problems get caught before the code is even committed. Then I'd run Bandit and Pylint in CI on every pull request and fail the build if there's a medium or high Bandit finding or the Pylint score drops below an agreed number. That way the checks happen on their own and nobody has to remember to run them.

**4. What improved after the fixes?**

The two security problems are gone. The SQL query can't be changed through the input anymore and the salary rule can't run arbitrary code. Errors in update_status are logged now instead of being hidden, shortlist always returns a list, and the report file gets closed properly. The code is easier to read too, with proper names and docstrings. Pylint went from 4.47 to 10.00, Bandit from 3 issues to 0 and Flake8 from 8 messages to 0, and the program still prints the same output.