<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use App\Models\SyncLog;
use App\Models\UserBookmark;
use App\Models\UserHighlight;
use App\Models\UserClipNote;
use App\Models\UserPrayerList;
use Illuminate\Support\Facades\DB;

class SyncController extends Controller
{
    /**
     * Handle incoming sync data from client
     */
    public function sync(Request $request)
    {
        $user = $request->user();
        $data = $request->all();
        
        Log::info('Sync received', ['user_id' => $user->id, 'data' => $data]);
        
        // Process sync logs
        if (isset($data['sync_logs']) && is_array($data['sync_logs'])) {
            foreach ($data['sync_logs'] as $logEntry) {
                $this->processSyncLog($user->id, $logEntry);
            }
        }
        
        return response()->json([
            'status' => 'success',
            'synced_items' => count($data['sync_logs'] ?? []),
        ]);
    }

    /**
     * Process a single sync log entry
     */
    private function processSyncLog(int $userId, array $logEntry)
    {
        $tableName = $logEntry['table_name'] ?? null;
        $recordKey = $logEntry['record_key'] ?? null;
        $action = $logEntry['action'] ?? null;
        $payload = $logEntry['payload'] ?? null;
        
        // Log the sync entry to database
        SyncLog::create([
            'user_id' => $userId,
            'table_name' => $tableName,
            'record_key' => $recordKey,
            'action' => $action,
            'payload' => $payload,
            'synced' => true,
        ]);
        
        // Apply the change to the appropriate table
        switch ($tableName) {
            case 'bookmarks':
                $this->syncBookmark($userId, $recordKey, $action, $payload);
                break;
            case 'highlights':
                $this->syncHighlight($userId, $recordKey, $action, $payload);
                break;
            case 'clip_notes':
                $this->syncClipNote($userId, $recordKey, $action, $payload);
                break;
            case 'prayer_lists':
                $this->syncPrayerList($userId, $recordKey, $action, $payload);
                break;
        }
    }

    /**
     * Sync bookmark data
     */
    private function syncBookmark(int $userId, string $key, string $action, ?array $payload)
    {
        if ($action === 'deleted') {
            UserBookmark::where('user_id', $userId)->where('key', $key)->delete();
        } elseif ($action === 'created') {
            UserBookmark::updateOrCreate(
                [
                    'user_id' => $userId,
                    'key' => $key,
                ],
                [
                    'study_space_name' => $payload['study_space_name'] ?? 'default',
                    'book_number' => $payload['book_number'],
                    'chapter' => $payload['chapter'],
                    'verse' => $payload['verse'],
                ]
            );
        }
    }

    /**
     * Sync highlight data
     */
    private function syncHighlight(int $userId, string $key, string $action, ?array $payload)
    {
        if ($action === 'deleted') {
            UserHighlight::where('user_id', $userId)->where('key', $key)->delete();
        } elseif ($action === 'created' || $action === 'updated') {
            UserHighlight::updateOrCreate(
                [
                    'user_id' => $userId,
                    'key' => $key,
                ],
                [
                    'study_space_name' => $payload['study_space_name'] ?? 'default',
                    'book_number' => $payload['book_number'],
                    'chapter' => $payload['chapter'],
                    'verse' => $payload['verse'],
                    'content' => $payload['content'],
                ]
            );
        }
    }

    /**
     * Sync clip note data
     */
    private function syncClipNote(int $userId, string $key, string $action, ?array $payload)
    {
        if ($action === 'deleted') {
            UserClipNote::where('user_id', $userId)->where('key', $key)->delete();
        } elseif ($action === 'created' || $action === 'updated') {
            UserClipNote::updateOrCreate(
                [
                    'user_id' => $userId,
                    'key' => $key,
                ],
                [
                    'study_space_name' => $payload['study_space_name'] ?? 'default',
                    'book_number' => $payload['book_number'],
                    'chapter' => $payload['chapter'],
                    'verse' => $payload['verse'],
                    'content' => $payload['content'],
                    'color' => $payload['color'] ?? '#FFD700',
                ]
            );
        }
    }

    /**
     * Sync prayer list data
     */
    private function syncPrayerList(int $userId, string $key, string $action, ?array $payload)
    {
        if ($action === 'deleted') {
            UserPrayerList::where('user_id', $userId)->where('key', $key)->delete();
        } elseif ($action === 'created' || $action === 'updated') {
            UserPrayerList::updateOrCreate(
                [
                    'user_id' => $userId,
                    'key' => $key,
                ],
                [
                    'title' => $payload['title'] ?? null,
                    'content' => $payload['content'],
                    'group' => $payload['group'] ?? null,
                    'index' => $payload['index'] ?? 0,
                    'status' => $payload['status'] ?? 'ongoing',
                ]
            );
        }
    }

    /**
     * Pull sync data from backend
     */
    public function pull(Request $request)
    {
        $user = $request->user();
        $since = $request->query('since', '0');
        
        // Get all sync logs since the timestamp
        $syncLogs = SyncLog::where('user_id', $user->id)
            ->where('created_at', '>', $since)
            ->orderBy('created_at', 'asc')
            ->get();
        
        // Get current state of all data
        $bookmarks = UserBookmark::where('user_id', $user->id)->get();
        $highlights = UserHighlight::where('user_id', $user->id)->get();
        $clipNotes = UserClipNote::where('user_id', $user->id)->get();
        $prayerLists = UserPrayerList::where('user_id', $user->id)->get();
        
        return response()->json([
            'status' => 'success',
            'sync_logs' => $syncLogs,
            'bookmarks' => $bookmarks,
            'highlights' => $highlights,
            'clip_notes' => $clipNotes,
            'prayer_lists' => $prayerLists,
            'last_sync_timestamp' => now()->toISOString(),
        ]);
    }
}
