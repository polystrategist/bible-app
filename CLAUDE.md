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
