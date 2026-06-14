# Desktop Games Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a fully-functional Games page to the Electron desktop app (Q&A, True/False, Four Pictures) with lives + group-progress syncing to the backend, matching the mobile app's architecture exactly.

**Architecture:** Three bundled SQLite content DBs (one per game type) are copied to `userData/Games/` at startup; user data (lives, progress) lives in the existing `Store.db`; a single `Games.ts` IPC module handles all three games; a unified `useGamesStore` Pinia store drives the Vue views.

**Tech Stack:** Electron + Knex (sqlite3), Vue 3 + Pinia (Naive UI), TypeScript.

---

## File Map

### New — Electron
| File | Purpose |
|---|---|
| `Electron/Setups/Setup/SetGamesDB.ts` | Seed all 3 game content DBs + FP images to userData on startup |
| `Electron/Setups/Setup/StoreDB/game_lives.migration.ts` | Create `game_lives` table |
| `Electron/Setups/Setup/StoreDB/qa_group_progress.migration.ts` | Create `qa_group_progress` table |
| `Electron/Setups/Setup/StoreDB/tf_group_progress.migration.ts` | Create `tf_group_progress` table |
| `Electron/Setups/Setup/StoreDB/fpow_level_progress.migration.ts` | Create `fpow_level_progress` table |
| `Electron/IpcMainEvents/Games/Games.ts` | All game IPC handlers (lives + Q&A + T/F + FP) |

### Modified — Electron
| File | Change |
|---|---|
| `Electron/DataBase/DataBase.ts` | Add `QaGamesDB`, `TfGamesDB`, `FpGamesDB` Knex connections |
| `Electron/Setups/setup.ts` | Call `setGamesDB` |
| `Electron/Setups/Setup/SetStoreDatabase.ts` | Register 4 new migrations |
| `Electron/IpcMainEvents/IpcMainEvents.ts` | Register `Games()` |
| `Electron/IpcMainEvents/Sync/SyncHandlers.ts` | Extend `applyPullData` for game tables |
| `Electron/preload.ts` | Expose all game IPC calls |

### New — Frontend
| File | Purpose |
|---|---|
| `FrontEndApp/src/store/useGamesStore.ts` | Unified Pinia store (lives + all game state) |
| `FrontEndApp/src/Views/Games/Games.vue` | Hub + in-page nav controller |
| `FrontEndApp/src/Views/Games/components/LivesBar.vue` | Hearts display + countdown |
| `FrontEndApp/src/Views/Games/components/GameCard.vue` | Game type card with progress |
| `FrontEndApp/src/Views/Games/QuestionAndAnswer/QAGroupsList.vue` | Q&A group list |
| `FrontEndApp/src/Views/Games/QuestionAndAnswer/QAGameplay.vue` | Q&A play screen |
| `FrontEndApp/src/Views/Games/TrueOrFalse/TFGroupsList.vue` | T/F group list |
| `FrontEndApp/src/Views/Games/TrueOrFalse/TFGameplay.vue` | T/F play screen |
| `FrontEndApp/src/Views/Games/FourPictures/FPGameplay.vue` | Four Pictures play screen |

### Modified — Frontend
| File | Change |
|---|---|
| `FrontEndApp/src/GlobalDeclare.ts` | Add game IPC types to `window.browserWindow` |
| `FrontEndApp/src/router/router.ts` | Add `/games` route |
| `FrontEndApp/src/store/menu.ts` | Add Games sidebar entry |
| `FrontEndApp/src/util/Sync/sync.ts` | Add game tables to push allowlist, pull destructure, and `reloadStoresAfterPull` |

### New — Assets
| Location | Source |
|---|---|
| `defaults/Main/games/qa/game_seed.db` | `D:\Projects\Personal\Believers Sword App\assets\game\question_and_answer\game_seed.db` |
| `defaults/Main/games/qa/version.json` | `D:\Projects\Personal\Believers Sword App\assets\game\question_and_answer\seed_data_version.json` |
| `defaults/Main/games/tf/game_seed.db` | `D:\Projects\Personal\Believers Sword App\assets\game\true_or_false\game_seed.db` |
| `defaults/Main/games/tf/version.json` | `D:\Projects\Personal\Believers Sword App\assets\game\true_or_false\seed_data_version.json` |
| `defaults/Main/games/fp/game_seed.db` | `D:\Projects\Personal\Believers Sword App\assets\game\4_picture_one_word\game_seed.db` |
| `defaults/Main/games/fp/version.json` | `D:\Projects\Personal\Believers Sword App\assets\game\4_picture_one_word\seed_data_version.json` |
| `defaults/Main/games/fp/images/` | `D:\Projects\Personal\Believers Sword App\assets\game\4_picture_one_word\images\` (entire folder) |
| `FrontEndApp/src/assets/sounds/correct.mp3` | `D:\Projects\Personal\Believers Sword App\assets\sound\correct.mp3` |
| `FrontEndApp/src/assets/sounds/wrong.mp3` | `D:\Projects\Personal\Believers Sword App\assets\sound\wrong.mp3` |

---

## Task 1: Copy Asset Files

**Files:**
- Create: `defaults/Main/games/qa/` (game_seed.db + version.json)
- Create: `defaults/Main/games/tf/` (game_seed.db + version.json)
- Create: `defaults/Main/games/fp/` (game_seed.db + version.json + images/)
- Create: `FrontEndApp/src/assets/sounds/correct.mp3` + `wrong.mp3`

- [ ] **Step 1: Create directory structure and copy game DBs**

Run from repo root (`D:\Projects\Personal\Believers-Sword`):
```powershell
$mobile = "D:\Projects\Personal\Believers Sword App"

New-Item -ItemType Directory -Force "defaults\Main\games\qa"
New-Item -ItemType Directory -Force "defaults\Main\games\tf"
New-Item -ItemType Directory -Force "defaults\Main\games\fp"
New-Item -ItemType Directory -Force "FrontEndApp\src\assets\sounds"

# Q&A
Copy-Item "$mobile\assets\game\question_and_answer\game_seed.db" "defaults\Main\games\qa\game_seed.db"
Copy-Item "$mobile\assets\game\question_and_answer\seed_data_version.json" "defaults\Main\games\qa\version.json"

# True/False
Copy-Item "$mobile\assets\game\true_or_false\game_seed.db" "defaults\Main\games\tf\game_seed.db"
Copy-Item "$mobile\assets\game\true_or_false\seed_data_version.json" "defaults\Main\games\tf\version.json"

# Four Pictures
Copy-Item "$mobile\assets\game\4_picture_one_word\game_seed.db" "defaults\Main\games\fp\game_seed.db"
Copy-Item "$mobile\assets\game\4_picture_one_word\seed_data_version.json" "defaults\Main\games\fp\version.json"
Copy-Item "$mobile\assets\game\4_picture_one_word\images" "defaults\Main\games\fp\images" -Recurse

# Sounds
Copy-Item "$mobile\assets\sound\correct.mp3" "FrontEndApp\src\assets\sounds\correct.mp3"
Copy-Item "$mobile\assets\sound\wrong.mp3" "FrontEndApp\src\assets\sounds\wrong.mp3"
```

- [ ] **Step 2: Verify files exist**

```powershell
ls defaults\Main\games\qa
ls defaults\Main\games\tf
ls defaults\Main\games\fp
ls defaults\Main\games\fp\images | Select-Object -First 5
ls FrontEndApp\src\assets\sounds
```

Expected: each directory has `game_seed.db` + `version.json`; fp/images has .jpg files; sounds has two .mp3 files.

- [ ] **Step 3: Commit**

```bash
git add defaults/Main/games/ FrontEndApp/src/assets/sounds/
git commit -m "feat(games): add bundled game seed DBs, FP images, and sound assets"
```

---

## Task 2: Electron DataBase Connections

**Files:**
- Modify: `Electron/DataBase/DataBase.ts`

- [ ] **Step 1: Add three new Knex connections after the existing ones**

Open `Electron/DataBase/DataBase.ts`. After the `DevotionalsDB` export (around line 35), add:

```typescript
export const QaGamesDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\Games\\qa_games.db`,
    },
});

export const TfGamesDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\Games\\tf_games.db`,
    },
});

export const FpGamesDB = knex({
    client: 'sqlite3',
    useNullAsDefault: false,
    connection: {
        filename: dataPath + `\\Games\\fp_games.db`,
    },
});
```

- [ ] **Step 2: Verify TypeScript compiles**

```bash
cd D:\Projects\Personal\Believers-Sword && yarn build 2>&1 | tail -5
```

Expected: no TypeScript errors.

- [ ] **Step 3: Commit**

```bash
git add Electron/DataBase/DataBase.ts
git commit -m "feat(games): add QaGamesDB, TfGamesDB, FpGamesDB Knex connections"
```

---

## Task 3: SetGamesDB Setup File

**Files:**
- Create: `Electron/Setups/Setup/SetGamesDB.ts`

- [ ] **Step 1: Create the file**

```typescript
// Electron/Setups/Setup/SetGamesDB.ts
import { app } from 'electron';
import fs from 'fs';
import path from 'path';
import UPath from 'upath';
import Log from 'electron-log';
import { setupPortableMode } from '../../util/portable';

setupPortableMode();
const isPackaged = app.isPackaged;
const dataPath = app.getPath('userData');
const gamesDataPath = UPath.join(dataPath, 'Games');

function defaultsBase(): string {
    return isPackaged
        ? UPath.toUnix(
              UPath.join(__dirname, 'defaults', 'Main', 'games')
          ).replace('app.asar/dist/Setups/Setup/', '')
        : './defaults/Main/games';
}

async function seedGameDb(
    type: 'qa' | 'tf' | 'fp',
    targetFilename: string
): Promise<void> {
    const base = defaultsBase();
    const defaultDbPath = UPath.join(base, type, 'game_seed.db');
    const defaultVersionPath = UPath.join(base, type, 'version.json');
    const targetDbPath = UPath.join(gamesDataPath, targetFilename);
    const installedVersionPath = UPath.join(gamesDataPath, `${type}_version.json`);

    let defaultVersion: number;
    try {
        defaultVersion = JSON.parse(fs.readFileSync(defaultVersionPath, 'utf-8')).version;
    } catch (err) {
        Log.error(`[SetGamesDB] Failed to read ${type} version.json:`, err);
        throw err;
    }

    fs.mkdirSync(gamesDataPath, { recursive: true });

    const copyDb = () => {
        fs.copyFileSync(defaultDbPath, targetDbPath);
        fs.writeFileSync(installedVersionPath, JSON.stringify({ version: defaultVersion }));
        Log.info(`[SetGamesDB] ${type} game DB seeded to version ${defaultVersion}`);
    };

    if (!fs.existsSync(targetDbPath)) {
        copyDb();
        return;
    }

    const installedVersion = fs.existsSync(installedVersionPath)
        ? (JSON.parse(fs.readFileSync(installedVersionPath, 'utf-8')).version as number)
        : 0;

    if (defaultVersion !== installedVersion) {
        copyDb();
    } else {
        Log.info(`[SetGamesDB] ${type} game DB up to date (v${defaultVersion})`);
    }
}

async function seedFpImages(): Promise<void> {
    const base = defaultsBase();
    const srcImages = UPath.join(base, 'fp', 'images');
    const destImages = UPath.join(gamesDataPath, 'fp_images');

    if (!fs.existsSync(destImages)) {
        fs.mkdirSync(destImages, { recursive: true });
        fs.cpSync(srcImages, destImages, { recursive: true });
        Log.info('[SetGamesDB] FP images copied to userData');
    } else {
        // Re-sync images on FP DB version change — existing images are overwritten
        // so new levels always have their images available.
        const fpVersionPath = UPath.join(gamesDataPath, 'fp_version.json');
        const defaultVersionPath = UPath.join(base, 'fp', 'version.json');
        const defaultVersion = JSON.parse(fs.readFileSync(defaultVersionPath, 'utf-8')).version as number;
        const installedVersion = fs.existsSync(fpVersionPath)
            ? (JSON.parse(fs.readFileSync(fpVersionPath, 'utf-8')).version as number)
            : 0;
        if (defaultVersion !== installedVersion) {
            fs.cpSync(srcImages, destImages, { recursive: true });
            Log.info('[SetGamesDB] FP images updated');
        }
    }
}

export const setGamesDB = new Promise<void>(async (resolve, reject) => {
    try {
        await seedGameDb('qa', 'qa_games.db');
        await seedGameDb('tf', 'tf_games.db');
        await seedGameDb('fp', 'fp_games.db');
        await seedFpImages();
        resolve();
    } catch (err) {
        Log.error('[SetGamesDB] Setup failed:', err);
        reject(err);
    }
});
```

- [ ] **Step 2: Register in setup.ts**

Open `Electron/Setups/setup.ts`. Add the import and call:

```typescript
import { setGamesDB } from './Setup/SetGamesDB';

export const setupDefault = new Promise(async (resolve, reject): Promise<void> => {
    await setDefaultBible.catch((e) => reject(e));
    await setStoreDB.catch((e) => reject(e));
    await setDictionaryDB.catch((e) => reject(e));
    await setCrossReferencesDB.catch((e) => reject(e));
    await setDevotionalsDB.catch((e) => reject(e));
    await setGamesDB.catch((e) => reject(e));   // ← add this line

    SetStoreDatabase();
    await createDatabaseIndexes().catch((e) => reject(e));

    resolve('Default is Set up');
});
```

- [ ] **Step 3: Verify TypeScript compiles**

```bash
yarn build 2>&1 | tail -5
```

Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add Electron/Setups/Setup/SetGamesDB.ts Electron/Setups/setup.ts
git commit -m "feat(games): add SetGamesDB to seed game content DBs and FP images on startup"
```

---

## Task 4: Store.db Migrations

**Files:**
- Create: `Electron/Setups/Setup/StoreDB/game_lives.migration.ts`
- Create: `Electron/Setups/Setup/StoreDB/qa_group_progress.migration.ts`
- Create: `Electron/Setups/Setup/StoreDB/tf_group_progress.migration.ts`
- Create: `Electron/Setups/Setup/StoreDB/fpow_level_progress.migration.ts`

- [ ] **Step 1: Create game_lives migration**

```typescript
// Electron/Setups/Setup/StoreDB/game_lives.migration.ts
import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

/**
 * `game_lives` tracks each life lost. Shared across all game types.
 * life_lost_at (ISO8601 UTC) is the unique key used by sync_logs record_key.
 * Mirrors mobile Store.db schema exactly.
 */
export default async () => {
    try {
        const exists = await StoreDB.schema.hasTable('game_lives');
        if (!exists) {
            await StoreDB.schema.createTable('game_lives', (table) => {
                table.increments('id').primary();
                table.string('life_lost_at').notNullable();
                table.integer('recovered').defaultTo(0);
                table.string('created_at').notNullable();
            });
        }
    } catch (e) {
        Log.error('[game_lives migration]', e);
    }
};
```

- [ ] **Step 2: Create qa_group_progress migration**

```typescript
// Electron/Setups/Setup/StoreDB/qa_group_progress.migration.ts
import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

export default async () => {
    try {
        const exists = await StoreDB.schema.hasTable('qa_group_progress');
        if (!exists) {
            await StoreDB.schema.createTable('qa_group_progress', (table) => {
                table.integer('group_id').primary();
                table.integer('is_completed').defaultTo(0);
                table.integer('high_score_percentage').defaultTo(0);
                table.integer('times_played').defaultTo(0);
                table.string('completed_at').nullable();
                table.string('updated_at').notNullable();
            });
        }
    } catch (e) {
        Log.error('[qa_group_progress migration]', e);
    }
};
```

- [ ] **Step 3: Create tf_group_progress migration**

```typescript
// Electron/Setups/Setup/StoreDB/tf_group_progress.migration.ts
import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

export default async () => {
    try {
        const exists = await StoreDB.schema.hasTable('tf_group_progress');
        if (!exists) {
            await StoreDB.schema.createTable('tf_group_progress', (table) => {
                table.integer('group_id').primary();
                table.integer('is_completed').defaultTo(0);
                table.integer('high_score_percentage').defaultTo(0);
                table.integer('times_played').defaultTo(0);
                table.string('completed_at').nullable();
                table.string('updated_at').notNullable();
            });
        }
    } catch (e) {
        Log.error('[tf_group_progress migration]', e);
    }
};
```

- [ ] **Step 4: Create fpow_level_progress migration**

```typescript
// Electron/Setups/Setup/StoreDB/fpow_level_progress.migration.ts
import { StoreDB } from '../../../DataBase/DataBase';
import Log from 'electron-log';

export default async () => {
    try {
        const exists = await StoreDB.schema.hasTable('fpow_level_progress');
        if (!exists) {
            await StoreDB.schema.createTable('fpow_level_progress', (table) => {
                table.integer('level_id').primary();
                table.string('solved_at').nullable();
                table.string('hint_state').nullable();
            });
        }
    } catch (e) {
        Log.error('[fpow_level_progress migration]', e);
    }
};
```

- [ ] **Step 5: Register all four migrations in SetStoreDatabase.ts**

Open `Electron/Setups/Setup/SetStoreDatabase.ts`. Add imports and calls:

```typescript
import gameLivesMigration from './StoreDB/game_lives.migration';
import qaGroupProgressMigration from './StoreDB/qa_group_progress.migration';
import tfGroupProgressMigration from './StoreDB/tf_group_progress.migration';
import fpowLevelProgressMigration from './StoreDB/fpow_level_progress.migration';

// Inside the exported async function, after devotionDaysMigration():
await gameLivesMigration();
await qaGroupProgressMigration();
await tfGroupProgressMigration();
await fpowLevelProgressMigration();
```

- [ ] **Step 6: Verify TypeScript compiles**

```bash
yarn build 2>&1 | tail -5
```

- [ ] **Step 7: Commit**

```bash
git add Electron/Setups/Setup/StoreDB/game_lives.migration.ts \
        Electron/Setups/Setup/StoreDB/qa_group_progress.migration.ts \
        Electron/Setups/Setup/StoreDB/tf_group_progress.migration.ts \
        Electron/Setups/Setup/StoreDB/fpow_level_progress.migration.ts \
        Electron/Setups/Setup/SetStoreDatabase.ts
git commit -m "feat(games): add Store.db migrations for game_lives, progress tables"
```

---

## Task 5: Games IPC Handler

**Files:**
- Create: `Electron/IpcMainEvents/Games/Games.ts`
- Modify: `Electron/IpcMainEvents/IpcMainEvents.ts`

- [ ] **Step 1: Create Games.ts**

```typescript
// Electron/IpcMainEvents/Games/Games.ts
import { ipcMain, app } from 'electron';
import path from 'path';
import Log from 'electron-log';
import { StoreDB, QaGamesDB, TfGamesDB, FpGamesDB } from '../../DataBase/DataBase';
import { logSyncChange } from '../../DataBase/SyncDB';

const MAX_LIVES = 7;
const RECOVERY_MS = 2 * 60 * 60 * 1000; // 2 hours in milliseconds

async function processRecoveries(): Promise<void> {
    const cutoff = new Date(Date.now() - RECOVERY_MS).toISOString();
    const rows = await StoreDB('game_lives')
        .where('recovered', 0)
        .where('life_lost_at', '<=', cutoff)
        .select('life_lost_at');

    if (rows.length === 0) return;

    await StoreDB('game_lives')
        .where('recovered', 0)
        .where('life_lost_at', '<=', cutoff)
        .update({ recovered: 1 });

    for (const row of rows) {
        try {
            await logSyncChange({
                table_name: 'game_lives',
                record_key: row.life_lost_at,
                action: 'updated',
                payload: { life_lost_at: row.life_lost_at, recovered: 1 },
                synced: 0,
            });
        } catch (e) {
            Log.error('[Games] logSync recovery failed:', e);
        }
    }
}

export default function Games() {
    // ── Lives ──────────────────────────────────────────────────────────────

    ipcMain.handle('game:getLives', async () => {
        try {
            await processRecoveries();
            const result = await StoreDB('game_lives').where('recovered', 0).count('id as cnt').first() as any;
            const lost = Number(result?.cnt ?? 0);
            return Math.max(0, MAX_LIVES - lost);
        } catch (e) {
            Log.error('[Games] game:getLives error:', e);
            return MAX_LIVES;
        }
    });

    ipcMain.handle('game:loseLife', async () => {
        try {
            await processRecoveries();
            const result = await StoreDB('game_lives').where('recovered', 0).count('id as cnt').first() as any;
            const lost = Number(result?.cnt ?? 0);
            if (lost >= MAX_LIVES) return 0;

            const lifeKey = new Date().toISOString();
            await StoreDB('game_lives').insert({
                life_lost_at: lifeKey,
                recovered: 0,
                created_at: lifeKey,
            });
            await logSyncChange({
                table_name: 'game_lives',
                record_key: lifeKey,
                action: 'created',
                payload: { life_lost_at: lifeKey, recovered: 0 },
                synced: 0,
            });
            return Math.max(0, MAX_LIVES - lost - 1);
        } catch (e) {
            Log.error('[Games] game:loseLife error:', e);
            return MAX_LIVES;
        }
    });

    ipcMain.handle('game:nextRecoveryAt', async () => {
        try {
            await processRecoveries();
            const row = await StoreDB('game_lives')
                .where('recovered', 0)
                .orderBy('life_lost_at', 'asc')
                .first();
            if (!row) return null;
            return new Date(new Date(row.life_lost_at).getTime() + RECOVERY_MS).toISOString();
        } catch (e) {
            Log.error('[Games] game:nextRecoveryAt error:', e);
            return null;
        }
    });

    ipcMain.handle('game:refillLives', async () => {
        try {
            const rows = await StoreDB('game_lives').where('recovered', 0).select('life_lost_at');
            await StoreDB('game_lives').where('recovered', 0).update({ recovered: 1 });
            for (const row of rows) {
                try {
                    await logSyncChange({
                        table_name: 'game_lives',
                        record_key: row.life_lost_at,
                        action: 'updated',
                        payload: { life_lost_at: row.life_lost_at, recovered: 1 },
                        synced: 0,
                    });
                } catch (e) {
                    Log.error('[Games] logSync refill failed:', e);
                }
            }
        } catch (e) {
            Log.error('[Games] game:refillLives error:', e);
        }
    });

    // ── Q&A ────────────────────────────────────────────────────────────────

    ipcMain.handle('qa:getGroups', async () => {
        try {
            return await QaGamesDB('question_groups').orderBy('display_order', 'asc').select();
        } catch (e) {
            Log.error('[Games] qa:getGroups error:', e);
            return [];
        }
    });

    ipcMain.handle('qa:getQuestionsForGroup', async (_, groupId: number) => {
        try {
            const rows = await QaGamesDB('questions')
                .where('group_id', groupId)
                .orderByRaw('RANDOM()')
                .select();
            // options is stored as a JSON string — parse it for the renderer
            return rows.map((q: any) => ({
                ...q,
                options: typeof q.options === 'string' ? JSON.parse(q.options) : q.options,
            }));
        } catch (e) {
            Log.error('[Games] qa:getQuestionsForGroup error:', e);
            return [];
        }
    });

    ipcMain.handle('qa:getAllGroupProgress', async () => {
        try {
            return await StoreDB('qa_group_progress').select();
        } catch (e) {
            Log.error('[Games] qa:getAllGroupProgress error:', e);
            return [];
        }
    });

    ipcMain.handle('qa:saveGroupProgress', async (_, args: {
        groupId: number;
        correctCount: number;
        totalCount: number;
        passingScore: number;
    }) => {
        try {
            const { groupId, correctCount, totalCount, passingScore } = args;
            const percentage = totalCount === 0 ? 0 : Math.round((correctCount / totalCount) * 100);
            const passed = percentage >= passingScore;
            const now = new Date().toISOString();
            const existing = await StoreDB('qa_group_progress').where('group_id', groupId).first();

            let newlyPassed = false;
            if (!existing) {
                const row = {
                    group_id: groupId,
                    is_completed: passed ? 1 : 0,
                    high_score_percentage: percentage,
                    times_played: 1,
                    completed_at: passed ? now : null,
                    updated_at: now,
                };
                await StoreDB('qa_group_progress').insert(row);
                newlyPassed = passed;
                await logSyncChange({
                    table_name: 'qa_group_progress',
                    record_key: `qa_group_${groupId}`,
                    action: 'created',
                    payload: row,
                    synced: 0,
                });
            } else {
                const wasCompleted = Boolean(existing.is_completed);
                const newCompleted = wasCompleted || passed;
                const newScore = Math.max(existing.high_score_percentage, percentage);
                const row = {
                    is_completed: newCompleted ? 1 : 0,
                    high_score_percentage: newScore,
                    times_played: existing.times_played + 1,
                    completed_at: existing.completed_at ?? (passed ? now : null),
                    updated_at: now,
                };
                await StoreDB('qa_group_progress').where('group_id', groupId).update(row);
                newlyPassed = passed && !wasCompleted;
                await logSyncChange({
                    table_name: 'qa_group_progress',
                    record_key: `qa_group_${groupId}`,
                    action: 'updated',
                    payload: { ...row, group_id: groupId },
                    synced: 0,
                });
            }
            return { newlyPassed };
        } catch (e) {
            Log.error('[Games] qa:saveGroupProgress error:', e);
            return { newlyPassed: false };
        }
    });

    // ── True/False ─────────────────────────────────────────────────────────

    ipcMain.handle('tf:getGroups', async () => {
        try {
            return await TfGamesDB('tf_groups').orderBy('display_order', 'asc').select();
        } catch (e) {
            Log.error('[Games] tf:getGroups error:', e);
            return [];
        }
    });

    ipcMain.handle('tf:getStatementsForGroup', async (_, groupId: number) => {
        try {
            return await TfGamesDB('tf_statements')
                .where('group_id', groupId)
                .orderByRaw('RANDOM()')
                .select();
        } catch (e) {
            Log.error('[Games] tf:getStatementsForGroup error:', e);
            return [];
        }
    });

    ipcMain.handle('tf:getAllGroupProgress', async () => {
        try {
            return await StoreDB('tf_group_progress').select();
        } catch (e) {
            Log.error('[Games] tf:getAllGroupProgress error:', e);
            return [];
        }
    });

    ipcMain.handle('tf:saveGroupProgress', async (_, args: {
        groupId: number;
        correctCount: number;
        totalCount: number;
        passingScore: number;
    }) => {
        try {
            const { groupId, correctCount, totalCount, passingScore } = args;
            const percentage = totalCount === 0 ? 0 : Math.round((correctCount / totalCount) * 100);
            const passed = percentage >= passingScore;
            const now = new Date().toISOString();
            const existing = await StoreDB('tf_group_progress').where('group_id', groupId).first();

            let newlyPassed = false;
            if (!existing) {
                const row = {
                    group_id: groupId,
                    is_completed: passed ? 1 : 0,
                    high_score_percentage: percentage,
                    times_played: 1,
                    completed_at: passed ? now : null,
                    updated_at: now,
                };
                await StoreDB('tf_group_progress').insert(row);
                newlyPassed = passed;
                await logSyncChange({
                    table_name: 'tf_group_progress',
                    record_key: `tf_group_${groupId}`,
                    action: 'created',
                    payload: row,
                    synced: 0,
                });
            } else {
                const wasCompleted = Boolean(existing.is_completed);
                const newCompleted = wasCompleted || passed;
                const newScore = Math.max(existing.high_score_percentage, percentage);
                const row = {
                    is_completed: newCompleted ? 1 : 0,
                    high_score_percentage: newScore,
                    times_played: existing.times_played + 1,
                    completed_at: existing.completed_at ?? (passed ? now : null),
                    updated_at: now,
                };
                await StoreDB('tf_group_progress').where('group_id', groupId).update(row);
                newlyPassed = passed && !wasCompleted;
                await logSyncChange({
                    table_name: 'tf_group_progress',
                    record_key: `tf_group_${groupId}`,
                    action: 'updated',
                    payload: { ...row, group_id: groupId },
                    synced: 0,
                });
            }
            return { newlyPassed };
        } catch (e) {
            Log.error('[Games] tf:saveGroupProgress error:', e);
            return { newlyPassed: false };
        }
    });

    // ── Four Pictures ──────────────────────────────────────────────────────

    ipcMain.handle('fp:getLevels', async () => {
        try {
            return await FpGamesDB('fpow_levels').orderBy('level_order', 'asc').select();
        } catch (e) {
            Log.error('[Games] fp:getLevels error:', e);
            return [];
        }
    });

    ipcMain.handle('fp:getSolvedLevelIds', async () => {
        try {
            const rows = await StoreDB('fpow_level_progress')
                .whereNotNull('solved_at')
                .select('level_id');
            return rows.map((r: any) => r.level_id as number);
        } catch (e) {
            Log.error('[Games] fp:getSolvedLevelIds error:', e);
            return [];
        }
    });

    ipcMain.handle('fp:markLevelSolved', async (_, levelId: number) => {
        try {
            const now = new Date().toISOString();
            const existing = await StoreDB('fpow_level_progress').where('level_id', levelId).first();
            if (existing) {
                await StoreDB('fpow_level_progress').where('level_id', levelId).update({ solved_at: now, hint_state: null });
            } else {
                await StoreDB('fpow_level_progress').insert({ level_id: levelId, solved_at: now, hint_state: null });
            }
            // No sync log — fpow_level_progress is local-only (backend not supported yet)
        } catch (e) {
            Log.error('[Games] fp:markLevelSolved error:', e);
        }
    });

    ipcMain.handle('fp:getImagesBasePath', () => {
        return path.join(app.getPath('userData'), 'Games', 'fp_images');
    });
}
```

- [ ] **Step 2: Register in IpcMainEvents.ts**

Open `Electron/IpcMainEvents/IpcMainEvents.ts`. Add import and call:

```typescript
import Games from './Games/Games';

// Inside the default export function, after DevotionDays():
Games();
```

- [ ] **Step 3: Verify TypeScript compiles**

```bash
yarn build 2>&1 | tail -5
```

Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add Electron/IpcMainEvents/Games/Games.ts Electron/IpcMainEvents/IpcMainEvents.ts
git commit -m "feat(games): add Games IPC handler (lives, Q&A, T/F, FP)"
```

---

## Task 6: Extend applyPullData + Push Allowlist

**Files:**
- Modify: `Electron/IpcMainEvents/Sync/SyncHandlers.ts`
- Modify: `FrontEndApp/src/util/Sync/sync.ts`

- [ ] **Step 1: Extend applyPullData in SyncHandlers.ts**

In `SyncHandlers.ts`, find the `ipcMain.handle('applyPullData', ...)` handler. Update the parameter type signature to include game tables:

```typescript
ipcMain.handle('applyPullData', async (event, pullData: {
    sync_logs?: any[];
    bookmarks?: any[];
    highlights?: any[];
    clip_notes?: any[];
    prayer_lists?: any[];
    prayer_days?: any[];
    devotion_days?: any[];
    notes?: any[];
    sermon_favorites?: any[];
    ai_conversations?: any[];
    game_lives?: any[];
    qa_group_progress?: any[];
    tf_group_progress?: any[];
}) => {
```

Then add three new blocks at the end of the `try` block, just before `return { success: true }`:

```typescript
            // 8. game_lives — insert new rows; update recovered flag if already exists
            for (const life of pullData.game_lives ?? []) {
                const key: string | undefined = life.life_key ?? life.life_lost_at;
                if (!key) continue;
                const existing = await StoreDB('game_lives').where('life_lost_at', key).first();
                if (!existing) {
                    await StoreDB('game_lives').insert({
                        life_lost_at: key,
                        recovered: life.recovered ? 1 : 0,
                        created_at: life.created_at ?? now,
                    });
                } else if (life.recovered && !existing.recovered) {
                    await StoreDB('game_lives').where('life_lost_at', key).update({ recovered: 1 });
                }
            }

            // 9. qa_group_progress — upsert; keep highest score, keep is_completed once true
            for (const p of pullData.qa_group_progress ?? []) {
                if (p.group_id == null) continue;
                const existing = await StoreDB('qa_group_progress').where('group_id', p.group_id).first();
                if (!existing) {
                    await StoreDB('qa_group_progress').insert({
                        group_id: p.group_id,
                        is_completed: p.is_completed ? 1 : 0,
                        high_score_percentage: p.high_score_percentage ?? 0,
                        times_played: p.times_played ?? 0,
                        completed_at: p.completed_at ?? null,
                        updated_at: now,
                    });
                } else {
                    const newScore = Math.max(existing.high_score_percentage, p.high_score_percentage ?? 0);
                    const newCompleted = existing.is_completed || (p.is_completed ? 1 : 0);
                    await StoreDB('qa_group_progress').where('group_id', p.group_id).update({
                        is_completed: newCompleted,
                        high_score_percentage: newScore,
                        times_played: Math.max(existing.times_played, p.times_played ?? 0),
                        completed_at: existing.completed_at ?? p.completed_at ?? null,
                        updated_at: now,
                    });
                }
            }

            // 10. tf_group_progress — same logic as qa_group_progress
            for (const p of pullData.tf_group_progress ?? []) {
                if (p.group_id == null) continue;
                const existing = await StoreDB('tf_group_progress').where('group_id', p.group_id).first();
                if (!existing) {
                    await StoreDB('tf_group_progress').insert({
                        group_id: p.group_id,
                        is_completed: p.is_completed ? 1 : 0,
                        high_score_percentage: p.high_score_percentage ?? 0,
                        times_played: p.times_played ?? 0,
                        completed_at: p.completed_at ?? null,
                        updated_at: now,
                    });
                } else {
                    const newScore = Math.max(existing.high_score_percentage, p.high_score_percentage ?? 0);
                    const newCompleted = existing.is_completed || (p.is_completed ? 1 : 0);
                    await StoreDB('tf_group_progress').where('group_id', p.group_id).update({
                        is_completed: newCompleted,
                        high_score_percentage: newScore,
                        times_played: Math.max(existing.times_played, p.times_played ?? 0),
                        completed_at: existing.completed_at ?? p.completed_at ?? null,
                        updated_at: now,
                    });
                }
            }
```

- [ ] **Step 2: Update sync.ts — push allowlist**

In `FrontEndApp/src/util/Sync/sync.ts`, find the `ALLOWED_TABLES` constant in `pushSync` (around line 29):

```typescript
const ALLOWED_TABLES = ['bookmarks', 'highlights', 'clip_notes', 'prayer_lists', 'prayer_days', 'devotion_days', 'notes', 'sermon_favorites', 'ai_conversations', 'game_lives', 'qa_group_progress', 'tf_group_progress'];
```

- [ ] **Step 3: Update sync.ts — pull destructure**

In `pullSync`, find the destructure from `response.data` (around line 112). Add the three game fields:

```typescript
const { sync_logs, bookmarks, highlights, clip_notes, prayer_lists, prayer_days, devotion_days,
        notes, sermon_favorites, ai_conversations, settings,
        game_lives, qa_group_progress, tf_group_progress,
        has_more, next_cursor, last_sync_timestamp } = response.data;
```

Then update the `applyPullData` call to pass them:

```typescript
await window.browserWindow.applyPullData({
    sync_logs,
    bookmarks,
    highlights,
    clip_notes,
    prayer_lists,
    prayer_days,
    devotion_days,
    notes,
    sermon_favorites,
    ai_conversations,
    settings,
    game_lives,
    qa_group_progress,
    tf_group_progress,
});
```

- [ ] **Step 4: Verify TypeScript compiles**

```bash
yarn build 2>&1 | tail -5
cd FrontEndApp && yarn typecheck 2>&1 | tail -10
```

- [ ] **Step 5: Commit**

```bash
git add Electron/IpcMainEvents/Sync/SyncHandlers.ts FrontEndApp/src/util/Sync/sync.ts
git commit -m "feat(games): extend applyPullData and push allowlist for game sync tables"
```

---

## Task 7: Preload + GlobalDeclare Types

**Files:**
- Modify: `Electron/preload.ts`
- Modify: `FrontEndApp/src/GlobalDeclare.ts`

- [ ] **Step 1: Add game IPC calls to preload.ts**

In `Electron/preload.ts`, add these entries inside the `contextBridge.exposeInMainWorld('browserWindow', { ... })` object, at the end before the closing `});`:

```typescript
        // Games — lives
        gameGetLives: () => ipcRenderer.invoke('game:getLives'),
        gameLoseLife: () => ipcRenderer.invoke('game:loseLife'),
        gameNextRecoveryAt: () => ipcRenderer.invoke('game:nextRecoveryAt'),
        gameRefillLives: () => ipcRenderer.invoke('game:refillLives'),

        // Games — Q&A
        qaGetGroups: () => ipcRenderer.invoke('qa:getGroups'),
        qaGetQuestionsForGroup: (groupId: number) => ipcRenderer.invoke('qa:getQuestionsForGroup', groupId),
        qaGetAllGroupProgress: () => ipcRenderer.invoke('qa:getAllGroupProgress'),
        qaSaveGroupProgress: (args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) =>
            ipcRenderer.invoke('qa:saveGroupProgress', args),

        // Games — True/False
        tfGetGroups: () => ipcRenderer.invoke('tf:getGroups'),
        tfGetStatementsForGroup: (groupId: number) => ipcRenderer.invoke('tf:getStatementsForGroup', groupId),
        tfGetAllGroupProgress: () => ipcRenderer.invoke('tf:getAllGroupProgress'),
        tfSaveGroupProgress: (args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) =>
            ipcRenderer.invoke('tf:saveGroupProgress', args),

        // Games — Four Pictures
        fpGetLevels: () => ipcRenderer.invoke('fp:getLevels'),
        fpGetSolvedLevelIds: () => ipcRenderer.invoke('fp:getSolvedLevelIds'),
        fpMarkLevelSolved: (levelId: number) => ipcRenderer.invoke('fp:markLevelSolved', levelId),
        fpGetImagesBasePath: () => ipcRenderer.invoke('fp:getImagesBasePath'),
```

- [ ] **Step 2: Add game types to GlobalDeclare.ts**

In `FrontEndApp/src/GlobalDeclare.ts`, add the following inside the `browserWindow: { ... }` interface, at the end before the closing `};`:

```typescript
            // Games — lives
            gameGetLives: () => Promise<number>;
            gameLoseLife: () => Promise<number>;
            gameNextRecoveryAt: () => Promise<string | null>;
            gameRefillLives: () => Promise<void>;

            // Games — Q&A
            qaGetGroups: () => Promise<Array<{ id: number; name: string; display_order: number; required_completed: number; passing_score: number }>>;
            qaGetQuestionsForGroup: (groupId: number) => Promise<Array<{ id: number; group_id: number; question: string; options: string[]; answer: number; proof: string; explanation: string | null }>>;
            qaGetAllGroupProgress: () => Promise<Array<{ group_id: number; is_completed: number; high_score_percentage: number; times_played: number; completed_at: string | null; updated_at: string }>>;
            qaSaveGroupProgress: (args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) => Promise<{ newlyPassed: boolean }>;

            // Games — True/False
            tfGetGroups: () => Promise<Array<{ id: number; name: string; display_order: number; required_completed: number; passing_score: number }>>;
            tfGetStatementsForGroup: (groupId: number) => Promise<Array<{ id: number; group_id: number; statement: string; answer: number; proof: string; explanation: string | null }>>;
            tfGetAllGroupProgress: () => Promise<Array<{ group_id: number; is_completed: number; high_score_percentage: number; times_played: number; completed_at: string | null; updated_at: string }>>;
            tfSaveGroupProgress: (args: { groupId: number; correctCount: number; totalCount: number; passingScore: number }) => Promise<{ newlyPassed: boolean }>;

            // Games — Four Pictures
            fpGetLevels: () => Promise<Array<{ id: number; level_order: number; word: string; image1: string; image2: string; image3: string; image4: string }>>;
            fpGetSolvedLevelIds: () => Promise<number[]>;
            fpMarkLevelSolved: (levelId: number) => Promise<void>;
            fpGetImagesBasePath: () => Promise<string>;
```

Also update the `applyPullData` type signature in `GlobalDeclare.ts` to add the three new game fields:

```typescript
            applyPullData: (data: {
                sync_logs?: any[];
                bookmarks?: any[];
                highlights?: any[];
                clip_notes?: any[];
                prayer_lists?: any[];
                prayer_days?: any[];
                devotion_days?: any[];
                notes?: any[];
                sermon_favorites?: any[];
                ai_conversations?: any[];
                settings?: any;
                game_lives?: any[];
                qa_group_progress?: any[];
                tf_group_progress?: any[];
            }) => Promise<{ success: boolean; error?: string }>;
```

- [ ] **Step 3: Verify TypeScript compiles**

```bash
yarn build 2>&1 | tail -5 && cd FrontEndApp && yarn typecheck 2>&1 | tail -10
```

- [ ] **Step 4: Commit**

```bash
git add Electron/preload.ts FrontEndApp/src/GlobalDeclare.ts
git commit -m "feat(games): expose game IPC in preload and add TypeScript types"
```

---

## Task 8: useGamesStore

**Files:**
- Create: `FrontEndApp/src/store/useGamesStore.ts`

- [ ] **Step 1: Create the store**

```typescript
// FrontEndApp/src/store/useGamesStore.ts
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import correctSoundUrl from '../assets/sounds/correct.mp3';
import wrongSoundUrl from '../assets/sounds/wrong.mp3';

export type GameType = 'qa' | 'tf' | 'fp';
export type GameState = 'idle' | 'playing' | 'answered' | 'gameOver' | 'completed';

interface GroupProgress {
    group_id: number;
    is_completed: number;
    high_score_percentage: number;
    times_played: number;
    completed_at: string | null;
    updated_at: string;
}

interface QAQuestion {
    id: number;
    group_id: number;
    question: string;
    options: string[];
    answer: number;
    proof: string;
    explanation: string | null;
}

interface TFStatement {
    id: number;
    group_id: number;
    statement: string;
    answer: number; // 1=True, 0=False
    proof: string;
    explanation: string | null;
}

interface FPLevel {
    id: number;
    level_order: number;
    word: string;
    image1: string;
    image2: string;
    image3: string;
    image4: string;
}

function playSound(url: string) {
    try { new Audio(url).play(); } catch (_) { /* best effort */ }
}

export const useGamesStore = defineStore('useGamesStore', () => {
    // ── Lives ────────────────────────────────────────────────────────────────
    const lives = ref(7);
    const nextRecoveryAt = ref<string | null>(null);
    let recoveryTimer: ReturnType<typeof setTimeout> | null = null;
    const isLoading = ref(false);

    // ── Q&A ──────────────────────────────────────────────────────────────────
    const qaGroups = ref<Array<{ id: number; name: string; display_order: number; required_completed: number; passing_score: number }>>([]);
    const qaGroupProgress = ref<Record<number, GroupProgress>>({});

    // ── T/F ──────────────────────────────────────────────────────────────────
    const tfGroups = ref<Array<{ id: number; name: string; display_order: number; required_completed: number; passing_score: number }>>([]);
    const tfGroupProgress = ref<Record<number, GroupProgress>>({});

    // ── FP ───────────────────────────────────────────────────────────────────
    const fpLevels = ref<FPLevel[]>([]);
    const fpSolvedIds = ref<Set<number>>(new Set());
    const fpImagesBasePath = ref('');

    // ── Active game state ────────────────────────────────────────────────────
    const activeGameType = ref<GameType | null>(null);
    const currentGroupId = ref<number | null>(null);
    const gameState = ref<GameState>('idle');
    const currentItems = ref<Array<QAQuestion | TFStatement>>([]);
    const currentIndex = ref(0);
    const score = ref(0);
    const streak = ref(0);
    const bestStreak = ref(0);
    const lastAnswerCorrect = ref<boolean | null>(null);
    const selectedAnswerIndex = ref<number | null>(null);
    const shuffledOptions = ref<string[]>([]);
    const shuffledCorrectIndex = ref(0);
    const newlyPassed = ref(false);

    // ── FP active state ──────────────────────────────────────────────────────
    const currentFpLevelIndex = ref(0);
    const fpGuessedLetters = ref<string[]>([]);
    const fpScrambledLetters = ref<string[]>([]);

    // ── Computed ─────────────────────────────────────────────────────────────
    const qaProgressSummary = computed(() => ({
        completed: Object.values(qaGroupProgress.value).filter(p => p.is_completed).length,
        total: qaGroups.value.length,
    }));
    const tfProgressSummary = computed(() => ({
        completed: Object.values(tfGroupProgress.value).filter(p => p.is_completed).length,
        total: tfGroups.value.length,
    }));
    const fpProgressSummary = computed(() => ({
        completed: fpSolvedIds.value.size,
        total: fpLevels.value.length,
    }));
    const currentQuestion = computed((): QAQuestion | TFStatement | null =>
        currentIndex.value < currentItems.value.length ? currentItems.value[currentIndex.value] : null
    );
    const totalItems = computed(() => currentItems.value.length);
    const canPlay = computed(() => lives.value > 0);
    const scorePercentage = computed(() =>
        totalItems.value === 0 ? 0 : Math.round((score.value / totalItems.value) * 100)
    );
    const currentFpLevel = computed((): FPLevel | null => {
        const unsolved = fpLevels.value.filter(l => !fpSolvedIds.value.has(l.id));
        return unsolved[currentFpLevelIndex.value] ?? null;
    });
    const qaIsGroupUnlocked = (groupId: number) => {
        const group = qaGroups.value.find(g => g.id === groupId);
        if (!group || group.required_completed === 0) return true;
        return Object.values(qaGroupProgress.value).filter(p => p.is_completed).length >= group.required_completed;
    };
    const tfIsGroupUnlocked = (groupId: number) => {
        const group = tfGroups.value.find(g => g.id === groupId);
        if (!group || group.required_completed === 0) return true;
        return Object.values(tfGroupProgress.value).filter(p => p.is_completed).length >= group.required_completed;
    };

    // ── Lives helpers ────────────────────────────────────────────────────────
    function scheduleRecoveryTimer() {
        if (recoveryTimer) clearTimeout(recoveryTimer);
        if (!nextRecoveryAt.value) return;
        const delay = new Date(nextRecoveryAt.value).getTime() - Date.now();
        if (delay <= 0) { refreshLives(); return; }
        recoveryTimer = setTimeout(refreshLives, delay);
    }

    async function refreshLives() {
        if (!window.isElectron) return;
        lives.value = await window.browserWindow.gameGetLives();
        nextRecoveryAt.value = await window.browserWindow.gameNextRecoveryAt();
        scheduleRecoveryTimer();
    }

    async function loseLife() {
        if (!window.isElectron) return;
        lives.value = await window.browserWindow.gameLoseLife();
        nextRecoveryAt.value = await window.browserWindow.gameNextRecoveryAt();
        scheduleRecoveryTimer();
    }

    // ── Init ─────────────────────────────────────────────────────────────────
    async function init() {
        if (!window.isElectron) return;
        isLoading.value = true;
        try {
            await Promise.all([
                refreshLives(),
                loadQAData(),
                loadTFData(),
                loadFPData(),
            ]);
        } finally {
            isLoading.value = false;
        }
    }

    async function loadQAData() {
        const [groups, progress] = await Promise.all([
            window.browserWindow.qaGetGroups(),
            window.browserWindow.qaGetAllGroupProgress(),
        ]);
        qaGroups.value = groups;
        qaGroupProgress.value = Object.fromEntries(progress.map(p => [p.group_id, p]));
    }

    async function loadTFData() {
        const [groups, progress] = await Promise.all([
            window.browserWindow.tfGetGroups(),
            window.browserWindow.tfGetAllGroupProgress(),
        ]);
        tfGroups.value = groups;
        tfGroupProgress.value = Object.fromEntries(progress.map(p => [p.group_id, p]));
    }

    async function loadFPData() {
        const [levels, solvedIds, basePath] = await Promise.all([
            window.browserWindow.fpGetLevels(),
            window.browserWindow.fpGetSolvedLevelIds(),
            window.browserWindow.fpGetImagesBasePath(),
        ]);
        fpLevels.value = levels;
        fpSolvedIds.value = new Set(solvedIds);
        fpImagesBasePath.value = basePath;
    }

    // Called after a pull sync to refresh lives + progress without resetting game state
    async function refreshAfterSync() {
        if (!window.isElectron) return;
        await Promise.all([refreshLives(), loadQAData(), loadTFData()]);
        // FP is local-only; no refresh needed
    }

    // ── Q&A game flow ─────────────────────────────────────────────────────────
    function shuffleQAOptions(q: QAQuestion) {
        const indexed = q.options.map((opt, i) => ({ i, opt }));
        for (let j = indexed.length - 1; j > 0; j--) {
            const k = Math.floor(Math.random() * (j + 1));
            [indexed[j], indexed[k]] = [indexed[k], indexed[j]];
        }
        shuffledOptions.value = indexed.map(x => x.opt);
        shuffledCorrectIndex.value = indexed.findIndex(x => x.i === q.answer);
    }

    async function startQAGame(groupId: number) {
        if (!canPlay.value) return;
        activeGameType.value = 'qa';
        currentGroupId.value = groupId;
        const questions = await window.browserWindow.qaGetQuestionsForGroup(groupId);
        currentItems.value = questions;
        currentIndex.value = 0;
        score.value = 0; streak.value = 0; bestStreak.value = 0;
        lastAnswerCorrect.value = null; selectedAnswerIndex.value = null; newlyPassed.value = false;
        shuffleQAOptions(questions[0] as QAQuestion);
        gameState.value = 'playing';
    }

    async function submitQAAnswer(answerIndex: number) {
        if (gameState.value !== 'playing') return;
        const correct = answerIndex === shuffledCorrectIndex.value;
        selectedAnswerIndex.value = answerIndex;
        lastAnswerCorrect.value = correct;
        if (correct) {
            score.value++; streak.value++;
            if (streak.value > bestStreak.value) bestStreak.value = streak.value;
            playSound(correctSoundUrl);
        } else {
            streak.value = 0;
            playSound(wrongSoundUrl);
            await loseLife();
        }
        gameState.value = 'answered';
    }

    async function nextQAQuestion() {
        if (gameState.value !== 'answered') return;
        if (lives.value <= 0) {
            await finalizeQAGame();
            gameState.value = 'gameOver';
            return;
        }
        currentIndex.value++;
        selectedAnswerIndex.value = null; lastAnswerCorrect.value = null;
        if (currentIndex.value >= currentItems.value.length) {
            await finalizeQAGame();
            gameState.value = 'completed';
        } else {
            shuffleQAOptions(currentItems.value[currentIndex.value] as QAQuestion);
            gameState.value = 'playing';
        }
    }

    async function finalizeQAGame() {
        if (currentGroupId.value == null) return;
        const group = qaGroups.value.find(g => g.id === currentGroupId.value);
        if (!group) return;
        const result = await window.browserWindow.qaSaveGroupProgress({
            groupId: currentGroupId.value,
            correctCount: score.value,
            totalCount: totalItems.value,
            passingScore: group.passing_score,
        });
        newlyPassed.value = result.newlyPassed;
        await loadQAData();
    }

    // ── T/F game flow ─────────────────────────────────────────────────────────
    async function startTFGame(groupId: number) {
        if (!canPlay.value) return;
        activeGameType.value = 'tf';
        currentGroupId.value = groupId;
        const statements = await window.browserWindow.tfGetStatementsForGroup(groupId);
        currentItems.value = statements;
        currentIndex.value = 0;
        score.value = 0; streak.value = 0; bestStreak.value = 0;
        lastAnswerCorrect.value = null; selectedAnswerIndex.value = null; newlyPassed.value = false;
        gameState.value = 'playing';
    }

    async function submitTFAnswer(isTrue: boolean) {
        if (gameState.value !== 'playing') return;
        const stmt = currentItems.value[currentIndex.value] as TFStatement;
        const correct = (isTrue ? 1 : 0) === stmt.answer;
        lastAnswerCorrect.value = correct;
        selectedAnswerIndex.value = isTrue ? 1 : 0;
        if (correct) {
            score.value++; streak.value++;
            if (streak.value > bestStreak.value) bestStreak.value = streak.value;
            playSound(correctSoundUrl);
        } else {
            streak.value = 0;
            playSound(wrongSoundUrl);
            await loseLife();
        }
        gameState.value = 'answered';
    }

    async function nextTFQuestion() {
        if (gameState.value !== 'answered') return;
        if (lives.value <= 0) {
            await finalizeTFGame();
            gameState.value = 'gameOver';
            return;
        }
        currentIndex.value++;
        selectedAnswerIndex.value = null; lastAnswerCorrect.value = null;
        if (currentIndex.value >= currentItems.value.length) {
            await finalizeTFGame();
            gameState.value = 'completed';
        } else {
            gameState.value = 'playing';
        }
    }

    async function finalizeTFGame() {
        if (currentGroupId.value == null) return;
        const group = tfGroups.value.find(g => g.id === currentGroupId.value);
        if (!group) return;
        const result = await window.browserWindow.tfSaveGroupProgress({
            groupId: currentGroupId.value,
            correctCount: score.value,
            totalCount: totalItems.value,
            passingScore: group.passing_score,
        });
        newlyPassed.value = result.newlyPassed;
        await loadTFData();
    }

    // ── FP game flow ───────────────────────────────────────────────────────────
    function buildFPScramble(word: string): string[] {
        const letters = word.toUpperCase().split('');
        // Pad to 12 scrambled tiles with random extras
        const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        while (letters.length < 12) {
            letters.push(alphabet[Math.floor(Math.random() * 26)]);
        }
        for (let j = letters.length - 1; j > 0; j--) {
            const k = Math.floor(Math.random() * (j + 1));
            [letters[j], letters[k]] = [letters[k], letters[j]];
        }
        return letters.slice(0, 12);
    }

    function startFPGame() {
        activeGameType.value = 'fp';
        currentFpLevelIndex.value = 0;
        const level = currentFpLevel.value;
        if (!level) return;
        fpGuessedLetters.value = new Array(level.word.length).fill('');
        fpScrambledLetters.value = buildFPScramble(level.word);
        gameState.value = 'playing';
    }

    function fpTapLetter(letter: string) {
        const emptyIndex = fpGuessedLetters.value.findIndex(l => l === '');
        if (emptyIndex === -1) return;
        fpGuessedLetters.value = [...fpGuessedLetters.value];
        fpGuessedLetters.value[emptyIndex] = letter;
        checkFPAnswer();
    }

    function fpRemoveLetter(index: number) {
        fpGuessedLetters.value = [...fpGuessedLetters.value];
        fpGuessedLetters.value[index] = '';
    }

    async function checkFPAnswer() {
        const level = currentFpLevel.value;
        if (!level) return;
        const guessed = fpGuessedLetters.value.join('').toUpperCase();
        if (guessed.length < level.word.length) return; // not yet complete
        if (guessed === level.word.toUpperCase()) {
            playSound(correctSoundUrl);
            await window.browserWindow.fpMarkLevelSolved(level.id);
            fpSolvedIds.value = new Set([...fpSolvedIds.value, level.id]);
            // Advance to next unsolved level
            const unsolved = fpLevels.value.filter(l => !fpSolvedIds.value.has(l.id));
            if (unsolved.length === 0) {
                gameState.value = 'completed';
            } else {
                currentFpLevelIndex.value = 0;
                const nextLevel = currentFpLevel.value;
                if (nextLevel) {
                    fpGuessedLetters.value = new Array(nextLevel.word.length).fill('');
                    fpScrambledLetters.value = buildFPScramble(nextLevel.word);
                }
            }
        } else {
            // Wrong — shake and clear
            playSound(wrongSoundUrl);
            await loseLife();
            if (lives.value <= 0) { gameState.value = 'gameOver'; return; }
            fpGuessedLetters.value = new Array(level.word.length).fill('');
        }
    }

    function exitGame() {
        gameState.value = 'idle';
        activeGameType.value = null;
        currentGroupId.value = null;
        currentItems.value = [];
        currentIndex.value = 0;
        score.value = 0; streak.value = 0; bestStreak.value = 0;
        lastAnswerCorrect.value = null; selectedAnswerIndex.value = null; newlyPassed.value = false;
        shuffledOptions.value = []; shuffledCorrectIndex.value = 0;
        fpGuessedLetters.value = []; fpScrambledLetters.value = [];
    }

    function $dispose() {
        if (recoveryTimer) clearTimeout(recoveryTimer);
    }

    return {
        // Lives
        lives, nextRecoveryAt, isLoading, refreshLives, loseLife,
        // Q&A
        qaGroups, qaGroupProgress, qaProgressSummary, qaIsGroupUnlocked,
        startQAGame, submitQAAnswer, nextQAQuestion,
        // T/F
        tfGroups, tfGroupProgress, tfProgressSummary, tfIsGroupUnlocked,
        startTFGame, submitTFAnswer, nextTFQuestion,
        // FP
        fpLevels, fpSolvedIds, fpImagesBasePath, fpProgressSummary,
        currentFpLevel, fpGuessedLetters, fpScrambledLetters,
        startFPGame, fpTapLetter, fpRemoveLetter,
        // Common game state
        activeGameType, currentGroupId, gameState, currentQuestion,
        totalItems, canPlay, scorePercentage, score, streak, bestStreak,
        lastAnswerCorrect, selectedAnswerIndex, shuffledOptions, shuffledCorrectIndex,
        newlyPassed, exitGame,
        // Init
        init, refreshAfterSync, $dispose,
    };
});
```

- [ ] **Step 2: Verify typecheck**

```bash
cd FrontEndApp && yarn typecheck 2>&1 | tail -15
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add FrontEndApp/src/store/useGamesStore.ts
git commit -m "feat(games): add useGamesStore Pinia store (lives, Q&A, T/F, FP)"
```

---

## Task 9: Router, Menu, and Sync Hook

**Files:**
- Modify: `FrontEndApp/src/router/router.ts`
- Modify: `FrontEndApp/src/store/menu.ts`
- Modify: `FrontEndApp/src/util/Sync/sync.ts`

- [ ] **Step 1: Add /games route to router.ts**

Open `FrontEndApp/src/router/router.ts`. Add the import and route:

```typescript
// Add near the top imports:
// (lazy-loaded — no static import needed)

// Add inside the routes array, after the DailyDevotional route:
{
    name: 'Games',
    path: '/games',
    component: () => import('../Views/Games/Games.vue'),
    beforeEnter: () => {
        // Games page is Electron-only — redirect web users away
        if (!window.isElectron) return { name: 'PrayerList' };
        return true;
    },
},
```

- [ ] **Step 2: Add Games entry to menu.ts**

Open `FrontEndApp/src/store/menu.ts`. Add the Trophy icon import from `@vicons/fluent`:

```typescript
import {
    // ... existing imports ...
    Trophy24Regular,
    Trophy24Filled,
} from '@vicons/fluent';
```

Then add a new entry to `menuUpperTabs` after the `DailyDevotional` entry and before `AI Assistant`:

```typescript
{
    label: 'Games',
    key: '/games',
    icon: renderNIcon(Trophy24Regular),
    iconDark: renderNIcon(Trophy24Filled),
},
```

Also add `'/games'` to the `enableTab` array:

```typescript
const enableTab = ref([
    'read-bible',
    'sermons',
    '/prayer-list',
    '/daily-devotional',
    '/games',          // ← add this
    '/ai-assistant',
    '/settings-page',
    '/create-sermon',
    '/donate-page',
]);
```

- [ ] **Step 3: Hook refreshAfterSync into reloadStoresAfterPull in sync.ts**

Open `FrontEndApp/src/util/Sync/sync.ts`. Add the import at the top:

```typescript
import { useGamesStore } from '../../store/useGamesStore';
```

Then in `reloadStoresAfterPull()`, add the call at the end:

```typescript
function reloadStoresAfterPull() {
    useNoteStore().loadNote();
    useBookmarkStore().getBookmarks();
    usePrayerListStore().loadPrayerLists();
    usePrayerStreakStore().loadDays();
    useDevotionStreakStore().loadDays();
    useBibleStore().getChapterHighlights();
    useClipNoteStore().getClipNotes();
    useConversationStore().loadConversations();
    useGamesStore().refreshAfterSync();   // ← add this line
}
```

- [ ] **Step 4: Verify typecheck**

```bash
cd FrontEndApp && yarn typecheck 2>&1 | tail -10
```

- [ ] **Step 5: Commit**

```bash
git add FrontEndApp/src/router/router.ts FrontEndApp/src/store/menu.ts FrontEndApp/src/util/Sync/sync.ts
git commit -m "feat(games): add /games route, Games sidebar entry, sync hook"
```

---

## Task 10: LivesBar and GameCard Components

**Files:**
- Create: `FrontEndApp/src/Views/Games/components/LivesBar.vue`
- Create: `FrontEndApp/src/Views/Games/components/GameCard.vue`

- [ ] **Step 1: Create LivesBar.vue**

```vue
<!-- FrontEndApp/src/Views/Games/components/LivesBar.vue -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps<{
    lives: number;
    nextRecoveryAt: string | null;
}>();

const MAX_LIVES = 7;
const countdown = ref('');
let ticker: ReturnType<typeof setInterval> | null = null;

function updateCountdown() {
    if (!props.nextRecoveryAt) { countdown.value = ''; return; }
    const diff = new Date(props.nextRecoveryAt).getTime() - Date.now();
    if (diff <= 0) { countdown.value = ''; return; }
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000).toString().padStart(2, '0');
    const s = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
    countdown.value = h > 0 ? `${h}h ${m}m ${s}s` : `${m}m ${s}s`;
}

onMounted(() => {
    updateCountdown();
    ticker = setInterval(updateCountdown, 1000);
});
onUnmounted(() => { if (ticker) clearInterval(ticker); });
</script>

<template>
    <div class="flex items-center justify-between p-4 rounded-xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800">
        <div>
            <p class="text-xs font-bold tracking-widest text-neutral-400 uppercase mb-2">Lives</p>
            <div class="flex gap-1">
                <span v-for="i in MAX_LIVES" :key="i" class="text-xl">
                    <span v-if="i <= lives" class="text-red-500">❤️</span>
                    <span v-else class="text-neutral-300 dark:text-neutral-600">🤍</span>
                </span>
            </div>
        </div>
        <div class="text-right">
            <span v-if="lives >= MAX_LIVES" class="px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">Full</span>
            <template v-else-if="countdown">
                <p class="text-xs text-neutral-400 mb-1">Next heart in</p>
                <span class="px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400">{{ countdown }}</span>
            </template>
        </div>
    </div>
</template>
```

- [ ] **Step 2: Create GameCard.vue**

```vue
<!-- FrontEndApp/src/Views/Games/components/GameCard.vue -->
<script setup lang="ts">
defineProps<{
    title: string;
    description: string;
    color: string;
    emoji: string;
    progress: { completed: number; total: number };
    disabled?: boolean;
}>();

const emit = defineEmits<{ play: [] }>();
</script>

<template>
    <div
        class="relative rounded-xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 p-4 cursor-pointer transition-opacity"
        :class="disabled ? 'opacity-50 cursor-not-allowed' : 'hover:shadow-md'"
        @click="!disabled && emit('play')"
    >
        <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl flex items-center justify-center text-2xl shrink-0" :style="`background: ${color}22`">
                {{ emoji }}
            </div>
            <div class="flex-1 min-w-0">
                <p class="font-semibold text-sm text-neutral-900 dark:text-neutral-100">{{ title }}</p>
                <p class="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5 line-clamp-2">{{ description }}</p>
                <div class="mt-3">
                    <div class="h-1.5 rounded-full bg-neutral-100 dark:bg-neutral-700 overflow-hidden">
                        <div
                            class="h-full rounded-full transition-all"
                            :style="`width: ${progress.total ? (progress.completed / progress.total) * 100 : 0}%; background: ${color}`"
                        />
                    </div>
                    <p class="text-xs text-neutral-400 mt-1.5 font-medium">
                        {{ progress.completed }} / {{ progress.total }} complete
                    </p>
                </div>
            </div>
            <span class="text-neutral-300 dark:text-neutral-600 text-lg">›</span>
        </div>
    </div>
</template>
```

- [ ] **Step 3: Commit**

```bash
git add FrontEndApp/src/Views/Games/components/
git commit -m "feat(games): add LivesBar and GameCard shared components"
```

---

## Task 11: Games Hub View

**Files:**
- Create: `FrontEndApp/src/Views/Games/Games.vue`

- [ ] **Step 1: Create Games.vue**

```vue
<!-- FrontEndApp/src/Views/Games/Games.vue -->
<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import { useGamesStore } from '../../store/useGamesStore';
import LivesBar from './components/LivesBar.vue';
import GameCard from './components/GameCard.vue';
import QAGroupsList from './QuestionAndAnswer/QAGroupsList.vue';
import QAGameplay from './QuestionAndAnswer/QAGameplay.vue';
import TFGroupsList from './TrueOrFalse/TFGroupsList.vue';
import TFGameplay from './TrueOrFalse/TFGameplay.vue';
import FPGameplay from './FourPictures/FPGameplay.vue';

type Screen = 'hub' | 'qa-groups' | 'qa-play' | 'tf-groups' | 'tf-play' | 'fp-play';

const store = useGamesStore();
const activeScreen = ref<Screen>('hub');

onMounted(() => store.init());
onUnmounted(() => store.$dispose());

function goHub() {
    store.exitGame();
    activeScreen.value = 'hub';
}
function openQA() { activeScreen.value = 'qa-groups'; }
function openTF() { activeScreen.value = 'tf-groups'; }
function openFP() {
    store.startFPGame();
    activeScreen.value = 'fp-play';
}
function onQAGroupSelected(groupId: number) {
    store.startQAGame(groupId);
    activeScreen.value = 'qa-play';
}
function onTFGroupSelected(groupId: number) {
    store.startTFGame(groupId);
    activeScreen.value = 'tf-play';
}
</script>

<template>
    <div class="h-full overflow-y-auto p-4 space-y-3 max-w-2xl mx-auto">
        <!-- Hub -->
        <template v-if="activeScreen === 'hub'">
            <h1 class="text-xl font-bold text-neutral-900 dark:text-neutral-100 pt-1">Bible Games</h1>
            <LivesBar :lives="store.lives" :next-recovery-at="store.nextRecoveryAt" />
            <div v-if="store.isLoading" class="space-y-3">
                <div v-for="i in 3" :key="i" class="h-28 rounded-xl bg-neutral-100 dark:bg-neutral-800 animate-pulse" />
            </div>
            <template v-else>
                <GameCard
                    title="Question & Answer"
                    description="Answer multiple-choice Bible questions and unlock new groups."
                    color="#3b82f6"
                    emoji="📖"
                    :progress="store.qaProgressSummary"
                    @play="openQA"
                />
                <GameCard
                    title="True or False"
                    description="Evaluate Bible statements as True or False."
                    color="#10b981"
                    emoji="✅"
                    :progress="store.tfProgressSummary"
                    @play="openTF"
                />
                <GameCard
                    title="4 Pictures 1 Word"
                    description="Guess the Bible word from four picture clues."
                    color="#f59e0b"
                    emoji="🖼️"
                    :progress="store.fpProgressSummary"
                    @play="openFP"
                />
            </template>
        </template>

        <!-- Q&A groups list -->
        <QAGroupsList
            v-else-if="activeScreen === 'qa-groups'"
            @back="goHub"
            @select="onQAGroupSelected"
        />

        <!-- Q&A gameplay -->
        <QAGameplay
            v-else-if="activeScreen === 'qa-play'"
            @back="activeScreen = 'qa-groups'"
            @exit="goHub"
        />

        <!-- T/F groups list -->
        <TFGroupsList
            v-else-if="activeScreen === 'tf-groups'"
            @back="goHub"
            @select="onTFGroupSelected"
        />

        <!-- T/F gameplay -->
        <TFGameplay
            v-else-if="activeScreen === 'tf-play'"
            @back="activeScreen = 'tf-groups'"
            @exit="goHub"
        />

        <!-- FP gameplay -->
        <FPGameplay
            v-else-if="activeScreen === 'fp-play'"
            @exit="goHub"
        />
    </div>
</template>
```

- [ ] **Step 2: Commit**

```bash
git add FrontEndApp/src/Views/Games/Games.vue
git commit -m "feat(games): add Games hub view with navigation controller"
```

---

## Task 12: Q&A Views

**Files:**
- Create: `FrontEndApp/src/Views/Games/QuestionAndAnswer/QAGroupsList.vue`
- Create: `FrontEndApp/src/Views/Games/QuestionAndAnswer/QAGameplay.vue`

- [ ] **Step 1: Create QAGroupsList.vue**

```vue
<!-- FrontEndApp/src/Views/Games/QuestionAndAnswer/QAGroupsList.vue -->
<script setup lang="ts">
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ back: []; select: [groupId: number] }>();
const store = useGamesStore();
</script>

<template>
    <div class="space-y-3">
        <div class="flex items-center gap-3">
            <button @click="emit('back')" class="p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 text-neutral-500">
                ← Back
            </button>
            <h2 class="text-lg font-bold text-neutral-900 dark:text-neutral-100">Question & Answer</h2>
        </div>
        <div v-for="group in store.qaGroups" :key="group.id"
             class="flex items-center justify-between p-4 rounded-xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800">
            <div class="flex-1">
                <p class="font-medium text-sm text-neutral-900 dark:text-neutral-100">{{ group.name }}</p>
                <p v-if="store.qaGroupProgress[group.id]" class="text-xs text-neutral-400 mt-0.5">
                    Best: {{ store.qaGroupProgress[group.id].high_score_percentage }}%
                    · Played {{ store.qaGroupProgress[group.id].times_played }}×
                </p>
                <p v-if="store.qaGroupProgress[group.id]?.is_completed" class="text-xs text-green-600 mt-0.5 font-medium">✓ Passed</p>
            </div>
            <button
                v-if="store.qaIsGroupUnlocked(group.id)"
                @click="emit('select', group.id)"
                class="px-4 py-1.5 rounded-lg text-sm font-semibold bg-blue-500 text-white hover:bg-blue-600 shrink-0 ml-3"
            >
                Play
            </button>
            <span v-else class="text-neutral-300 text-lg ml-3">🔒</span>
        </div>
    </div>
</template>
```

- [ ] **Step 2: Create QAGameplay.vue**

```vue
<!-- FrontEndApp/src/Views/Games/QuestionAndAnswer/QAGameplay.vue -->
<script setup lang="ts">
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ back: []; exit: [] }>();
const store = useGamesStore();

function answerClass(i: number) {
    if (store.gameState !== 'answered') return 'bg-white dark:bg-neutral-800 border-neutral-200 dark:border-neutral-700 hover:border-blue-400';
    if (i === store.shuffledCorrectIndex) return 'bg-green-50 dark:bg-green-900/30 border-green-500 text-green-700 dark:text-green-300';
    if (i === store.selectedAnswerIndex && !store.lastAnswerCorrect) return 'bg-red-50 dark:bg-red-900/30 border-red-500 text-red-700 dark:text-red-300';
    return 'bg-white dark:bg-neutral-800 border-neutral-200 dark:border-neutral-700 opacity-50';
}
</script>

<template>
    <div class="space-y-4">
        <!-- Header -->
        <div class="flex items-center justify-between">
            <button @click="emit('back')" class="p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 text-neutral-500 text-sm">← Groups</button>
            <div class="flex items-center gap-3 text-sm text-neutral-500">
                <span>❤️ {{ store.lives }}</span>
                <span>Score: {{ store.score }}/{{ store.totalItems }}</span>
            </div>
        </div>

        <!-- Game over / completed overlays -->
        <div v-if="store.gameState === 'gameOver' || store.gameState === 'completed'"
             class="p-6 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-center space-y-4">
            <p class="text-3xl">{{ store.gameState === 'completed' ? '🎉' : '💔' }}</p>
            <p class="text-xl font-bold text-neutral-900 dark:text-neutral-100">
                {{ store.gameState === 'completed' ? (store.newlyPassed ? 'Passed!' : 'Completed!') : 'Out of lives' }}
            </p>
            <p class="text-neutral-500">Score: {{ store.score }} / {{ store.totalItems }} ({{ store.scorePercentage }}%)</p>
            <p class="text-neutral-500">Best streak: {{ store.bestStreak }}</p>
            <div class="flex gap-3 justify-center">
                <button @click="emit('back')" class="px-5 py-2 rounded-xl bg-blue-500 text-white font-semibold hover:bg-blue-600">Back to Groups</button>
                <button @click="emit('exit')" class="px-5 py-2 rounded-xl border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700">Exit</button>
            </div>
        </div>

        <!-- Playing / answered -->
        <template v-else-if="store.currentQuestion">
            <div class="p-5 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800">
                <p class="text-xs text-neutral-400 mb-2 font-medium">Question {{ store.currentIndex + 1 }} of {{ store.totalItems }}</p>
                <p class="text-base font-medium text-neutral-900 dark:text-neutral-100 leading-relaxed">
                    {{ (store.currentQuestion as any).question }}
                </p>
            </div>

            <div class="space-y-2">
                <button
                    v-for="(opt, i) in store.shuffledOptions"
                    :key="i"
                    :disabled="store.gameState === 'answered'"
                    @click="store.submitQAAnswer(i)"
                    class="w-full text-left px-4 py-3 rounded-xl border text-sm font-medium transition-colors"
                    :class="answerClass(i)"
                >
                    {{ opt }}
                </button>
            </div>

            <!-- Explanation + Next -->
            <template v-if="store.gameState === 'answered'">
                <p v-if="(store.currentQuestion as any).explanation" class="text-sm text-neutral-500 bg-neutral-50 dark:bg-neutral-800 p-3 rounded-xl border border-neutral-200 dark:border-neutral-700">
                    {{ (store.currentQuestion as any).explanation }}
                </p>
                <button @click="store.nextQAQuestion()" class="w-full py-3 rounded-xl bg-blue-500 text-white font-semibold hover:bg-blue-600">
                    {{ store.currentIndex + 1 >= store.totalItems ? 'Finish' : 'Next' }}
                </button>
            </template>
        </template>
    </div>
</template>
```

- [ ] **Step 3: Commit**

```bash
git add FrontEndApp/src/Views/Games/QuestionAndAnswer/
git commit -m "feat(games): add QAGroupsList and QAGameplay views"
```

---

## Task 13: True/False Views

**Files:**
- Create: `FrontEndApp/src/Views/Games/TrueOrFalse/TFGroupsList.vue`
- Create: `FrontEndApp/src/Views/Games/TrueOrFalse/TFGameplay.vue`

- [ ] **Step 1: Create TFGroupsList.vue**

```vue
<!-- FrontEndApp/src/Views/Games/TrueOrFalse/TFGroupsList.vue -->
<script setup lang="ts">
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ back: []; select: [groupId: number] }>();
const store = useGamesStore();
</script>

<template>
    <div class="space-y-3">
        <div class="flex items-center gap-3">
            <button @click="emit('back')" class="p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 text-neutral-500">← Back</button>
            <h2 class="text-lg font-bold text-neutral-900 dark:text-neutral-100">True or False</h2>
        </div>
        <div v-for="group in store.tfGroups" :key="group.id"
             class="flex items-center justify-between p-4 rounded-xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800">
            <div class="flex-1">
                <p class="font-medium text-sm text-neutral-900 dark:text-neutral-100">{{ group.name }}</p>
                <p v-if="store.tfGroupProgress[group.id]" class="text-xs text-neutral-400 mt-0.5">
                    Best: {{ store.tfGroupProgress[group.id].high_score_percentage }}%
                    · Played {{ store.tfGroupProgress[group.id].times_played }}×
                </p>
                <p v-if="store.tfGroupProgress[group.id]?.is_completed" class="text-xs text-green-600 mt-0.5 font-medium">✓ Passed</p>
            </div>
            <button
                v-if="store.tfIsGroupUnlocked(group.id)"
                @click="emit('select', group.id)"
                class="px-4 py-1.5 rounded-lg text-sm font-semibold bg-emerald-500 text-white hover:bg-emerald-600 shrink-0 ml-3"
            >
                Play
            </button>
            <span v-else class="text-neutral-300 text-lg ml-3">🔒</span>
        </div>
    </div>
</template>
```

- [ ] **Step 2: Create TFGameplay.vue**

```vue
<!-- FrontEndApp/src/Views/Games/TrueOrFalse/TFGameplay.vue -->
<script setup lang="ts">
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ back: []; exit: [] }>();
const store = useGamesStore();

function btnClass(isTrue: boolean) {
    const selected = store.selectedAnswerIndex === (isTrue ? 1 : 0);
    const correct = (store.currentQuestion as any)?.answer === (isTrue ? 1 : 0);
    if (store.gameState !== 'answered') {
        return isTrue
            ? 'bg-emerald-500 hover:bg-emerald-600 text-white'
            : 'bg-red-500 hover:bg-red-600 text-white';
    }
    if (correct) return 'bg-green-100 dark:bg-green-900/30 border-2 border-green-500 text-green-700 dark:text-green-300';
    if (selected) return 'bg-red-100 dark:bg-red-900/30 border-2 border-red-500 text-red-700 dark:text-red-300';
    return 'opacity-40 ' + (isTrue ? 'bg-emerald-500 text-white' : 'bg-red-500 text-white');
}
</script>

<template>
    <div class="space-y-4">
        <div class="flex items-center justify-between">
            <button @click="emit('back')" class="p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-700 text-neutral-500 text-sm">← Groups</button>
            <div class="flex items-center gap-3 text-sm text-neutral-500">
                <span>❤️ {{ store.lives }}</span>
                <span>Score: {{ store.score }}/{{ store.totalItems }}</span>
            </div>
        </div>

        <div v-if="store.gameState === 'gameOver' || store.gameState === 'completed'"
             class="p-6 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-center space-y-4">
            <p class="text-3xl">{{ store.gameState === 'completed' ? '🎉' : '💔' }}</p>
            <p class="text-xl font-bold text-neutral-900 dark:text-neutral-100">
                {{ store.gameState === 'completed' ? (store.newlyPassed ? 'Passed!' : 'Completed!') : 'Out of lives' }}
            </p>
            <p class="text-neutral-500">Score: {{ store.score }} / {{ store.totalItems }} ({{ store.scorePercentage }}%)</p>
            <div class="flex gap-3 justify-center">
                <button @click="emit('back')" class="px-5 py-2 rounded-xl bg-emerald-500 text-white font-semibold hover:bg-emerald-600">Back to Groups</button>
                <button @click="emit('exit')" class="px-5 py-2 rounded-xl border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300 hover:bg-neutral-50 dark:hover:bg-neutral-700">Exit</button>
            </div>
        </div>

        <template v-else-if="store.currentQuestion">
            <div class="p-5 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800">
                <p class="text-xs text-neutral-400 mb-2 font-medium">Statement {{ store.currentIndex + 1 }} of {{ store.totalItems }}</p>
                <p class="text-base font-medium text-neutral-900 dark:text-neutral-100 leading-relaxed">
                    {{ (store.currentQuestion as any).statement }}
                </p>
            </div>

            <div class="grid grid-cols-2 gap-3">
                <button :disabled="store.gameState === 'answered'" @click="store.submitTFAnswer(true)"
                        class="py-4 rounded-xl text-lg font-bold transition-all" :class="btnClass(true)">
                    ✓ True
                </button>
                <button :disabled="store.gameState === 'answered'" @click="store.submitTFAnswer(false)"
                        class="py-4 rounded-xl text-lg font-bold transition-all" :class="btnClass(false)">
                    ✗ False
                </button>
            </div>

            <template v-if="store.gameState === 'answered'">
                <p v-if="(store.currentQuestion as any).explanation" class="text-sm text-neutral-500 bg-neutral-50 dark:bg-neutral-800 p-3 rounded-xl border border-neutral-200 dark:border-neutral-700">
                    {{ (store.currentQuestion as any).explanation }}
                </p>
                <button @click="store.nextTFQuestion()" class="w-full py-3 rounded-xl bg-emerald-500 text-white font-semibold hover:bg-emerald-600">
                    {{ store.currentIndex + 1 >= store.totalItems ? 'Finish' : 'Next' }}
                </button>
            </template>
        </template>
    </div>
</template>
```

- [ ] **Step 3: Commit**

```bash
git add FrontEndApp/src/Views/Games/TrueOrFalse/
git commit -m "feat(games): add TFGroupsList and TFGameplay views"
```

---

## Task 14: Four Pictures View

**Files:**
- Create: `FrontEndApp/src/Views/Games/FourPictures/FPGameplay.vue`

- [ ] **Step 1: Create FPGameplay.vue**

```vue
<!-- FrontEndApp/src/Views/Games/FourPictures/FPGameplay.vue -->
<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue';
import { useGamesStore } from '../../../store/useGamesStore';

const emit = defineEmits<{ exit: [] }>();
const store = useGamesStore();

const level = computed(() => store.currentFpLevel);
const images = computed(() => {
    if (!level.value) return [];
    const base = store.fpImagesBasePath;
    return [level.value.image1, level.value.image2, level.value.image3, level.value.image4]
        .map(name => `file://${base}/${name}`);
});

function onKeyDown(e: KeyboardEvent) {
    if (store.gameState !== 'playing') return;
    const letter = e.key.toUpperCase();
    if (/^[A-Z]$/.test(letter)) {
        store.fpTapLetter(letter);
    } else if (e.key === 'Backspace') {
        const lastFilled = [...store.fpGuessedLetters].reverse().findIndex(l => l !== '');
        if (lastFilled !== -1) store.fpRemoveLetter(store.fpGuessedLetters.length - 1 - lastFilled);
    }
}

onMounted(() => window.addEventListener('keydown', onKeyDown));
onUnmounted(() => window.removeEventListener('keydown', onKeyDown));
</script>

<template>
    <div class="space-y-4">
        <div class="flex items-center justify-between">
            <h2 class="text-lg font-bold text-neutral-900 dark:text-neutral-100">4 Pictures 1 Word</h2>
            <div class="flex items-center gap-3 text-sm text-neutral-500">
                <span>❤️ {{ store.lives }}</span>
                <span>{{ store.fpProgressSummary.completed }}/{{ store.fpProgressSummary.total }}</span>
            </div>
        </div>

        <!-- Completed -->
        <div v-if="store.gameState === 'completed'"
             class="p-6 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-center space-y-4">
            <p class="text-4xl">🏆</p>
            <p class="text-xl font-bold text-neutral-900 dark:text-neutral-100">All levels complete!</p>
            <p class="text-neutral-500">You solved all {{ store.fpProgressSummary.total }} levels.</p>
            <button @click="emit('exit')" class="px-5 py-2 rounded-xl bg-amber-500 text-white font-semibold hover:bg-amber-600">Back to Hub</button>
        </div>

        <!-- Game over -->
        <div v-else-if="store.gameState === 'gameOver'"
             class="p-6 rounded-2xl border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-center space-y-4">
            <p class="text-3xl">💔</p>
            <p class="text-xl font-bold text-neutral-900 dark:text-neutral-100">Out of lives</p>
            <div class="flex gap-3 justify-center">
                <button @click="store.startFPGame()" class="px-5 py-2 rounded-xl bg-amber-500 text-white font-semibold hover:bg-amber-600">Try Again</button>
                <button @click="emit('exit')" class="px-5 py-2 rounded-xl border border-neutral-300 dark:border-neutral-600 text-neutral-700 dark:text-neutral-300">Exit</button>
            </div>
        </div>

        <!-- Playing -->
        <template v-else-if="level">
            <!-- 2×2 image grid -->
            <div class="grid grid-cols-2 gap-2">
                <div v-for="(src, i) in images" :key="i"
                     class="aspect-square rounded-xl overflow-hidden bg-neutral-100 dark:bg-neutral-700">
                    <img :src="src" class="w-full h-full object-cover" @error="(e) => (e.target as HTMLImageElement).style.display='none'" />
                </div>
            </div>

            <!-- Word tiles -->
            <div class="flex gap-2 justify-center flex-wrap">
                <div v-for="(letter, i) in store.fpGuessedLetters" :key="i"
                     class="w-10 h-10 rounded-lg border-2 flex items-center justify-center text-lg font-bold cursor-pointer select-none transition-colors"
                     :class="letter ? 'border-amber-400 bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300' : 'border-neutral-300 dark:border-neutral-600'"
                     @click="letter && store.fpRemoveLetter(i)">
                    {{ letter }}
                </div>
            </div>

            <!-- Scrambled letters -->
            <div class="flex gap-2 justify-center flex-wrap">
                <button v-for="(letter, i) in store.fpScrambledLetters" :key="i"
                        @click="store.fpTapLetter(letter)"
                        class="w-10 h-10 rounded-lg bg-neutral-100 dark:bg-neutral-700 hover:bg-neutral-200 dark:hover:bg-neutral-600 flex items-center justify-center text-sm font-bold text-neutral-700 dark:text-neutral-300 transition-colors">
                    {{ letter }}
                </button>
            </div>

            <p class="text-xs text-neutral-400 text-center">Tap a letter tile to remove it · Type or click letters to guess</p>
        </template>
    </div>
</template>
```

- [ ] **Step 2: Commit**

```bash
git add FrontEndApp/src/Views/Games/FourPictures/FPGameplay.vue
git commit -m "feat(games): add FPGameplay view (Four Pictures 1 Word)"
```

---

## Task 15: End-to-End Smoke Test

- [ ] **Step 1: Start the app in dev mode**

```bash
cd D:\Projects\Personal\Believers-Sword && yarn start
```

Wait for the Electron window to open.

- [ ] **Step 2: Verify game DBs were seeded**

In the Electron DevTools console (Ctrl+Shift+I), run:

```javascript
window.browserWindow.qaGetGroups().then(g => console.log('QA groups:', g.length))
window.browserWindow.tfGetGroups().then(g => console.log('TF groups:', g.length))
window.browserWindow.fpGetLevels().then(l => console.log('FP levels:', l.length))
```

Expected: each returns a non-zero array of groups/levels.

- [ ] **Step 3: Verify the Games sidebar entry appears**

Click the trophy icon in the sidebar. Expected: navigates to `/games`, shows the hub with LivesBar and 3 GameCards.

- [ ] **Step 4: Test Q&A game**

- Click Q&A → group list appears  
- Click Play on the first group → play screen appears with a question  
- Click an answer → correct (green) or wrong (red) highlighted  
- Click Next → next question or game over/completed  
- Check DevTools console: no errors

- [ ] **Step 5: Test True/False game**

Same flow as Q&A but with True/False buttons.

- [ ] **Step 6: Test Four Pictures**

- Click 4 Pictures 1 Word → FPGameplay screen  
- Four images appear (or gray placeholder if image missing)  
- Tapping letter tiles fills word slots  
- Correct word → moves to next level  
- Check DevTools console: no errors

- [ ] **Step 7: Verify lives sync (if logged in and Sync-entitled)**

- Lose a life in a game  
- Open DevTools console: `window.browserWindow.getUnsyncedChanges().then(c => console.log(c.filter(x => x.table_name === 'game_lives')))`  
- Expected: one unsynced `game_lives` entry with `action: 'created'`

- [ ] **Step 8: Commit final verification note**

```bash
git commit --allow-empty -m "chore(games): smoke-tested E2E — all 3 games load, play, sync"
```

---

## Task 16: Update docs/desktop.md

**Files:**
- Modify: `docs/desktop.md`

- [ ] **Step 1: Add Games section to desktop docs**

Open `docs/desktop.md`. Add a new entry to the Views directory listing:

```markdown
│   ├── Games/                              # Bible Games hub + gameplay
│   │   ├── Games.vue                       # Hub: lives bar + 3 game cards, in-page nav controller
│   │   ├── components/LivesBar.vue         # 7-heart lives display with recovery countdown
│   │   ├── components/GameCard.vue         # Game type card with progress bar
│   │   ├── QuestionAndAnswer/QAGroupsList.vue  # Q&A group selection
│   │   ├── QuestionAndAnswer/QAGameplay.vue    # Q&A multiple-choice play screen
│   │   ├── TrueOrFalse/TFGroupsList.vue    # T/F group selection
│   │   ├── TrueOrFalse/TFGameplay.vue      # T/F play screen
│   │   └── FourPictures/FPGameplay.vue     # 4 Pictures 1 Word play screen
```

Also add `useGamesStore.ts` to the store listing, and note in the Architecture section:

```markdown
**Games**: All 3 game types (Q&A, True/False, Four Pictures) run inside the `/games` route. Game content DBs are seeded to `userData/Games/` by `SetGamesDB.ts` on startup (same versioned-copy pattern as devotionals.db). `game_lives`, `qa_group_progress`, and `tf_group_progress` sync via `sync_logs` to the backend — same tables as mobile. `fpow_level_progress` is local-only. Electron-only: the route guard redirects web users.
```

- [ ] **Step 2: Commit**

```bash
git add docs/desktop.md
git commit -m "docs: update desktop.md with Games page architecture"
```
