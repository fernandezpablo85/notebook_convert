#!/usr/bin/env python
from .formatter import Formatter


def main(args):
    notebooks = args[1:]
    fmt = Formatter(output="pdf")
    converted = [n for n in notebooks if convert(fmt, file=n)]
    if converted:
        exit(1)

    non_staged = [n for n in notebooks if not is_staged_with_conversion(fmt, file=n)]
    for non_s in non_staged:
        print(f"{fmt.dst_path(non_s)} is not staged")

    if non_staged:
        exit(1)

    exit(0)  # this is fine


def convert(fmt: Formatter, file: str) -> bool:
    if not fmt.needs_format(file):
        return False

    print(f"{fmt.dst_path(file)} is outdated or inexistent, converting... ", end="")
    fmt.convert(file)
    print("OK")

    return True


def is_staged_with_conversion(fmt: Formatter, file: str) -> bool:
    from .git import is_staged

    out_file = fmt.dst_path(file)
    return is_staged(file) and is_staged(out_file)


if __name__ == "__main__":
    import sys

    main(sys.argv)
