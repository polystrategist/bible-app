import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../models/book.dart';
import '../providers/bible_provider.dart';
import '../services/store_service.dart';

class BookmarksScreen extends StatefulWidget {
  const BookmarksScreen({super.key});

  @override
  State<BookmarksScreen> createState() => _BookmarksScreenState();
}

class _BookmarksScreenState extends State<BookmarksScreen> {
  final StoreService _store = StoreService();
  List<Map<String, dynamic>> _bookmarks = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadBookmarks();
  }

  Future<void> _loadBookmarks() async {
    final bookmarks = await _store.getBookmarks();
    if (!mounted) return;
    setState(() {
      _bookmarks = bookmarks;
      _isLoading = false;
    });
  }

  String _getBookName(int bookNumber) {
    return bibleBooks
        .firstWhere(
          (b) => b.bookNumber == bookNumber,
          orElse: () => const Book(
            title: 'Unknown',
            shortName: '?',
            bookNumber: 0,
            chapterCount: 0,
          ),
        )
        .title;
  }

  @override
  Widget build(BuildContext context) {
    final theme = ShadTheme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Bookmarks')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _bookmarks.isEmpty
              ? Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(LucideIcons.bookmark,
                          size: 48, color: theme.colorScheme.mutedForeground),
                      const SizedBox(height: 12),
                      Text('No bookmarks yet', style: theme.textTheme.muted),
                      const SizedBox(height: 4),
                      Text(
                        'Long-press a verse to bookmark it',
                        style: theme.textTheme.muted.copyWith(fontSize: 12),
                      ),
                    ],
                  ),
                )
              : ListView.separated(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  itemCount: _bookmarks.length,
                  separatorBuilder: (_, _) =>
                      Divider(height: 1, color: theme.colorScheme.border),
                  itemBuilder: (context, index) {
                    final bm = _bookmarks[index];
                    final bookNumber = bm['book_number'] as int;
                    final chapter = bm['chapter'] as int;
                    final verse = bm['verse'] as int;
                    final bookName = _getBookName(bookNumber);

                    return ListTile(
                      leading: Icon(LucideIcons.bookmark,
                          color: theme.colorScheme.primary, size: 20),
                      title: Text(
                        '$bookName $chapter:$verse',
                        style: theme.textTheme.small
                            .copyWith(fontWeight: FontWeight.w600),
                      ),
                      trailing: const Icon(LucideIcons.chevronRight, size: 16),
                      onTap: () {
                        final bible = context.read<BibleProvider>();
                        final book = bibleBooks.firstWhere(
                          (b) => b.bookNumber == bookNumber,
                          orElse: () => bibleBooks.first,
                        );
                        bible.goToVerse(book, chapter, verse: verse);
                        Navigator.pop(context);
                      },
                    );
                  },
                ),
    );
  }
}
