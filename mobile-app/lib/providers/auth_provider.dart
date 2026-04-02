import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../services/store_service.dart';
import '../services/sync_service.dart';

class AuthProvider extends ChangeNotifier {
  final StoreService _store;
  late final SyncService _syncService;

  String? _token;
  Map<String, dynamic>? _user;
  bool _isAuthenticated = false;
  bool _syncEnabled = false;

  String get apiBaseUrl => const String.fromEnvironment(
        'API_BASE_URL',
        defaultValue: 'http://10.0.2.2', // Android emulator localhost
      );

  String? get token => _token;
  Map<String, dynamic>? get user => _user;
  bool get isAuthenticated => _isAuthenticated;
  bool get syncEnabled => _syncEnabled;

  AuthProvider(this._store) {
    _syncService = SyncService(_store, apiBaseUrl: apiBaseUrl);
  }

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();
    _token = prefs.getString('auth_token');
    if (_token != null) {
      _isAuthenticated = true;
      await getUser();
      final syncVal = await _store.getSyncSetting('sync_enabled');
      _syncEnabled = syncVal == '1';
      if (_syncEnabled) {
        _syncService.startPeriodicSync(_token!);
      }
    }
    notifyListeners();
  }

  Future<Map<String, dynamic>> login(String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse('$apiBaseUrl/api/auth/login'),
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode == 200 && data['status'] == 'success') {
        _token = data['token'];
        _user = data['user'];
        _isAuthenticated = true;
        _syncEnabled = data['user']['sync_enabled'] == true;

        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('auth_token', _token!);

        if (_syncEnabled) {
          await _store.setSyncSetting('sync_enabled', '1');
          _syncService.startPeriodicSync(_token!);
        }

        notifyListeners();
        return {'success': true, 'message': data['message'] ?? 'Login successful'};
      }

      return {'success': false, 'message': data['message'] ?? 'Login failed'};
    } catch (e) {
      return {'success': false, 'message': e.toString()};
    }
  }

  Future<Map<String, dynamic>> register(
      String name, String email, String password, String passwordConfirmation) async {
    try {
      final response = await http.post(
        Uri.parse('$apiBaseUrl/api/auth/register'),
        headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
        body: jsonEncode({
          'name': name,
          'email': email,
          'password': password,
          'password_confirmation': passwordConfirmation,
        }),
      );

      final data = jsonDecode(response.body);

      if (response.statusCode == 200 && data['status'] == 'success') {
        _token = data['token'];
        _user = data['user'];
        _isAuthenticated = true;

        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('auth_token', _token!);

        notifyListeners();
        return {'success': true, 'message': data['message'] ?? 'Registration successful'};
      }

      return {'success': false, 'message': data['message'] ?? 'Registration failed'};
    } catch (e) {
      return {'success': false, 'message': e.toString()};
    }
  }

  Future<void> logout() async {
    if (_token != null) {
      try {
        await http.post(
          Uri.parse('$apiBaseUrl/api/auth/logout'),
          headers: {
            'Authorization': 'Bearer $_token',
            'Accept': 'application/json',
          },
        );
      } catch (_) {}
    }

    _syncService.stopPeriodicSync();
    _token = null;
    _user = null;
    _isAuthenticated = false;
    _syncEnabled = false;

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('auth_token');

    notifyListeners();
  }

  Future<void> getUser() async {
    if (_token == null) return;
    try {
      final response = await http.get(
        Uri.parse('$apiBaseUrl/api/auth/user'),
        headers: {
          'Authorization': 'Bearer $_token',
          'Accept': 'application/json',
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['status'] == 'success') {
          _user = data['user'];
          _syncEnabled = data['user']['sync_enabled'] == true;
          notifyListeners();
        }
      } else if (response.statusCode == 401) {
        await logout();
      }
    } catch (_) {
      // Offline — keep existing state
    }
  }

  Future<void> setSyncEnabled(bool enabled) async {
    _syncEnabled = enabled;
    await _store.setSyncSetting('sync_enabled', enabled ? '1' : '0');

    if (enabled && _token != null) {
      _syncService.startPeriodicSync(_token!);
    } else {
      _syncService.stopPeriodicSync();
    }

    // Push preference to server
    if (_token != null) {
      try {
        await http.patch(
          Uri.parse('$apiBaseUrl/api/auth/preferences'),
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer $_token',
            'Accept': 'application/json',
          },
          body: jsonEncode({'sync_enabled': enabled}),
        );
      } catch (_) {}
    }

    notifyListeners();
  }

  void triggerSync() {
    if (_syncEnabled && _token != null) {
      _syncService.runSync(_token!);
    }
  }
}
