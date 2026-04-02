import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/verse.dart';
import '../providers/user_data_provider.dart';

class VerseActionsSheet extends StatelessWidget {
  final Verse verse;
  final String bookName;
  final bool isBookmarked;
  final bool hasHighlight;
  final bool hasClipNote;
  final String clipNoteContent;

  const VerseActionsSheet({
    super.key,
    required this.verse,
    required this.bookName,
    required this.isBookmarked,
    required this.hasHighlight,
    required this.hasClipNote,
    this.clipNoteContent = '',
  });

  static const List<_HighlightOption> _highlightColors = [
    _HighlightOption('Yellow', '#FFEB3B'),
    _HighlightOption('Green', '#A5D6A7'),
    _HighlightOption('Blue', '#90CAF9'),
    _HighlightOption('Pink', '#F48FB1'),
    _HighlightOption('Orange', '#FFCC80'),
  ];

  @override
  Widget build(BuildContext context) {
    final userData = context.read<UserDataProvider>();

    return SafeArea(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: Text(
                '$bookName ${verse.chapter}:${verse.verse}',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
              ),
            ),
            const Divider(height: 1),

            // Bookmark
            ListTile(
              leading: Icon(
                isBookmarked ? Icons.bookmark : Icons.bookmark_border,
                color: isBookmarked ? Theme.of(context).colorScheme.primary : null,
              ),
              title: Text(isBookmarked ? 'Remove Bookmark' : 'Bookmark'),
              onTap: () {
                userData.toggleBookmark(
                    verse.bookNumber, verse.chapter, verse.verse);
                Navigator.pop(context);
              },
            ),

            // Highlight
            ListTile(
              leading: const Icon(Icons.highlight),
              title: Text(hasHighlight ? 'Change Highlight' : 'Highlight'),
              onTap: () {
                Navigator.pop(context);
                _showHighlightPicker(context, userData);
              },
            ),
            if (hasHighlight)
              ListTile(
                leading: const Icon(Icons.highlight_off),
                title: const Text('Remove Highlight'),
                onTap: () {
                  userData.removeHighlight(
                      verse.bookNumber, verse.chapter, verse.verse);
                  Navigator.pop(context);
                },
              ),

            // Clip Note
            ListTile(
              leading: const Icon(Icons.sticky_note_2_outlined),
              title: Text(hasClipNote ? 'Edit Note' : 'Add Note'),
              onTap: () {
                Navigator.pop(context);
                _showClipNoteDialog(context, userData);
              },
            ),
            if (hasClipNote)
              ListTile(
                leading: const Icon(Icons.delete_outline),
                title: const Text('Remove Note'),
                onTap: () {
                  userData.removeClipNote(
                      verse.bookNumber, verse.chapter, verse.verse);
                  Navigator.pop(context);
                },
              ),
          ],
        ),
      ),
    );
  }

  void _showHighlightPicker(BuildContext context, UserDataProvider userData) {
    showModalBottomSheet(
      context: context,
      builder: (_) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('Choose Highlight Color',
                  style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: _highlightColors.map((opt) {
                  final color = Color(
                      int.parse('FF${opt.hex.substring(1)}', radix: 16));
                  return GestureDetector(
                    onTap: () {
                      userData.setHighlight(
                          verse.bookNumber, verse.chapter, verse.verse, opt.hex);
                      Navigator.pop(context);
                    },
                    child: Container(
                      width: 48,
                      height: 48,
                      decoration: BoxDecoration(
                        color: color,
                        shape: BoxShape.circle,
                        border: Border.all(color: Colors.black26),
                      ),
                    ),
                  );
                }).toList(),
              ),
              const SizedBox(height: 8),
            ],
          ),
        ),
      ),
    );
  }

  void _showClipNoteDialog(BuildContext context, UserDataProvider userData) {
    final controller = TextEditingController(text: clipNoteContent);

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Note — $bookName ${verse.chapter}:${verse.verse}'),
        content: TextField(
          controller: controller,
          maxLines: 4,
          decoration: const InputDecoration(
            hintText: 'Write your note...',
            border: OutlineInputBorder(),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text('Cancel'),
          ),
          FilledButton(
            onPressed: () {
              final text = controller.text.trim();
              if (text.isNotEmpty) {
                userData.saveClipNote(
                    verse.bookNumber, verse.chapter, verse.verse, text, '#FFD700');
              }
              Navigator.pop(ctx);
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }
}

class _HighlightOption {
  final String name;
  final String hex;
  const _HighlightOption(this.name, this.hex);
}
