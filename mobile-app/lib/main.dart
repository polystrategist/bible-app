import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:provider/provider.dart';
import 'package:shadcn_ui/shadcn_ui.dart';

import 'providers/auth_provider.dart';
import 'providers/bible_provider.dart';
import 'providers/theme_provider.dart';
import 'providers/user_data_provider.dart';
import 'screens/reader_screen.dart';
import 'services/store_service.dart';

void main() {
  final storeService = StoreService();
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => BibleProvider()..init()),
        ChangeNotifierProvider(create: (_) => AuthProvider(storeService)..init()),
        ChangeNotifierProvider(create: (_) => UserDataProvider()),
        ChangeNotifierProvider(create: (_) => ThemeProvider()..init()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    final themeProv = context.watch<ThemeProvider>();
    return ShadApp.custom(
      themeMode: themeProv.themeMode,
      theme: ShadThemeData(
        brightness: Brightness.light,
        colorScheme: ShadColorScheme.fromName(themeProv.colorSchemeName),
      ),
      darkTheme: ShadThemeData(
        brightness: Brightness.dark,
        colorScheme: ShadColorScheme.fromName(
          themeProv.colorSchemeName,
          brightness: Brightness.dark,
        ),
      ),
      appBuilder: (context) {
        return MaterialApp(
          title: 'Believers Sword',
          debugShowCheckedModeBanner: false,
          theme: Theme.of(context),
          localizationsDelegates: const [
            GlobalShadLocalizations.delegate,
            GlobalMaterialLocalizations.delegate,
            GlobalCupertinoLocalizations.delegate,
            GlobalWidgetsLocalizations.delegate,
          ],
          builder: (context, child) {
            return ShadAppBuilder(child: child!);
          },
          home: const ReaderScreen(),
        );
      },
    );
  }
}
