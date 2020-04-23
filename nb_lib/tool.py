#!/usr/bin/env python
from .formatter import Formatter


def main(notebooks, output_format, destination_mode):
    fmt = Formatter(output_format=output_format, destination_mode=destination_mode)
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


def parse_args():
    import sys

    fmt_flag = "--format="
    destination_flag = "--fileDestinationMode="

    notebooks = []
    fmt = None
    destination = None
    args = sys.argv[1:]

    for arg in args:
        if arg.startswith(fmt_flag):
            fmt = arg.replace(fmt_flag, "")
        elif arg.startswith(destination_flag):
            destination = arg.replace(destination_flag, "")
        else:
            notebooks.append(arg)

    return notebooks, fmt or "md", destination or "same_place"


if __name__ == "__main__":

    notebooks, fmt, dest_mode = parse_args()
    main(notebooks, output_format=fmt, destination_mode=dest_mode)
