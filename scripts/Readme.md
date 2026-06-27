# Scripts

Utility scripts for managing and maintaining the project — releases, data
generation, and other one-off / repeatable maintenance tasks.

## `release-beta.js`

Tags and pushes a beta release (`v<version>-beta.<n>`). The base version comes
from `package.json`; the next beta number is found by scanning remote tags so it
never collides with a beta pushed from another machine. Pushing the tag triggers
`.github/workflows/build-beta.yml`.

```bash
node scripts/release-beta.js        # auto-increment to the next free beta number
node scripts/release-beta.js 3      # use beta number 3 explicitly
```

## `manage-defaults/`

Contributor tooling for editing the seed databases in `defaults/Main/`, starting
with the Strong's dictionary. Edits a git-diffable JSON source of truth
(`data/strongs.json`) and regenerates `defaults/Main/strongs.db` + bumps its
version file — so changes are reviewable as text diffs instead of binary blobs.

Includes a browser admin UI (NiceGUI — pure Python, rendered with Vue 3 +
Quasar) for non-technical contributors:

```bash
yarn manage:default:win      # or :mac / :linux
```

See [`manage-defaults/README.md`](manage-defaults/README.md) for the full flow,
CLI scripts (`extract_strongs.py`, `build_strongs.py`), and the
`strongs_dictionary` schema.

## `Generate Strong Number Sqlite/` (superseded)

The original one-shot generator that built `strongs.db` from standalone Greek and
Hebrew JSON files. Those source files have been removed and the data now lives in
`manage-defaults/data/strongs.json`, so use `manage-defaults/` instead. This
folder is kept only for historical reference and can be deleted.
