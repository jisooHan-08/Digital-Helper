// typing_mode_screen.dart
import 'package:flutter/material.dart';
import '../screens/typing_screen.dart';

class TypingPracticeModeScreen extends StatelessWidget {
  final Map<String, String> modes = {
    'one-letter': '한 글자 연습',
    'two-letter': '두 글자 연습',
    'three-letter': '세 글자 연습',
    'sentence': '한 문장 연습',
    'paragraph': '한 문단 연습',
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('타자 연습 모드 선택')),
      body: ListView(
        padding: EdgeInsets.all(20),
        children: modes.entries.map((entry) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0),
            child: ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => TypingScreen(mode: entry.key),
                  ),
                );
              },
              child: Text(entry.value),
            ),
          );
        }).toList(),
      ),
    );
  }
}
