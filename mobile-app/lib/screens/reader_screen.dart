import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

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
