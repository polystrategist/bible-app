import 'dart:io';
import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';
import '../models/verse.dart';

class BibleService {
  final Map<String, Database> _cache = {};

  /// Bundled Bible modules that ship with the app.
  static const List<String> bundledModules = [
    'King James Version - 1769.SQLite3',
  ];

  Future<String> get _modulesPath async {
    final dir = await getApplicationDocumentsDirectory();
    final modulesDir = Directory(p.join(dir.path, 'modules', 'bible'));
    if (!await modulesDir.exists()) {
      await modulesDir.create(recursive: true);
    }
    return modulesDir.path;
  }

  /// Copy bundled Bible modules from assets to the documents directory
  /// if they don't already exist.
  Future<void> copyBundledModules() async {
    final destDir = await _modulesPath;

    for (final fileName in bundledModules) {
      final destFile = File(p.join(destDir, fileName));
      if (await destFile.exists()) continue;

      final data = await rootBundle.load('assets/modules/$fileName');
      final bytes = data.buffer.asUint8List(
        data.offsetInBytes,
        data.lengthInBytes,
      );
      await destFile.writeAsBytes(bytes, flush: true);
    }
  }

  Future<List<String>> getAvailableBibles() async {
    final path = await _modulesPath;
    final dir = Directory(path);
    if (!await dir.exists()) return [];

    return dir
        .listSync()
        .where((f) => f.path.endsWith('.SQLite3') || f.path.endsWith('.db'))
        .map((f) => p.basename(f.path))
        .toList()
      ..sort();
  }

  Future<Database> _getDatabase(String fileName) async {
    if (_cache.containsKey(fileName)) return _cache[fileName]!;

    final path = await _modulesPath;
    final dbPath = p.join(path, fileName);

    final db = await openDatabase(dbPath, readOnly: true);
    _cache[fileName] = db;
    return db;
  }

  Future<List<Verse>> getVerses({
    required String version,
    required int bookNumber,
    required int chapter,
  }) async {
    final db = await _getDatabase(version);
    final rows = await db.query(
      'verses',
      where: 'book_number = ? AND chapter = ?',
      whereArgs: [bookNumber, chapter],
      orderBy: 'verse ASC',
    );
    return rows.map((r) => Verse.fromMap(r)).toList();
  }

  Future<List<Verse>> search({
    required String version,
    required String query,
    int limit = 50,
    int offset = 0,
  }) async {
    final db = await _getDatabase(version);
    final rows = await db.query(
      'verses',
      where: 'text LIKE ?',
      whereArgs: ['%$query%'],
      limit: limit,
      offset: offset,
      orderBy: 'book_number ASC, chapter ASC, verse ASC',
    );
    return rows.map((r) => Verse.fromMap(r)).toList();
  }

  Future<void> closeAll() async {
    for (final db in _cache.values) {
      await db.close();
    }
    _cache.clear();
  }
}
