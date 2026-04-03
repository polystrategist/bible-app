import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/book.dart';
import '../models/verse.dart';
import '../services/bible_service.dart';

class BibleProvider extends ChangeNotifier {
  final BibleService _service = BibleService();

  List<String> _availableBibles = [];
  String? _selectedVersion;
  Book _selectedBook = bibleBooks.first;
  int _selectedChapter = 1;
  List<Verse> _verses = [];
  bool _isLoading = false;
  bool _isInitialized = false;
  double _fontSize = 18;
  double _scrollOffset = 0;
  int? _targetVerse;
  final Map<String, String> _shortNames = {};

  // --- Split screen ---
  bool _splitEnabled = false;
  String? _splitVersion;
  List<Verse> _splitVerses = [];
  bool _splitHorizontal = false; // false = vertical (top/bottom), true = horizontal (side by side)
  double _splitProportion = 0.5; // 0.0–1.0, proportion of space for primary pane

  /// Full module list from assets/bible_modules.json.
  List<Map<String, dynamic>> _allModules = [];

  /// Tracks which file is currently being downloaded, if any.
  String? _downloadingFileName;

  /// Download progress for the active download, 0.0–1.0.
  double _downloadProgress = 0.0;

  // --- Getters ---

  List<String> get availableBibles => _availableBibles;
  String? get selectedVersion => _selectedVersion;
  Book get selectedBook => _selectedBook;
  int get selectedChapter => _selectedChapter;
  List<Verse> get verses => _verses;
  bool get isLoading => _isLoading;
  bool get isInitialized => _isInitialized;
  double get fontSize => _fontSize;
  double get scrollOffset => _scrollOffset;
  int? get targetVerse => _targetVerse;

  bool get isDownloading => _downloadingFileName != null;
  String? get downloadingFileName => _downloadingFileName;
  double get downloadProgress => _downloadProgress;

  bool get splitEnabled => _splitEnabled;
  String? get splitVersion => _splitVersion;
  List<Verse> get splitVerses => _splitVerses;
  bool get splitHorizontal => _splitHorizontal;
  double get splitProportion => _splitProportion;

  String get splitVersionShortName {
    if (_splitVersion == null) return '';
    if (_shortNames.containsKey(_splitVersion)) {
      return _shortNames[_splitVersion]!;
    }
    return _splitVersion!
        .replaceAll('.SQLite3', '')
        .replaceAll('.db', '');
  }

  /// All modules from the JSON that have a non-null download link AND are
  /// not already present in the modules directory.
  List<Map<String, dynamic>> get downloadableModules {
    return _allModules.where((module) {
      final link = module['download_link'] as String?;
      if (link == null || link.isEmpty) return false;
      final fileName = module['file_name'] as String?;
      if (fileName == null) return false;
      return !_availableBibles.contains(fileName);
    }).toList();
  }

  /// Returns true if the given fileName is already installed.
  bool isInstalled(String fileName) => _availableBibles.contains(fileName);

  /// Consume the target verse (returns it once, then clears).
  int? consumeTargetVerse() {
    final v = _targetVerse;
    _targetVerse = null;
    return v;
  }

  String get selectedVersionTitle =>
      _selectedVersion?.replaceAll('.SQLite3', '').replaceAll('.db', '') ??
      'No Bible Selected';

  String get selectedVersionShortName {
    if (_selectedVersion == null) return 'N/A';
    if (_shortNames.containsKey(_selectedVersion)) {
      return _shortNames[_selectedVersion]!;
    }
    // Fuzzy match: strip extensions/stars and compare normalised titles
    final title = _selectedVersion!
        .replaceAll('.SQLite3', '')
        .replaceAll('.db', '')
        .replaceAll('★', '')
        .trim()
        .toLowerCase();
    for (final entry in _shortNames.entries) {
      final key = entry.key
          .replaceAll('.SQLite3', '')
          .replaceAll('.db', '')
          .replaceAll('★', '')
          .trim()
          .toLowerCase();
      if (title.contains(key) || key.contains(title)) {
        return entry.value;
      }
    }
    return selectedVersionTitle;
  }

  Future<void> init() async {
    try {
      await _loadModules();
      await _service.copyBundledModules();
      _availableBibles = await _service.getAvailableBibles();

      // Restore saved reading position
      final prefs = await SharedPreferences.getInstance();
      final savedVersion = prefs.getString('reading_version');
      final savedBookNumber = prefs.getInt('reading_book_number');
      final savedChapter = prefs.getInt('reading_chapter');
      final savedFontSize = prefs.getDouble('reading_font_size');
      _scrollOffset = prefs.getDouble('reading_scroll_offset') ?? 0;

      if (savedFontSize != null) {
        _fontSize = savedFontSize.clamp(12.0, 36.0);
      }

      if (_availableBibles.isNotEmpty) {
        if (savedVersion != null && _availableBibles.contains(savedVersion)) {
          _selectedVersion = savedVersion;
        } else {
          _selectedVersion = _availableBibles.first;
        }

        if (savedBookNumber != null) {
          final book =
              bibleBooks.where((b) => b.bookNumber == savedBookNumber);
          if (book.isNotEmpty) _selectedBook = book.first;
        }

        if (savedChapter != null &&
            savedChapter <= _selectedBook.chapterCount) {
          _selectedChapter = savedChapter;
        }

        // Restore split state
        final savedSplitEnabled = prefs.getBool('split_enabled') ?? false;
        final savedSplitVersion = prefs.getString('split_version');
        if (savedSplitEnabled &&
            savedSplitVersion != null &&
            _availableBibles.contains(savedSplitVersion)) {
          _splitEnabled = true;
          _splitVersion = savedSplitVersion;
        }
        _splitHorizontal = prefs.getBool('split_horizontal') ?? false;
        _splitProportion = prefs.getDouble('split_proportion') ?? 0.5;

        await loadVerses();
      }
    } catch (e) {
      debugPrint('[BibleProvider] init error: $e');
    }
    _isInitialized = true;
    notifyListeners();
  }

  /// Loads the full module list and builds the short-name map in one pass.
  Future<void> _loadModules() async {
    try {
      final raw = await rootBundle.loadString('assets/bible_modules.json');
      final list = jsonDecode(raw) as List<dynamic>;

      _allModules = list.cast<Map<String, dynamic>>();

      for (final item in _allModules) {
        final fileName = item['file_name'] as String?;
        final shortRaw = item['version_short_name_and_date'] as String?;
        if (fileName == null || shortRaw == null) continue;
        // Extract abbreviation: "KJV1611-1769[KJV1769+]" → "KJV1769+"
        // or "ASV1901[ASV+]" → "ASV+"  or "Niobe2009" → "Niobe"
        final bracketMatch = RegExp(r'\[(.+?)\]').firstMatch(shortRaw);
        final short = bracketMatch != null
            ? bracketMatch.group(1)!
            : shortRaw.replaceAll(RegExp(r'\d+$'), '');
        _shortNames[fileName] = short;
      }
    } catch (e) {
      debugPrint('[BibleProvider] Failed to load modules: $e');
    }
  }

  /// Returns the short name for any module entry from the JSON list.
  String shortNameForModule(Map<String, dynamic> module) {
    final fileName = module['file_name'] as String?;
    if (fileName != null && _shortNames.containsKey(fileName)) {
      return _shortNames[fileName]!;
    }
    // Derive from version_short_name_and_date directly as fallback
    final shortRaw = module['version_short_name_and_date'] as String?;
    if (shortRaw == null) return '';
    final bracketMatch = RegExp(r'\[(.+?)\]').firstMatch(shortRaw);
    return bracketMatch != null
        ? bracketMatch.group(1)!
        : shortRaw.replaceAll(RegExp(r'\d+$'), '');
  }

  /// Downloads a Bible module and refreshes the installed list.
  /// Only one download runs at a time; concurrent calls are rejected.
  Future<void> downloadVersion(Map<String, dynamic> module) async {
    if (_downloadingFileName != null) {
      debugPrint('[BibleProvider] Download already in progress — ignoring.');
      return;
    }

    final url = module['download_link'] as String?;
    final fileName = module['file_name'] as String?;
    if (url == null || fileName == null) return;

    _downloadingFileName = fileName;
    _downloadProgress = 0.0;
    notifyListeners();

    try {
      await _service.downloadBible(
        url,
        fileName,
        onProgress: (progress) {
          _downloadProgress = progress;
          notifyListeners();
        },
      );
      _availableBibles = await _service.getAvailableBibles();
    } catch (e) {
      debugPrint('[BibleProvider] Download error for $fileName: $e');
      rethrow;
    } finally {
      _downloadingFileName = null;
      _downloadProgress = 0.0;
      notifyListeners();
    }
  }

  /// Deletes a downloaded version. Bundled modules are protected.
  Future<void> deleteVersion(String fileName) async {
    try {
      await _service.deleteBible(fileName);
      // If the deleted version was selected, fall back to the first available
      if (_selectedVersion == fileName) {
        _selectedVersion = null;
      }
      _availableBibles = await _service.getAvailableBibles();
      if (_selectedVersion == null && _availableBibles.isNotEmpty) {
        _selectedVersion = _availableBibles.first;
        await loadVerses();
      }
      notifyListeners();
    } catch (e) {
      debugPrint('[BibleProvider] Delete error for $fileName: $e');
      rethrow;
    }
  }

  // --- Split screen ---

  Future<void> enableSplit(String version) async {
    _splitEnabled = true;
    _splitVersion = version;
    await _loadSplitVerses();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('split_enabled', true);
    await prefs.setString('split_version', version);
    notifyListeners();
  }

  void disableSplit() async {
    _splitEnabled = false;
    _splitVersion = null;
    _splitVerses = [];
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('split_enabled', false);
    await prefs.remove('split_version');
    notifyListeners();
  }

  void toggleSplitOrientation() async {
    _splitHorizontal = !_splitHorizontal;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('split_horizontal', _splitHorizontal);
  }

  void setSplitProportion(double prop) async {
    _splitProportion = prop.clamp(0.2, 0.8);
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('split_proportion', _splitProportion);
  }

  Future<void> _loadSplitVerses() async {
    if (_splitVersion == null || !_splitEnabled) {
      _splitVerses = [];
      return;
    }
    try {
      _splitVerses = await _service.getVerses(
        version: _splitVersion!,
        bookNumber: _selectedBook.bookNumber,
        chapter: _selectedChapter,
      );
    } catch (e) {
      debugPrint('[BibleProvider] Split verses error: $e');
      _splitVerses = [];
    }
  }

  Future<void> _saveState() async {
    final prefs = await SharedPreferences.getInstance();
    if (_selectedVersion != null) {
      await prefs.setString('reading_version', _selectedVersion!);
    }
    await prefs.setInt('reading_book_number', _selectedBook.bookNumber);
    await prefs.setInt('reading_chapter', _selectedChapter);
    await prefs.setDouble('reading_font_size', _fontSize);
  }

  void saveScrollOffset(double offset) async {
    _scrollOffset = offset;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('reading_scroll_offset', offset);
  }

  Future<void> selectVersion(String version) async {
    _selectedVersion = version;
    _scrollOffset = 0;
    await loadVerses();
    _saveState();
  }

  Future<void> selectBook(Book book) async {
    _selectedBook = book;
    _selectedChapter = 1;
    _scrollOffset = 0;
    await loadVerses();
    _saveState();
  }

  Future<void> selectChapter(int chapter) async {
    _selectedChapter = chapter;
    _scrollOffset = 0;
    await loadVerses();
    _saveState();
  }

  Future<void> nextChapter() async {
    if (_selectedChapter < _selectedBook.chapterCount) {
      _selectedChapter++;
      _scrollOffset = 0;
      await loadVerses();
      _saveState();
    }
  }

  Future<void> previousChapter() async {
    if (_selectedChapter > 1) {
      _selectedChapter--;
      _scrollOffset = 0;
      await loadVerses();
      _saveState();
    }
  }

  /// Navigate to a specific book, chapter, and optionally scroll to a verse.
  Future<void> goToVerse(Book book, int chapter, {int? verse}) async {
    _selectedBook = book;
    _selectedChapter = chapter;
    _targetVerse = verse;
    _scrollOffset = 0;
    await loadVerses();
    _saveState();
  }

  void setFontSize(double size) {
    _fontSize = size.clamp(12.0, 36.0);
    notifyListeners();
    _saveState();
  }

  Future<void> loadVerses() async {
    if (_selectedVersion == null) return;

    _isLoading = true;
    notifyListeners();

    _verses = await _service.getVerses(
      version: _selectedVersion!,
      bookNumber: _selectedBook.bookNumber,
      chapter: _selectedChapter,
    );

    if (_splitEnabled) {
      await _loadSplitVerses();
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<int> getVerseCount(int bookNumber, int chapter) async {
    if (_selectedVersion == null) return 0;
    return _service.getVerseCount(
      version: _selectedVersion!,
      bookNumber: bookNumber,
      chapter: chapter,
    );
  }

  Future<List<Verse>> search(String query) async {
    if (_selectedVersion == null) return [];
    return _service.search(version: _selectedVersion!, query: query);
  }
}
