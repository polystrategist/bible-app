import 'package:flutter/material.dart';
import '../services/store_service.dart';

/// Manages bookmarks, highlights, and clip notes for the current chapter.
class UserDataProvider extends ChangeNotifier {
  final StoreService _store = StoreService();

  // Keyed by "bookNumber-chapter-verse"
  Set<String> _bookmarks = {};
  Map<String, String> _highlights = {}; // key -> color/content
  Map<String, Map<String, dynamic>> _clipNotes = {}; // key -> {content, color}

  Set<String> get bookmarks => _bookmarks;
  Map<String, String> get highlights => _highlights;
  Map<String, Map<String, dynamic>> get clipNotes => _clipNotes;

  StoreService get store => _store;

  bool isBookmarked(int bookNumber, int chapter, int verse) {
    return _bookmarks.contains('$bookNumber-$chapter-$verse');
  }

  String? getHighlightColor(int bookNumber, int chapter, int verse) {
    return _highlights['$bookNumber-$chapter-$verse'];
  }

  Map<String, dynamic>? getClipNote(int bookNumber, int chapter, int verse) {
    return _clipNotes['$bookNumber-$chapter-$verse'];
  }

  /// Load all user data for the given chapter.
  Future<void> loadChapterData(int bookNumber, int chapter) async {
    // Bookmarks
    final allBookmarks = await _store.getBookmarks();
    _bookmarks = allBookmarks
        .map((b) => b['key'] as String)
        .toSet();

    // Highlights
    final hlRows = await _store.getChapterHighlights(bookNumber, chapter);
    _highlights = {
      for (final hl in hlRows)
        hl['key'] as String: hl['content'] as String? ?? '#FFEB3B',
    };

    // Clip notes
    final cnRows = await _store.getChapterClipNotes(bookNumber, chapter);
    _clipNotes = {
      for (final cn in cnRows)
        cn['key'] as String: {
          'content': cn['content'] ?? '',
          'color': cn['color'] ?? '#FFD700',
        },
    };

    notifyListeners();
  }

  // ─── Bookmarks ─────────────────────────────────────────────────

  Future<void> toggleBookmark(int bookNumber, int chapter, int verse) async {
    await _store.toggleBookmark(bookNumber, chapter, verse);
    final key = '$bookNumber-$chapter-$verse';
    if (_bookmarks.contains(key)) {
      _bookmarks.remove(key);
    } else {
      _bookmarks.add(key);
    }
    notifyListeners();
  }

  // ─── Highlights ────────────────────────────────────────────────

  Future<void> setHighlight(
      int bookNumber, int chapter, int verse, String color) async {
    await _store.saveHighlight(bookNumber, chapter, verse, color);
    _highlights['$bookNumber-$chapter-$verse'] = color;
    notifyListeners();
  }

  Future<void> removeHighlight(
      int bookNumber, int chapter, int verse) async {
    await _store.deleteHighlight(bookNumber, chapter, verse);
    _highlights.remove('$bookNumber-$chapter-$verse');
    notifyListeners();
  }

  // ─── Clip Notes ────────────────────────────────────────────────

  Future<void> saveClipNote(int bookNumber, int chapter, int verse,
      String content, String color) async {
    await _store.saveClipNote(bookNumber, chapter, verse, content, color);
    _clipNotes['$bookNumber-$chapter-$verse'] = {
      'content': content,
      'color': color,
    };
    notifyListeners();
  }

  Future<void> removeClipNote(
      int bookNumber, int chapter, int verse) async {
    await _store.deleteClipNote(bookNumber, chapter, verse);
    _clipNotes.remove('$bookNumber-$chapter-$verse');
    notifyListeners();
  }
}
