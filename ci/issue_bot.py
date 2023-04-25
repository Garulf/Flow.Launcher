import sys
import re
import os
import uuid
from typing import List, Optional, Tuple

EMPTY_LOG = r"\`\`\`shell.*Replace this line with the important log contents\..*\`\`\`.*</details>.*<!-- # Or drag and drop the log file and delete the above detail part. -->.*"


def missing_log(issue_body: str) -> Optional[Tuple[str, str]]:
    match = re.search(EMPTY_LOG, issue_body, re.DOTALL)
    if match:
        return "Missing log file", "Please provide a log file if possible as it will help us debug the issue."
    return None


CHECKS = [
    missing_log
]


def set_multiline_output(output: List[str]):
    if 'GITHUB_OUTPUT' not in os.environ:
        filename = f"{uuid.uuid4()}.md"
        os.environ['GITHUB_OUTPUT'] = filename
        print(f"::set-output name=filename::{filename}")
    with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
        for line in output:
            print(line, file=fh)


def output_problem(output: List[str], problem: Optional[Tuple[str, str]]) -> None:
    if problem:
        output.append(f"## {problem[0]}")
        output.append("")
        output.append(f"{problem[1]}")
        output.append("")


def main():
    issue_body = sys.argv[1]
    # print(issue_body)
    problems = []
    for check in CHECKS:
        result = check(issue_body)
        if result:
            problems.append(result)

    if problems:
        output = []
        output.append("# The following problems were found:")
        output.append("")
        for problem in problems:
            output_problem(output, problem)

        output.append("\nPlease consider these recommendations so we may help you better.")

        set_multiline_output(output)


if __name__ == "__main__":
    main()
