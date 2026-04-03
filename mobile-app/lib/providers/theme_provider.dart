import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ThemeProvider extends ChangeNotifier {
  static const _keyThemeMode = 'theme_mode';
  static const _keyColorScheme = 'color_scheme';

  ThemeMode _themeMode = ThemeMode.system;
  String _colorSchemeName = 'slate';

  ThemeMode get themeMode => _themeMode;
  String get colorSchemeName => _colorSchemeName;

  Future<void> init() async {
    final prefs = await SharedPreferences.getInstance();

    final modeIndex = prefs.getInt(_keyThemeMode) ?? ThemeMode.system.index;
    _themeMode = ThemeMode.values[modeIndex];

    _colorSchemeName = prefs.getString(_keyColorScheme) ?? 'slate';

    notifyListeners();
  }

  Future<void> setThemeMode(ThemeMode mode) async {
    _themeMode = mode;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_keyThemeMode, mode.index);
  }

  Future<void> setColorScheme(String name) async {
    _colorSchemeName = name;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyColorScheme, name);
  }
}
