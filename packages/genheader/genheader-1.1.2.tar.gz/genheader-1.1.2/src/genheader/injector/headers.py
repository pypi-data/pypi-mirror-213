from pathlib import Path

from genheader.utils import RegexRules, cstr, get_lines_from


def get_flag_span(lines: "list[str]") -> "tuple[int, int]":
    """
    Find the beginning and end line indices of the function flag header.

    Args:
        lines (list[str]): List of lines in the header file.

    Returns:
        tuple[int, int]: Beginning and end line indices of the function flag header.

    Raises:
        SyntaxError: Raised if the function flag header is not found.
    """
    begin = None
    for i, line in enumerate(lines):
        if RegexRules.FLAG_BEGIN.match(line):
            begin = i
        elif begin and any(reg.match(line) for reg in RegexRules.FLAG_END):
            return begin, i
    raise SyntaxError(cstr("red", "function flag header was never found"))


def cut_lines_by_flag_span(lines: "list[str]", span: "tuple[int, int]"):
    """
    Cut the lines in the header file based on the flag span.

    Args:
        lines (list[str]): List of lines in the header file.
        span (tuple[int, int]): Beginning and end line indices of the function flag header.

    Returns:
        tuple[list[str], list[str]]: Lines before the flag span and lines after the flag span.
    """
    return lines[: span[0] + 1], lines[span[1] :]


def try_insert(dest: Path, protos: "list[str]") -> bool:
    """
    Try to insert prototypes into the header file.

    Args:
        dest (Path): Path to the header file.
        protos (list[str]): List of prototypes to insert.

    Returns:
        bool: True if insertion is successful, False otherwise.
    """
    lines = get_lines_from(dest)
    try:
        before, after = cut_lines_by_flag_span(lines, get_flag_span(lines))
        dest.write_text("\n".join(before + protos + after))
        return True
    except SyntaxError:
        return False


def insert_prototypes(dest_path: Path, *, protos: "list[str]") -> None:
    """
    Insert prototypes into the header files.

    Args:
        dest_path (Path): Path to the header file or directory containing header files.
        protos (list[str]): List of prototypes to insert.

    Raises:
        NotImplementedError: Raised if neither header nor function definition flags are found.
    """
    def headererror():
        raise NotImplementedError(
            f"searched {dest_path.absolute()} but could not find "
            "neither header or function definition flags.\n"
            "a header in the given directory should contain "
            f"{RegexRules.FLAG_BEGIN}"
        )

    if not dest_path.is_dir():
        oper_ok = try_insert(dest_path, protos)
        if oper_ok:
            return
        else:
            headererror()

    for dest in dest_path.glob("**/*.h"):
        print(dest)
        oper_ok = try_insert(dest, protos)
        if oper_ok:
            break
    else:
        headererror()
