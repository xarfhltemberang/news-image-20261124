#!/usr/bin/env python3
"""Ship the pre-rendered front page to the grader's output directory.

The entry image is rendered ahead of time by draw.py and stored in this
repository as entry.png. This program only copies that file to the
location the grader expects, so it needs nothing but the standard
library and no network access.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    target_dir = os.path.expanduser(
        os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.png")
    )
    # MAKEFUN_OUTPUT_DIR may name a directory or the file itself.
    if target_dir.endswith(".png"):
        destination = target_dir
        folder = os.path.dirname(destination)
    else:
        folder = target_dir
        destination = os.path.join(folder, "entry.png")
    if folder:
        os.makedirs(folder, exist_ok=True)
    if not os.path.isfile(source):
        print(f"missing shipped image: {source}", file=sys.stderr)
        return 1
    shutil.copyfile(source, destination)
    print(f"copied {source} -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
