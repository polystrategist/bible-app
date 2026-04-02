import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bible_provider.dart';
import '../providers/user_data_provider.dart';
import '../widgets/verse_list.dart';
import 'book_selector_screen.dart';
import 'chapter_selector_screen.dart';
import 'login_screen.dart';
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
      // Load user data (bookmarks, highlights, notes) for this chapter
      context.read<UserDataProvider>().loadChapterData(
            bible.selectedBook.bookNumber,
            bible.selectedChapter,
          );
    }
  }

  @override
  Widget build(BuildContext context) {
    final bible = context.watch<BibleProvider>();
    final theme = Theme.of(context);

    if (bible.availableBibles.isEmpty && !bible.isLoading) {
      return Scaffold(
        appBar: AppBar(title: const Text('Believers Sword')),
        body: const Center(
          child: Padding(
            padding: EdgeInsets.all(32),
            child: Text(
              'No Bible modules found.\n\n'
              'Copy .SQLite3 Bible files to the app\'s modules/bible/ directory.',
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 16),
            ),
          ),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: GestureDetector(
          onTap: () => Navigator.push(
            context,
            MaterialPageRoute(builder: (_) => const VersionSelectorScreen()),
          ),
          child: Text(
            bible.selectedVersionTitle,
            style: const TextStyle(fontSize: 14),
            overflow: TextOverflow.ellipsis,
          ),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.search),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const SearchScreen()),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.text_fields),
            onPressed: () => _showFontSizeSlider(context, bible),
          ),
          IconButton(
            icon: const Icon(Icons.person_outline),
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const LoginScreen()),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          // Navigation bar
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            color: theme.colorScheme.surfaceContainerHighest,
            child: Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.chevron_left),
                  onPressed: bible.selectedChapter > 1
                      ? () => bible.previousChapter()
                      : null,
                ),
                Expanded(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      TextButton(
                        onPressed: () => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const BookSelectorScreen(),
                          ),
                        ),
                        child: Text(
                          bible.selectedBook.title,
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                      ),
                      TextButton(
                        onPressed: () => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const ChapterSelectorScreen(),
                          ),
                        ),
                        child: Text(
                          '${bible.selectedChapter}',
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 16,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.chevron_right),
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

  void _showFontSizeSlider(BuildContext context, BibleProvider bible) {
    showModalBottomSheet(
      context: context,
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Font Size', style: TextStyle(fontWeight: FontWeight.bold)),
            StatefulBuilder(
              builder: (ctx, setState) => Slider(
                value: bible.fontSize,
                min: 12,
                max: 36,
                divisions: 24,
                label: bible.fontSize.round().toString(),
                onChanged: (v) {
                  bible.setFontSize(v);
                  setState(() {});
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
