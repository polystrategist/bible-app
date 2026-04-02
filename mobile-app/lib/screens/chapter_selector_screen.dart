import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bible_provider.dart';

class ChapterSelectorScreen extends StatelessWidget {
  const ChapterSelectorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final bible = context.read<BibleProvider>();
    final chapterCount = bible.selectedBook.chapterCount;

    return Scaffold(
      appBar: AppBar(title: Text('${bible.selectedBook.title} - Chapters')),
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
          final isSelected = chapter == bible.selectedChapter;

          return Material(
            color: isSelected
                ? Theme.of(context).colorScheme.primaryContainer
                : Theme.of(context).colorScheme.surfaceContainerHighest,
            borderRadius: BorderRadius.circular(8),
            child: InkWell(
              borderRadius: BorderRadius.circular(8),
              onTap: () {
                bible.selectChapter(chapter);
                Navigator.pop(context);
              },
              child: Center(
                child: Text(
                  '$chapter',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
