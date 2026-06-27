"""Build defaults/Main/strongs.db from data/strongs.json.

The JSON is the source of truth; this regenerates the shipped SQLite artifact
from it. Pass --bump to also increment defaults/Main/strongs.version.json, which
is what tells the desktop client to replace its installed copy.

Usage:
    python build_strongs.py            # rebuild strongs.db only
    python build_strongs.py --bump     # rebuild and bump the version file
"""

import argparse

import common


def build(bump=False):
    rows = common.load_rows_from_json()
    if not rows:
        raise SystemExit(
            f"No entries found in {common.JSON_PATH}. "
            "Run extract_strongs.py first to seed it from the DB."
        )
    count = common.build_db(rows)
    version = common.bump_version() if bump else common.read_version()
    return count, version, bump


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bump",
        action="store_true",
        help="increment strongs.version.json after building",
    )
    args = parser.parse_args()

    count, version, bumped = build(bump=args.bump)
    print(f"Wrote {count} entries to {common.DB_PATH}")
    print(f"Version {'bumped to' if bumped else 'unchanged at'} {version}")


if __name__ == "__main__":
    main()
