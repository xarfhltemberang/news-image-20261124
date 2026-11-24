#!/usr/bin/env python3
"""Copies the pre-rendered news infographic (entry.png) to the
grader's output directory.

The grader sandbox runs this file with ``python3 -P -s`` in a
python:3.13-slim image that contains only the standard library, so
this program uses nothing but the stdlib: it simply copies the
pre-rendered entry.png that ships in this repository to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).

The image itself was drawn by draw.py (Pillow), which is kept in this
repository as the record of how entry.png was made; the grader never
runs draw.py.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png not found next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    except OSError as exc:
        print("error: could not write entry.png: %s" % exc, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
