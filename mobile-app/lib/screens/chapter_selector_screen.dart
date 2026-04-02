import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../models/book.dart';
import '../providers/bible_provider.dart';
import 'verse_selector_screen.dart';

class ChapterSelectorScreen extends StatelessWidget {
  final Book book;

  const ChapterSelectorScreen({super.key, required this.book});

  @override
  Widget build(BuildContext context) {
    final bible = context.read<BibleProvider>();
    final chapterCount = book.chapterCount;

    return Scaffold(
      appBar: AppBar(title: Text('${book.title} - Chapter')),
      body: GridView.builder(
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 6,
          crossAxisSpacing: 8,
          mainAxisSpacing: 8,
        ),
        itemCount: chapterCount,
        itemBuilder: (context, index) {
          final chapter = index + 1;
          final isSelected =
              book.bookNumber == bible.selectedBook.bookNumber &&
                  chapter == bible.selectedChapter;

          if (isSelected) {
            return ShadButton(
              onPressed: () => _goToVerseSelector(context, bible, chapter),
              child: Text(
                '$chapter',
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            );
          }
          return ShadButton.outline(
            onPressed: () => _goToVerseSelector(context, bible, chapter),
            child: Text(
              '$chapter',
              style: const TextStyle(fontSize: 16),
            ),
          );
        },
      ),
    );
  }

  Future<void> _goToVerseSelector(
      BuildContext context, BibleProvider bible, int chapter) async {
    final verseCount =
        await bible.getVerseCount(book.bookNumber, chapter);
    if (!context.mounted) return;
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => VerseSelectorScreen(
          book: book,
          chapter: chapter,
          verseCount: verseCount,
        ),
      ),
    );
  }
}
