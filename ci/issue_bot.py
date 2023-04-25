import sys

EMPTY_LOG = "Replace this line with the important log contents."


def missing_log(body: str):
    if EMPTY_LOG in body:
        return "In order to help us debug your issue please provide a log file. Thank you!"


CHECKS = [
    missing_log
]


def main():
    issue_body = sys.argv[1]
    problems = []
    for check in CHECKS:
        result = check(issue_body)
        if result:
            problems.append(result)

    if problems:
        print("The following problems were found:")
        for problem in problems:
            print(f"* {problem}")
