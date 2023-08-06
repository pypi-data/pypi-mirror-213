from argparse import Namespace
from pathlib import Path
from sys import argv, stderr

from genheader.injector import insert_prototypes
from genheader.proto import get_prototypes
from genheader.utils import create_parser, visualize


def update_header_prototypes(args: Namespace):
    prototypes: list[str] = []

    dest_path = args.includes

    for path in args.paths:
        if args.recursive and path.is_dir():
            for src_path in path.glob("**/*.c"):
                visualize(dest_path, src_path)
                prototypes.extend(get_prototypes(src_path))
        else:
            src_path = path
            visualize(dest_path, src_path)
            prototypes.extend(get_prototypes(src_path))

    insert_prototypes(dest_path, protos=prototypes)


def main():
    parser = create_parser()
    if len(argv) == 1:
        parser.print_usage(stderr)
        exit()

    args = parser.parse_args()
    update_header_prototypes(args)


if __name__ == "__main__":
    main()
