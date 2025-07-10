import 'package:flutter/material.dart';
import 'typing_screen.dart';

class ReviewModeScreen extends StatelessWidget {
  final String userId;

  ReviewModeScreen({required this.userId});

  final categories = {
    'correct': '정답 복습',
    'minor_mistake': '사소한 실수 복습',
    'major_mistake': '큰 실수 복습',
  };

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('복습 유형 선택')),
      body: ListView(
        padding: EdgeInsets.all(20),
        children: categories.entries.map((e) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 8.0),
            child: ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => TypingScreen(mode: e.key, userId: userId),
                  ),
                );
              },
              child: Text(e.value),
            ),
          );
        }).toList(),
      ),
    );
  }
}
