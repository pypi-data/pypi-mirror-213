from argparse import ArgumentParser
from pathlib import Path

from hgen._version import __version__

from .utils import cstr


def create_parser():
    prog = "hgen"
    parser = ArgumentParser(
        prog=prog,
        usage=f"{prog} [-hv] [-r] -I header.h [path ...]",
        description=cstr("green", "HGEN: Header prototype GENerator"),
    )
    parser.add_argument(
        "-I",
        "--includes",
        type=Path,
        default=Path(".") / "includes",
        required=True,
        help="Path to header file",
        metavar="",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively search for source files in subfolders",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        default=Path(".") / "src",
        help=(
            "List of paths to search for source files. "
            "Either directory or file works"
        ),
        metavar="",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=__version__
    )

    return parser


if __name__ == "__main__":
    from sys import argv

    argv.append("--version")
    parser = create_parser()
    args = parser.parse_args()
    print(args)
