import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/book.dart';
import '../providers/bible_provider.dart';

class BookSelectorScreen extends StatelessWidget {
  const BookSelectorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final bible = context.read<BibleProvider>();
    final otBooks = bibleBooks.where((b) => b.bookNumber < 470 && !b.deuterocanonical).toList();
    final ntBooks = bibleBooks.where((b) => b.bookNumber >= 470 && !b.deuterocanonical).toList();

    return Scaffold(
      appBar: AppBar(title: const Text('Select Book')),
      body: ListView(
        children: [
          _buildSection(context, 'Old Testament', otBooks, bible),
          _buildSection(context, 'New Testament', ntBooks, bible),
        ],
      ),
    );
  }

  Widget _buildSection(BuildContext context, String title, List<Book> books, BibleProvider bible) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
          child: Text(
            title,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Theme.of(context).colorScheme.primary,
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

            return Material(
              color: isSelected
                  ? Theme.of(context).colorScheme.primaryContainer
                  : Theme.of(context).colorScheme.surfaceContainerHighest,
              borderRadius: BorderRadius.circular(8),
              child: InkWell(
                borderRadius: BorderRadius.circular(8),
                onTap: () {
                  bible.selectBook(book);
                  Navigator.pop(context);
                },
                child: Center(
                  child: Text(
                    book.shortName,
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                    ),
                  ),
                ),
              ),
            );
          },
        ),
      ],
    );
  }
}
