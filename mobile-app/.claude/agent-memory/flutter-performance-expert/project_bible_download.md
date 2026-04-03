---
name: Bible Version Download Feature
description: Architecture of the Bible module download/delete system added to BibleService, BibleProvider, and VersionSelectorScreen
type: project
---

Bible module download feature implemented across three files.

**Why:** Users need to download additional Bible translations (37+ available via ph4.org) beyond the bundled KJV module.

**How to apply:** When touching BibleService, BibleProvider, or VersionSelectorScreen, be aware of these contracts:

- `BibleService.downloadBible(url, fileName, {onProgress})` — streams download bytes, extracts first `.SQLite3`/`.db` from zip, fires `onProgress` (0.0–1.0, with 0–0.9 = download phase, 0.9–1.0 = extraction).
- `BibleService.deleteBible(fileName)` — guards against deleting bundled modules (`bundledModules` static list), closes DB cache entry.
- `BibleProvider._allModules` — full JSON list loaded in `_loadModules()` (replaces the old `_loadShortNames()` — short names are now extracted in the same pass).
- `BibleProvider.downloadableModules` — computed getter: modules with non-null `download_link` that are not yet in `_availableBibles`.
- `BibleProvider.downloadVersion(module)` / `deleteVersion(fileName)` — single-download guard via `_downloadingFileName != null`.
- `BibleProvider.shortNameForModule(module)` — public helper for the Download tab to get the short name without needing to know the internal map.
- `VersionSelectorScreen` — `StatefulWidget` with `TabController` (2 tabs: Installed / Download). Download tab has a search field filtering on title + short name. Progress shown as `LinearProgressIndicator` beneath tile + `CircularProgressIndicator` in trailing. All download buttons disabled while any download is in progress.
- `BibleService.bundledModules` is a `static const` — check it anywhere to guard delete operations.
