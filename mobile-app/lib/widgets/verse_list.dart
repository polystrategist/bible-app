import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../models/verse.dart';
import '../providers/bible_provider.dart';
import '../providers/user_data_provider.dart';

/// Represents the scroll position as a verse number + proportion scrolled.
class VerseScrollPosition {
  final int verseNumber;

  /// 0.0 = top of verse visible, 1.0 = fully scrolled past
  final double proportion;

  const VerseScrollPosition(this.verseNumber, this.proportion);
}

class VerseList extends StatefulWidget {
  final List<Verse> verses;
  final double fontSize;
  final Set<int> selectedVerses;
  final ValueChanged<int> onVerseTap;

  /// Called with the top visible verse and scroll proportion during user scroll.
  final ValueChanged<VerseScrollPosition>? onVerseScroll;

  /// Listen to this notifier to sync scroll from another pane.
  final ValueNotifier<VerseScrollPosition?>? syncScrollNotifier;

  /// Whether to save/restore scroll offset via BibleProvider.
  final bool persistScroll;

  const VerseList({
    super.key,
    required this.verses,
    this.fontSize = 18,
    required this.selectedVerses,
    required this.onVerseTap,
    this.onVerseScroll,
    this.syncScrollNotifier,
    this.persistScroll = true,
  });

  @override
  State<VerseList> createState() => _VerseListState();
}

class _VerseListState extends State<VerseList> {
  final ScrollController _scrollController = ScrollController();
  final Map<int, GlobalKey> _verseKeys = {};
  double _pinchBaseSize = 0;
  bool _isSyncing = false;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(_onScroll);
    widget.syncScrollNotifier?.addListener(_onSyncScroll);
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _restoreOrScrollToTarget();
    });
  }

  @override
  void didUpdateWidget(VerseList oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.syncScrollNotifier != widget.syncScrollNotifier) {
      oldWidget.syncScrollNotifier?.removeListener(_onSyncScroll);
      widget.syncScrollNotifier?.addListener(_onSyncScroll);
    }
    if (oldWidget.verses != widget.verses) {
      _verseKeys.clear();
      WidgetsBinding.instance.addPostFrameCallback((_) {
        _restoreOrScrollToTarget();
      });
    }
  }

  void _onSyncScroll() {
    final pos = widget.syncScrollNotifier?.value;
    if (pos == null || !mounted || !_scrollController.hasClients) return;

    _isSyncing = true;

    // Use Scrollable.ensureVisible to bring the verse to the top
    final key = _verseKeys[pos.verseNumber];
    if (key?.currentContext != null) {
      Scrollable.ensureVisible(
        key!.currentContext!,
        alignment: 0.0, // put it at the very top
        duration: Duration.zero, // instant, no animation
      ).then((_) {
        // After jumping to the verse, adjust by the proportion
        if (mounted && _scrollController.hasClients) {
          final box = key.currentContext?.findRenderObject() as RenderBox?;
          if (box != null && box.hasSize) {
            final offset = _scrollController.offset +
                (pos.proportion * box.size.height);
            _scrollController.jumpTo(
              offset.clamp(0.0, _scrollController.position.maxScrollExtent),
            );
          }
        }
        Future.delayed(const Duration(milliseconds: 100), () {
          if (mounted) _isSyncing = false;
        });
      });
      return;
    }

    // Fallback: estimate
    final verseIndex =
        widget.verses.indexWhere((v) => v.verse == pos.verseNumber);
    if (verseIndex >= 0) {
      final estimatedHeight = widget.fontSize * 4;
      final offset = verseIndex * estimatedHeight +
          pos.proportion * estimatedHeight;
      _scrollController.jumpTo(
        offset.clamp(0.0, _scrollController.position.maxScrollExtent),
      );
    }
    Future.delayed(const Duration(milliseconds: 100), () {
      if (mounted) _isSyncing = false;
    });
  }

  void _restoreOrScrollToTarget() {
    final bible = context.read<BibleProvider>();
    final target = bible.consumeTargetVerse();

    if (target != null) {
      _scrollToVerse(target);
    } else if (widget.persistScroll &&
        bible.scrollOffset > 0 &&
        _scrollController.hasClients &&
        _scrollController.position.maxScrollExtent >= bible.scrollOffset) {
      _scrollController.jumpTo(bible.scrollOffset);
    }
  }

  Future<void> _scrollToVerse(int verseNumber) async {
    if (!_scrollController.hasClients) return;

    final estimatedItemHeight = widget.fontSize * 4;
    final estimatedOffset = (verseNumber - 1) * estimatedItemHeight;
    final maxScroll = _scrollController.position.maxScrollExtent;

    if (estimatedOffset > 0) {
      _scrollController.jumpTo(estimatedOffset.clamp(0, maxScroll));
      await Future.delayed(const Duration(milliseconds: 50));
      await WidgetsBinding.instance.endOfFrame;
    }

    final key = _verseKeys[verseNumber];
    if (key?.currentContext != null) {
      await Scrollable.ensureVisible(
        key!.currentContext!,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        alignment: 0.1,
      );
    }
  }

  void _onScroll() {
    if (widget.persistScroll) {
      context.read<BibleProvider>().saveScrollOffset(_scrollController.offset);
    }
    if (!_isSyncing && widget.onVerseScroll != null) {
      _reportTopVerse();
    }
  }

  void _reportTopVerse() {
    if (!_scrollController.hasClients) return;

    // Get the top edge of the ListView viewport in global coordinates
    final listRenderBox = context.findRenderObject() as RenderBox?;
    if (listRenderBox == null) return;
    final listTop = listRenderBox.localToGlobal(Offset.zero).dy;

    int? topVerse;
    double topProp = 0;

    for (final verse in widget.verses) {
      final key = _verseKeys[verse.verse];
      if (key?.currentContext == null) continue;
      final box = key!.currentContext!.findRenderObject() as RenderBox?;
      if (box == null || !box.hasSize) continue;

      final globalPos = box.localToGlobal(Offset.zero);
      final relativeTop = globalPos.dy - listTop;
      final relativeBottom = relativeTop + box.size.height;

      // First verse whose bottom is below the viewport top
      // (meaning it's at least partially visible at the top)
      if (relativeBottom > 0) {
        topVerse = verse.verse;
        if (relativeTop >= 0) {
          topProp = 0;
        } else {
          topProp = (-relativeTop) / box.size.height;
        }
        break;
      }
    }

    if (topVerse != null) {
      widget.onVerseScroll!(VerseScrollPosition(topVerse, topProp));
    }
  }

  @override
  void dispose() {
    widget.syncScrollNotifier?.removeListener(_onSyncScroll);
    _scrollController.removeListener(_onScroll);
    _scrollController.dispose();
    super.dispose();
  }

  String _stripHtml(String html) {
    return html
        // Remove Strong's numbers: <S>1234</S>, <s>1234</s>
        .replaceAll(RegExp(r'<[Ss]>\d+</[Ss]>'), '')
        // Remove footnotes: <f>[1]</f>, <f>text</f>
        .replaceAll(RegExp(r'<f>.*?</f>', caseSensitive: false), '')
        // Remove remaining HTML tags
        .replaceAll(RegExp(r'<[^>]*>'), '')
        .replaceAll('&nbsp;', ' ')
        .replaceAll(RegExp(r'\[\d+\]'), '')
        // Remove Strong's concordance numbers glued to words/punctuation
        .replaceAll(RegExp(r'(?<=[\w,.:;!?\-])\d{1,5}(?=\s|[,.:;!?\-]|$)'), '')
        // Collapse multiple spaces
        .replaceAll(RegExp(r' {2,}'), ' ')
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
          final isSelected = widget.selectedVerses.contains(verse.verse);

          _verseKeys.putIfAbsent(verse.verse, () => GlobalKey());
          final verseKey = _verseKeys[verse.verse]!;

          return GestureDetector(
            key: verseKey,
            onTap: () => widget.onVerseTap(verse.verse),
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
                            decoration: isSelected
                                ? TextDecoration.underline
                                : TextDecoration.none,
                            decorationStyle: isSelected
                                ? TextDecorationStyle.dashed
                                : null,
                            decorationColor: isSelected
                                ? theme.colorScheme.primary
                                : null,
                            decorationThickness: isSelected ? 2 : null,
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
                      padding: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 6),
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
