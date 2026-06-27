"""Extract defaults/Main/strongs.db into data/strongs.json (the source of truth).

Run this once to seed strongs.json from the existing shipped DB, or any time you
want to re-sync the JSON with a DB that was changed elsewhere.

Usage:
    python extract_strongs.py
"""

import common


def main():
    rows = common.load_rows_from_db()
    count = common.save_rows_to_json(rows)
    by_lang = {}
    for row in rows:
        by_lang[row["language"]] = by_lang.get(row["language"], 0) + 1
    for language, n in sorted(by_lang.items()):
        print(f"  {language:7} {n:>6} entries")
    print(f"Wrote {count} entries to {common.JSON_PATH}")


if __name__ == "__main__":
    main()
