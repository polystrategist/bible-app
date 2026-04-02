import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../providers/bible_provider.dart';
import '../providers/user_data_provider.dart';
import '../widgets/verse_list.dart';
import 'book_selector_screen.dart';
import 'bookmarks_screen.dart';
import 'highlights_screen.dart';
import 'login_screen.dart';
import 'clip_notes_screen.dart';
import 'search_screen.dart';
import 'version_selector_screen.dart';

class ReaderScreen extends StatefulWidget {
  const ReaderScreen({super.key});

  @override
  State<ReaderScreen> createState() => _ReaderScreenState();
}

class _ReaderScreenState extends State<ReaderScreen> {
  int? _lastBook;
  int? _lastChapter;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final bible = context.watch<BibleProvider>();
    if (bible.selectedBook.bookNumber != _lastBook ||
        bible.selectedChapter != _lastChapter) {
      _lastBook = bible.selectedBook.bookNumber;
      _lastChapter = bible.selectedChapter;
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
      appBar: AppBar(
        leading: Builder(
          builder: (ctx) => ShadIconButton.ghost(
            icon: const Icon(LucideIcons.menu, size: 20),
            onPressed: () => Scaffold.of(ctx).openDrawer(),
          ),
        ),
        title: GestureDetector(
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const VersionSelectorScreen()),
          ),
          child: Text(
            bible.selectedVersionTitle,
            style: theme.textTheme.small,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        actions: [
          ShadIconButton.ghost(
            icon: const Icon(LucideIcons.search, size: 20),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const SearchScreen()),
            ),
          ),
          ShadIconButton.ghost(
            icon: const Icon(LucideIcons.aLargeSmall, size: 20),
            onPressed: () => _showFontSizeSheet(context, bible),
          ),
          ShadIconButton.ghost(
            icon: const Icon(LucideIcons.user, size: 20),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const LoginScreen()),
            ),
          ),
        ],
      ),
      drawer: _buildDrawer(context, theme),
      body: Column(
        children: [
          // Navigation bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
            decoration: BoxDecoration(
              color: theme.colorScheme.muted,
              border: Border(
                bottom: BorderSide(color: theme.colorScheme.border, width: 1),
              ),
            ),
            child: Row(
              children: [
                ShadIconButton.ghost(
                  icon: const Icon(LucideIcons.chevronLeft, size: 20),
                  onPressed: bible.selectedChapter > 1
                      ? () => bible.previousChapter()
                      : null,
                ),
                Expanded(
                  child: Center(
                    child: ShadButton.ghost(
                      onPressed: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => const BookSelectorScreen(),
                        ),
                      ),
                      child: Text(
                        '${bible.selectedBook.title}  ${bible.selectedChapter}',
                        style: theme.textTheme.small.copyWith(
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                  ),
                ),
                ShadIconButton.ghost(
                  icon: const Icon(LucideIcons.chevronRight, size: 20),
                  onPressed:
                      bible.selectedChapter < bible.selectedBook.chapterCount
                          ? () => bible.nextChapter()
                          : null,
                ),
              ],
            ),
          ),
          // Verses
          Expanded(
            child: bible.isLoading
                ? const Center(child: CircularProgressIndicator())
                : VerseList(
                    verses: bible.verses,
                    fontSize: bible.fontSize,
                  ),
          ),
        ],
      ),
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
              child: Text(
                'Believers Sword',
                style: theme.textTheme.h4,
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Text(
                'Bible Study App',
                style: theme.textTheme.muted,
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
