import 'dart:convert';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';

/// Local user-data store — mirrors the desktop app's Store.db schema.
class StoreService {
  static Database? _db;

  Future<Database> get db async {
    if (_db != null) return _db!;
    _db = await _initDb();
    return _db!;
  }

  Future<Database> _initDb() async {
    final dir = await getApplicationDocumentsDirectory();
    final dbPath = p.join(dir.path, 'Store.db');

    return openDatabase(
      dbPath,
      version: 1,
      onCreate: (db, version) async {
        // Study spaces
        await db.execute('''
          CREATE TABLE IF NOT EXISTS study_spaces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            description TEXT,
            is_selected INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
          )
        ''');

        // Bookmarks
        await db.execute('''
          CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_space_id INTEGER,
            key TEXT,
            book_number INTEGER,
            chapter INTEGER,
            verse INTEGER,
            created_at TEXT,
            updated_at TEXT
          )
        ''');

        // Highlights
        await db.execute('''
          CREATE TABLE IF NOT EXISTS highlights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_space_id INTEGER,
            key TEXT,
            book_number INTEGER,
            chapter INTEGER,
            verse INTEGER,
            content TEXT,
            created_at TEXT,
            updated_at TEXT
          )
        ''');

        // Clip notes
        await db.execute('''
          CREATE TABLE IF NOT EXISTS clip_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_space_id INTEGER,
            key TEXT,
            book_number INTEGER,
            chapter INTEGER,
            verse INTEGER,
            content TEXT,
            color TEXT DEFAULT '#FFD700',
            created_at TEXT,
            updated_at TEXT
          )
        ''');

        // Sync logs
        await db.execute('''
          CREATE TABLE IF NOT EXISTS sync_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT NOT NULL,
            record_key TEXT NOT NULL,
            action TEXT NOT NULL,
            payload TEXT,
            synced INTEGER DEFAULT 0,
            created_at TEXT,
            updated_at TEXT
          )
        ''');
        await db.execute(
            'CREATE INDEX IF NOT EXISTS idx_sync_table_synced ON sync_logs (table_name, synced)');
        await db.execute(
            'CREATE INDEX IF NOT EXISTS idx_sync_created ON sync_logs (created_at)');

        // Sync settings
        await db.execute('''
          CREATE TABLE IF NOT EXISTS sync_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            created_at TEXT,
            updated_at TEXT
          )
        ''');

        // Default sync timestamp
        final now = DateTime.now().toUtc().toIso8601String();
        await db.insert('sync_settings', {
          'key': 'last_sync_timestamp',
          'value': '0',
          'created_at': now,
          'updated_at': now,
        });

        // Default study space
        await db.insert('study_spaces', {
          'title': 'My Study Space',
          'description': 'My Study Space',
          'is_selected': 1,
          'created_at': now,
          'updated_at': now,
        });
      },
    );
  }

  // ─── Study Space ───────────────────────────────────────────────

  Future<int> getSelectedStudySpaceId() async {
    final d = await db;
    final rows = await d.query('study_spaces',
        where: 'is_selected = 1', limit: 1);
    if (rows.isNotEmpty) return rows.first['id'] as int;
    // Fallback: first space
    final all = await d.query('study_spaces', limit: 1);
    return all.isNotEmpty ? all.first['id'] as int : 1;
  }

  // ─── Bookmarks ─────────────────────────────────────────────────

  Future<List<Map<String, dynamic>>> getBookmarks() async {
    final d = await db;
    final spaceId = await getSelectedStudySpaceId();
    return d.query('bookmarks',
        where: 'study_space_id = ?',
        whereArgs: [spaceId],
        orderBy: 'created_at DESC');
  }

  Future<bool> isBookmarked(int bookNumber, int chapter, int verse) async {
    final d = await db;
    final spaceId = await getSelectedStudySpaceId();
    final key = '$bookNumber-$chapter-$verse';
    final rows = await d.query('bookmarks',
        where: 'study_space_id = ? AND key = ?',
        whereArgs: [spaceId, key]);
    return rows.isNotEmpty;
  }

  Future<void> toggleBookmark(int bookNumber, int chapter, int verse) async {
    final d = await db;
    final spaceId = await getSelectedStudySpaceId();
    final key = '$bookNumber-$chapter-$verse';
    final now = DateTime.now().toUtc().toIso8601String();

    final existing = await d.query('bookmarks',
        where: 'study_space_id = ? AND key = ?',
        whereArgs: [spaceId, key]);

    if (existing.isNotEmpty) {
      await d.delete('bookmarks',
          where: 'study_space_id = ? AND key = ?',
          whereArgs: [spaceId, key]);
      await _logSync('bookmarks', key, 'deleted', {
        'key': key,
        'study_space_id': spaceId,
      });
    } else {
      await d.insert('bookmarks', {
        'study_space_id': spaceId,
        'key': key,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'created_at': now,
        'updated_at': now,
      });
      await _logSync('bookmarks', key, 'created', {
        'key': key,
        'study_space_id': spaceId,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
      });
    }
  }

  // ─── Highlights ────────────────────────────────────────────────

  Future<List<Map<String, dynamic>>> getChapterHighlights(
      int bookNumber, int chapter) async {
    final d = await db;
    final spaceId = await getSelectedStudySpaceId();
    return d.query('highlights',
        where: 'study_space_id = ? AND book_number = ? AND chapter = ?',
        whereArgs: [spaceId, bookNumber, chapter]);
  }

  Future<void> saveHighlight(
      int bookNumber, int chapter, int verse, String content) async {
    final d = await db;
    final spaceId = await getSelectedStudySpaceId();
    final key = '$bookNumber-$chapter-$verse';
    final now = DateTime.now().toUtc().toIso8601String();

    final existing = await d.query('highlights',
        where: 'study_space_id = ? AND key = ?',
        whereArgs: [spaceId, key]);

    if (existing.isNotEmpty) {
      await d.update(
        'highlights',
        {'content': content, 'updated_at': now},
        where: 'study_space_id = ? AND key = ?',
        whereArgs: [spaceId, key],
      );
      await _logSync('highlights', key, 'updated', {
        'key': key,
        'study_space_id': spaceId,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'content': content,
      });
    } else {
      await d.insert('highlights', {
        'study_space_id': spaceId,
        'key': key,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'content': content,
        'created_at': now,
        'updated_at': now,
      });
      await _logSync('highlights', key, 'created', {
        'key': key,
        'study_space_id': spaceId,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'content': content,
      });
    }
  }

  Future<void> deleteHighlight(int bookNumber, int chapter, int verse) async {
    final d = await db;
    final spaceId = await getSelectedStudySpaceId();
    final key = '$bookNumber-$chapter-$verse';

    await d.delete('highlights',
        where: 'study_space_id = ? AND key = ?',
        whereArgs: [spaceId, key]);
    await _logSync('highlights', key, 'deleted', {
      'key': key,
      'study_space_id': spaceId,
    });
  }

  // ─── Clip Notes ────────────────────────────────────────────────

  Future<List<Map<String, dynamic>>> getChapterClipNotes(
      int bookNumber, int chapter) async {
    final d = await db;
    final spaceId = await getSelectedStudySpaceId();
    return d.query('clip_notes',
        where: 'study_space_id = ? AND book_number = ? AND chapter = ?',
        whereArgs: [spaceId, bookNumber, chapter]);
  }

  Future<void> saveClipNote(int bookNumber, int chapter, int verse,
      String content, String color) async {
    final d = await db;
    final spaceId = await getSelectedStudySpaceId();
    final key = '$bookNumber-$chapter-$verse';
    final now = DateTime.now().toUtc().toIso8601String();

    final existing = await d.query('clip_notes',
        where: 'study_space_id = ? AND key = ?',
        whereArgs: [spaceId, key]);

    if (existing.isNotEmpty) {
      await d.update(
        'clip_notes',
        {'content': content, 'color': color, 'updated_at': now},
        where: 'study_space_id = ? AND key = ?',
        whereArgs: [spaceId, key],
      );
      await _logSync('clip_notes', key, 'updated', {
        'key': key,
        'study_space_id': spaceId,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'content': content,
        'color': color,
      });
    } else {
      await d.insert('clip_notes', {
        'study_space_id': spaceId,
        'key': key,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'content': content,
        'color': color,
        'created_at': now,
        'updated_at': now,
      });
      await _logSync('clip_notes', key, 'created', {
        'key': key,
        'study_space_id': spaceId,
        'book_number': bookNumber,
        'chapter': chapter,
        'verse': verse,
        'content': content,
        'color': color,
      });
    }
  }

  Future<void> deleteClipNote(int bookNumber, int chapter, int verse) async {
    final d = await db;
    final spaceId = await getSelectedStudySpaceId();
    final key = '$bookNumber-$chapter-$verse';

    await d.delete('clip_notes',
        where: 'study_space_id = ? AND key = ?',
        whereArgs: [spaceId, key]);
    await _logSync('clip_notes', key, 'deleted', {
      'key': key,
      'study_space_id': spaceId,
    });
  }

  // ─── Sync Logs ─────────────────────────────────────────────────

  Future<void> _logSync(
      String tableName, String recordKey, String action, Map payload) async {
    final d = await db;
    final now = DateTime.now().toUtc().toIso8601String();
    await d.insert('sync_logs', {
      'table_name': tableName,
      'record_key': recordKey,
      'action': action,
      'payload': jsonEncode(payload),
      'synced': 0,
      'created_at': now,
      'updated_at': now,
    });
  }

  Future<List<Map<String, dynamic>>> getUnsyncedChanges() async {
    final d = await db;
    return d.query('sync_logs',
        where: 'synced = 0', orderBy: 'created_at ASC');
  }

  Future<void> markAsSynced(List<int> ids) async {
    if (ids.isEmpty) return;
    final d = await db;
    final now = DateTime.now().toUtc().toIso8601String();
    final placeholders = ids.map((_) => '?').join(',');
    await d.rawUpdate(
      'UPDATE sync_logs SET synced = 1, updated_at = ? WHERE id IN ($placeholders)',
      [now, ...ids],
    );
  }

  // ─── Sync Settings ────────────────────────────────────────────

  Future<String?> getSyncSetting(String key) async {
    final d = await db;
    final rows = await d.query('sync_settings',
        where: 'key = ?', whereArgs: [key], limit: 1);
    return rows.isNotEmpty ? rows.first['value'] as String? : null;
  }

  Future<void> setSyncSetting(String key, String value) async {
    final d = await db;
    final now = DateTime.now().toUtc().toIso8601String();
    final existing = await d.query('sync_settings',
        where: 'key = ?', whereArgs: [key], limit: 1);
    if (existing.isNotEmpty) {
      await d.update('sync_settings', {'value': value, 'updated_at': now},
          where: 'key = ?', whereArgs: [key]);
    } else {
      await d.insert('sync_settings', {
        'key': key,
        'value': value,
        'created_at': now,
        'updated_at': now,
      });
    }
  }

  Future<String> getLastSyncTimestamp() async {
    return await getSyncSetting('last_sync_timestamp') ?? '0';
  }

  Future<void> updateLastSyncTimestamp(String timestamp) async {
    await setSyncSetting('last_sync_timestamp', timestamp);
  }

  // ─── Apply Pull Data (from server) ────────────────────────────

  Future<void> applyPullData(Map<String, dynamic> pullData) async {
    final d = await db;
    final now = DateTime.now().toUtc().toIso8601String();

    Future<int?> getStudySpaceId(String spaceName) async {
      final rows = await d.query('study_spaces',
          where: 'title = ?', whereArgs: [spaceName], limit: 1);
      return rows.isNotEmpty ? rows.first['id'] as int : null;
    }

    // Study spaces
    for (final space in (pullData['study_spaces'] as List?) ?? []) {
      final existing = await d.query('study_spaces',
          where: 'title = ?', whereArgs: [space['name']], limit: 1);
      if (existing.isNotEmpty) {
        await d.update('study_spaces',
            {'description': space['description'], 'updated_at': now},
            where: 'title = ?', whereArgs: [space['name']]);
      } else {
        await d.insert('study_spaces', {
          'title': space['name'],
          'description': space['description'],
          'is_selected': 0,
          'created_at': now,
          'updated_at': now,
        });
      }
    }

    // Bookmarks
    for (final bm in (pullData['bookmarks'] as List?) ?? []) {
      final spaceId = await getStudySpaceId(bm['study_space_name']);
      if (spaceId == null) continue;
      final existing = await d.query('bookmarks',
          where: 'key = ? AND study_space_id = ?',
          whereArgs: [bm['key'], spaceId],
          limit: 1);
      if (existing.isNotEmpty) {
        await d.update('bookmarks', {
          'book_number': bm['book_number'],
          'chapter': bm['chapter'],
          'verse': bm['verse'],
          'updated_at': now,
        }, where: 'key = ? AND study_space_id = ?', whereArgs: [bm['key'], spaceId]);
      } else {
        await d.insert('bookmarks', {
          'key': bm['key'],
          'study_space_id': spaceId,
          'book_number': bm['book_number'],
          'chapter': bm['chapter'],
          'verse': bm['verse'],
          'created_at': now,
          'updated_at': now,
        });
      }
    }

    // Highlights
    for (final hl in (pullData['highlights'] as List?) ?? []) {
      final spaceId = await getStudySpaceId(hl['study_space_name']);
      if (spaceId == null) continue;
      final existing = await d.query('highlights',
          where: 'key = ? AND study_space_id = ?',
          whereArgs: [hl['key'], spaceId],
          limit: 1);
      if (existing.isNotEmpty) {
        await d.update('highlights', {
          'book_number': hl['book_number'],
          'chapter': hl['chapter'],
          'verse': hl['verse'],
          'content': hl['content'],
          'updated_at': now,
        }, where: 'key = ? AND study_space_id = ?', whereArgs: [hl['key'], spaceId]);
      } else {
        await d.insert('highlights', {
          'key': hl['key'],
          'study_space_id': spaceId,
          'book_number': hl['book_number'],
          'chapter': hl['chapter'],
          'verse': hl['verse'],
          'content': hl['content'],
          'created_at': now,
          'updated_at': now,
        });
      }
    }

    // Clip notes
    for (final cn in (pullData['clip_notes'] as List?) ?? []) {
      final spaceId = await getStudySpaceId(cn['study_space_name']);
      if (spaceId == null) continue;
      final existing = await d.query('clip_notes',
          where: 'key = ? AND study_space_id = ?',
          whereArgs: [cn['key'], spaceId],
          limit: 1);
      if (existing.isNotEmpty) {
        await d.update('clip_notes', {
          'book_number': cn['book_number'],
          'chapter': cn['chapter'],
          'verse': cn['verse'],
          'content': cn['content'],
          'color': cn['color'],
          'updated_at': now,
        }, where: 'key = ? AND study_space_id = ?', whereArgs: [cn['key'], spaceId]);
      } else {
        await d.insert('clip_notes', {
          'key': cn['key'],
          'study_space_id': spaceId,
          'book_number': cn['book_number'],
          'chapter': cn['chapter'],
          'verse': cn['verse'],
          'content': cn['content'],
          'color': cn['color'] ?? '#FFD700',
          'created_at': now,
          'updated_at': now,
        });
      }
    }
  }
}
