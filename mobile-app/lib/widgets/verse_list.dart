import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../models/verse.dart';
import '../providers/bible_provider.dart';
import '../providers/user_data_provider.dart';
import 'verse_actions_sheet.dart';

class VerseList extends StatefulWidget {
  final List<Verse> verses;
  final double fontSize;

  const VerseList({
    super.key,
    required this.verses,
    this.fontSize = 18,
  });

  @override
  State<VerseList> createState() => _VerseListState();
}

class _VerseListState extends State<VerseList> {
  final ScrollController _scrollController = ScrollController();
  final Map<int, GlobalKey> _verseKeys = {};
  double _pinchBaseSize = 0;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToTarget());
  }

  @override
  void didUpdateWidget(VerseList oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.verses != widget.verses) {
      _verseKeys.clear();
      WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToTarget());
    }
  }

  void _scrollToTarget() {
    final bible = context.read<BibleProvider>();
    final target = bible.consumeTargetVerse();
    if (target == null) return;

    final key = _verseKeys[target];
    if (key?.currentContext != null) {
      Scrollable.ensureVisible(
        key!.currentContext!,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        alignment: 0.1,
      );
    }
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

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
    final theme = ShadTheme.of(context);

    if (widget.verses.isEmpty) {
      return Center(
        child: Text('No verses found', style: theme.textTheme.muted),
      );
    }

    final userData = context.watch<UserDataProvider>();
    final bible = context.read<BibleProvider>();

    return GestureDetector(
      onScaleStart: (_) => _pinchBaseSize = widget.fontSize,
      onScaleUpdate: (details) {
        if (details.pointerCount < 2) return;
        final newSize = (_pinchBaseSize * details.scale).clamp(12.0, 36.0);
        bible.setFontSize(newSize);
      },
      child: ListView.builder(
      controller: _scrollController,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      itemCount: widget.verses.length,
      itemBuilder: (context, index) {
        final verse = widget.verses[index];
        final text = _stripHtml(verse.text);
        final isBookmarked = userData.isBookmarked(
            verse.bookNumber, verse.chapter, verse.verse);
        final highlightColor = userData.getHighlightColor(
            verse.bookNumber, verse.chapter, verse.verse);
        final clipNote = userData.getClipNote(
            verse.bookNumber, verse.chapter, verse.verse);
        final bgColor = _parseHighlightColor(highlightColor);

        // Store a key for each verse so we can scroll to it
        _verseKeys.putIfAbsent(verse.verse, () => GlobalKey());
        final verseKey = _verseKeys[verse.verse]!;

        return GestureDetector(
          key: verseKey,
          onLongPress: () {
            showShadSheet(
              side: ShadSheetSide.bottom,
              context: context,
              builder: (_) => VerseActionsSheet(
                verse: verse,
                bookName: bible.selectedBook.title,
                isBookmarked: isBookmarked,
                hasHighlight: highlightColor != null,
                hasClipNote: clipNote != null,
                clipNoteContent: clipNote?['content'] as String? ?? '',
                clipNoteColor: clipNote?['color'] as String? ?? '#FFD700',
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
                          fontSize: widget.fontSize * 0.7,
                          fontWeight: FontWeight.bold,
                          color: theme.colorScheme.primary,
                        ),
                      ),
                      TextSpan(
                        text: text,
                        style: TextStyle(
                          fontSize: widget.fontSize,
                          height: 1.6,
                          color: theme.colorScheme.foreground,
                        ),
                      ),
                    ],
                  ),
                ),
                // Indicators row
                if (isBookmarked)
                  Padding(
                    padding: const EdgeInsets.only(left: 20, top: 2),
                    child: Icon(LucideIcons.bookmark,
                        size: 14, color: theme.colorScheme.primary),
                  ),
                if (clipNote != null)
                  Container(
                    margin: const EdgeInsets.only(top: 4),
                    padding:
                        const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                    decoration: BoxDecoration(
                      color: (_parseHighlightColor(
                                  clipNote['color'] as String?) ??
                              Colors.amber)
                          .withAlpha(60),
                      borderRadius: BorderRadius.circular(6),
                      border: Border.all(
                        color: (_parseHighlightColor(
                                    clipNote['color'] as String?) ??
                                Colors.amber)
                            .withAlpha(120),
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(LucideIcons.paperclip,
                            size: 12,
                            color: theme.colorScheme.mutedForeground),
                        const SizedBox(width: 4),
                        Flexible(
                          child: Text(
                            clipNote['content'] as String? ?? '',
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                            style: TextStyle(
                              fontSize: widget.fontSize * 0.75,
                              color: theme.colorScheme.foreground,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
              ],
            ),
          ),
        );
      },
    ),
    );
  }
}
