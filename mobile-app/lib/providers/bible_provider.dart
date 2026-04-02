import 'package:flutter/material.dart';
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
  double _fontSize = 18;

  List<String> get availableBibles => _availableBibles;
  String? get selectedVersion => _selectedVersion;
  Book get selectedBook => _selectedBook;
  int get selectedChapter => _selectedChapter;
  List<Verse> get verses => _verses;
  bool get isLoading => _isLoading;
  double get fontSize => _fontSize;

  String get selectedVersionTitle =>
      _selectedVersion?.replaceAll('.SQLite3', '').replaceAll('.db', '') ?? 'No Bible Selected';

  Future<void> init() async {
    _availableBibles = await _service.getAvailableBibles();
    if (_availableBibles.isNotEmpty) {
      _selectedVersion = _availableBibles.first;
      await loadVerses();
    }
    notifyListeners();
  }

  Future<void> selectVersion(String version) async {
    _selectedVersion = version;
    await loadVerses();
  }

  Future<void> selectBook(Book book) async {
    _selectedBook = book;
    _selectedChapter = 1;
    await loadVerses();
  }

  Future<void> selectChapter(int chapter) async {
    _selectedChapter = chapter;
    await loadVerses();
  }

  Future<void> nextChapter() async {
    if (_selectedChapter < _selectedBook.chapterCount) {
      _selectedChapter++;
      await loadVerses();
    }
  }

  Future<void> previousChapter() async {
    if (_selectedChapter > 1) {
      _selectedChapter--;
      await loadVerses();
    }
  }

  void setFontSize(double size) {
    _fontSize = size.clamp(12.0, 36.0);
    notifyListeners();
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

  Future<List<Verse>> search(String query) async {
    if (_selectedVersion == null) return [];
    return _service.search(version: _selectedVersion!, query: query);
  }
}
