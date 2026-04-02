import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/auth_provider.dart';
import 'providers/bible_provider.dart';
import 'providers/user_data_provider.dart';
import 'services/store_service.dart';
import 'screens/reader_screen.dart';

void main() {
  runApp(const BelieversWordApp());
}

class BelieversWordApp extends StatelessWidget {
  const BelieversWordApp({super.key});

  @override
  Widget build(BuildContext context) {
    final storeService = StoreService();

    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => BibleProvider()..init()),
        ChangeNotifierProvider(create: (_) => UserDataProvider()),
        ChangeNotifierProvider(create: (_) => AuthProvider(storeService)..init()),
      ],
      child: MaterialApp(
        title: 'Believers Sword',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFFFC4201),
          ),
          useMaterial3: true,
        ),
        darkTheme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFFFC4201),
            brightness: Brightness.dark,
          ),
          useMaterial3: true,
        ),
        home: const ReaderScreen(),
      ),
    );
  }
}
