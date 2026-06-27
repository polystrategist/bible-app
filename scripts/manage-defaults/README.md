# Manage Defaults

Contributor tooling for the seed databases in `defaults/Main/`. The NiceGUI
admin (`admin.py`) has a left drawer with one section per database:

| Section          | Backing data               | Capability                                   |
| ---------------- | -------------------------- | -------------------------------------------- |
| Strong's         | `data/strongs.json`        | add / edit / delete → build + bump version   |
| Dictionary       | `data/Dictionary.db`       | search, paginate, add / edit / delete → ship |
| Cross References | `data/cross_references.db` | search, paginate, add / edit / delete → ship |

The tool works out of `data/`, so edits never touch the shipped `defaults/Main/`
copies until you explicitly **Save & ship**. Destructive and persisting actions
(delete, save, build, ship) all ask for confirmation first.

## Source-of-truth model (Strong's)

`strongs.db` is a **build artifact**, not something you edit directly. The
editable source of truth is `data/strongs.json`:

```
data/strongs.json   ← edit this (NiceGUI app or by hand); git-diffable
      │  build_strongs.py
      ▼
defaults/Main/strongs.db            ← generated SQLite shipped to the app
defaults/Main/strongs.version.json  ← bumped so clients pick up the new DB
```

Editing JSON instead of the binary keeps pull requests reviewable (you can see
exactly which entries changed) and means the version bump is automatic when you
build.

## Working copies (Dictionary, Cross References)

These are too large (176k / 433k rows) for a JSON source, so the admin edits a
**working copy** in `data/` instead. The copies are git-ignored (canonical lives
in `defaults/Main/`); `admin.py` auto-copies any missing one on first open, or
refresh them explicitly:

```bash
python sync_data.py
```

Add / edit / delete write straight to the `data/` copy. **Save & ship** then
copies that copy over `defaults/Main/` and bumps the version — for Cross
References that's `cross_references_version.json`; for Dictionary it's the
in-DB `version` table (`dictionary_version`). Both write a binary DB, so commit
the result knowing the diff won't be human-readable.

## Change logs

Every add / edit / delete (plus save / build / ship) is appended to a dated log
in `logs/`, so changes stay trackable even though the shipped DBs are opaque
binaries:

```
logs/strongs-2026-06-27.db.log
logs/dictionary-2026-06-27.db.log
logs/cross_references-2026-06-27.db.log
```

Each line is `timestamp | ACTION | identity | detail`, e.g.:

```
2026-06-27 11:13:58 | UPDATE | strong_number=G1 | kjv_def: '--Alpha' -> 'Alpha'
2026-06-27 11:14:10 | ADD    | rowid=176024 | word='zztest', wordtype='n', definition='x'
2026-06-27 11:15:02 | DELETE | id=5 | from_book=10, votes=59
```

These logs are committed (not git-ignored) so the change history is reviewable in
pull requests alongside the binary DB updates.

## Setup

Create a Python 3.13 virtual environment in `venv/` and install dependencies
once. The venv is git-ignored, so each contributor creates their own.

**Windows**

```powershell
cd "scripts/manage-defaults"
py -3.13 -m venv venv
./venv/Scripts/python.exe -m pip install -r requirements.txt
```

**macOS / Linux**

```bash
cd "scripts/manage-defaults"
python3 -m venv venv
./venv/bin/python -m pip install -r requirements.txt
```

## Usage

### Edit in the UI (recommended)

From the repo root, use the matching package.json script:

```bash
yarn manage:default:win      # Windows
yarn manage:default:mac      # macOS
yarn manage:default:linux    # Linux
```

Or launch directly from this folder:

```bash
./venv/Scripts/python.exe admin.py   # Windows
./venv/bin/python admin.py           # macOS / Linux
```

This opens a browser admin (NiceGUI, rendered with Vue 3 + Quasar) at
`http://localhost:8080`. Filter/search to find entries, use the per-row
**Edit** / **Delete** buttons in the Actions column, **➕ Add entry** for new
ones, then the header buttons:

- **Save to strongs.json** — writes your edits to the source file.
- **Build strongs.db + bump version** — rebuilds the shipped DB and bumps
  `strongs.version.json` (this is what ships an update to clients).
- **Reload** — discards in-memory edits and reloads from `strongs.json`.

Env overrides: `MANAGE_PORT` (default 8080), `MANAGE_SHOW=0` to not auto-open a
browser.

### Command line

`PY` below is `./venv/Scripts/python.exe` on Windows, `./venv/bin/python` on
macOS / Linux.

```bash
# Re-sync the JSON source from an existing DB (seed / recover).
PY extract_strongs.py

# Rebuild the DB from the JSON source.
PY build_strongs.py          # build only
PY build_strongs.py --bump   # build + bump version
```

## Files

| File                 | Purpose                                                       |
| -------------------- | ------------------------------------------------------------- |
| `admin.py`           | NiceGUI admin UI (left drawer: Strong's / Dictionary / Cross Refs). |
| `common.py`          | Shared paths, schema, and JSON/DB/version IO helpers.         |
| `extract_strongs.py` | `defaults/Main/strongs.db` → `data/strongs.json`.             |
| `build_strongs.py`   | `data/strongs.json` → `defaults/Main/strongs.db` (+ version). |
| `sync_data.py`       | Copy Dictionary/cross_references DBs into `data/` working copies. |
| `data/strongs.json`  | Strong's source of truth — commit changes here.               |
| `data/*.db`          | Git-ignored working copies of the large shipped DBs.          |
| `logs/*.db.log`      | Dated change logs (add / edit / delete / save / build / ship). |

## `strongs_dictionary` schema

| column          | notes                                          |
| --------------- | ---------------------------------------------- |
| `strong_number` | PRIMARY KEY — JSON object key (e.g. `G2274`).   |
| `language`      | `greek` or `hebrew`.                            |
| `lemma`         | original-language word.                         |
| `translit`      | transliteration.                                |
| `pronunciation` | Hebrew only (NULL for Greek).                   |
| `derivation`    | etymology note.                                 |
| `strongs_def`   | Strong's definition.                            |
| `kjv_def`       | KJV usage.                                       |
