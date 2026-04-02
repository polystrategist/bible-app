import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/verse.dart';
import '../providers/bible_provider.dart';
import '../providers/user_data_provider.dart';
import 'verse_actions_sheet.dart';

class VerseList extends StatelessWidget {
  final List<Verse> verses;
  final double fontSize;

  const VerseList({
    super.key,
    required this.verses,
    this.fontSize = 18,
  });

  String _stripHtml(String html) {
    return html
        .replaceAll(RegExp(r'<[^>]*>'), '')
        .replaceAll('&nbsp;', ' ')
        .replaceAll(RegExp(r'\[\d+\]'), '')
        .trim();
  }

  Color? _parseHighlightColor(String? colorStr) {
    if (colorStr == null) return null;
    if (colorStr.startsWith('#') && colorStr.length == 7) {
      return Color(int.parse('FF${colorStr.substring(1)}', radix: 16));
    }
    // Named colors
    switch (colorStr.toLowerCase()) {
      case 'yellow':
        return Colors.yellow.shade100;
      case 'green':
        return Colors.green.shade100;
      case 'blue':
        return Colors.blue.shade100;
      case 'pink':
        return Colors.pink.shade100;
      case 'orange':
        return Colors.orange.shade100;
      default:
        return Colors.yellow.shade100;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (verses.isEmpty) {
      return const Center(child: Text('No verses found'));
    }

    final userData = context.watch<UserDataProvider>();
    final bible = context.read<BibleProvider>();

    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      itemCount: verses.length,
      itemBuilder: (context, index) {
        final verse = verses[index];
        final text = _stripHtml(verse.text);
        final isBookmarked = userData.isBookmarked(
            verse.bookNumber, verse.chapter, verse.verse);
        final highlightColor = userData.getHighlightColor(
            verse.bookNumber, verse.chapter, verse.verse);
        final clipNote = userData.getClipNote(
            verse.bookNumber, verse.chapter, verse.verse);
        final bgColor = _parseHighlightColor(highlightColor);

        return GestureDetector(
          onLongPress: () {
            showModalBottomSheet(
              context: context,
              builder: (_) => VerseActionsSheet(
                verse: verse,
                bookName: bible.selectedBook.title,
                isBookmarked: isBookmarked,
                hasHighlight: highlightColor != null,
                hasClipNote: clipNote != null,
                clipNoteContent: clipNote?['content'] as String? ?? '',
              ),
            );
          },
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 4),
            decoration: bgColor != null
                ? BoxDecoration(
                    color: bgColor.withAlpha(80),
                    borderRadius: BorderRadius.circular(4),
                  )
                : null,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                RichText(
                  text: TextSpan(
                    children: [
                      TextSpan(
                        text: '${verse.verse}  ',
                        style: TextStyle(
                          fontSize: fontSize * 0.7,
                          fontWeight: FontWeight.bold,
                          color: Theme.of(context).colorScheme.primary,
                        ),
                      ),
                      TextSpan(
                        text: text,
                        style: TextStyle(
                          fontSize: fontSize,
                          height: 1.6,
                          color: Theme.of(context).colorScheme.onSurface,
                        ),
                      ),
                    ],
                  ),
                ),
                // Indicators row
                if (isBookmarked || clipNote != null)
                  Padding(
                    padding: const EdgeInsets.only(left: 20, top: 2),
                    child: Row(
                      children: [
                        if (isBookmarked)
                          Icon(Icons.bookmark,
                              size: 14,
                              color: Theme.of(context).colorScheme.primary),
                        if (clipNote != null) ...[
                          const SizedBox(width: 4),
                          Icon(Icons.sticky_note_2,
                              size: 14,
                              color: _parseHighlightColor(
                                      clipNote['color'] as String?) ??
                                  Colors.amber),
                          const SizedBox(width: 4),
                          Flexible(
                            child: Text(
                              clipNote['content'] as String? ?? '',
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                fontSize: 11,
                                fontStyle: FontStyle.italic,
                                color: Theme.of(context)
                                    .colorScheme
                                    .onSurfaceVariant,
                              ),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }
}
