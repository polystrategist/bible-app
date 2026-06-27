"""Shared paths, schema, and IO helpers for managing the default databases.

Source-of-truth model for strongs.db:

    data/strongs.json   <- editable, git-diffable source of truth
        | build_strongs.py / build_db()
        v
    defaults/Main/strongs.db        <- shipped binary artifact
    defaults/Main/strongs.version.json  <- bumped when shipping

The JSON is what contributors edit (via the NiceGUI admin or by hand). The DB
and version file are generated outputs, so changes are reviewable as text diffs
in git instead of opaque binary blobs.
"""

import json
import os
import sqlite3

# scripts/manage-defaults/common.py -> repo root is two levels up.
HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))

JSON_PATH = os.path.join(HERE, "data", "strongs.json")
DB_PATH = os.path.join(REPO_ROOT, "defaults", "Main", "strongs.db")
VERSION_PATH = os.path.join(REPO_ROOT, "defaults", "Main", "strongs.version.json")

TABLE = "strongs_dictionary"

# strong_number is the primary key / JSON object key; the rest are the entry's
# fields. Order here is the column order used in the DB and the JSON entries.
KEY_COLUMN = "strong_number"
ENTRY_FIELDS = [
    "language",
    "lemma",
    "translit",
    "pronunciation",
    "derivation",
    "strongs_def",
    "kjv_def",
]
COLUMNS = [KEY_COLUMN] + ENTRY_FIELDS


def sort_key(strong_number):
    """Stable sort: by testament letter (G before H), then numeric id.

    Keeps JSON diffs minimal and predictable across regenerations.
    """
    prefix = strong_number[:1]
    try:
        num = int(strong_number[1:])
    except ValueError:
        num = 0
    return (prefix, num, strong_number)


def _clean(value):
    """Normalize a cell to a stripped string, or None if empty."""
    if value is None:
        return None
    text = str(value).strip()
    return text or None


# --- JSON (source of truth) -------------------------------------------------

def load_rows_from_json(path=JSON_PATH):
    """Return a list of full row dicts (every column present, missing -> "")."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    rows = []
    for strong_number, entry in data.items():
        row = {KEY_COLUMN: strong_number}
        for field in ENTRY_FIELDS:
            row[field] = entry.get(field) or ""
        rows.append(row)
    rows.sort(key=lambda r: sort_key(r[KEY_COLUMN]))
    return rows


def save_rows_to_json(rows, path=JSON_PATH):
    """Write row dicts to JSON as a sorted object keyed by strong_number.

    Empty fields are omitted so entries stay compact and diffs stay readable.
    Returns the number of entries written.
    """
    obj = {}
    for row in sorted(rows, key=lambda r: sort_key(r[KEY_COLUMN])):
        key = _clean(row.get(KEY_COLUMN))
        if not key:
            continue  # skip rows without an id
        entry = {}
        for field in ENTRY_FIELDS:
            cleaned = _clean(row.get(field))
            if cleaned is not None:
                entry[field] = cleaned
        obj[key] = entry

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return len(obj)


# --- SQLite (shipped artifact) ----------------------------------------------

def load_rows_from_db(path=DB_PATH):
    """Return a list of full row dicts read from an existing strongs.db."""
    conn = sqlite3.connect(path)
    try:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(f"SELECT {', '.join(COLUMNS)} FROM {TABLE}")
        rows = []
        for record in cur.fetchall():
            rows.append({col: (record[col] or "") for col in COLUMNS})
    finally:
        conn.close()
    rows.sort(key=lambda r: sort_key(r[KEY_COLUMN]))
    return rows


def build_db(rows, path=DB_PATH):
    """(Re)create strongs.db from row dicts. Returns the row count written."""
    if os.path.exists(path):
        os.remove(path)

    conn = sqlite3.connect(path)
    try:
        conn.execute(
            f"""
            CREATE TABLE {TABLE} (
                strong_number TEXT PRIMARY KEY,
                language      TEXT NOT NULL,
                lemma         TEXT,
                translit      TEXT,
                pronunciation TEXT,
                derivation    TEXT,
                strongs_def   TEXT,
                kjv_def       TEXT
            )
            """
        )
        payload = [
            tuple(_clean(row.get(col)) for col in COLUMNS)
            for row in sorted(rows, key=lambda r: sort_key(r[KEY_COLUMN]))
            if _clean(row.get(KEY_COLUMN))
        ]
        conn.executemany(
            f"INSERT INTO {TABLE} ({', '.join(COLUMNS)}) "
            f"VALUES ({', '.join('?' * len(COLUMNS))})",
            payload,
        )
        conn.execute(f"CREATE INDEX idx_strongs_language ON {TABLE}(language)")
        conn.commit()
    finally:
        conn.close()
    return len(payload)


# --- Version file -----------------------------------------------------------

def read_version(path=VERSION_PATH):
    """Return the current shipped version number (0 if missing/empty)."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return 0
    with open(path, "r", encoding="utf-8") as fh:
        return int(json.load(fh).get("version", 0))


def bump_version(path=VERSION_PATH):
    """Increment the version by 1 and write it back. Returns the new version."""
    new_version = read_version(path) + 1
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"version": new_version}, fh, indent=4)
        fh.write("\n")
    return new_version
