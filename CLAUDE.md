# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

**Believers Sword** is a desktop Bible study app (Electron + Vue 3) and a companion web app (Nuxt 3). It allows believers to read Bible translations, take notes, bookmark/highlight verses, manage prayer lists, view/create sermons, and organize study spaces. The desktop app is distributed as a Windows NSIS installer and portable `.exe`.

---

## Repository Structure

| Directory | Purpose |
|---|---|
| `Electron/` | Electron main process (TypeScript) — app lifecycle, IPC handlers, DB access, auto-updater |
| `FrontEndApp/` | Vue 3 renderer (TypeScript + Vite) — all desktop UI |
| `web/` | Nuxt 3 web app (separate pnpm project) |
| `Databases/` | Bundled SQLite Bible translation `.db` files |
| `Modules/` | User-downloaded Bible module `.db` files |
| `defaults/` | Default bundled data shipped with the installer |
| `dist/` | Compiled Electron output (TypeScript → JS) |
| `dist_electron/` | Final packaged Electron app output |

### Electron Sub-directories

| Directory | Purpose |
|---|---|
| `Electron/DataBase/` | Knex.js DB helpers — `DataBase.ts` (StoreDB, DictionaryDB, setDB), `SyncDB.ts` (sync log CRUD) |
| `Electron/ElectronStore/` | `electron-store` wrappers — `Configuration.ts` (window bounds, app scale, settings) |
| `Electron/IpcMainEvents/` | All IPC handlers, one sub-folder per feature (see below) |
| `Electron/IpcMainEvents/bookmark/` | Save, get, delete bookmarks |
| `Electron/IpcMainEvents/ClipNotes/` | Get, store, delete verse-attached clip notes |
| `Electron/IpcMainEvents/DailyDevotional/` | Get today's / a specific day's devotional |
| `Electron/IpcMainEvents/dictionaries/` | Search dictionary, get word definitions |
| `Electron/IpcMainEvents/downloading/` | Download Bible/commentary module files |
| `Electron/IpcMainEvents/exporting/` | Export notes to PDF/DOCX |
| `Electron/IpcMainEvents/highlights/` | Save, get, delete verse highlights |
| `Electron/IpcMainEvents/importing/` | Import a Bible module from a local file |
| `Electron/IpcMainEvents/notes/` | Upsert, get, delete notes (per-note rows keyed by `note_id`) |
| `Electron/IpcMainEvents/Piper/` | Piper TTS binary management and speech synthesis |
| `Electron/IpcMainEvents/PrayerList/` | CRUD for prayer list items |
| `Electron/IpcMainEvents/SpaceeStudy/` | Study space management |
| `Electron/IpcMainEvents/Sync/` | Sync log, unsynced changes, apply pull data, sync settings |
| `Electron/IpcMainEvents/Versions/` | List available Bible translations/modules |
| `Electron/IpcMainEvents/WindowEvents/` | Minimize, maximize, close, zoom, scale |
| `Electron/Modules/Bible/` | Bible module loader — reads verses from `.db` files, caches versions |
| `Electron/Modules/Commentaries/` | Commentary module loader — reads commentary data from `.db` files |
| `Electron/Setups/` | App startup logic — DB migrations, default data seeding, index creation |
| `Electron/Windows/` | Secondary window creation (CompareVerse window) |
| `Electron/util/` | Shared utilities — `dayjs.ts`, `portable.ts`, `window.ts` (window state) |

### FrontEndApp Sub-directories

| Directory | Purpose |
|---|---|
| `FrontEndApp/src/Views/` | Full-page route views (one folder per page) |
| `FrontEndApp/src/Views/ReadBible/` | Main Bible reader — verses, left/right sidebars, TakeNote panel, FlipBook |
| `FrontEndApp/src/Views/ReadBible/ViewVerses/` | Verse display and context menu (highlight, bookmark, clip note, compare) |
| `FrontEndApp/src/Views/ReadBible/LeftSideBar/` | Navigation sidebar (book/chapter selector) |
| `FrontEndApp/src/Views/ReadBible/RightSideBar/` | Bookmarks, highlights, clip notes, multiple Bibles, dictionary panel |
| `FrontEndApp/src/Views/ReadBible/TakeNote/` | Full notes editor (list + rich text editor) |
| `FrontEndApp/src/Views/ReadBible/FlipBook/` | Flip-book verse presentation mode |
| `FrontEndApp/src/Views/DailyDevotional/` | Daily devotional page (5-step: pause/listen/think/pray/go) |
| `FrontEndApp/src/Views/PrayerList/` | Prayer list management page |
| `FrontEndApp/src/Views/UserProfile/` | Profile page (auth, sync toggle, settings) |
| `FrontEndApp/src/Views/CreateSermon/` | Sermon creation editor |
| `FrontEndApp/src/Views/Sermons/` | Sermon list/viewer |
| `FrontEndApp/src/Views/CompareVerse/` | Secondary window — compare a verse across translations |
| `FrontEndApp/src/components/` | Reusable components shared across views |
| `FrontEndApp/src/components/Editor/` | Rich text editor (Tiptap-based) used in notes and sermons |
| `FrontEndApp/src/components/Settings/` | Settings panels (appearance, Bible reader, TTS, updates) |
| `FrontEndApp/src/components/TitleBar/` | Custom frameless window title bar |
| `FrontEndApp/src/components/TTS/` | Text-to-speech UI controls |
| `FrontEndApp/src/components/ThemeChanger/` | Theme and background picker |
| `FrontEndApp/src/components/ProfilePage/` | Profile dropdown and auth UI |
| `FrontEndApp/src/store/` | Pinia stores — one per feature (see key stores below) |
| `FrontEndApp/src/util/` | Shared utilities |
| `FrontEndApp/src/util/Sync/` | `sync.ts` — `runPushSync`, `runPullSync`, `runSync`, `debouncedRunSync` |
| `FrontEndApp/src/util/Modules/` | Bible module helpers (`FeBibleController.ts`) |
| `FrontEndApp/src/services/` | Service layer wrappers (e.g. `BibleService.ts`) |
| `FrontEndApp/src/router/` | Vue Router config — hash history for Electron, route definitions |
| `FrontEndApp/src/assets/` | Static assets — styles, JSON data files |

### Key Pinia Stores

| Store file | Responsibility |
|---|---|
| `authStore.ts` | Auth state, token, sync enabled flag, sync interval, settings flush, quit-sync hook |
| `BibleStore.ts` | Active translation, chapter verses, highlights |
| `useNoteStore.ts` | Notes CRUD, auto-save watch, hydration guard (`isHydrating`) |
| `ClipNotes.ts` | Verse-attached clip notes CRUD |
| `bookmark.ts` | Bookmark list |
| `prayerListStore.ts` | Prayer list CRUD |
| `theme.ts` | Theme state, dark mode, background theme, remote settings watcher |
| `settingStore.ts` | App-wide settings (font size, scale, reader options) |
| `piperTTSStore.ts` | Piper TTS binary state, voice selection, speak/stop |
| `ttsStore.ts` | Web Speech API TTS (online fallback) |

---

## Development Commands

### Desktop App (Electron + Vue 3)

```bash
# Install all dependencies (root + FrontEndApp)
yarn setup

# Run full app in dev (Electron + Vite dev server concurrently)
yarn start

# Build for production (Windows NSIS + portable)
yarn app:build

# Build nightly version
yarn app:build:nightly

# Compile Electron TypeScript only
yarn build

# Type-check both Electron and FrontEndApp (no emit)
yarn typecheck

# Run Vite dev server only (frontend)
cd FrontEndApp && yarn dev
```

### Web App (Nuxt 3 in `web/`)

```bash
cd web
pnpm dev        # Dev server
pnpm build      # Production build
pnpm generate   # Static generation
pnpm preview    # Preview production build
```

---

## Architecture & Data Flow

### Electron ↔ Vue IPC Pattern

All frontend-to-backend communication goes through Electron IPC. There is no direct database access from the renderer.

```
Vue Component → Pinia Store → window.ipcRenderer.invoke('channel', payload)
    → Electron/IpcMainEvents/<feature>/ → Knex.js → SQLite
    → response back → store update → UI re-render
```

- **Preload bridge**: `Electron/preload.ts` exposes `ipcRenderer` to the renderer via `contextBridge`
- **IPC handlers**: defined in `Electron/IpcMainEvents/` grouped by feature (bookmark, notes, highlights, PrayerList, Versions, SpaceeStudy, downloading, dictionaries, Sync, etc.)
- **IPC registration**: all handlers are registered in `Electron/IpcMainEvents/IpcMainEvents.ts`

### Databases

- **StoreDB** (`StoreDB/Store.db`) — user data: notes, bookmarks, highlights, prayer lists, study spaces, sync log
- **DictionaryDB** (`StoreDB/Dictionary.db`) — Bible dictionary
- **Bible modules** — individual `.db` files in `Modules/`, loaded dynamically via `Electron/Modules/Bible/`
- All DB access uses Knex.js helpers from `Electron/DataBase/DataBase.ts` (`StoreDB`, `DictionaryDB`, `setDB`)
- DB tables are initialized at startup in `Electron/Setups/setup.ts`

### Cloud Sync

Sync runs via `/api/sync` (POST push) and `/api/sync/pull` (GET pull) against the Laravel backend.

| Function | Where called | What it does |
|---|---|---|
| `runPushSync()` | `debouncedRunSync` → user actions | Push unsynced local changes only — no pull, no `loadNote` |
| `runPullSync()` | 5-min interval, window focus (throttled 1/min) | Pull remote changes + `loadNote` to refresh UI |
| `runSync()` | App start, app quit, coming back online | Full push + pull + `loadNote` |
| `debouncedRunSync()` | All user actions (edit, bookmark, highlight, etc.) | 3s debounce → calls `runPushSync` |

- `isSyncing` flag prevents concurrent runs across all four functions (shared module-level var)
- Exponential backoff (`backoffUntil`) on network failures: 5min → 10min → 20min → max 60min
- 401 from any sync call → auto-logout
- `isHydrating` guard in `useNoteStore` — `loadNote()` sets it before writing `notes.value` and clears it after `nextTick()` so the auto-save watcher never fires during a pull-triggered reload

### Frontend State

- **Pinia stores** in `FrontEndApp/src/store/` — one store per feature (BibleStore, bookmark, ClipNotes, useNoteStore, SpaceStudyStore, settingStore, theme, authStore, etc.)
- **Vue Router** uses hash history (Electron) or web history (web build), configured in `FrontEndApp/src/router/router.ts`
- **App settings** (window bounds, preferences) are persisted via `electron-store` in `Electron/ElectronStore/Configuration.ts`

### Build Variants

- **Production**: `app-id = com.official-believers-sword.app`, `productName = Believers Sword`
- **Nightly**: `app-id = com.official-believers-sword-nightly.app`, `productName = Believers Sword Nightly`
- Controlled by `APP_IS_DEV` and `APP_IS_NIGHTLY` environment variables (see `Electron/config.ts`)
- `yarn nightly:rename` / `yarn prod:rename` mutate `package.json` fields before building

### Web App (`web/`)

A separate Nuxt 3 app with SSR enabled. Uses:
- **PrimeVue 4** (Aura theme preset) for UI components
- **UnoCSS** for styling
- Dark mode toggled via `.my-app-dark` class selector
- App structure follows Nuxt 4 compatibility layout: `web/app/` contains `pages/`, `components/`, `layouts/`, `assets/`

---

## Coding Conventions

- All Vue components use `<script setup lang="ts">` (Composition API)
- Use Pinia for any state shared across components; avoid prop-drilling
- IPC channel names are plain descriptive strings grouped by feature (e.g., `bible:getChapter`, `notes:save`)
- Database operations in Electron always go through `DataBase.ts` helpers — never instantiate Knex directly in IPC handlers
- The frontend loads from `http://localhost:3000` in dev and `file://dist/index.html` in production
- TypeScript root `tsconfig.json` covers `Electron/` only; `FrontEndApp/` has its own `tsconfig.json` for Vue/Vite
