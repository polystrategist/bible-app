import 'package:flutter_test/flutter_test.dart';
import 'package:believers_sword_mobile/main.dart';

void main() {
  testWidgets('App starts', (WidgetTester tester) async {
    await tester.pumpWidget(const BelieversWordApp());
  });
}
