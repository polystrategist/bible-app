import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../models/verse.dart';
import '../providers/user_data_provider.dart';

class VerseActionsSheet extends StatelessWidget {
  final Verse verse;
  final String bookName;
  final bool isBookmarked;
  final bool hasHighlight;
  final bool hasClipNote;
  final String clipNoteContent;
  final String clipNoteColor;

  const VerseActionsSheet({
    super.key,
    required this.verse,
    required this.bookName,
    required this.isBookmarked,
    required this.hasHighlight,
    required this.hasClipNote,
    this.clipNoteContent = '',
    this.clipNoteColor = '#FFD700',
  });

  static const List<_ColorOption> _highlightColors = [
    _ColorOption('Yellow', '#FFEB3B'),
    _ColorOption('Green', '#A5D6A7'),
    _ColorOption('Blue', '#90CAF9'),
    _ColorOption('Pink', '#F48FB1'),
    _ColorOption('Orange', '#FFCC80'),
  ];

  static const List<_ColorOption> _clipNoteColors = [
    _ColorOption('Gold', '#FFD700'),
    _ColorOption('Yellow', '#FFEB3B'),
    _ColorOption('Green', '#A5D6A7'),
    _ColorOption('Blue', '#90CAF9'),
    _ColorOption('Pink', '#F48FB1'),
    _ColorOption('Orange', '#FFCC80'),
  ];

  @override
  Widget build(BuildContext context) {
    final userData = context.read<UserDataProvider>();
    final theme = ShadTheme.of(context);

    return ShadSheet(
      title: Text('$bookName ${verse.chapter}:${verse.verse}'),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 8),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Bookmark
            ShadButton.ghost(
              leading: Icon(
                isBookmarked ? LucideIcons.bookmarkMinus : LucideIcons.bookmark,
                size: 18,
                color: isBookmarked ? theme.colorScheme.primary : null,
              ),
              onPressed: () {
                userData.toggleBookmark(
                    verse.bookNumber, verse.chapter, verse.verse);
                Navigator.pop(context);
              },
              child: Text(isBookmarked ? 'Remove Bookmark' : 'Bookmark'),
            ),

            // Highlight
            ShadButton.ghost(
              leading: const Icon(LucideIcons.highlighter, size: 18),
              onPressed: () {
                Navigator.pop(context);
                _showHighlightPicker(context, userData);
              },
              child: Text(hasHighlight ? 'Change Highlight' : 'Highlight'),
            ),
            if (hasHighlight)
              ShadButton.ghost(
                leading: const Icon(LucideIcons.paintbrushVertical, size: 18),
                onPressed: () {
                  userData.removeHighlight(
                      verse.bookNumber, verse.chapter, verse.verse);
                  Navigator.pop(context);
                },
                child: const Text('Remove Highlight'),
              ),

            // Clip Note
            ShadButton.ghost(
              leading: const Icon(LucideIcons.stickyNote, size: 18),
              onPressed: () {
                Navigator.pop(context);
                _showClipNoteDialog(context, userData);
              },
              child: Text(hasClipNote ? 'Edit Clip Note' : 'Add Clip Note'),
            ),
            if (hasClipNote)
              ShadButton.ghost(
                leading: Icon(LucideIcons.trash2,
                    size: 18, color: theme.colorScheme.destructive),
                onPressed: () {
                  userData.removeClipNote(
                      verse.bookNumber, verse.chapter, verse.verse);
                  Navigator.pop(context);
                },
                child: Text(
                  'Remove Clip Note',
                  style: TextStyle(color: theme.colorScheme.destructive),
                ),
              ),
          ],
        ),
      ),
    );
  }

  void _showHighlightPicker(BuildContext context, UserDataProvider userData) {
    showShadSheet(
      side: ShadSheetSide.bottom,
      context: context,
      builder: (sheetContext) => ShadSheet(
        title: const Text('Choose Highlight Color'),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 16),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: _highlightColors.map((opt) {
              final color = _hexToColor(opt.hex);
              return GestureDetector(
                onTap: () {
                  userData.setHighlight(
                      verse.bookNumber, verse.chapter, verse.verse, opt.hex);
                  Navigator.pop(sheetContext);
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

  void _showClipNoteDialog(BuildContext context, UserDataProvider userData) {
    final controller = TextEditingController(text: clipNoteContent);

    showShadDialog(
      context: context,
      builder: (ctx) => _ClipNoteDialog(
        title: '$bookName ${verse.chapter}:${verse.verse}',
        controller: controller,
        initialColor: clipNoteColor,
        colors: _clipNoteColors,
        onSave: (text, color) {
          if (text.isNotEmpty) {
            userData.saveClipNote(
                verse.bookNumber, verse.chapter, verse.verse, text, color);
          }
          Navigator.pop(ctx);
        },
        onCancel: () => Navigator.pop(ctx),
      ),
    );
  }

  static Color _hexToColor(String hex) {
    return Color(int.parse('FF${hex.substring(1)}', radix: 16));
  }
}

class _ClipNoteDialog extends StatefulWidget {
  final String title;
  final TextEditingController controller;
  final String initialColor;
  final List<_ColorOption> colors;
  final void Function(String text, String color) onSave;
  final VoidCallback onCancel;

  const _ClipNoteDialog({
    required this.title,
    required this.controller,
    required this.initialColor,
    required this.colors,
    required this.onSave,
    required this.onCancel,
  });

  @override
  State<_ClipNoteDialog> createState() => _ClipNoteDialogState();
}

class _ClipNoteDialogState extends State<_ClipNoteDialog> {
  late String _selectedColor;

  @override
  void initState() {
    super.initState();
    _selectedColor = widget.initialColor;
  }

  Color _hexToColor(String hex) {
    return Color(int.parse('FF${hex.substring(1)}', radix: 16));
  }

  @override
  Widget build(BuildContext context) {
    final theme = ShadTheme.of(context);

    return ShadDialog(
      title: Text('Clip Note — ${widget.title}'),
      actions: [
        ShadButton.outline(
          onPressed: widget.onCancel,
          child: const Text('Cancel'),
        ),
        ShadButton(
          onPressed: () =>
              widget.onSave(widget.controller.text.trim(), _selectedColor),
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
              controller: widget.controller,
              placeholder: const Text('Write your note...'),
              maxLines: 4,
            ),
            const SizedBox(height: 16),
            Text('Color', style: theme.textTheme.small),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: widget.colors.map((opt) {
                final color = _hexToColor(opt.hex);
                final isSelected = opt.hex == _selectedColor;
                return GestureDetector(
                  onTap: () => setState(() => _selectedColor = opt.hex),
                  child: Container(
                    width: 36,
                    height: 36,
                    margin: const EdgeInsets.only(right: 8),
                    decoration: BoxDecoration(
                      color: color,
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
                            size: 16, color: theme.colorScheme.foreground)
                        : null,
                  ),
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}

class _ColorOption {
  final String name;
  final String hex;
  const _ColorOption(this.name, this.hex);
}
