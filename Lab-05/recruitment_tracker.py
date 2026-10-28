"""Applicant tracking system backed by an in-memory SQLite database."""
import ast
import csv
import logging
import operator
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE applicants (id INTEGER PRIMARY KEY, name TEXT, role TEXT, "
    "expected_salary INTEGER, status TEXT)"
)

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul}


def _calc(node):
    number = isinstance(node, ast.Constant)
    if number and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        op = OPS[type(node.op)]
        return op(_calc(node.left), _calc(node.right))
    raise ValueError("unsupported salary rule")


def parse_salary_rule(rule):
    """Safely evaluate a simple arithmetic rule like '500000 + 150000'."""
    return _calc(ast.parse(rule, mode="eval").body)


def add_applicant(name, role, expected_salary, status="applied"):
    """Insert a new applicant into the database."""
    conn.execute(
        "INSERT INTO applicants (name, role, expected_salary, status) VALUES (?, ?, ?, ?)",
        (name, role, expected_salary, status),
    )
    conn.commit()


def shortlist(role, salary_rule):
    """Return names of applicants for a role within the salary limit."""
    rows = conn.execute(
        "SELECT name, expected_salary FROM applicants WHERE role = ?", (role,)
    ).fetchall()
    limit = parse_salary_rule(salary_rule)
    return [name for name, salary in rows if salary <= limit]


def update_status(applicant_id, status):
    """Update the hiring status of an applicant."""
    try:
        conn.execute(
            "UPDATE applicants SET status = ? WHERE id = ?",
            (status, applicant_id),
        )
        conn.commit()
    except sqlite3.Error:
        logging.exception("Could not update applicant %s", applicant_id)

def export_report(path):
    """Write name, role and status of every applicant to a CSV file."""
    rows = conn.execute("SELECT name, role, status FROM applicants")
    with open(path, "w", encoding="utf-8", newline="") as csv_file:
        csv.writer(csv_file).writerows(rows)


def count_by_status(status):
    """Count applicants with the given status."""
    return conn.execute("SELECT COUNT(*) FROM applicants WHERE status = ?", (status,)).fetchone()[0]


def main():
    """Run a short demonstration."""
    add_applicant("Nina", "analyst", 600000)
    add_applicant("Omar", "analyst", 750000, "interview")
    add_applicant("Priya", "developer", 900000)
    update_status(1, "interview")
    print(shortlist("analyst", "500000 + 150000"))
    export_report("applicants_report.csv")
    print(count_by_status("interview"), "in interview")


if __name__ == "__main__":
    main()