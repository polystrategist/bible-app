<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\DB;
use App\Models\SyncLog;
use App\Models\UserBookmark;
use App\Models\UserHighlight;
use App\Models\UserClipNote;
use App\Models\UserPrayerList;
use App\Models\UserStudySpace;
use App\Models\UserNote;

class SyncController extends Controller
{
    private const ALLOWED_TABLES = ['bookmarks', 'highlights', 'clip_notes', 'prayer_lists', 'study_spaces', 'notes'];
    private const ALLOWED_ACTIONS = ['created', 'updated', 'deleted'];
    private const PRAYER_STATUSES = ['ongoing', 'done'];

    /**
     * Handle incoming sync data from client
     */
    public function sync(Request $request)
    {
        $request->validate([
            'sync_logs'              => ['required', 'array', 'max:500'],
            'sync_logs.*.table_name' => ['required', 'string', 'in:' . implode(',', self::ALLOWED_TABLES)],
            'sync_logs.*.record_key' => ['required', 'string', 'max:255'],
            'sync_logs.*.action'     => ['required', 'string', 'in:' . implode(',', self::ALLOWED_ACTIONS)],
            'sync_logs.*.payload'    => ['nullable', 'array'],
        ]);

        $user = $request->user();
        $syncLogs = $request->input('sync_logs');
        $syncedCount = 0;

        DB::transaction(function () use ($user, $syncLogs, &$syncedCount) {
            foreach ($syncLogs as $logEntry) {
                $this->processSyncLog($user->id, $logEntry);
                $syncedCount++;
            }
        });

        return response()->json([
            'status'       => 'success',
            'synced_count' => $syncedCount,
        ]);
    }

    /**
     * Process a single sync log entry
     */
    private function processSyncLog(int $userId, array $logEntry): void
    {
        $tableName = $logEntry['table_name'];
        $recordKey = $logEntry['record_key'];
        $action    = $logEntry['action'];
        $payload   = $logEntry['payload'] ?? null;

        SyncLog::create([
            'user_id'    => $userId,
            'table_name' => $tableName,
            'record_key' => $recordKey,
            'action'     => $action,
            'payload'    => $payload,
            'synced'     => true,
        ]);

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
            case 'study_spaces':
                $this->syncStudySpace($userId, $recordKey, $action, $payload);
                break;
            case 'notes':
                $this->syncNote($userId, $recordKey, $action, $payload);
                break;
        }
    }

    /**
     * Sync bookmark data
     */
    private function syncBookmark(int $userId, string $key, string $action, ?array $payload): void
    {
        if ($action === 'deleted') {
            UserBookmark::where('user_id', $userId)->where('key', $key)->delete();
        } elseif (in_array($action, ['created', 'updated'])) {
            if ($payload === null) return;
            UserBookmark::updateOrCreate(
                ['user_id' => $userId, 'key' => $key],
                [
                    'study_space_name' => $payload['study_space_name'] ?? 'default',
                    'book_number'      => $payload['book_number'],
                    'chapter'          => $payload['chapter'],
                    'verse'            => $payload['verse'],
                ]
            );
        }
    }

    /**
     * Sync highlight data
     */
    private function syncHighlight(int $userId, string $key, string $action, ?array $payload): void
    {
        if ($action === 'deleted') {
            UserHighlight::where('user_id', $userId)->where('key', $key)->delete();
        } elseif (in_array($action, ['created', 'updated'])) {
            if ($payload === null) return;
            UserHighlight::updateOrCreate(
                ['user_id' => $userId, 'key' => $key],
                [
                    'study_space_name' => $payload['study_space_name'] ?? 'default',
                    'book_number'      => $payload['book_number'],
                    'chapter'          => $payload['chapter'],
                    'verse'            => $payload['verse'],
                    'content'          => $payload['content'],
                ]
            );
        }
    }

    /**
     * Sync clip note data
     */
    private function syncClipNote(int $userId, string $key, string $action, ?array $payload): void
    {
        if ($action === 'deleted') {
            UserClipNote::where('user_id', $userId)->where('key', $key)->delete();
        } elseif (in_array($action, ['created', 'updated'])) {
            if ($payload === null) return;
            UserClipNote::updateOrCreate(
                ['user_id' => $userId, 'key' => $key],
                [
                    'study_space_name' => $payload['study_space_name'] ?? 'default',
                    'book_number'      => $payload['book_number'],
                    'chapter'          => $payload['chapter'],
                    'verse'            => $payload['verse'],
                    'content'          => $payload['content'],
                    'color'            => $payload['color'] ?? '#FFD700',
                ]
            );
        }
    }

    /**
     * Sync prayer list data
     */
    private function syncPrayerList(int $userId, string $key, string $action, ?array $payload): void
    {
        if ($action === 'deleted') {
            UserPrayerList::where('user_id', $userId)->where('key', $key)->delete();
        } elseif (in_array($action, ['created', 'updated'])) {
            if ($payload === null) return;
            $status = in_array($payload['status'] ?? null, self::PRAYER_STATUSES)
                ? $payload['status']
                : 'ongoing';
            UserPrayerList::updateOrCreate(
                ['user_id' => $userId, 'key' => $key],
                [
                    'title'   => $payload['title'] ?? null,
                    'content' => $payload['content'] ?? '',
                    'group'   => $payload['group'] ?? null,
                    'index'   => $payload['index'] ?? 0,
                    'status'  => $status,
                ]
            );
        }
    }

    /**
     * Sync study space data
     */
    private function syncStudySpace(int $userId, string $key, string $action, ?array $payload): void
    {
        if ($action === 'deleted') {
            $spaceName = $payload['title'] ?? $key;
            UserStudySpace::where('user_id', $userId)->where('name', $spaceName)->delete();
        } elseif (in_array($action, ['created', 'updated'])) {
            if ($payload === null || empty($payload['title'])) return;
            UserStudySpace::updateOrCreate(
                ['user_id' => $userId, 'name' => $payload['title']],
                ['description' => $payload['description'] ?? null]
            );
        }
    }

    /**
     * Sync note data
     */
    private function syncNote(int $userId, string $key, string $action, ?array $payload): void
    {
        if ($action === 'deleted') {
            $spaceName = $payload['study_space_name'] ?? $key;
            UserNote::where('user_id', $userId)->where('study_space_name', $spaceName)->delete();
        } elseif (in_array($action, ['created', 'updated'])) {
            if ($payload === null) return;
            UserNote::updateOrCreate(
                ['user_id' => $userId, 'study_space_name' => $payload['study_space_name'] ?? 'default'],
                ['content' => $payload['content'] ?? '']
            );
        }
    }

    /**
     * Pull sync data from backend since a given timestamp
     */
    public function pull(Request $request)
    {
        $user = $request->user();
        $since = $request->query('since', '0');
        $filterBySince = $since !== '0';

        $syncLogs = SyncLog::where('user_id', $user->id)
            ->when($filterBySince, fn ($q) => $q->where('created_at', '>', $since))
            ->orderBy('created_at', 'asc')
            ->get(['table_name', 'record_key', 'action', 'created_at']);

        $bookmarks = UserBookmark::where('user_id', $user->id)
            ->when($filterBySince, fn ($q) => $q->where('updated_at', '>=', $since))
            ->get();

        $highlights = UserHighlight::where('user_id', $user->id)
            ->when($filterBySince, fn ($q) => $q->where('updated_at', '>=', $since))
            ->get();

        $clipNotes = UserClipNote::where('user_id', $user->id)
            ->when($filterBySince, fn ($q) => $q->where('updated_at', '>=', $since))
            ->get();

        $prayerLists = UserPrayerList::where('user_id', $user->id)
            ->when($filterBySince, fn ($q) => $q->where('updated_at', '>=', $since))
            ->get();

        $studySpaces = UserStudySpace::where('user_id', $user->id)
            ->when($filterBySince, fn ($q) => $q->where('updated_at', '>=', $since))
            ->get();

        $notes = UserNote::where('user_id', $user->id)
            ->when($filterBySince, fn ($q) => $q->where('updated_at', '>=', $since))
            ->get();

        return response()->json([
            'status'               => 'success',
            'sync_logs'            => $syncLogs,
            'bookmarks'            => $bookmarks,
            'highlights'           => $highlights,
            'clip_notes'           => $clipNotes,
            'prayer_lists'         => $prayerLists,
            'study_spaces'         => $studySpaces,
            'notes'                => $notes,
            'last_sync_timestamp'  => now()->toISOString(),
        ]);
    }
}
