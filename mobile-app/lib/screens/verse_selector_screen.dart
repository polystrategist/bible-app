import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../models/book.dart';
import '../providers/bible_provider.dart';

class VerseSelectorScreen extends StatelessWidget {
  final Book book;
  final int chapter;
  final int verseCount;

  const VerseSelectorScreen({
    super.key,
    required this.book,
    required this.chapter,
    required this.verseCount,
  });

  @override
  Widget build(BuildContext context) {
    final bible = context.read<BibleProvider>();

    return Scaffold(
      appBar: AppBar(title: Text('${book.title} $chapter - Verse')),
      body: GridView.builder(
        padding: const EdgeInsets.all(16),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 6,
          crossAxisSpacing: 8,
          mainAxisSpacing: 8,
        ),
        itemCount: verseCount,
        itemBuilder: (context, index) {
          final verse = index + 1;

          return ShadButton.outline(
            onPressed: () {
              bible.goToVerse(book, chapter, verse: verse);
              // Pop all the way back to the reader
              Navigator.of(context).popUntil((route) => route.isFirst);
            },
            child: Text(
              '$verse',
              style: const TextStyle(fontSize: 14),
            ),
          );
        },
      ),
    );
  }
}
