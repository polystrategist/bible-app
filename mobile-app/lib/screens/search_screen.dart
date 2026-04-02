import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

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

  Widget _buildHighlightedText(String text, String query, ShadThemeData theme) {
    if (query.isEmpty) {
      return Text(text, maxLines: 2, overflow: TextOverflow.ellipsis);
    }

    final lowerText = text.toLowerCase();
    final lowerQuery = query.toLowerCase();
    final spans = <TextSpan>[];
    var start = 0;

    while (true) {
      final index = lowerText.indexOf(lowerQuery, start);
      if (index == -1) {
        spans.add(TextSpan(text: text.substring(start)));
        break;
      }
      if (index > start) {
        spans.add(TextSpan(text: text.substring(start, index)));
      }
      spans.add(TextSpan(
        text: text.substring(index, index + query.length),
        style: TextStyle(
          backgroundColor: theme.colorScheme.primary.withAlpha(60),
          fontWeight: FontWeight.w600,
          color: theme.colorScheme.primary,
        ),
      ));
      start = index + query.length;
    }

    return RichText(
      maxLines: 2,
      overflow: TextOverflow.ellipsis,
      text: TextSpan(
        style: TextStyle(color: theme.colorScheme.foreground, fontSize: 14),
        children: spans,
      ),
    );
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
    final theme = ShadTheme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: ShadInput(
          controller: _controller,
          placeholder: const Text('Search Bible...'),
          onSubmitted: (v) => _search(v),
        ),
        actions: [
          ShadIconButton.ghost(
            icon: const Icon(LucideIcons.search, size: 20),
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
                    style: theme.textTheme.muted,
                  ),
                )
              : ListView.builder(
                  itemCount: _results.length,
                  itemBuilder: (context, index) {
                    final verse = _results[index];
                    return ListTile(
                      title: Text(
                        '${_getBookName(verse.bookNumber)} ${verse.chapter}:${verse.verse}',
                        style: theme.textTheme.small.copyWith(
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      subtitle: _buildHighlightedText(
                        _stripHtml(verse.text),
                        _controller.text.trim(),
                        theme,
                      ),
                      onTap: () {
                        final bible = context.read<BibleProvider>();
                        final book = bibleBooks.firstWhere(
                          (b) => b.bookNumber == verse.bookNumber,
                        );
                        bible.goToVerse(book, verse.chapter,
                            verse: verse.verse);
                        Navigator.pop(context);
                      },
                    );
                  },
                ),
    );
  }
}
