import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../providers/bible_provider.dart';

class VersionSelectorScreen extends StatelessWidget {
  const VersionSelectorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final bible = context.watch<BibleProvider>();
    final theme = ShadTheme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Select Version')),
      body: bible.availableBibles.isEmpty
          ? Center(
              child: Text(
                'No Bible modules found',
                style: theme.textTheme.muted,
              ),
            )
          : ListView.builder(
              itemCount: bible.availableBibles.length,
              itemBuilder: (context, index) {
                final version = bible.availableBibles[index];
                final title = version
                    .replaceAll('.SQLite3', '')
                    .replaceAll('.db', '');
                final isSelected = version == bible.selectedVersion;

                return ListTile(
                  title: Text(title),
                  leading: Icon(
                    isSelected ? LucideIcons.circleCheck : LucideIcons.circle,
                    color: isSelected ? theme.colorScheme.primary : null,
                  ),
                  onTap: () {
                    bible.selectVersion(version);
                    Navigator.pop(context);
                  },
                );
              },
            ),
    );
  }
}
