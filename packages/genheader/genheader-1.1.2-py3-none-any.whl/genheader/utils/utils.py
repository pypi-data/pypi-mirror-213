#!/usr/bin/env python3

from pathlib import Path

from genheader.utils.colors import cstr

TAB = "\t"


# Function to read lines from a file
def get_lines_from(file: Path) -> "list[str]":
    return file.read_text().splitlines(keepends=False)


# Function to visualize the paths
def visualize(dest_path: Path, src_path: Path):
    cols = {"d": "", "s": ""}
    for n, path in (("d", dest_path), ("s", src_path)):
        p = path.resolve()
        cols[n] += (
            cstr("cyan", f"{p.parent.parent.name}/")
            + cstr("yellow", f"{p.parent.name}/")
            + cstr("red", p.name)
        )
    print(f"{cols['s']} -> {cols['d']}")
