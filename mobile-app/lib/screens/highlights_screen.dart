import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../models/book.dart';
import '../providers/bible_provider.dart';
import '../services/store_service.dart';

class HighlightsScreen extends StatefulWidget {
  const HighlightsScreen({super.key});

  @override
  State<HighlightsScreen> createState() => _HighlightsScreenState();
}

class _HighlightsScreenState extends State<HighlightsScreen> {
  final StoreService _store = StoreService();
  List<Map<String, dynamic>> _highlights = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadHighlights();
  }

  Future<void> _loadHighlights() async {
    final d = await _store.db;
    final spaceId = await _store.getSelectedStudySpaceId();
    final highlights = await d.query('highlights',
        where: 'study_space_id = ?',
        whereArgs: [spaceId],
        orderBy: 'created_at DESC');
    if (!mounted) return;
    setState(() {
      _highlights = highlights;
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

  Color _parseColor(String? hex) {
    if (hex != null && hex.startsWith('#') && hex.length == 7) {
      return Color(int.parse('FF${hex.substring(1)}', radix: 16));
    }
    return Colors.yellow.shade200;
  }

  @override
  Widget build(BuildContext context) {
    final theme = ShadTheme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Highlights')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _highlights.isEmpty
              ? Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(LucideIcons.highlighter,
                          size: 48, color: theme.colorScheme.mutedForeground),
                      const SizedBox(height: 12),
                      Text('No highlights yet', style: theme.textTheme.muted),
                      const SizedBox(height: 4),
                      Text(
                        'Long-press a verse to highlight it',
                        style: theme.textTheme.muted.copyWith(fontSize: 12),
                      ),
                    ],
                  ),
                )
              : ListView.separated(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  itemCount: _highlights.length,
                  separatorBuilder: (_, _) =>
                      Divider(height: 1, color: theme.colorScheme.border),
                  itemBuilder: (context, index) {
                    final hl = _highlights[index];
                    final bookNumber = hl['book_number'] as int;
                    final chapter = hl['chapter'] as int;
                    final verse = hl['verse'] as int;
                    final color = _parseColor(hl['content'] as String?);
                    final bookName = _getBookName(bookNumber);

                    return ListTile(
                      leading: Container(
                        width: 24,
                        height: 24,
                        decoration: BoxDecoration(
                          color: color,
                          shape: BoxShape.circle,
                          border: Border.all(color: theme.colorScheme.border),
                        ),
                      ),
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
