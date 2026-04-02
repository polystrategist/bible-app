import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'store_service.dart';

class SyncService {
  final StoreService _store;
  final String apiBaseUrl;
  bool _isSyncing = false;
  Timer? _syncTimer;

  SyncService(this._store, {required this.apiBaseUrl});

  /// Run a full sync cycle: push local changes, then pull remote changes.
  Future<void> runSync(String token) async {
    if (_isSyncing) return;
    _isSyncing = true;

    try {
      await _pushSync(token);
      await _pullSync(token);
    } catch (e) {
      // Silently fail — user is probably offline
    } finally {
      _isSyncing = false;
    }
  }

  Future<void> _pushSync(String token) async {
    final unsynced = await _store.getUnsyncedChanges();
    if (unsynced.isEmpty) return;

    final payload = unsynced.map((entry) {
      final entryPayload = entry['payload'];
      return {
        'table_name': entry['table_name'],
        'record_key': entry['record_key'],
        'action': entry['action'],
        'payload': entryPayload is String ? jsonDecode(entryPayload) : entryPayload,
        'timestamp': entry['created_at'],
      };
    }).toList();

    final response = await http.post(
      Uri.parse('$apiBaseUrl/api/sync'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
        'Accept': 'application/json',
      },
      body: jsonEncode({'sync_logs': payload}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      if (data['status'] == 'success') {
        final ids = unsynced.map((e) => e['id'] as int).toList();
        await _store.markAsSynced(ids);
      }
    }
  }

  Future<void> _pullSync(String token) async {
    final lastTimestamp = await _store.getLastSyncTimestamp();

    final response = await http.get(
      Uri.parse('$apiBaseUrl/api/sync/pull?since=$lastTimestamp'),
      headers: {
        'Authorization': 'Bearer $token',
        'Accept': 'application/json',
      },
    );

    if (response.statusCode != 200) return;

    final data = jsonDecode(response.body);
    if (data['status'] != 'success') return;

    await _store.applyPullData(data);

    if (data['last_sync_timestamp'] != null) {
      await _store.updateLastSyncTimestamp(data['last_sync_timestamp'].toString());
    }
  }

  void startPeriodicSync(String token, {Duration interval = const Duration(minutes: 5)}) {
    stopPeriodicSync();
    runSync(token);
    _syncTimer = Timer.periodic(interval, (_) => runSync(token));
  }

  void stopPeriodicSync() {
    _syncTimer?.cancel();
    _syncTimer = null;
  }
}
