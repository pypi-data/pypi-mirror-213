import re
from typing import List
from ansi2html import Ansi2HTMLConverter
import strip_ansi


def fold_regex_lines(lines: List[str], regex: str) -> str:
    """
    Refactored code
    Search each line of console output and look for a regex match.
    If a line contains a regex match, then the line is folded.
    Consecutive lines that match the regex are folded together.
    """
    converter = Ansi2HTMLConverter()

    html_str = ""
    fold_started = False

    for line in lines:
        line_stripped = strip_ansi.strip_ansi(line)
        line_converted = converter.convert(line, full=False)

        match = re.search(regex, line_stripped)
        if match:
            if not fold_started:
                fold_started = True
                html_str += (
                    f"<details><summary style='nobr'>Folded RegEx: '{regex}'</summary>"
                )
            html_str += line_converted

        elif fold_started:
            fold_started = False
            html_str += "</details>"
            html_str += f"{line_converted}"

        else:
            html_str += line_converted

    return html_str


def main():
    with open("/Users/jwr003/coding/pytest-tui/ptt_files/test.ansi" , "r") as f:
        lines = f.readlines()
    html_str = fold_regex_lines(lines, "  \*->")
    print(html_str)
    with open("/Users/jwr003/coding/pytest-tui/ptt_files/test.html" , "w") as f:
        f.write(html_str)


if __name__ == "__main__":
    main()
