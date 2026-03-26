# Believers Sword Sync System Documentation

## Overview

The Believers Sword sync system enables users to synchronize their Bible study data (bookmarks, highlights, clip notes, and prayer lists) across multiple devices through a backend server. The system uses a **log-based approach** where all data changes are tracked and synchronized.

---

## Architecture

### Components

1. **Frontend Sync Module** (`FrontEndApp/src/util/Sync/sync.ts`)
   - Handles sending sync data to the backend
   - Provides batch sync capabilities
   - Supports pull sync (downloading data from backend)

2. **Electron Main Process**
   - Local SQLite database with sync logging
   - IPC handlers for sync operations
   - Tracks all data changes in `sync_logs` table

3. **Backend Laravel API** (`backend/`)
   - RESTful API endpoints for sync operations
   - MySQL/PostgreSQL database for user data
   - Authentication via Laravel Sanctum

---

## Database Schema

### Electron Local Database (SQLite)

#### `sync_logs` Table

Stores all local data changes pending synchronization.

```sql
CREATE TABLE sync_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,        -- e.g., 'bookmarks', 'highlights', 'clip_notes', 'prayer_lists'
    record_key TEXT NOT NULL,        -- Unique identifier for the record
    action TEXT NOT NULL,            -- 'created', 'updated', 'deleted'
    payload JSON,                    -- The data that was changed
    synced INTEGER DEFAULT 0,        -- 0 = not synced, 1 = synced
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes:**
- `(table_name, synced)` - For querying unsynced changes by table
- `created_at` - For ordering by timestamp

#### `sync_settings` Table

Stores sync configuration and metadata.

```sql
CREATE TABLE sync_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Default Settings:**
- `last_sync_timestamp` - Timestamp of last successful sync

---

### Backend Database (MySQL/PostgreSQL)

#### `sync_logs` Table

Tracks all sync operations from clients.

```sql
CREATE TABLE sync_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    record_key VARCHAR(255) NOT NULL,
    action VARCHAR(50) NOT NULL,
    payload JSON NOT NULL,
    synced BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Indexes:**
- `(user_id, table_name, synced)`
- `(user_id, created_at)`

#### `user_bookmarks` Table

```sql
CREATE TABLE user_bookmarks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    study_space_name VARCHAR(255) DEFAULT 'default',
    key VARCHAR(255) NOT NULL,
    book_number INT NOT NULL,
    chapter INT NOT NULL,
    verse INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_bookmark (user_id, study_space_name, key)
);
```

#### `user_highlights` Table

```sql
CREATE TABLE user_highlights (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    study_space_name VARCHAR(255) DEFAULT 'default',
    key VARCHAR(255) NOT NULL,
    book_number INT NOT NULL,
    chapter INT NOT NULL,
    verse INT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_highlight (user_id, study_space_name, key)
);
```

#### `user_clip_notes` Table

```sql
CREATE TABLE user_clip_notes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    study_space_name VARCHAR(255) DEFAULT 'default',
    key VARCHAR(255) NOT NULL,
    book_number INT NOT NULL,
    chapter INT NOT NULL,
    verse INT NOT NULL,
    content TEXT NOT NULL,
    color VARCHAR(50) DEFAULT '#FFD700',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_clip_note (user_id, study_space_name, key)
);
```

#### `user_prayer_lists` Table

```sql
CREATE TABLE user_prayer_lists (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    key VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255),
    content TEXT NOT NULL,
    group VARCHAR(255),
    index INT DEFAULT 0,
    status ENUM('ongoing', 'done') DEFAULT 'ongoing',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## API Endpoints

### Public Routes (No Authentication Required)

#### POST `/api/auth/register`

**Description:** Register a new user account.

**Request Body:**
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirmation": "securepassword123"
}
```

**Response (201 Created):**
```json
{
    "status": "success",
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "token": "1|abc123xyz..."
}
```

**Validation Rules:**
- `name`: required, string, max 255 characters
- `email`: required, valid email format, unique in database
- `password`: required, min 8 characters, must match `password_confirmation`

#### POST `/api/auth/login`

**Description:** Authenticate user and receive access token.

**Request Body:**
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Login successful",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    },
    "token": "1|abc123xyz..."
}
```

**Response (401 Unauthorized):**
```json
{
    "status": "error",
    "message": "The provided credentials are incorrect."
}
```

---

### Authentication Required

All sync endpoints and user-specific routes require authentication via Laravel Sanctum Bearer token. Include the token in the `Authorization` header:

```
Authorization: Bearer <your-token>
```

#### POST `/api/auth/logout`

**Description:** Revoke all user tokens (logout from all devices).

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
    "status": "success",
    "message": "Successfully logged out"
}
```

#### GET `/api/auth/user`

**Description:** Get the currently authenticated user's information.

**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
    "status": "success",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }
}
```

#### POST `/api/sync`

**Description:** Push local sync changes to the backend.

**Request Body:**
```json
{
    "sync_logs": [
        {
            "table_name": "bookmarks",
            "record_key": "1_1_1",
            "action": "created",
            "payload": {
                "key": "1_1_1",
                "book_number": 1,
                "chapter": 1,
                "verse": 1,
                "study_space_name": "default"
            },
            "timestamp": "2025-01-01T00:00:00.000Z"
        }
    ],
    "user_id": 1
}
```

**Response:**
```json
{
    "status": "success",
    "synced_items": 1
}
```

#### GET `/api/sync/pull`

**Description:** Pull sync data from backend (download changes since last sync).

**Query Parameters:**
- `since` (string, optional): ISO 8601 timestamp. Defaults to '0' (all time).

**Response:**
```json
{
    "status": "success",
    "sync_logs": [...],
    "bookmarks": [...],
    "highlights": [...],
    "clip_notes": [...],
    "prayer_lists": [...],
    "last_sync_timestamp": "2025-01-01T12:00:00.000Z"
}
```

---

## Sync Flow

### Push Sync (Local → Backend)

1. **User performs action** (create/update/delete bookmark, highlight, etc.)
2. **Electron IPC handler** captures the operation
3. **Log sync change** to local `sync_logs` table with `synced = 0`
4. **Frontend sync.ts** sends the log entry to backend via `POST /api/sync`
5. **Backend SyncController** processes the log:
   - Saves to `sync_logs` table
   - Applies change to appropriate user data table
6. **Frontend marks as synced** in local database (`synced = 1`)

### Pull Sync (Backend → Local)

1. **User initiates pull sync** (e.g., on app start or manual trigger)
2. **Frontend calls** `GET /api/sull?since=<last_sync_timestamp>`
3. **Backend returns** all changes since timestamp + current state
4. **Frontend applies changes** to local database
5. **Update last_sync_timestamp** in local settings

---

## Implementation Details

### Frontend Integration

The sync system is integrated into existing data operations through the `sync.ts` utility:

```typescript
import { triggerSync } from '@/util/Sync/sync';

// When creating a bookmark
await window.browserWindow.saveBookMark(bookmarkData);
await triggerSync('bookmarks', bookmarkKey, 'created', bookmarkData);

// When deleting a highlight
await window.browserWindow.deleteHighlight(args);
await triggerSync('highlights', highlightKey, 'deleted', highlightData);
```

### Electron IPC Handlers

Each data module (bookmarks, highlights, clip notes, prayer lists) has been updated to:

1. **Detect changes** (create, update, delete)
2. **Log to sync_logs** before/after the operation
3. **Include sync metadata** (table_name, record_key, action, payload)

Example from `bookmark.ts`:
```typescript
if (!existingBookmark) {
    await StoreDB('bookmarks').insert({...});
    
    // Log sync change
    await logSyncChange({
        table_name: 'bookmarks',
        record_key: key,
        action: 'created',
        payload: {...},
        synced: 0,
    });
}
```

### Backend Processing

The `SyncController` uses a strategy pattern to route sync logs to appropriate handlers:

```php
private function processSyncLog(int $userId, array $logEntry)
{
    // Save log entry
    SyncLog::create([...]);
    
    // Route to specific handler
    switch ($logEntry['table_name']) {
        case 'bookmarks':
            $this->syncBookmark($userId, $key, $action, $payload);
            break;
        // ... other tables
    }
}
```

---

## Data Models

### Electron Database Helper (`Electron/DataBase/SyncDB.ts`)

Provides utility functions for sync operations:

```typescript
// Log a new change
await logSyncChange(entry: SyncLogEntry);

// Get all pending changes
await getUnsyncedChanges();

// Mark as synced after successful API call
await markAsSynced([id1, id2, ...]);

// Get/update last sync timestamp
await getLastSyncTimestamp();
await updateLastSyncTimestamp(timestamp);
```

### Backend Models

- `SyncLog` - Tracks sync operations
- `UserBookmark` - User's saved bookmarks
- `UserHighlight` - User's highlights
- `UserClipNote` - User's clip notes
- `UserPrayerList` - User's prayer items

All models use Laravel's `HasFactory` trait and define proper relationships to the `User` model.

---

## Error Handling

### Frontend

- Graceful degradation if sync is disabled
- Skip sync if user not authenticated
- Log errors to console
- Continue local operations even if sync fails

### Backend

- Validates user authentication
- Logs all sync operations
- Transactional integrity for data operations
- Returns detailed error messages

---

## Security Considerations

1. **Authentication Required**: All sync endpoints protected by Laravel Sanctum
2. **User Isolation**: All queries filtered by `user_id`
3. **Data Validation**: Payload structure validated before database operations
4. **Audit Trail**: All sync operations logged with timestamps

---

## Performance Optimizations

1. **Batch Syncing**: Multiple changes sent in single API call
2. **Incremental Sync**: Only unsynced changes transmitted
3. **Timestamp-based Pull**: Only fetch changes since last sync
4. **Database Indexes**: Optimized queries on frequently accessed columns
5. **Cleanup**: Old synced logs can be purged (e.g., >30 days)

---

## Usage Examples

### Authentication

#### Register New User

```typescript
import { useAuthStore } from '@/store/authStore';

const authStore = useAuthStore();

const result = await authStore.register(
    'John Doe',
    'john@example.com',
    'securepassword123',
    'securepassword123'
);

if (result.success) {
    console.log('Registration successful:', result.user);
    console.log('Auth token:', result.token);
} else {
    console.error('Registration failed:', result.message);
}
```

#### Login

```typescript
import { useAuthStore } from '@/store/authStore';

const authStore = useAuthStore();

const result = await authStore.login('john@example.com', 'securepassword123');

if (result.success) {
    console.log('Login successful:', result.user);
    console.log('Auth token:', result.token);
    // Token is automatically stored in localStorage
} else {
    console.error('Login failed:', result.message);
}
```

#### Logout

```typescript
import { useAuthStore } from '@/store/authStore';

const authStore = useAuthStore();

const result = await authStore.logout();

if (result.success) {
    console.log('Logout successful');
    // Token is removed from localStorage
} else {
    console.error('Logout failed:', result.message);
}
```

#### Check Authentication Status

```typescript
import { useAuthStore } from '@/store/authStore';

const authStore = useAuthStore();

// Initialize auth state from localStorage on app start
authStore.initAuth();

if (authStore.isAuthenticated) {
    console.log('User is logged in:', authStore.user);
    console.log('Token:', authStore.token);
} else {
    console.log('User is not authenticated');
}
```

### Enable Sync in Frontend

```typescript
import { useAuthStore } from '@/store/authStore';
import { triggerSync } from '@/util/Sync/sync';

const authStore = useAuthStore();

// Check if sync is enabled
if (authStore.syncData && authStore.isAuthenticated) {
    // Sync is enabled
    await triggerSync('bookmarks', key, 'created', data);
}
```

### Manual Sync Trigger

```typescript
// Get unsynced changes
const unsyncedChanges = await window.browserWindow.getUnsyncedChanges();

// Send to backend
if (unsyncedChanges.length > 0) {
    const response = await batchSyncData(unsyncedChanges);
    
    if (response.status === 'success') {
        await window.browserWindow.markAsSynced(
            unsyncedChanges.map(c => c.id)
        );
    }
}
```

### Pull Latest Data

```typescript
const lastSync = await window.browserWindow.getLastSyncTimestamp();
const result = await pullSyncData(lastSync);

if (result.status === 'success') {
    // Apply remote changes to local database
    // Update timestamp
    await window.browserWindow.updateLastSyncTimestamp(
        result.last_sync_timestamp
    );
}
```

---

## Migration Guide

### Running Backend Migrations

```bash
cd backend
php artisan migrate
```

This will create all sync-related tables in your backend database.

### First-Time Setup

1. Run migrations on backend
2. Launch Electron app (creates local sync tables)
3. Enable sync in user settings
4. Authenticate user
5. Perform initial sync

---

## Troubleshooting

### Common Issues

1. **Sync not working**
   - Check if `syncData` flag is enabled in user store
   - Verify user authentication
   - Check backend API endpoint availability

2. **Duplicate records**
   - Ensure unique constraints on `(user_id, key)` pairs
   - Check sync log deduplication logic

3. **Missing changes**
   - Verify `last_sync_timestamp` is being updated
   - Check timezone handling in timestamp comparisons

4. **Performance issues**
   - Run database cleanup for old synced logs
   - Check indexes on sync_logs table
   - Consider pagination for large datasets

---

## Future Enhancements

1. **Conflict Resolution**: Handle simultaneous edits from multiple devices
2. **Compression**: Compress large sync payloads
3. **Background Sync**: Automatic periodic sync without user intervention
4. **Selective Sync**: Choose which data types to sync
5. **Encryption**: End-to-end encryption for sensitive data
6. **Webhook Support**: Real-time sync notifications

---

## File Structure

```
Electron/
├── DataBase/
│   └── SyncDB.ts                    # Sync database helpers
├── IpcMainEvents/
│   ├── Sync/
│   │   └── SyncHandlers.ts          # IPC handlers for sync
│   ├── bookmark/
│   │   └── bookmark.ts              # Updated with sync logging
│   ├── highlights/
│   │   └── highlighting.ts          # Updated with sync logging
│   ├── ClipNotes/
│   │   └── ClipNotes.ts             # Updated with sync logging
│   └── PrayerList/
│       └── PrayerList.ts            # Updated with sync logging
├── Setups/Setup/StoreDB/
│   └── sync_logs.migration.ts       # Local database schema
└── preload.ts                       # Exposed sync IPC methods

FrontEndApp/src/
├── util/Sync/
│   └── sync.ts                      # Main sync utility
└── store/
    ├── authStore.ts                 # Authentication state & API calls
    └── userStore.ts                 # User auth & sync flag

backend/
├── app/
│   ├── Http/Controllers/
│   │   ├── AuthController.php       # Auth API controller
│   │   └── SyncController.php       # Sync API controller
│   └── Models/
│       ├── SyncLog.php              # Sync log model
│       ├── UserBookmark.php         # Bookmark model
│       ├── UserHighlight.php        # Highlight model
│       ├── UserClipNote.php         # Clip note model
│       └── UserPrayerList.php       # Prayer list model
├── database/
│   └── migrations/
│       ├── 2025_01_01_000003_create_sync_logs_table.php
│       ├── 2025_01_01_000004_create_user_bookmarks_table.php
│       ├── 2025_01_01_000005_create_user_highlights_table.php
│       ├── 2025_01_01_000006_create_user_clip_notes_table.php
│       └── 2025_01_01_000007_create_user_prayer_lists_table.php
└── routes/
    └── api.php                      # Auth & Sync API routes
```

---

## Testing

### Manual Testing Checklist

- [ ] Create bookmark → verify sync log created
- [ ] Update highlight → verify sync log updated
- [ ] Delete clip note → verify sync log deleted
- [ ] Add prayer item → verify sync to backend
- [ ] Pull sync → verify data downloaded correctly
- [ ] Disable sync → verify operations still work locally
- [ ] Test with invalid auth token → verify graceful failure

### Automated Testing

Future implementation should include:
- Unit tests for SyncDB functions
- Integration tests for IPC handlers
- API tests for backend endpoints
- E2E tests for full sync flow

---

## Conclusion

The Believers Sword sync system provides a robust, scalable solution for synchronizing user Bible study data across devices. The log-based architecture ensures data integrity while maintaining offline functionality. The system is designed for extensibility, allowing easy addition of new data types in the future.

**Version:** 1.0.0  
**Last Updated:** March 24, 2026  
**Author:** Believers Sword Development Team
