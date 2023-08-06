#!/usr/bin/env python3

from itertools import chain
from pathlib import Path

from genheader.proto import Protos
from genheader.utils import TAB, cprint, cstr


def _crawl_prototypes(src_path: Path) -> "list[Protos]":
    def crawl_file(src: Path):
        status, res = "green", ""
        try:
            target = Protos(src)
            res = f"(x{len(target)})"
            # Append the Protos instance to the results list
            results.append(target)
        except ValueError:
            status, res = "yellow", "none"
        finally:
            # Print the status and file name
            print(f"{cstr(status, f'{res} in')} {cstr('blue', src.name)}")

    def checked(results: "list[Protos]"):
        if not len(results):
            raise ValueError(
                cstr(
                    "red",
                    f"no function prototypes found in {src_path}",
                )
            )
        return results

    results: list[Protos] = []
    # Print the source path in magenta color
    cprint("magenta", f">> from {src_path}")

    if not src_path.is_dir():
        crawl_file(src_path)
        return checked(results)

    for src in sorted(src_path.glob("**/*.c")):
        crawl_file(src)

    return checked(results)


# This function aligns the indentation of the prototypes
def _align_protos_indentation(protolist: "list[Protos]"):
    def before_len(proto):
        return len(proto.split(TAB)[0])

    def get_longest_funcname_len():
        result = 0
        for container in protolist:
            for proto in container:
                funcname_parts = proto.split("(")[0].rsplit(" ", maxsplit=1)
                if len(funcname_parts) > 1:
                    result = max(result, len(funcname_parts[1]))
        return result

    def in_loop():
        parts = proto.split("(")
        if len(parts) < 2:
            return [proto]

        funcname_params = parts[0]
        params = parts[1].rstrip(")").split(", ")

        funcname_parts = funcname_params.rsplit(" ", maxsplit=1)
        if len(funcname_parts) < 2:
            return [proto]

        types, funcname = funcname_parts

        to_pad = longest // 4 - before_len(proto) // 4
        nl_tabs = TAB * (1 + len(types) // 4 + to_pad)

        result = [f"{types}{TAB * to_pad}{funcname}("]
        i = 0
        while True:
            is_first = True
            while len(params) and len(result[i].replace(TAB, "....") + params[0]) < 79:
                if is_first:
                    is_first = False
                else:
                    result[i] += " "
                result[i] += params.pop(0)
                if len(params):
                    result[i] += ","
            i += 1
            if len(params):
                result.append(nl_tabs)
            else:
                break

        # Add a condition to handle #endif
        if "endif" in proto:
            result.append("")

        return result

    longest = get_longest_funcname_len()

    for container in protolist:
        results = []
        for proto in container:
            result = in_loop()
            results.append("\n".join(result))

        # Add a newline before the last prototype in the container
        if results:
            results[-1] += "\n"

        container.prototypes = results




def _protolist_to_strlist(protolist: "list[Protos]") -> "list[str]":
    return [repr(s) for s in chain(protolist)]


def get_prototypes(src_path: Path) -> "list[str]":
    protolist = _crawl_prototypes(src_path)
    _align_protos_indentation(protolist)
    return _protolist_to_strlist(protolist)


if __name__ == "__main__":
    try:
        results = get_prototypes(Path("../so_long/src"))
    except ValueError as e:
        print(e, "\n====")
        print(get_prototypes(Path("../so_long/lib/src")))
