import ast
import logging
import operator
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE applicants (id INTEGER PRIMARY KEY, name TEXT, role TEXT, expected_salary INTEGER, status TEXT)")

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
    return _calc(ast.parse(rule, mode="eval").body)


def addApplicant(name, role, expected_salary, status="applied"):
    conn.execute("INSERT INTO applicants (name, role, expected_salary, status) VALUES (?, ?, ?, ?)", (name, role, expected_salary, status))
    conn.commit()


def shortlist(role, salary_rule):
    rows = conn.execute("SELECT name, expected_salary FROM applicants WHERE role = ?", (role,)).fetchall()
    limit = parse_salary_rule(salary_rule)
    total_seen = len(rows)
    result = []
    for name, salary in rows:
        if salary <= limit:
            result.append(name)
    if result:
        return result


def updateStatus(applicant_id, status):
    try:
        conn.execute("UPDATE applicants SET status = ? WHERE id = ?", (status, applicant_id))
        conn.commit()
    except sqlite3.Error:
        logging.exception("Could not update applicant %s", applicant_id)

def exportReport(path):
    f = open(path, "w")
    for row in conn.execute("SELECT name, role, status FROM applicants"):
        f.write(",".join(row) + "\n")
    f.close()


def countByStatus(status):
    return conn.execute("SELECT COUNT(*) FROM applicants WHERE status = ?", (status,)).fetchone()[0]


def main():
    addApplicant("Nina", "analyst", 600000)
    addApplicant("Omar", "analyst", 750000, "interview")
    addApplicant("Priya", "developer", 900000)
    updateStatus(1, "interview")
    print(shortlist("analyst", "500000 + 150000"))
    exportReport("applicants_report.csv")
    print(countByStatus("interview"), "in interview")


main()