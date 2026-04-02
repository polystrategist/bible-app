import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../models/book.dart';
import '../providers/bible_provider.dart';
import 'chapter_selector_screen.dart';

class BookSelectorScreen extends StatelessWidget {
  const BookSelectorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final bible = context.read<BibleProvider>();
    final theme = ShadTheme.of(context);
    final otBooks =
        bibleBooks.where((b) => b.bookNumber < 470 && !b.deuterocanonical).toList();
    final ntBooks =
        bibleBooks.where((b) => b.bookNumber >= 470 && !b.deuterocanonical).toList();

    return Scaffold(
      appBar: AppBar(title: const Text('Select Book')),
      body: ListView(
        children: [
          _buildSection(context, 'Old Testament', otBooks, bible, theme),
          _buildSection(context, 'New Testament', ntBooks, bible, theme),
        ],
      ),
    );
  }

  Widget _buildSection(BuildContext context, String title, List<Book> books,
      BibleProvider bible, ShadThemeData theme) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
          child: Text(
            title,
            style: theme.textTheme.small.copyWith(
              fontWeight: FontWeight.w600,
              color: theme.colorScheme.primary,
            ),
          ),
        ),
        GridView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          padding: const EdgeInsets.symmetric(horizontal: 12),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 4,
            childAspectRatio: 2.5,
            crossAxisSpacing: 6,
            mainAxisSpacing: 6,
          ),
          itemCount: books.length,
          itemBuilder: (context, index) {
            final book = books[index];
            final isSelected = book.bookNumber == bible.selectedBook.bookNumber;

            if (isSelected) {
              return ShadButton(
                size: ShadButtonSize.sm,
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => ChapterSelectorScreen(book: book),
                    ),
                  );
                },
                child: Text(
                  book.shortName,
                  style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                ),
              );
            }
            return ShadButton.outline(
              size: ShadButtonSize.sm,
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ChapterSelectorScreen(book: book),
                  ),
                );
              },
              child: Text(
                book.shortName,
                style: const TextStyle(fontSize: 12),
              ),
            );
          },
        ),
      ],
    );
  }
}
