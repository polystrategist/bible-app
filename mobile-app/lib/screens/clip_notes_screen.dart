import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../models/book.dart';
import '../providers/bible_provider.dart';
import '../services/store_service.dart';

class ClipNotesScreen extends StatefulWidget {
  const ClipNotesScreen({super.key});

  @override
  State<ClipNotesScreen> createState() => _ClipNotesScreenState();
}

class _ClipNotesScreenState extends State<ClipNotesScreen> {
  final StoreService _store = StoreService();
  List<Map<String, dynamic>> _clipNotes = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadClipNotes();
  }

  Future<void> _loadClipNotes() async {
    final d = await _store.db;
    final spaceId = await _store.getSelectedStudySpaceId();
    final clipNotes = await d.query('clip_notes',
        where: 'study_space_id = ?',
        whereArgs: [spaceId],
        orderBy: 'created_at DESC');
    if (!mounted) return;
    setState(() {
      _clipNotes = clipNotes;
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
      appBar: AppBar(title: const Text('Clip Notes')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _clipNotes.isEmpty
              ? Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(LucideIcons.stickyNote,
                          size: 48, color: theme.colorScheme.mutedForeground),
                      const SizedBox(height: 12),
                      Text('No clip notes yet', style: theme.textTheme.muted),
                      const SizedBox(height: 4),
                      Text(
                        'Long-press a verse to clip a note',
                        style: theme.textTheme.muted.copyWith(fontSize: 12),
                      ),
                    ],
                  ),
                )
              : ListView.separated(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  itemCount: _clipNotes.length,
                  separatorBuilder: (_, _) =>
                      Divider(height: 1, color: theme.colorScheme.border),
                  itemBuilder: (context, index) {
                    final clipNote = _clipNotes[index];
                    final bookNumber = clipNote['book_number'] as int;
                    final chapter = clipNote['chapter'] as int;
                    final verse = clipNote['verse'] as int;
                    final content = clipNote['content'] as String? ?? '';
                    final bookName = _getBookName(bookNumber);

                    return ListTile(
                      leading: Icon(LucideIcons.stickyNote,
                          color: Colors.amber, size: 20),
                      title: Text(
                        '$bookName $chapter:$verse',
                        style: theme.textTheme.small
                            .copyWith(fontWeight: FontWeight.w600),
                      ),
                      subtitle: Text(
                        content,
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                        style: theme.textTheme.muted.copyWith(fontSize: 12),
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
