# Modules Turso

Content-authoring and staging area for **Believers Sword** downloadable **modules** — Bible
translations and chapter commentaries — packaged as SQLite databases, plus the generator
scripts that produce them.

This folder is **not shipped inside the app**. It is a workspace where module data is
scraped, generated, converted, and prepared before being published to users (who download
individual modules from within the app).

## Why "Turso"?

[Turso](https://turso.tech/) is a hosted database service built on
[libSQL](https://github.com/tursodatabase/libsql), a fork of **SQLite**. Its model is to
take ordinary SQLite databases, host/replicate them in the cloud, and sync them down to
local embedded replicas (local-first).

Everything in this folder is SQLite (`.SQLite3` / `.db`) — the exact format libSQL/Turso
hosts — so the name marks these as "the SQLite modules destined for Turso." The commentary
schema is also built local-first: every table carries `sync_status`
(`local` / `synced` / `pending` / `conflict`) and `server_id` columns, the standard shape
for data that syncs up to a remote libSQL/Turso server.

> ⚠️ **Note:** there is currently **no Turso/libSQL client code** in this repository. The
> generators write plain local SQLite files. The "Turso" name is organizational — it
> describes where this content is headed (and how its schema is modeled), not an active
> integration. If/when a real Turso backend is wired up, this is the data that feeds it.

## Directory layout

```
Modules Turso/
├── Bible/                 Finished MyBible-format Bible modules (.SQLite3) + source notes
├── zipped/                Zipped Bible modules (distribution-ready archives)
├── Commentaries/          AI commentary database, schema, generator, and JSON backups
│   ├── commentary_schema.sql
│   ├── generate_commentaries_batch.py
│   ├── believers_sword_commentaries.db
│   ├── commentary_generation_progress.json
│   ├── commentary_generation_log.jsonl
│   └── generated/<NN-book>/<NN>.json
└── ModuleGenerator/       Scripts that scrape sources and build module files
    ├── eBibleOrg/         eBible.org scraper → JSON list + .SQLite3 modules
    └── myBible/           ph4.org (MyBible) scraper → JSON list
```

## Module format

Modules use the **MyBible** SQLite schema so the app can read every translation with one
code path (see the app-side loaders in `FrontEndApp/src/util/Modules/Bible`). New sources
should be converted to this format rather than introducing a new shape — see
[`Bible/readme.md`](./Bible/readme.md).

---

## `Bible/` and `zipped/`

`Bible/` holds ready MyBible `.SQLite3` translations (e.g. KJV 1769, KJV 1611, Catholic
Public Domain Version, Almeida 1819). `zipped/` holds the same kind of modules as `.zip`
archives for distribution.

### Adding a Bible module

1. Obtain a MyBible-format SQLite from a source such as <https://www.ph4.org/b4_index.php?hd=b>
   (must match the MyBible format so no conversion is needed).
2. Create a new entry file under `FrontEndApp/src/util/Modules/Bible` (copy an existing one
   and update its fields).

---

## `ModuleGenerator/`

### `eBibleOrg/` — eBible.org generator

Scrapes [ebible.org](https://ebible.org/) for public-domain translations.

| Script | Purpose |
|---|---|
| `generate-json-module.py` | Scrapes the listing + details pages and builds `eBible.module.json` (the app's download list). Full Bibles only. |
| `generate.py` | Downloads one translation and converts its VPL dump into a MyBible-format `.SQLite3`. |

See [`ModuleGenerator/eBibleOrg/README.md`](./ModuleGenerator/eBibleOrg/README.md) for full
arguments, merge behavior, and output format.

### `myBible/` — ph4.org generator

Grabs URLs/links from ph4.org and generates
`FrontEndApp/src/assets/json/ph4_mybible.module.json`. See
[`ModuleGenerator/myBible/readme.md`](./ModuleGenerator/myBible/readme.md).

---

## `Commentaries/` — AI commentary pipeline

Generates evangelical, chapter-level commentary for all 66 books into a SQLite database that
the app reads (the "Believers Sword Commentaries" collection).

### Files

| File | Role |
|---|---|
| [`commentary_schema.sql`](./Commentaries/commentary_schema.sql) | Full SQLite schema (authors, collections, entries, verses, tags, sources, revisions, generation batches/progress). Run once to create the DB. |
| [`generate_commentaries_batch.py`](./Commentaries/generate_commentaries_batch.py) | Resumable batch generator. Writes **5 chapters per run** and advances a cursor. |
| `believers_sword_commentaries.db` | The generated SQLite database (the actual module). |
| `commentary_generation_progress.json` | Human-readable cursor: next book/chapter to generate. |
| `commentary_generation_log.jsonl` | Append-only log, one JSON line per run. |
| `generated/<NN-book>/<NN>.json` | Per-chapter JSON backup of every entry written to the DB. |

### How the batch generator works

`main()` in [`generate_commentaries_batch.py`](./Commentaries/generate_commentaries_batch.py):

1. Ensures the DB exists (runs `commentary_schema.sql` if missing).
2. Ensures the AI author + `believers-sword-commentaries` collection rows exist.
3. Opens a new generation **batch** row.
4. Reads the resume point from `commentary_generation_progress` (DB), falling back to
   `commentary_generation_progress.json`, then to Genesis 1.
5. Generates up to **5 chapters**, inserting a `commentary_entries` row and writing a
   matching `generated/.../NN.json` backup for each.
6. Advances the cursor (Genesis 1 → … → Revelation 22), updates progress, commits, and
   appends a line to the log.

Each entry contains a `title`, `summary`, long-form `content`, `application`, `prayer`,
`key_points`, and `study_questions`, marked `is_ai_generated = 1`, `status = 'draft'`.

### Running it

```bash
python Commentaries/generate_commentaries_batch.py
```

Run repeatedly to walk through the whole Bible 5 chapters at a time; it is **idempotent**
(already-generated chapters are skipped) and **resumable** (safe to stop/restart).

> ⚠️ **Gotcha — hard-coded path.** `BASE` at the top of the script is an absolute WSL path
> (`/mnt/d/Projects/Personal/Believers-Sword/Modules Turso/Commentaries`). The script is
> meant to be run under **WSL**. If you move the repo or run it on native Windows/macOS,
> update `BASE` (or change it to derive from `Path(__file__).parent`).

### Status / output schema

- `status` flows `draft → reviewed → published` (generator emits `draft`).
- Entries are reviewed before being published to users.
- Sync columns (`sync_status`, `server_id`) exist on every table for future remote sync.

---

## Related app code

- Commentary loading / caching: `Electron/Modules/Commentaries/`
- Commentary import + UI: `Electron/IpcMainEvents/importing/importCommentary.ts`,
  `FrontEndApp/src/store/commentaryStore.ts`,
  `FrontEndApp/src/Views/ReadBible/BottomPanel/Commentaries.vue`
- Bible module loaders / download lists: `FrontEndApp/src/util/Modules/Bible`,
  `FrontEndApp/src/assets/json/*.module.json`
