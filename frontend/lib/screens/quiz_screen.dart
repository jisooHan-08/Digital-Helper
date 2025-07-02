import 'package:flutter/material.dart';

class QuizScreen extends StatefulWidget {
  @override
  _QuizScreenState createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  String _selectedAnswer = '';
  bool _submitted = false;

  final String question = '택배 문자에 있는 링크는 모두 안전할까?';
  final List<String> options = ['O', 'X'];
  final String correctAnswer = 'X';
  final String explanation = '출처를 모르면 절대 누르지 마세요!';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('보안 퀴즈')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(question, style: TextStyle(fontSize: 18)),
            ...options.map(
              (opt) => RadioListTile(
                title: Text(opt),
                value: opt,
                groupValue: _selectedAnswer,
                onChanged: (value) {
                  if (!_submitted) {
                    setState(() {
                      _selectedAnswer = value!;
                    });
                  }
                },
              ),
            ),
            ElevatedButton(
              child: Text('제출'),
              onPressed: _submitted || _selectedAnswer == ''
                  ? null
                  : () {
                      setState(() {
                        _submitted = true;
                      });
                    },
            ),
            if (_submitted)
              Column(
                children: [
                  Text(
                    _selectedAnswer == correctAnswer
                        ? '정답입니다! 👍'
                        : '틀렸어요 😢 정답은 $correctAnswer',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  SizedBox(height: 8),
                  Text('해설: $explanation'),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
