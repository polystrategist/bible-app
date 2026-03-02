# Believers Sword – GitHub Copilot Instructions

## What This Project Is

**Believers Sword** is a desktop Bible study application built for the Christian community. It helps believers read the Bible, take notes, bookmark/highlight verses, manage prayer lists, view sermons, and organize study spaces. The app is distributed as a Windows desktop app (NSIS installer or portable `.exe`), with a web version also in progress.

---

## Architecture Overview

This is an **Electron + Vue 3** monorepo. The project has the following main directories:

| Directory | Purpose |
|---|---|
| `Electron/` | Electron **main process** (Node.js/TypeScript) — app lifecycle, IPC handlers, database access, auto-updater |
| `FrontEndApp/` | Vue 3 **renderer process** (TypeScript + Vite) — all UI/views |
| `BackendServer/` | Lightweight backend server (used for the web version) |
| `bs-web-app/` | Web app variant of the frontend |
| `Databases/` | SQLite Bible translation database files |
| `Modules/` | Downloaded Bible module `.db` files (user-installed Bible translations) |
| `GenerateMyBibleModules/` | Utility to generate custom Bible module databases |
| `defaults/` | Default bundled data shipped with the installer |
| `dist/` | Compiled Electron main process output (TypeScript → JS) |
| `dist_electron/` | Final packaged Electron app output |

---

## Tech Stack

### Electron Main Process (`Electron/`)
- **Language**: TypeScript (compiled to `dist/` via `tsc`)
- **Database**: SQLite via **Knex.js** (`better-sqlite3` / `sqlite3`)
  - `StoreDB` → `StoreDB/Store.db` — stores user data (notes, bookmarks, highlights, prayer list, etc.)
  - `DictionaryDB` → `StoreDB/Dictionary.db` — Bible dictionary
  - Bible translation DBs are loaded dynamically from `Modules/`
- **Config persistence**: `electron-store` for app settings/bounds
- **IPC**: All communication between frontend and main process goes through Electron IPC (`ipcMain` / `ipcRenderer`)
  - IPC handlers are defined in `Electron/IpcMainEvents/` grouped by feature
- **Auto-update**: `electron-updater` (GitHub Releases, owner: `Bible-Projects`)
- **Logging**: `electron-log`
- **Portable mode**: Supported — `Electron/util/portable.ts` redirects `userData` path

### Frontend (`FrontEndApp/`)
- **Framework**: Vue 3 (Composition API, `<script setup>`)
- **Language**: TypeScript
- **Build tool**: Vite
- **UI library**: Naive UI (`naive-ui`)
- **State management**: Pinia (stores in `FrontEndApp/src/store/`)
- **Routing**: Vue Router 4 (hash history mode for Electron, web history for web mode)
- **Rich text editor**: TipTap (used for notes and sermons)
- **Styling**: UnoCSS + SASS
- **Icons**: `@iconify/vue` with `@iconify-json/solar`, `@vicons/carbon`, `@vicons/fa`, `@vicons/fluent`
- **i18n**: `vue-i18n` v11
- **HTTP client**: Axios (for Supabase/backend calls)
- **Backend/auth**: Supabase (`@supabase/supabase-js`)
- **Drag & drop**: `vuedraggable`
- **Utility**: `@vueuse/core`, `dayjs`, `splitpanes`, `notiflix`, `intro.js`

---

## Key Features & Their Code Locations

| Feature | Frontend | Electron IPC |
|---|---|---|
| Bible reading | `FrontEndApp/src/Views/ReadBible/` | `Electron/IpcMainEvents/Versions/` |
| Notes | `FrontEndApp/src/components/Editor/` | `Electron/IpcMainEvents/notes/` |
| Bookmarks | `FrontEndApp/src/store/bookmark.ts` | `Electron/IpcMainEvents/bookmark/` |
| Highlights | `FrontEndApp/src/store/` | `Electron/IpcMainEvents/highlights/` |
| Clip Notes | `FrontEndApp/src/store/ClipNotes.ts` | `Electron/IpcMainEvents/ClipNotes/` |
| Prayer List | `FrontEndApp/src/Views/PrayerList/` | `Electron/IpcMainEvents/PrayerList/` |
| Sermons | `FrontEndApp/src/Views/Sermons/` | — |
| Create Sermon | `FrontEndApp/src/Views/CreateSermon/` | — |
| Study Space | `FrontEndApp/src/store/SpaceStudyStore.ts` | `Electron/IpcMainEvents/SpaceeStudy/` |
| Download Bible | `FrontEndApp/src/store/downloadBible.ts` | `Electron/IpcMainEvents/downloading/` |
| Dictionaries | — | `Electron/IpcMainEvents/dictionaries/` |
| Settings | `FrontEndApp/src/store/settingStore.ts` | `Electron/ElectronStore/Configuration.ts` |
| Themes | `FrontEndApp/src/store/theme.ts` | — |
| User/Auth | `FrontEndApp/src/Views/UserProfile/` | — (Supabase) |

---

## IPC Communication Pattern

The frontend communicates with the Electron main process exclusively via IPC:

```ts
// Renderer (frontend) → calls preload-exposed APIs
window.ipcRenderer.invoke('channel-name', payload)

// Main process → listens in Electron/IpcMainEvents/
ipcMain.handle('channel-name', async (event, payload) => { ... })
```

Preload script: `Electron/preload.ts` — exposes `ipcRenderer` to the renderer.

---

## Bible Module Format

Bible translations are stored as **SQLite databases** (`.db` files) located in the `Modules/` directory. Each module database contains Bible books, chapters, and verses. The `Electron/Modules/Bible/` directory handles loading and querying these modules. Modules can be downloaded in-app from a remote source.

---

## Build & Development

```bash
# Install all dependencies (root + frontend)
yarn setup

# Run in development (Electron + Vite dev server concurrently)
yarn start

# Build for production (Windows NSIS + portable)
yarn app:build

# Build nightly version
yarn app:build:nightly
```

- The app has two build variants: **Production** (`believers-sword`) and **Nightly** (`believers-sword-nightly`).
- `APP_IS_DEV` and `APP_IS_NIGHTLY` environment variables control build behavior.
- TypeScript root config compiles `Electron/` only. The frontend uses `vue-tsc` via Vite.

---

## Coding Conventions

- Use **Vue 3 Composition API** with `<script setup lang="ts">` in all components.
- Use **Pinia** for all shared state; avoid component-level state for anything that needs to be shared.
- IPC channel names are plain strings — keep them descriptive and grouped by feature (e.g., `bible:getChapter`, `notes:save`).
- Database operations in Electron always go through `Electron/DataBase/DataBase.ts` helpers (`StoreDB`, `DictionaryDB`, `setDB`).
- App settings (window bounds, user preferences) are stored via `electron-store` in `Electron/ElectronStore/Configuration.ts`.
- The frontend is loaded from `http://localhost:3000` in dev and from `file://dist/index.html` in production.
