import sys
import re
from typing import Optional, Tuple

EMPTY_LOG = r"\`\`\`shell.*Replace this line with the important log contents\..*\`\`\`.*</details>.*<!-- # Or drag and drop the log file and delete the above detail part. -->.*"


def missing_log(issue_body: str) -> Optional[Tuple[str, str]]:
    match = re.search(EMPTY_LOG, issue_body, re.DOTALL)
    if match:
        return "Missing log file", "Please provide a log file if possible as it will help us debug the issue."
    return None


CHECKS = [
    missing_log
]


def output_problem(problem: Optional[Tuple[str, str]]) -> None:
    if problem:
        print(f"## {problem[0]}\n")
        print(f"{problem[1]}\n")


def main():
    issue_body = sys.argv[1]
    # print(issue_body)
    problems = []
    for check in CHECKS:
        result = check(issue_body)
        if result:
            problems.append(result)

    if problems:
        print("# The following problems were found:\n")
        for problem in problems:
            output_problem(problem)

        print("\nPlease consider these recommendations so we may help you better.")


if __name__ == "__main__":
    main()
