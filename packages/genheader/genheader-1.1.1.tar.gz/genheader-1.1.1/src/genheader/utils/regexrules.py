#!/usr/bin/env python3

from re import IGNORECASE, compile


# Function to create a regular expression pattern for flagged comments
def _make_flagged_comment_regex(which):
    COMMENT_BEGIN = r"[/][/*].*"
    return compile(rf"{COMMENT_BEGIN}{which}", IGNORECASE)


class RegexRules:
    """Regex Rules to parse *.c and *.h files."""

    FUNCTION = compile(r"^(?P<type>([\w\*]+\s+)+)(?P<name>[\w\*]+\()")
    FLAG_BEGIN = _make_flagged_comment_regex(r"@(func|functions?)\b")
    FLAG_END = [
        compile("#endif"),
        _make_flagged_comment_regex(r"=+.*=+"),
        _make_flagged_comment_regex(r"@end\b"),
    ]


if __name__ == "__main__":
    print(RegexRules.FUNCTION)
    print(RegexRules.FLAG_BEGIN)
