# FrontEndApp

Vue 3 + TypeScript + Vite frontend for **Believers Sword**.

This package is consumed by the Electron shell in the repository root. It can also be built as a standalone web SPA (`yarn build:web` → `dist-web/`).

## Development

From the repository root:

```bash
yarn setup
yarn start
```

To work on the frontend only:

```bash
cd FrontEndApp
yarn
yarn dev
```

## Project Notes

- Shared GitHub and project URLs: `src/config/project.ts`
- Internationalization: `src/util/Internationalization/`
- Bible module manifests: `src/assets/json/believers-sword.module.json`

See the root [README](../README.md) and [AGENTS.md](../AGENTS.md) for full project documentation.
