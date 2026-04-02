import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/book.dart';
import '../models/verse.dart';
import '../providers/bible_provider.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final _controller = TextEditingController();
  List<Verse> _results = [];
  bool _isSearching = false;

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
        .shortName;
  }

  String _stripHtml(String html) {
    return html
        .replaceAll(RegExp(r'<[^>]*>'), '')
        .replaceAll('&nbsp;', ' ')
        .replaceAll(RegExp(r'\[\d+\]'), '')
        .trim();
  }

  Future<void> _search(String query) async {
    if (query.trim().isEmpty) {
      setState(() => _results = []);
      return;
    }

    setState(() => _isSearching = true);
    final bible = context.read<BibleProvider>();
    final results = await bible.search(query.trim());
    setState(() {
      _results = results;
      _isSearching = false;
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: _controller,
          autofocus: true,
          decoration: const InputDecoration(
            hintText: 'Search Bible...',
            border: InputBorder.none,
          ),
          onSubmitted: _search,
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () => _search(_controller.text),
          ),
        ],
      ),
      body: _isSearching
          ? const Center(child: CircularProgressIndicator())
          : _results.isEmpty
              ? Center(
                  child: Text(
                    _controller.text.isEmpty
                        ? 'Type to search'
                        : 'No results found',
                    style: TextStyle(
                      color: Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                  ),
                )
              : ListView.builder(
                  itemCount: _results.length,
                  itemBuilder: (context, index) {
                    final verse = _results[index];
                    return ListTile(
                      title: Text(
                        '${_getBookName(verse.bookNumber)} ${verse.chapter}:${verse.verse}',
                        style: const TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 13,
                        ),
                      ),
                      subtitle: Text(
                        _stripHtml(verse.text),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      onTap: () {
                        final bible = context.read<BibleProvider>();
                        final book = bibleBooks.firstWhere(
                          (b) => b.bookNumber == verse.bookNumber,
                        );
                        bible.selectBook(book);
                        bible.selectChapter(verse.chapter);
                        Navigator.pop(context);
                      },
                    );
                  },
                ),
    );
  }
}
