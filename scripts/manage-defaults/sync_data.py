"""Copy the large default DBs into data/ as the admin's working copies.

Strong's uses data/strongs.json (seeded by extract_strongs.py). Dictionary and
cross_references are too big for a JSON source, so the admin works on a copy of
the shipped DB here in data/. Run this to (re)sync those copies from
defaults/Main — the admin also auto-copies any missing one on first open.

Usage:
    python sync_data.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS_DIR = os.path.join(HERE, "..", "..", "defaults", "Main")
DATA_DIR = os.path.join(HERE, "data")

DBS = ["Dictionary.db", "cross_references.db"]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    for name in DBS:
        dst = os.path.join(DATA_DIR, name)
        shutil.copy2(os.path.join(DEFAULTS_DIR, name), dst)
        print(f"copied {name} ({os.path.getsize(dst) / 1048576:.1f} MB)")


if __name__ == "__main__":
    main()
