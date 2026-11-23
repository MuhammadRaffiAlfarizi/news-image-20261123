#!/usr/bin/env python3
"""Entry program for make.fun news-image-20261123.

Writes the entry image to /output/entry.png. The image is held in this
repository as entry.png (a 1024x1024 PNG of the day's world news, drawn by
render.py), so this program only copies it: stdlib only, no network, no
clock, no randomness, both runs write exactly the same bytes.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")


if __name__ == "__main__":
    main()
