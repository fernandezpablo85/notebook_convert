#!/usr/bin/env python
import sys
import os
import nbformat
from nbconvert import RSTExporter
import pygit2
from pygit2 import GIT_STATUS_INDEX_NEW, GIT_STATUS_INDEX_MODIFIED

SUPPORTED_FORMATS = "rst"


def main(args):
    notebooks = args[1:]
    to_format = "rst"
    converted = [n for n in notebooks if convert(n, to_format=to_format)]
    none_converted = len(converted) == 0
    if len(converted) != 0:
        for c in converted:
            print(f"{c} {to_format} missing, had to be generated")
        exit(1)

    non_staged = [n for n in notebooks if not _is_staged_with_conversion(n, to_format)]
    if len(non_staged) != 0:
        for non_s in non_staged:
            print(f"{non_s} {to_format} representation is not staged")
        exit(1)

    exit(0)  # this is fine


def _convertion_format(notebook: str, to_format: str) -> str:
    return notebook.replace(".ipynb", f".{to_format}")


def convert(notebook: str, to_format="rst") -> bool:
    assert to_format in SUPPORTED_FORMATS, f"supported formats are {SUPPORTED_FORMATS}"
    assert os.path.exists(notebook), f"this should not happen, path {notebook} must exist"
    if not must_convert(notebook, to_format):
        return False

    do_convert(notebook, to_format)
    return True


def must_convert(notebook: str, to_format: str) -> bool:
    formatted_path = _convertion_format(notebook, to_format)

    if not os.path.exists(formatted_path):
        return True

    notebook_modified = os.stat(notebook).st_mtime
    formatted_modified = os.stat(formatted_path).st_mtime

    return notebook_modified > formatted_modified


def do_convert(notebook, to_format):
    print(f"{notebook} {to_format} format is outdated or inexistent, converting ...")
    with open(notebook, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
        body, resources = RSTExporter().from_notebook_node(nb)
        to_path = _convertion_format(notebook, to_format)
        with open(to_path, "w+", encoding="utf-8") as to_file:
            to_file.write(body)
        for key, value in resources.items():
            print(key)
            print(value)
    print(f"generated {to_path}")


def _is_staged_with_conversion(notebook, to_format):
    repo = pygit2.Repository(".")
    staged_statuses = set([GIT_STATUS_INDEX_NEW, GIT_STATUS_INDEX_MODIFIED])
    staged = [f for f, flag in repo.status().items() if flag in staged_statuses]
    out_file = _convertion_format(notebook, to_format)
    return (out_file in staged) and (notebook in staged)


if __name__ == "__main__":
    main(sys.argv)
