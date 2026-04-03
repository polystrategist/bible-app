import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import '../providers/bible_provider.dart';
import '../services/bible_service.dart';

class VersionSelectorScreen extends StatefulWidget {
  const VersionSelectorScreen({super.key});

  @override
  State<VersionSelectorScreen> createState() => _VersionSelectorScreenState();
}

class _VersionSelectorScreenState extends State<VersionSelectorScreen> {
  final TextEditingController _searchController = TextEditingController();
  final ShadTabsController<String> _tabController =
      ShadTabsController(value: 'installed');
  String _searchQuery = '';

  @override
  void initState() {
    super.initState();
    _searchController.addListener(() {
      setState(() => _searchQuery = _searchController.text.toLowerCase());
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = ShadTheme.of(context);

    return Scaffold(
      appBar: AppBar(title: const Text('Bible Versions')),
      body: ShadTabs<String>(
        controller: _tabController,
        tabs: [
          ShadTab(
            value: 'installed',
            content: _InstalledTab(theme: theme),
            child: const Text('Installed'),
          ),
          ShadTab(
            value: 'download',
            content: SizedBox(
              height: MediaQuery.of(context).size.height - 200,
              child: _DownloadTab(
                theme: theme,
                searchController: _searchController,
                searchQuery: _searchQuery,
              ),
            ),
            child: const Text('Download'),
          ),
        ],
      ),
    );
  }
}

// ---------------------------------------------------------------------------
// Installed tab
// ---------------------------------------------------------------------------

class _InstalledTab extends StatelessWidget {
  const _InstalledTab({required this.theme});

  final ShadThemeData theme;

  @override
  Widget build(BuildContext context) {
    final bible = context.watch<BibleProvider>();
    final installed = bible.availableBibles;

    if (installed.isEmpty) {
      return Padding(
        padding: const EdgeInsets.all(32),
        child: Center(
          child: Text('No Bible modules found', style: theme.textTheme.muted),
        ),
      );
    }

    return Column(
      children: installed.map((fileName) {
        final title =
            fileName.replaceAll('.SQLite3', '').replaceAll('.db', '');
        final isSelected = fileName == bible.selectedVersion;
        final isBundled = BibleService.bundledModules.contains(fileName);

        return ListTile(
          key: ValueKey(fileName),
          leading: Icon(
            isSelected ? LucideIcons.circleCheck : LucideIcons.circle,
            color: isSelected ? theme.colorScheme.primary : null,
            size: 20,
          ),
          title: Text(
            title,
            style: isSelected
                ? TextStyle(
                    fontWeight: FontWeight.w600,
                    color: theme.colorScheme.primary,
                  )
                : null,
          ),
          trailing: !isBundled
              ? IconButton(
                  icon: Icon(
                    LucideIcons.trash2,
                    size: 18,
                    color: theme.colorScheme.destructive,
                  ),
                  tooltip: 'Remove',
                  onPressed: () =>
                      _confirmDelete(context, bible, fileName, title),
                )
              : null,
          onTap: () {
            bible.selectVersion(fileName);
            Navigator.pop(context);
          },
        );
      }).toList(),
    );
  }

  Future<void> _confirmDelete(
    BuildContext context,
    BibleProvider bible,
    String fileName,
    String title,
  ) async {
    final confirmed = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Remove version'),
        content: Text('Remove "$title" from your device?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx, false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Remove'),
          ),
        ],
      ),
    );

    if (confirmed == true && context.mounted) {
      try {
        await bible.deleteVersion(fileName);
      } catch (e) {
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Failed to remove version: $e')),
          );
        }
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Download tab
// ---------------------------------------------------------------------------

class _DownloadTab extends StatelessWidget {
  const _DownloadTab({
    required this.theme,
    required this.searchController,
    required this.searchQuery,
  });

  final ShadThemeData theme;
  final TextEditingController searchController;
  final String searchQuery;

  @override
  Widget build(BuildContext context) {
    final bible = context.watch<BibleProvider>();

    final modules = bible.downloadableModules.where((m) {
      if (searchQuery.isEmpty) return true;
      final title = (m['title'] as String? ?? '').toLowerCase();
      final short = bible.shortNameForModule(m).toLowerCase();
      return title.contains(searchQuery) || short.contains(searchQuery);
    }).toList();

    return Column(
      children: [
        // Search field
        Padding(
          padding: const EdgeInsets.fromLTRB(12, 12, 12, 8),
          child: ShadInput(
            controller: searchController,
            placeholder: const Text('Search versions...'),
            leading: const Padding(
              padding: EdgeInsets.only(right: 8),
              child: Icon(LucideIcons.search, size: 16),
            ),
            trailing: searchQuery.isNotEmpty
                ? GestureDetector(
                    onTap: searchController.clear,
                    child: const Icon(LucideIcons.x, size: 16),
                  )
                : null,
          ),
        ),

        // List
        Expanded(
          child: modules.isEmpty
              ? Center(
                  child: Text(
                    searchQuery.isEmpty
                        ? 'All versions are installed'
                        : 'No results for "$searchQuery"',
                    style: theme.textTheme.muted,
                    textAlign: TextAlign.center,
                  ),
                )
              : ListView.builder(
                  itemCount: modules.length,
                  itemBuilder: (context, index) {
                    final module = modules[index];
                    final fileName = module['file_name'] as String? ?? '';
                    final title = module['title'] as String? ?? fileName;
                    final shortName = bible.shortNameForModule(module);
                    final isThisDownloading =
                        bible.downloadingFileName == fileName;
                    final isAlreadyInstalled = bible.isInstalled(fileName);

                    return Column(
                      key: ValueKey(fileName),
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        ListTile(
                          title: Text(title),
                          subtitle: shortName.isNotEmpty
                              ? Text(shortName,
                                  style: theme.textTheme.muted)
                              : null,
                          trailing: _buildTrailing(
                            context,
                            bible,
                            module,
                            title,
                            isAlreadyInstalled,
                            isThisDownloading,
                          ),
                        ),
                        if (isThisDownloading)
                          Padding(
                            padding:
                                const EdgeInsets.symmetric(horizontal: 16),
                            child: LinearProgressIndicator(
                              value: bible.downloadProgress > 0
                                  ? bible.downloadProgress
                                  : null,
                              minHeight: 2,
                              backgroundColor: theme.colorScheme.primary
                                  .withValues(alpha: 0.15),
                              valueColor: AlwaysStoppedAnimation<Color>(
                                theme.colorScheme.primary,
                              ),
                            ),
                          ),
                      ],
                    );
                  },
                ),
        ),
      ],
    );
  }

  Widget _buildTrailing(
    BuildContext context,
    BibleProvider bible,
    Map<String, dynamic> module,
    String title,
    bool isAlreadyInstalled,
    bool isThisDownloading,
  ) {
    if (isAlreadyInstalled) {
      return Icon(
        LucideIcons.circleCheck,
        color: theme.colorScheme.primary,
        size: 20,
      );
    }

    if (isThisDownloading) {
      return SizedBox(
        width: 20,
        height: 20,
        child: CircularProgressIndicator(
          strokeWidth: 2,
          value: bible.downloadProgress > 0 ? bible.downloadProgress : null,
          color: theme.colorScheme.primary,
        ),
      );
    }

    final canDownload = !bible.isDownloading;
    return IconButton(
      icon: Icon(
        LucideIcons.download,
        size: 20,
        color:
            canDownload ? theme.colorScheme.primary : theme.colorScheme.muted,
      ),
      tooltip: 'Download',
      onPressed: canDownload
          ? () => _startDownload(context, bible, module, title)
          : null,
    );
  }

  Future<void> _startDownload(
    BuildContext context,
    BibleProvider bible,
    Map<String, dynamic> module,
    String title,
  ) async {
    try {
      await bible.downloadVersion(module);
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('"$title" downloaded successfully')),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Download failed: $e')),
        );
      }
    }
  }
}
