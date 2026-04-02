import 'package:flutter/material.dart';
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

  /// Consume the target verse (returns it once, then clears).
  int? consumeTargetVerse() {
    final v = _targetVerse;
    _targetVerse = null;
    return v;
  }

  String get selectedVersionTitle =>
      _selectedVersion?.replaceAll('.SQLite3', '').replaceAll('.db', '') ?? 'No Bible Selected';

  Future<void> init() async {
    try {
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
          final book = bibleBooks.where((b) => b.bookNumber == savedBookNumber);
          if (book.isNotEmpty) _selectedBook = book.first;
        }

        if (savedChapter != null && savedChapter <= _selectedBook.chapterCount) {
          _selectedChapter = savedChapter;
        }

        await loadVerses();
      }
    } catch (e) {
      debugPrint('[BibleProvider] init error: $e');
    }
    _isInitialized = true;
    notifyListeners();
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
