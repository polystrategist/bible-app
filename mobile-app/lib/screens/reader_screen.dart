import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';
import 'package:share_plus/share_plus.dart';

import '../providers/bible_provider.dart';
import '../providers/theme_provider.dart';
import '../providers/user_data_provider.dart';
import '../widgets/verse_list.dart';
import 'book_selector_screen.dart';
import 'bookmarks_screen.dart';
import 'highlights_screen.dart';
import 'login_screen.dart';
import 'clip_notes_screen.dart';
import 'search_screen.dart';
import 'version_selector_screen.dart';

const _themeColors = [
  'blue', 'gray', 'green', 'neutral', 'orange', 'red',
  'rose', 'slate', 'stone', 'violet', 'yellow', 'zinc',
];

class ReaderScreen extends StatefulWidget {
  const ReaderScreen({super.key});

  @override
  State<ReaderScreen> createState() => _ReaderScreenState();
}

class _ReaderScreenState extends State<ReaderScreen> {
  int? _lastBook;
  int? _lastChapter;
  final Set<int> _selectedVerses = {};

  // Split scroll sync
  final ValueNotifier<VerseScrollPosition?> _syncToPrimary =
      ValueNotifier(null);
  final ValueNotifier<VerseScrollPosition?> _syncToSplit =
      ValueNotifier(null);

  void _onVerseTap(int verseNumber) {
    setState(() {
      if (_selectedVerses.contains(verseNumber)) {
        _selectedVerses.remove(verseNumber);
      } else {
        _selectedVerses.add(verseNumber);
      }
    });
  }

  void _clearSelection() {
    setState(() => _selectedVerses.clear());
  }

  @override
  void dispose() {
    _syncToPrimary.dispose();
    _syncToSplit.dispose();
    super.dispose();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final bible = context.watch<BibleProvider>();
    if (bible.selectedBook.bookNumber != _lastBook ||
        bible.selectedChapter != _lastChapter) {
      _lastBook = bible.selectedBook.bookNumber;
      _lastChapter = bible.selectedChapter;
      _selectedVerses.clear();
      context.read<UserDataProvider>().loadChapterData(
            bible.selectedBook.bookNumber,
            bible.selectedChapter,
          );
    }
  }

  @override
  Widget build(BuildContext context) {
    final bible = context.watch<BibleProvider>();
    final theme = ShadTheme.of(context);
    final hasSelection = _selectedVerses.isNotEmpty;

    if (!bible.isInitialized) {
      return Scaffold(
        appBar: AppBar(title: const Text('Believers Sword')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    if (bible.availableBibles.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: const Text('Believers Sword')),
        body: Center(
          child: Padding(
            padding: const EdgeInsets.all(32),
            child: Text(
              'No Bible modules found.\n\n'
              'Copy .SQLite3 Bible files to the app\'s modules/bible/ directory.',
              textAlign: TextAlign.center,
              style: theme.textTheme.p,
            ),
          ),
        ),
      );
    }

    return Scaffold(
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(kToolbarHeight),
        child: AnimatedSwitcher(
          duration: const Duration(milliseconds: 250),
          switchInCurve: Curves.easeOut,
          switchOutCurve: Curves.easeIn,
          transitionBuilder: (child, animation) {
            return FadeTransition(opacity: animation, child: child);
          },
          child: hasSelection
              ? _buildSelectionAppBar(context, bible, theme)
              : _buildDefaultAppBar(context, bible, theme),
        ),
      ),
      drawer: hasSelection ? null : _buildDrawer(context, theme),
      body: bible.isLoading
          ? const Center(child: CircularProgressIndicator())
          : bible.splitEnabled
              ? Column(
                  children: [
                    // Primary version
                    Expanded(
                      child: VerseList(
                        verses: bible.verses,
                        fontSize: bible.fontSize,
                        selectedVerses: _selectedVerses,
                        onVerseTap: _onVerseTap,
                        syncScrollNotifier: _syncToPrimary,
                        onVerseScroll: (verse) {
                          _syncToSplit.value = verse;
                        },
                      ),
                    ),
                    // Divider handle
                    Container(
                      height: 28,
                      color: theme.colorScheme.muted,
                      child: Row(
                        children: [
                          // Primary version label — tap to change
                          Expanded(
                            child: GestureDetector(
                              behavior: HitTestBehavior.opaque,
                              onTap: () => _showVersionSwitcher(
                                context, isPrimary: true),
                              child: Row(
                                children: [
                                  const SizedBox(width: 12),
                                  Icon(LucideIcons.chevronUp,
                                      size: 12,
                                      color: theme
                                          .colorScheme.mutedForeground),
                                  const SizedBox(width: 4),
                                  Flexible(
                                    child: Text(
                                      bible.selectedVersionShortName,
                                      style: theme.textTheme.muted
                                          .copyWith(fontSize: 11),
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ),
                          Icon(LucideIcons.columns2,
                              size: 14,
                              color: theme.colorScheme.mutedForeground),
                          // Split version label — tap to change
                          Expanded(
                            child: GestureDetector(
                              behavior: HitTestBehavior.opaque,
                              onTap: () => _showVersionSwitcher(
                                context, isPrimary: false),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.end,
                                children: [
                                  Flexible(
                                    child: Text(
                                      bible.splitVersionShortName,
                                      style: theme.textTheme.muted
                                          .copyWith(fontSize: 11),
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ),
                                  const SizedBox(width: 4),
                                  Icon(LucideIcons.chevronDown,
                                      size: 12,
                                      color: theme
                                          .colorScheme.mutedForeground),
                                  const SizedBox(width: 12),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    // Secondary version
                    Expanded(
                      child: VerseList(
                        verses: bible.splitVerses,
                        fontSize: bible.fontSize,
                        selectedVerses: _selectedVerses,
                        onVerseTap: _onVerseTap,
                        persistScroll: false,
                        syncScrollNotifier: _syncToSplit,
                        onVerseScroll: (verse) {
                          _syncToPrimary.value = verse;
                        },
                      ),
                    ),
                  ],
                )
              : VerseList(
                  verses: bible.verses,
                  fontSize: bible.fontSize,
                  selectedVerses: _selectedVerses,
                  onVerseTap: _onVerseTap,
                ),
    );
  }

  PreferredSizeWidget _buildDefaultAppBar(
      BuildContext context, BibleProvider bible, ShadThemeData theme) {
    return AppBar(
      key: const ValueKey('default'),
      leading: Builder(
        builder: (ctx) => ShadIconButton.ghost(
          icon: Icon(LucideIcons.menu,
              size: 20, color: theme.colorScheme.foreground),
          onPressed: () => Scaffold.of(ctx).openDrawer(),
        ),
      ),
      titleSpacing: 0,
      title: Row(
        children: [
          IconButton(
            icon: Icon(LucideIcons.chevronLeft,
                size: 20, color: theme.colorScheme.foreground),
            visualDensity: VisualDensity.compact,
            onPressed: bible.selectedChapter > 1
                ? () {
                    _clearSelection();
                    bible.previousChapter();
                  }
                : null,
          ),
          Flexible(
            child: GestureDetector(
              behavior: HitTestBehavior.opaque,
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (_) => const BookSelectorScreen()),
              ),
              child: Padding(
                padding:
                    const EdgeInsets.symmetric(horizontal: 4, vertical: 12),
                child: Text(
                  '${bible.selectedBook.title} ${bible.selectedChapter}',
                  style: theme.textTheme.small
                      .copyWith(fontWeight: FontWeight.w600),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ),
          ),
          IconButton(
            icon: Icon(LucideIcons.chevronRight,
                size: 20, color: theme.colorScheme.foreground),
            visualDensity: VisualDensity.compact,
            onPressed:
                bible.selectedChapter < bible.selectedBook.chapterCount
                    ? () {
                        _clearSelection();
                        bible.nextChapter();
                      }
                    : null,
          ),
        ],
      ),
      actions: [
        // Version picker — hidden in split mode (shown in split bar)
        if (!bible.splitEnabled)
        GestureDetector(
          behavior: HitTestBehavior.opaque,
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(
                builder: (_) => const VersionSelectorScreen()),
          ),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 12),
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 90),
              child: Row(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Flexible(
                    child: Text(
                      bible.selectedVersionShortName,
                      style: theme.textTheme.muted.copyWith(fontSize: 12),
                      overflow: TextOverflow.ellipsis,
                      maxLines: 1,
                    ),
                  ),
                  const SizedBox(width: 2),
                  Icon(LucideIcons.chevronDown,
                      size: 12, color: theme.colorScheme.mutedForeground),
                ],
              ),
            ),
          ),
        ),
        ShadIconButton.ghost(
          icon: Icon(LucideIcons.search,
              size: 20, color: theme.colorScheme.foreground),
          onPressed: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const SearchScreen()),
          ),
        ),
      ],
    );
  }

  PreferredSizeWidget _buildSelectionAppBar(
      BuildContext context, BibleProvider bible, ShadThemeData theme) {
    final count = _selectedVerses.length;
    final userData = context.read<UserDataProvider>();
    final sortedVerses = _selectedVerses.toList()..sort();
    final verseLabel = sortedVerses.join(', ');

    return AppBar(
      key: const ValueKey('selection'),
      leading: ShadIconButton.ghost(
        icon: const Icon(LucideIcons.x, size: 20),
        onPressed: _clearSelection,
      ),
      title: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '${bible.selectedBook.title} ${bible.selectedChapter}:$verseLabel',
            style: theme.textTheme.small.copyWith(fontWeight: FontWeight.w600),
            overflow: TextOverflow.ellipsis,
          ),
          Text(
            '$count verse${count > 1 ? 's' : ''} selected',
            style: theme.textTheme.muted.copyWith(fontSize: 12),
          ),
        ],
      ),
      actions: [
        PopupMenuButton<String>(
          icon: const Icon(LucideIcons.plus, size: 22),
          onSelected: (value) {
            switch (value) {
              case 'bookmark':
                userData.toggleBookmark(bible.selectedBook.bookNumber,
                    bible.selectedChapter, sortedVerses.first);
                _clearSelection();
              case 'highlight':
                _showHighlightPicker(context, bible, userData, sortedVerses);
              case 'clipnote':
                final v = sortedVerses.first;
                final clipNote = userData.getClipNote(
                    bible.selectedBook.bookNumber, bible.selectedChapter, v);
                _showClipNoteDialog(
                  context,
                  bible,
                  userData,
                  v,
                  clipNote?['content'] as String? ?? '',
                  clipNote?['color'] as String? ?? '#FFD700',
                );
            }
          },
          itemBuilder: (context) => [
            const PopupMenuItem(
              value: 'bookmark',
              child: Row(
                children: [
                  Icon(LucideIcons.bookmark, size: 18),
                  SizedBox(width: 12),
                  Text('Bookmark'),
                ],
              ),
            ),
            if (count == 1)
              const PopupMenuItem(
                value: 'clipnote',
                child: Row(
                  children: [
                    Icon(LucideIcons.stickyNote, size: 18),
                    SizedBox(width: 12),
                    Text('Clip Note'),
                  ],
                ),
              ),
            const PopupMenuItem(
              value: 'highlight',
              child: Row(
                children: [
                  Icon(LucideIcons.highlighter, size: 18),
                  SizedBox(width: 12),
                  Text('Highlight'),
                ],
              ),
            ),
          ],
        ),
        PopupMenuButton<String>(
          icon: const Icon(LucideIcons.ellipsisVertical, size: 22),
          onSelected: (value) {
            final verseTexts = sortedVerses.map((v) {
              final verse = bible.verses.firstWhere((vs) => vs.verse == v);
              return '${verse.verse} ${verse.text.replaceAll(RegExp(r'<[^>]*>'), '').replaceAll('&nbsp;', ' ').replaceAll(RegExp(r'\[\d+\]'), '').trim()}';
            }).join('\n');
            final ref =
                '${bible.selectedBook.title} ${bible.selectedChapter}:${sortedVerses.join(', ')}';
            final fullText = '$verseTexts\n— $ref';

            switch (value) {
              case 'copy':
                Clipboard.setData(ClipboardData(text: fullText));
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Verse copied'),
                    duration: Duration(seconds: 2),
                  ),
                );
                _clearSelection();
              case 'share':
                SharePlus.instance.share(ShareParams(text: fullText));
                _clearSelection();
            }
          },
          itemBuilder: (context) => const [
            PopupMenuItem(
              value: 'copy',
              child: Row(
                children: [
                  Icon(LucideIcons.copy, size: 18),
                  SizedBox(width: 12),
                  Text('Copy verse'),
                ],
              ),
            ),
            PopupMenuItem(
              value: 'share',
              child: Row(
                children: [
                  Icon(LucideIcons.share2, size: 18),
                  SizedBox(width: 12),
                  Text('Share'),
                ],
              ),
            ),
          ],
        ),
      ],
    );
  }

  void _showHighlightPicker(BuildContext context, BibleProvider bible,
      UserDataProvider userData, List<int> verses) {
    const colors = [
      ('Yellow', '#FFEB3B'),
      ('Green', '#A5D6A7'),
      ('Blue', '#90CAF9'),
      ('Pink', '#F48FB1'),
      ('Orange', '#FFCC80'),
    ];

    showShadSheet(
      side: ShadSheetSide.bottom,
      context: context,
      builder: (sheetContext) => ShadSheet(
        title: const Text('Choose Highlight Color'),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 16),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: colors.map((opt) {
              final color =
                  Color(int.parse('FF${opt.$2.substring(1)}', radix: 16));
              return GestureDetector(
                onTap: () {
                  for (final v in verses) {
                    userData.setHighlight(bible.selectedBook.bookNumber,
                        bible.selectedChapter, v, opt.$2);
                  }
                  Navigator.pop(sheetContext);
                  _clearSelection();
                },
                child: Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: color,
                    shape: BoxShape.circle,
                    border: Border.all(
                      color: ShadTheme.of(sheetContext).colorScheme.border,
                    ),
                  ),
                ),
              );
            }).toList(),
          ),
        ),
      ),
    );
  }

  void _showClipNoteDialog(BuildContext context, BibleProvider bible,
      UserDataProvider userData, int verse, String content, String color) {
    final controller = TextEditingController(text: content);
    final bookName = bible.selectedBook.title;
    final chapter = bible.selectedChapter;
    final bookNumber = bible.selectedBook.bookNumber;

    showShadDialog(
      context: context,
      builder: (ctx) {
        String selectedColor = color;
        return StatefulBuilder(
          builder: (ctx, setDialogState) {
            final theme = ShadTheme.of(ctx);
            const clipNoteColors = [
              ('Gold', '#FFD700'),
              ('Yellow', '#FFEB3B'),
              ('Green', '#A5D6A7'),
              ('Blue', '#90CAF9'),
              ('Pink', '#F48FB1'),
              ('Orange', '#FFCC80'),
            ];

            return ShadDialog(
              title: Text('Clip Note — $bookName $chapter:$verse'),
              actions: [
                ShadButton.outline(
                  onPressed: () => Navigator.pop(ctx),
                  child: const Text('Cancel'),
                ),
                ShadButton(
                  onPressed: () {
                    final text = controller.text.trim();
                    if (text.isNotEmpty) {
                      userData.saveClipNote(
                          bookNumber, chapter, verse, text, selectedColor);
                    }
                    Navigator.pop(ctx);
                    _clearSelection();
                  },
                  child: const Text('Save'),
                ),
              ],
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 16),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    ShadInput(
                      controller: controller,
                      placeholder: const Text('Write your note...'),
                      maxLines: 4,
                    ),
                    const SizedBox(height: 16),
                    Text('Color', style: theme.textTheme.small),
                    const SizedBox(height: 8),
                    Row(
                      children: clipNoteColors.map((opt) {
                        final c = Color(int.parse(
                            'FF${opt.$2.substring(1)}',
                            radix: 16));
                        final isSelected = opt.$2 == selectedColor;
                        return GestureDetector(
                          onTap: () =>
                              setDialogState(() => selectedColor = opt.$2),
                          child: Container(
                            width: 36,
                            height: 36,
                            margin: const EdgeInsets.only(right: 8),
                            decoration: BoxDecoration(
                              color: c,
                              shape: BoxShape.circle,
                              border: Border.all(
                                color: isSelected
                                    ? theme.colorScheme.foreground
                                    : theme.colorScheme.border,
                                width: isSelected ? 2.5 : 1,
                              ),
                            ),
                            child: isSelected
                                ? Icon(LucideIcons.check,
                                    size: 16,
                                    color: theme.colorScheme.foreground)
                                : null,
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildDrawer(BuildContext context, ShadThemeData theme) {
    return Drawer(
      child: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 24, 16, 8),
              child: Row(
                children: [
                  SvgPicture.asset(
                    'assets/icon/logo.svg',
                    width: 36,
                    height: 36,
                    colorFilter: ColorFilter.mode(
                      theme.colorScheme.primary,
                      BlendMode.srcIn,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    'Believers Sword',
                    style: theme.textTheme.h4,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Divider(height: 1, color: theme.colorScheme.border),
            const SizedBox(height: 8),
            _drawerItem(
              context,
              icon: LucideIcons.bookmark,
              label: 'Bookmarks',
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context,
                    MaterialPageRoute(builder: (_) => const BookmarksScreen()));
              },
            ),
            _drawerItem(
              context,
              icon: LucideIcons.highlighter,
              label: 'Highlights',
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context,
                    MaterialPageRoute(builder: (_) => const HighlightsScreen()));
              },
            ),
            _drawerItem(
              context,
              icon: LucideIcons.stickyNote,
              label: 'Clip Notes',
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context,
                    MaterialPageRoute(builder: (_) => const ClipNotesScreen()));
              },
            ),
            Divider(height: 1, color: theme.colorScheme.border),
            _drawerItem(
              context,
              icon: LucideIcons.search,
              label: 'Search',
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context,
                    MaterialPageRoute(builder: (_) => const SearchScreen()));
              },
            ),
            _drawerItem(
              context,
              icon: LucideIcons.bookOpen,
              label: 'Bible Versions',
              onTap: () {
                Navigator.pop(context);
                Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (_) => const VersionSelectorScreen()));
              },
            ),
            Divider(height: 1, color: theme.colorScheme.border),
            const SizedBox(height: 8),
            _buildSplitToggle(context, theme),
            const SizedBox(height: 8),
            Divider(height: 1, color: theme.colorScheme.border),
            const SizedBox(height: 8),
            _buildThemeSection(context, theme),
            const SizedBox(height: 8),
            const Spacer(),
            Divider(height: 1, color: theme.colorScheme.border),
            _drawerItem(
              context,
              icon: LucideIcons.user,
              label: 'Account',
              onTap: () {
                Navigator.pop(context);
                Navigator.push(context,
                    MaterialPageRoute(builder: (_) => const LoginScreen()));
              },
            ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }

  Widget _drawerItem(
    BuildContext context, {
    required IconData icon,
    required String label,
    required VoidCallback onTap,
  }) {
    final theme = ShadTheme.of(context);
    return ListTile(
      leading: Icon(icon, size: 20, color: theme.colorScheme.foreground),
      title: Text(label, style: theme.textTheme.small),
      onTap: onTap,
    );
  }

  void _showVersionSwitcher(BuildContext context,
      {required bool isPrimary}) {
    final bible = context.read<BibleProvider>();
    final theme = ShadTheme.of(context);

    // Exclude the version already used in the other pane
    final excludeVersion =
        isPrimary ? bible.splitVersion : bible.selectedVersion;
    final installed = bible.availableBibles
        .where((v) => v != excludeVersion)
        .toList();

    showShadSheet(
      side: ShadSheetSide.bottom,
      context: context,
      builder: (sheetContext) => ShadSheet(
        title: Text(isPrimary ? 'Primary Version' : 'Split Version'),
        child: Material(
          color: Colors.transparent,
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ...installed.map((fileName) {
                  final title = fileName
                      .replaceAll('.SQLite3', '')
                      .replaceAll('.db', '');
                  final current = isPrimary
                      ? bible.selectedVersion
                      : bible.splitVersion;
                  final isSelected = fileName == current;
                  return ListTile(
                    leading: Icon(
                      isSelected
                          ? LucideIcons.circleCheck
                          : LucideIcons.circle,
                      size: 20,
                      color:
                          isSelected ? theme.colorScheme.primary : null,
                    ),
                    title: Text(title),
                    onTap: () {
                      if (isPrimary) {
                        bible.selectVersion(fileName);
                      } else {
                        bible.enableSplit(fileName);
                      }
                      Navigator.pop(sheetContext);
                    },
                  );
                }),
                Divider(
                    height: 1,
                    color:
                        theme.colorScheme.border.withValues(alpha: 0.5)),
                ListTile(
                  leading: Icon(LucideIcons.download,
                      size: 20, color: theme.colorScheme.primary),
                  title: const Text('Download more versions'),
                  onTap: () {
                    Navigator.pop(sheetContext);
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (_) => const VersionSelectorScreen()),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildSplitToggle(BuildContext context, ShadThemeData theme) {
    final bible = context.read<BibleProvider>();
    return _drawerItem(
      context,
      icon: LucideIcons.columns2,
      label: bible.splitEnabled ? 'Split (On)' : 'Split',
      onTap: () {
        Navigator.pop(context);
        WidgetsBinding.instance.addPostFrameCallback((_) {
          if (mounted) _showSplitVersionPicker(this.context);
        });
      },
    );
  }

  void _showSplitVersionPicker(BuildContext context) {
    final bible = context.read<BibleProvider>();
    final theme = ShadTheme.of(context);
    final versions = bible.availableBibles
        .where((v) => v != bible.selectedVersion)
        .toList();

    showShadSheet(
      side: ShadSheetSide.bottom,
      context: context,
      builder: (sheetContext) => ShadSheet(
        title: const Text('Split View'),
        child: Material(
          color: Colors.transparent,
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Disable option
              if (bible.splitEnabled)
                ListTile(
                  leading: Icon(LucideIcons.x,
                      size: 20, color: theme.colorScheme.destructive),
                  title: Text('Disable Split',
                      style: TextStyle(
                          color: theme.colorScheme.destructive)),
                  onTap: () {
                    bible.disableSplit();
                    Navigator.pop(sheetContext);
                  },
                ),
              if (bible.splitEnabled)
                Divider(
                    height: 1,
                    color: theme.colorScheme.border
                        .withValues(alpha: 0.5)),
              if (versions.isEmpty)
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Text(
                    'Download more versions to use split view.',
                    style: theme.textTheme.muted,
                    textAlign: TextAlign.center,
                  ),
                ),
              ...versions.map((fileName) {
                final title = fileName
                    .replaceAll('.SQLite3', '')
                    .replaceAll('.db', '');
                final isCurrentSplit = fileName == bible.splitVersion;
                return ListTile(
                  leading: Icon(
                    isCurrentSplit
                        ? LucideIcons.circleCheck
                        : LucideIcons.circle,
                    size: 20,
                    color: isCurrentSplit ? theme.colorScheme.primary : null,
                  ),
                  title: Text(title),
                  onTap: () {
                    bible.enableSplit(fileName);
                    Navigator.pop(sheetContext);
                  },
                );
              }),
            ],
          ),
        ),
        ),
      ),
    );
  }

  Widget _buildThemeSection(BuildContext context, ShadThemeData theme) {
    final themeProv = context.watch<ThemeProvider>();
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'APPEARANCE',
            style: theme.textTheme.muted.copyWith(
              fontSize: 11,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.1,
            ),
          ),
          const SizedBox(height: 10),
          ShadCard(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Theme mode
                Row(
                  children: [
                    Icon(
                      LucideIcons.sun,
                      size: 16,
                      color: theme.colorScheme.mutedForeground,
                    ),
                    const SizedBox(width: 8),
                    Text(
                      'Theme Mode',
                      style: theme.textTheme.small
                          .copyWith(fontWeight: FontWeight.w500),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                Container(
                  decoration: BoxDecoration(
                    color: theme.colorScheme.muted,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  padding: const EdgeInsets.all(3),
                  child: Row(
                    children: [
                      _themeModeButton(
                        theme: theme,
                        icon: LucideIcons.sun,
                        label: 'Light',
                        selected: themeProv.themeMode == ThemeMode.light,
                        onTap: () =>
                            themeProv.setThemeMode(ThemeMode.light),
                      ),
                      _themeModeButton(
                        theme: theme,
                        icon: LucideIcons.monitor,
                        label: 'Auto',
                        selected: themeProv.themeMode == ThemeMode.system,
                        onTap: () =>
                            themeProv.setThemeMode(ThemeMode.system),
                      ),
                      _themeModeButton(
                        theme: theme,
                        icon: LucideIcons.moon,
                        label: 'Dark',
                        selected: themeProv.themeMode == ThemeMode.dark,
                        onTap: () =>
                            themeProv.setThemeMode(ThemeMode.dark),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 16),
                Divider(
                  height: 1,
                  color: theme.colorScheme.border.withValues(alpha: 0.5),
                ),
                const SizedBox(height: 16),
                // Theme color
                Row(
                  children: [
                    Icon(
                      LucideIcons.palette,
                      size: 16,
                      color: theme.colorScheme.mutedForeground,
                    ),
                    const SizedBox(width: 8),
                    Text(
                      'Theme Color',
                      style: theme.textTheme.small
                          .copyWith(fontWeight: FontWeight.w500),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                ShadSelect<String>(
                  initialValue: themeProv.colorSchemeName,
                  maxHeight: 320,
                  options: _themeColors.map(
                    (name) => ShadOption(
                      value: name,
                      child: Row(
                        children: [
                          _colorDot(name),
                          const SizedBox(width: 8),
                          Text(name[0].toUpperCase() +
                              name.substring(1)),
                        ],
                      ),
                    ),
                  ),
                  selectedOptionBuilder: (context, value) => Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      _colorDot(value),
                      const SizedBox(width: 6),
                      Text(value[0].toUpperCase() +
                          value.substring(1)),
                    ],
                  ),
                  onChanged: (value) {
                    if (value != null) {
                      themeProv.setColorScheme(value);
                    }
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _themeModeButton({
    required ShadThemeData theme,
    required IconData icon,
    required String label,
    required bool selected,
    required VoidCallback onTap,
  }) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 150),
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
          decoration: BoxDecoration(
            color: selected
                ? theme.colorScheme.background
                : Colors.transparent,
            borderRadius: BorderRadius.circular(6),
            boxShadow: selected
                ? [
                    BoxShadow(
                      color: Colors.black.withValues(alpha: 0.06),
                      blurRadius: 4,
                      offset: const Offset(0, 1),
                    ),
                  ]
                : null,
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                icon,
                size: 14,
                color: selected
                    ? theme.colorScheme.foreground
                    : theme.colorScheme.mutedForeground,
              ),
              const SizedBox(height: 2),
              Text(
                label,
                style: theme.textTheme.muted.copyWith(
                  fontSize: 10,
                  fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
                  color: selected
                      ? theme.colorScheme.foreground
                      : theme.colorScheme.mutedForeground,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _colorDot(String name) {
    return Container(
      width: 14,
      height: 14,
      decoration: BoxDecoration(
        color: ShadColorScheme.fromName(name).primary,
        shape: BoxShape.circle,
      ),
    );
  }

  void _showFontSizeSheet(BuildContext context, BibleProvider bible) {
    showShadSheet(
      side: ShadSheetSide.bottom,
      context: context,
      builder: (context) => ShadSheet(
        title: const Text('Font Size'),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 16),
          child: StatefulBuilder(
            builder: (ctx, setState) => ShadSlider(
              initialValue: bible.fontSize,
              min: 12,
              max: 36,
              onChanged: (v) {
                bible.setFontSize(v);
                setState(() {});
              },
            ),
          ),
        ),
      ),
    );
  }
}
