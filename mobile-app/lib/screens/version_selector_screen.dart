import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/bible_provider.dart';

class VersionSelectorScreen extends StatelessWidget {
  const VersionSelectorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final bible = context.watch<BibleProvider>();

    return Scaffold(
      appBar: AppBar(title: const Text('Select Version')),
      body: bible.availableBibles.isEmpty
          ? const Center(child: Text('No Bible modules found'))
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
                    isSelected ? Icons.check_circle : Icons.circle_outlined,
                    color: isSelected
                        ? Theme.of(context).colorScheme.primary
                        : null,
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
