# Believers Sword — Agent Guide

Cross-platform desktop Bible study app built with **Electron** and **Vue 3**.

## Repository

- **GitHub:** https://github.com/polystrategist/bible-app
- **Product name:** Believers Sword
- **License:** PolyForm Noncommercial License 1.0.0 (see `LICENSE`)

## Project Layout

| Path | Purpose |
| --- | --- |
| `Electron/` | Electron main process — IPC, SQLite (Knex), auto-update, window management |
| `FrontEndApp/` | Vue 3 + Vite frontend (also builds web SPA to `dist-web/`) |
| `defaults/` | Seed databases bundled via `electron-builder` |
| `assets/` | App icons for packaging |
| `design-assets/` | Marketing screenshots and store listing assets |
| `Modules Turso/` | Bible module authoring workspace (not shipped in the app) |
| `scripts/` | Release helpers and Python admin tools |
| `docs/` | Architecture notes for auth and sync |

## Development

```bash
yarn setup    # install root + frontend dependencies
yarn start    # run Electron + Vite dev server
yarn app:build  # build desktop packages
```

- **Node.js** and **Yarn** are required.
- App version lives in root `package.json`.
- Frontend env samples: `FrontEndApp/.env.development.sample`.

## Conventions

- Use `path.join()` for filesystem paths in Electron (cross-platform).
- Centralize GitHub URLs in `FrontEndApp/src/config/project.ts`.
- Match existing naming, imports, and TypeScript patterns in each area.
- Keep changes focused — avoid unrelated refactors.
- Docs belong in `docs/`; reference them from this file when adding new docs.

## Key Configuration

| Setting | Location |
| --- | --- |
| Electron publish / auto-update | `package.json` → `build.publish` |
| API base URL | `VITE_API_BASE_URL` (set in CI and `.env`) |
| Module download URLs | `FrontEndApp/src/assets/json/believers-sword.module.json` |
| Release notes | `release_note.md` (used by CI when present) |

## CI/CD

- **Stable:** tag `v*` on `main` → `.github/workflows/build.yml`
- **Beta:** tag `v*-beta*` on `development` → `.github/workflows/build-beta.yml`

## Documentation

- [Authentication](./docs/authentication.md)
- [Sync system](./docs/sync_system.md)

## Related Links

- [README](./README.md) — user-facing project overview
- [Electron readme](./Electron/readme.md) — build variant notes
