# Desktop Games Page — Design Spec

**Date:** 2026-06-13
**Scope:** Electron desktop app only. Web view deferred.
**Goal:** Add a fully-functional Games page to the desktop app that mirrors the mobile app's game architecture and syncs `game_lives`, `qa_group_progress`, and `tf_group_progress` with the backend (same tables mobile uses).

---

## Overview

The mobile app has three Bible quiz games — Q&A, True/False, and Four Pictures — backed by bundled SQLite content DBs, a shared 7-life system stored in `Store.db`, and backend sync for lives and group progress. The desktop has no game infrastructure at all. This spec adds it end-to-end.

---

## Sync Scope

| Table | Mobile syncs | Backend supports | Desktop target |
|---|---|---|---|
| `game_lives` | Yes — `logSync` on loseLife/recover | Yes — `user_game_lives` | Match mobile exactly |
| `qa_group_progress` | Yes — `logSync` on saveGroupProgress | Yes — `user_game_qa_progress` | Match mobile exactly |
| `tf_group_progress` | Yes — `logSync` on saveGroupProgress | Yes — `user_game_tf_progress` | Match mobile exactly |
| `fpow_level_progress` | `logSync` called but backend ignores it | Not supported yet | Local only (same as mobile) |

The desktop's `applyPullData` IPC handler must be extended to apply all three synced game tables when pulling from the backend.

---

## Asset Setup

Game content DBs and images are bundled in `defaults/Main/games/` (picked up by `extraResources` in `package.json`). On startup, `SetGamesDB.ts` copies each to `userData/Games/` — same version-check pattern as `SetDevotionalsDB.ts`.

```
defaults/Main/games/
  qa/
    game_seed.db          ← copy from mobile assets/game/question_and_answer/game_seed.db
    version.json          ← copy from mobile assets/game/question_and_answer/seed_data_version.json
  tf/
    game_seed.db          ← copy from mobile assets/game/true_or_false/game_seed.db
    version.json          ← copy from mobile assets/game/true_or_false/seed_data_version.json
  fp/
    game_seed.db          ← copy from mobile assets/game/4_picture_one_word/game_seed.db
    version.json          ← copy from mobile assets/game/4_picture_one_word/seed_data_version.json
    images/               ← copy from mobile assets/game/4_picture_one_word/images/
```

Sound files are bundled in the Vite renderer (no IPC needed):
```
FrontEndApp/src/assets/sounds/
  correct.mp3             ← copy from mobile assets/sound/correct.mp3
  wrong.mp3               ← copy from mobile assets/sound/wrong.mp3
```

---

## Electron Layer

### DataBase.ts — new connections

```ts
export const QaGamesDB = knex({ client: 'sqlite3', useNullAsDefault: false,
  connection: { filename: dataPath + '\\Games\\qa_games.db' } });
export const TfGamesDB = knex({ client: 'sqlite3', useNullAsDefault: false,
  connection: { filename: dataPath + '\\Games\\tf_games.db' } });
export const FpGamesDB = knex({ client: 'sqlite3', useNullAsDefault: false,
  connection: { filename: dataPath + '\\Games\\fp_games.db' } });
```

### SetGamesDB.ts

Reads `version.json` from defaults, compares against `userData/Games/{type}_version.json`, copies DB (and images folder for FP) if missing or outdated. Resolves a `Promise<void>` same as `setDevotionalsDB`. Called from `setup.ts`.

### Store.db Migrations (4 new files)

**`game_lives.migration.ts`** — identical schema to mobile:
```sql
CREATE TABLE game_lives (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  life_lost_at TEXT NOT NULL,   -- ISO8601 UTC; also used as the sync record_key
  recovered    INTEGER DEFAULT 0,
  created_at   TEXT NOT NULL
)
```

**`qa_group_progress.migration.ts`**:
```sql
CREATE TABLE qa_group_progress (
  group_id              INTEGER PRIMARY KEY,
  is_completed          INTEGER DEFAULT 0,
  high_score_percentage INTEGER DEFAULT 0,
  times_played          INTEGER DEFAULT 0,
  completed_at          TEXT,
  updated_at            TEXT NOT NULL
)
```

**`tf_group_progress.migration.ts`** — same schema as qa, table name `tf_group_progress`.

**`fpow_level_progress.migration.ts`**:
```sql
CREATE TABLE fpow_level_progress (
  level_id   INTEGER PRIMARY KEY,
  solved_at  TEXT,
  hint_state TEXT
)
```

### IpcMainEvents/Games/Games.ts

Single handler file for all game types. All handlers follow the `try/catch + Log.error` pattern.

**Lives (sync-aware):**
- `game:getLives` — processes recoveries (mark rows where `life_lost_at <= now - 2h` as recovered=1, log sync update for each), returns `maxLives - unrecovedCount`
- `game:loseLife` — inserts row, logs sync `created`, returns new lives count
- `game:nextRecoveryAt` — returns ISO string of `life_lost_at + 2h` for oldest unrecovered row, or null
- `game:refillLives` — marks all unrecovered rows as recovered=1, logs sync `updated` for each

**Q&A:**
- `qa:getGroups` — `SELECT * FROM question_groups ORDER BY display_order ASC` on `QaGamesDB`
- `qa:getQuestionsForGroup(groupId)` — questions for group, shuffled via `ORDER BY RANDOM()`
- `qa:getAllGroupProgress` — all rows from `StoreDB('qa_group_progress')`
- `qa:saveGroupProgress({groupId, correctCount, totalCount, passingScore})` — upsert, log sync `created`/`updated`

**True/False:**
- `tf:getGroups` — `SELECT * FROM tf_groups ORDER BY display_order ASC` on `TfGamesDB`
- `tf:getStatementsForGroup(groupId)` — statements for group, shuffled
- `tf:getAllGroupProgress` — all rows from `StoreDB('tf_group_progress')`
- `tf:saveGroupProgress(...)` — same pattern as Q&A, record_key `tf_group_${groupId}`

**Four Pictures:**
- `fp:getLevels` — `SELECT * FROM fpow_levels ORDER BY level_order ASC` on `FpGamesDB`
- `fp:getSolvedLevelIds` — solved level_ids from `fpow_level_progress WHERE solved_at IS NOT NULL`
- `fp:markLevelSolved(levelId)` — upsert `fpow_level_progress` — **no** sync log (same as mobile)
- `fp:getImagesBasePath` — returns `userData/Games/fp_images/` path

### SyncHandlers.ts — applyPullData extension

Add three new blocks to the existing handler:

```ts
// game_lives — insert new; update recovered flag if already exists
for (const life of pullData.game_lives ?? []) {
  const key = life.life_key ?? life.life_lost_at;
  if (!key) continue;
  const existing = await StoreDB('game_lives').where('life_lost_at', key).first();
  if (!existing) {
    await StoreDB('game_lives').insert({ life_lost_at: key, recovered: life.recovered ?? 0, created_at: now });
  } else if (life.recovered && !existing.recovered) {
    await StoreDB('game_lives').where('life_lost_at', key).update({ recovered: 1 });
  }
}

// qa_group_progress — upsert, higher high_score wins
for (const p of pullData.qa_group_progress ?? []) {
  const existing = await StoreDB('qa_group_progress').where('group_id', p.group_id).first();
  if (!existing) {
    await StoreDB('qa_group_progress').insert({ group_id: p.group_id, is_completed: p.is_completed ? 1 : 0,
      high_score_percentage: p.high_score_percentage ?? 0, times_played: p.times_played ?? 0,
      completed_at: p.completed_at ?? null, updated_at: now });
  } else {
    const newScore = Math.max(existing.high_score_percentage, p.high_score_percentage ?? 0);
    const newCompleted = existing.is_completed || (p.is_completed ? 1 : 0);
    await StoreDB('qa_group_progress').where('group_id', p.group_id)
      .update({ is_completed: newCompleted, high_score_percentage: newScore,
        times_played: Math.max(existing.times_played, p.times_played ?? 0),
        completed_at: existing.completed_at ?? p.completed_at ?? null, updated_at: now });
  }
}

// tf_group_progress — same logic
```

### preload.ts additions

```ts
// Games — lives
gameGetLives: () => ipcRenderer.invoke('game:getLives'),
gameLoseLife: () => ipcRenderer.invoke('game:loseLife'),
gameNextRecoveryAt: () => ipcRenderer.invoke('game:nextRecoveryAt'),
gameRefillLives: () => ipcRenderer.invoke('game:refillLives'),
// Q&A
qaGetGroups: () => ipcRenderer.invoke('qa:getGroups'),
qaGetQuestionsForGroup: (groupId: number) => ipcRenderer.invoke('qa:getQuestionsForGroup', groupId),
qaGetAllGroupProgress: () => ipcRenderer.invoke('qa:getAllGroupProgress'),
qaSaveGroupProgress: (args: any) => ipcRenderer.invoke('qa:saveGroupProgress', args),
// True/False
tfGetGroups: () => ipcRenderer.invoke('tf:getGroups'),
tfGetStatementsForGroup: (groupId: number) => ipcRenderer.invoke('tf:getStatementsForGroup', groupId),
tfGetAllGroupProgress: () => ipcRenderer.invoke('tf:getAllGroupProgress'),
tfSaveGroupProgress: (args: any) => ipcRenderer.invoke('tf:saveGroupProgress', args),
// Four Pictures
fpGetLevels: () => ipcRenderer.invoke('fp:getLevels'),
fpGetSolvedLevelIds: () => ipcRenderer.invoke('fp:getSolvedLevelIds'),
fpMarkLevelSolved: (levelId: number) => ipcRenderer.invoke('fp:markLevelSolved', levelId),
fpGetImagesBasePath: () => ipcRenderer.invoke('fp:getImagesBasePath'),
```

---

## Frontend Layer

### useGamesStore.ts

Pinia store — mirrors `GamesProvider.dart`. Key state:

```ts
// Lives
lives: number               // 0–7
nextRecoveryAt: string|null // ISO UTC
recoveryTimer: ReturnType<typeof setTimeout> | null

// Q&A
qaGroups: QAGroup[]
qaGroupProgress: Record<number, GroupProgress>

// T/F
tfGroups: TFGroup[]
tfGroupProgress: Record<number, GroupProgress>

// FP
fpLevels: FPLevel[]
fpSolvedIds: Set<number>
fpImagesBasePath: string

// Current game state (shared across game types)
activeGameType: 'qa'|'tf'|'fp'|null
currentGroupId: number|null
gameState: 'idle'|'playing'|'answered'|'gameOver'|'completed'
currentQuestions: Question[]    // or Statements[]
currentIndex: number
score: number
streak: number
bestStreak: number
lastAnswerCorrect: boolean|null
selectedAnswerIndex: number|null
shuffledOptions: string[]
shuffledCorrectIndex: number
newlyPassed: boolean

// Progress summaries (for hub cards)
qaProgressSummary: { completed: number; total: number }
tfProgressSummary: { completed: number; total: number }
fpProgressSummary: { completed: number; total: number }
```

Key actions:
- `init()` — loads lives + all group data + FP images path; starts recovery timer
- `loseLife()` — calls IPC, updates lives + nextRecoveryAt, reschedules timer
- `startQAGame(groupId)` / `startTFGame(groupId)` / `startFPGame()`
- `submitQAAnswer(index)` / `submitTFAnswer(bool)` / `submitFPAnswer(word)`
- `nextQuestion()` → advances index or finalizes game
- `saveGroupProgress()` → called from `finalizeGame()`, upserts via IPC, refreshes progress
- `refreshAfterSync()` — re-fetches lives + progress after a pull sync completes

**Sound**: played directly in store actions via `new Audio(correctSoundUrl).play()`.

**Recovery timer**: `setTimeout` re-calls `refreshLives()` when `nextRecoveryAt` fires (same logic as Flutter's `Timer`). Cleared on store `$dispose`.

### Router

```ts
{
  name: 'Games',
  path: '/games',
  component: () => import('../Views/Games/Games.vue'),
}
```

### Menu (menu.ts)

New entry in `menuUpperTabs` after Daily Devotional, before AI Assistant:

```ts
{
  label: 'Games',
  key: '/games',
  icon: renderNIcon(GameControllerIcon),   // from @vicons/ionicons5 or similar
  iconDark: renderNIcon(GameControllerIcon),
}
```

Also add `'/games'` to `enableTab`.

### View Components

**`Games.vue`** — owns `activeScreen` ref. Renders:
- `activeScreen === 'hub'` → `LivesBar` + 3 `GameCard`s
- `activeScreen === 'qa-groups'` → `QAGroupsList` with back button
- `activeScreen === 'qa-play'` → `QAGameplay`
- `activeScreen === 'tf-groups'` → `TFGroupsList`
- `activeScreen === 'tf-play'` → `TFGameplay`
- `activeScreen === 'fp-play'` → `FPGameplay`

**`LivesBar.vue`** — 7 heart icons (filled/empty), countdown pill, ticks every second via `setInterval`.

**`GameCard.vue`** — props: `title`, `description`, `color`, `icon`, `progress { completed, total }`, `disabled`. Shows progress bar + "X / Y groups complete".

**`QAGroupsList.vue`** — list of groups. Each row: lock icon if locked, group name, high score badge, Play button. Clicking Play → store `startQAGame(groupId)` → parent sets `activeScreen = 'qa-play'`.

**`QAGameplay.vue`** — question text + 4 answer buttons. On answer: buttons flash correct (green) / wrong (red), lives update. Next button advances. Game over / completed overlay with score, best streak, Retry / Back to groups.

**`TFGroupsList.vue`** / **`TFGameplay.vue`** — same structure, two buttons (True / False).

**`FPGameplay.vue`** — 2×2 image grid (`<img :src="'file://' + basePath + '/' + image">`), word display tiles, letter-tap input. Keyboard keydown also accepted. Correct: green flash, auto-advance. Hint button (reveal one letter, costs 1 life).

### After Sync Pull

In `util/Sync/sync.ts`, after `applyPullData` succeeds, call:
```ts
useGamesStore().refreshAfterSync()
```
This re-fetches lives and progress so the hub and active game reflect synced state.

---

## Error Handling

| Scenario | Behavior |
|---|---|
| Game DB not seeded yet (first launch delay) | Store `isLoading = true`; GameCards show skeleton |
| Missing FP image file | `<img onerror>` shows a gray placeholder tile |
| IPC failure on loseLife | Non-fatal; lives count unchanged; error logged |
| Sync log write failure | Non-fatal; logged to `electron-log` (same as all other tables) |
| Web view | Games route is Electron-only. Add `beforeEnter: () => window.isElectron || false` guard on the `/games` route so web users are redirected away if they somehow reach it. |

---

## Files Summary

| File | Action |
|---|---|
| `defaults/Main/games/qa/game_seed.db` + `version.json` | New (copy from mobile) |
| `defaults/Main/games/tf/game_seed.db` + `version.json` | New (copy from mobile) |
| `defaults/Main/games/fp/game_seed.db` + `version.json` + `images/` | New (copy from mobile) |
| `FrontEndApp/src/assets/sounds/correct.mp3` + `wrong.mp3` | New (copy from mobile) |
| `Electron/Setups/Setup/SetGamesDB.ts` | New |
| `Electron/Setups/Setup/StoreDB/game_lives.migration.ts` | New |
| `Electron/Setups/Setup/StoreDB/qa_group_progress.migration.ts` | New |
| `Electron/Setups/Setup/StoreDB/tf_group_progress.migration.ts` | New |
| `Electron/Setups/Setup/StoreDB/fpow_level_progress.migration.ts` | New |
| `Electron/IpcMainEvents/Games/Games.ts` | New |
| `Electron/DataBase/DataBase.ts` | Modify — add 3 game DB connections |
| `Electron/Setups/setup.ts` | Modify — call setGamesDB |
| `Electron/Setups/Setup/SetStoreDatabase.ts` | Modify — register 4 migrations |
| `Electron/IpcMainEvents/IpcMainEvents.ts` | Modify — register Games() |
| `Electron/IpcMainEvents/Sync/SyncHandlers.ts` | Modify — extend applyPullData |
| `Electron/preload.ts` | Modify — expose game IPC |
| `FrontEndApp/src/store/useGamesStore.ts` | New |
| `FrontEndApp/src/Views/Games/Games.vue` | New |
| `FrontEndApp/src/Views/Games/components/LivesBar.vue` | New |
| `FrontEndApp/src/Views/Games/components/GameCard.vue` | New |
| `FrontEndApp/src/Views/Games/QuestionAndAnswer/QAGroupsList.vue` | New |
| `FrontEndApp/src/Views/Games/QuestionAndAnswer/QAGameplay.vue` | New |
| `FrontEndApp/src/Views/Games/TrueOrFalse/TFGroupsList.vue` | New |
| `FrontEndApp/src/Views/Games/TrueOrFalse/TFGameplay.vue` | New |
| `FrontEndApp/src/Views/Games/FourPictures/FPGameplay.vue` | New |
| `FrontEndApp/src/router/router.ts` | Modify — add /games route |
| `FrontEndApp/src/store/menu.ts` | Modify — add Games menu entry |
