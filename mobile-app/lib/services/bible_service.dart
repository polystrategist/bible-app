import 'dart:io';

import 'package:archive/archive.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';

import '../models/verse.dart';

class BibleService {
  final Map<String, Database> _cache = {};

  /// Bundled Bible modules that ship with the app — these must never be deleted.
  static const List<String> bundledModules = [
    'King James Version - 1769.SQLite3',
    'Ang Salita ng Dios 2015.SQLite3',
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

  /// Downloads a zipped Bible module from [url], extracts the first
  /// `.SQLite3`/`.db` file found in the zip, and saves it as [fileName]
  /// in the modules directory.
  ///
  /// [onProgress] receives values 0.0–1.0 as data is received. The download
  /// phase is 0–0.9 and the extraction phase is 0.9–1.0.
  Future<void> downloadBible(
    String url,
    String fileName, {
    void Function(double progress)? onProgress,
  }) async {
    final destDir = await _modulesPath;
    final destFile = File(p.join(destDir, fileName));

    // --- Download with progress ---
    final request = http.Request('GET', Uri.parse(url));
    final response = await request.send();

    if (response.statusCode != 200) {
      throw Exception(
        'Download failed with HTTP ${response.statusCode}: $url',
      );
    }

    final totalBytes = response.contentLength ?? 0;
    var receivedBytes = 0;
    final chunks = <List<int>>[];

    await for (final chunk in response.stream) {
      chunks.add(chunk);
      receivedBytes += chunk.length;
      if (totalBytes > 0) {
        // Reserve the last 10% for extraction
        onProgress?.call((receivedBytes / totalBytes) * 0.9);
      }
    }

    // Flatten all chunks into a single byte array
    final rawBytes = Uint8List(receivedBytes);
    var offset = 0;
    for (final chunk in chunks) {
      rawBytes.setRange(offset, offset + chunk.length, chunk);
      offset += chunk.length;
    }

    // --- Extract the SQLite file from the zip ---
    onProgress?.call(0.9);
    final archive = ZipDecoder().decodeBytes(rawBytes);

    ArchiveFile? target;
    for (final file in archive) {
      final name = file.name.toLowerCase();
      if (!file.isFile) continue;
      // Skip commentaries files — they don't contain verses
      if (name.contains('commentaries')) continue;
      if (name.endsWith('.sqlite3') || name.endsWith('.db')) {
        target = file;
        break;
      }
    }

    if (target == null) {
      throw Exception(
        'No SQLite3 file found inside the downloaded archive for $fileName',
      );
    }

    await destFile.writeAsBytes(target.content as List<int>, flush: true);
    onProgress?.call(1.0);
  }

  /// Deletes a downloaded Bible module. Bundled modules are protected and
  /// cannot be removed through this method.
  Future<void> deleteBible(String fileName) async {
    if (bundledModules.contains(fileName)) {
      throw StateError('Bundled module "$fileName" cannot be deleted.');
    }

    final destDir = await _modulesPath;
    final file = File(p.join(destDir, fileName));

    if (await file.exists()) {
      await file.delete();
    }

    // Close and evict the cached database connection so subsequent
    // lookups don't try to open a now-deleted file.
    if (_cache.containsKey(fileName)) {
      await _cache[fileName]!.close();
      _cache.remove(fileName);
    }
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

  Future<int> getVerseCount({
    required String version,
    required int bookNumber,
    required int chapter,
  }) async {
    final db = await _getDatabase(version);
    final result = await db.rawQuery(
      'SELECT COUNT(*) as cnt FROM verses WHERE book_number = ? AND chapter = ?',
      [bookNumber, chapter],
    );
    return Sqflite.firstIntValue(result) ?? 0;
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
