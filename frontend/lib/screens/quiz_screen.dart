import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:math';
import 'package:flutter/services.dart' show rootBundle;

import '/model/security_quiz.dart';

class QuizScreen extends StatefulWidget {
  const QuizScreen({super.key});

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  List<SecurityQuiz> _quizzes = [];
  List<SecurityHint> _hints = [];

  int _currentIndex = 0;
  int? _selectedIndex;
  bool _showExplanation = false;
  List<int> _wrongAnswers = [];

  // ✅ 피드백 멘트용 리스트
  List<String> correctFeedback = [];
  List<String> almostFeedback = [];
  List<String> wrongFeedback = [];

  @override
  void initState() {
    super.initState();
    loadQuizData();
  }

  Future<void> loadQuizData() async {
    try {
      final quizJson = await rootBundle.loadString(
        'assets/data/4. 50 Security Quiz Questions - Base.json',
      );
      final hintJson = await rootBundle.loadString(
        'assets/data/4-0. Security_Education_Quiz_Help_Tips.json',
      );
      final feedbackJson = await rootBundle.loadString(
        'assets/data/4-0. Security_Quiz_Feedback_Messages.json',
      );

      final quizList = json.decode(quizJson) as List;
      final hintList = json.decode(hintJson) as List;

      final feedbackMap = json.decode(feedbackJson) as Map<String, dynamic>;
      final feedbackGroups =
          feedbackMap['security_quiz_feedback'] as Map<String, dynamic>;

      correctFeedback = List<String>.from(feedbackGroups['correct'] ?? []);
      almostFeedback = List<String>.from(
        feedbackGroups['almost_correct'] ?? [],
      );
      wrongFeedback = List<String>.from(feedbackGroups['wrong'] ?? []);

      setState(() {
        _quizzes = quizList.map((e) => SecurityQuiz.fromJson(e)).toList();
        _hints = hintList.map((e) => SecurityHint.fromJson(e)).toList();
      });
    } catch (e) {
      print('❌ 로딩 중 오류 발생: $e');
    }
  }

  void checkAnswer() {
    final correctIndex = _quizzes[_currentIndex].answerIndex;

    setState(() {
      _showExplanation = true;
      if (_selectedIndex != correctIndex) {
        _wrongAnswers.add(_currentIndex);
      }
    });
  }

  void nextQuestion() {
    if (_currentIndex < _quizzes.length - 1) {
      setState(() {
        _currentIndex++;
        _selectedIndex = null;
        _showExplanation = false;
      });
    } else {
      showResultDialog();
    }
  }

  void showResultDialog() {
    int correctCount = _quizzes.length - _wrongAnswers.length;
    double scoreRatio = correctCount / _quizzes.length;

    String message;
    if (scoreRatio >= 0.9) {
      message = correctFeedback[Random().nextInt(correctFeedback.length)];
    } else if (scoreRatio >= 0.6) {
      message = almostFeedback[Random().nextInt(almostFeedback.length)];
    } else {
      message = wrongFeedback[Random().nextInt(wrongFeedback.length)];
    }

    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('퀴즈 완료!'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('총 ${_quizzes.length}문제 중 $correctCount문제 맞춤!'),
            const SizedBox(height: 12),
            Text(message),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              setState(() {
                _currentIndex = 0;
                _selectedIndex = null;
                _showExplanation = false;
                _wrongAnswers.clear();
              });
            },
            child: const Text('전체 다시 풀기'),
          ),
          if (_wrongAnswers.isNotEmpty)
            TextButton(
              onPressed: () {
                Navigator.of(context).pop();
                setState(() {
                  // 오답 문제만 다시 풀기
                  _quizzes = _wrongAnswers
                      .map((index) => _quizzes[index])
                      .toList();
                  _currentIndex = 0;
                  _selectedIndex = null;
                  _showExplanation = false;
                  _wrongAnswers.clear();
                });
              },
              child: const Text('오답만 다시 풀기'),
            ),
        ],
      ),
    );
  }

  String? getHintForCurrentQuestion() {
    final stepId = '4-${_currentIndex + 1}';
    final hint = _hints.firstWhere(
      (h) => h.step == stepId,
      orElse: () => SecurityHint(step: '', helperMessage: ''),
    );
    return hint.helperMessage.isNotEmpty ? hint.helperMessage : null;
  }

  @override
  Widget build(BuildContext context) {
    if (_quizzes.isEmpty) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    final quiz = _quizzes[_currentIndex];

    return Scaffold(
      appBar: AppBar(title: const Text('보안 퀴즈')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(
              '진행률: ${_currentIndex + 1} / ${_quizzes.length}',
              style: TextStyle(fontSize: 16),
            ),

            Text(
              'Q${_currentIndex + 1}. ${quiz.question}',
              style: const TextStyle(fontSize: 18),
            ),
            const SizedBox(height: 12),
            if (getHintForCurrentQuestion() != null)
              Text(
                '💡 힌트: ${getHintForCurrentQuestion()!}',
                style: const TextStyle(fontSize: 14, color: Colors.grey),
              ),
            const SizedBox(height: 12),
            ...List.generate(quiz.options.length, (index) {
              return RadioListTile<int>(
                value: index,
                groupValue: _selectedIndex,
                onChanged: _showExplanation
                    ? null
                    : (val) => setState(() => _selectedIndex = val),
                title: Text(quiz.options[index]),
              );
            }),
            const SizedBox(height: 12),
            if (_showExplanation)
              Column(
                children: [
                  Text(
                    _selectedIndex == quiz.answerIndex ? '✅ 정답입니다!' : '❌ 틀렸어요!',
                    style: TextStyle(
                      fontSize: 16,
                      color: _selectedIndex == quiz.answerIndex
                          ? Colors.green
                          : Colors.red,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '해설: ${quiz.explanation}',
                    style: const TextStyle(color: Colors.black87),
                  ),
                ],
              ),
            const Spacer(),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                ElevatedButton(
                  onPressed: _selectedIndex != null && !_showExplanation
                      ? checkAnswer
                      : null,
                  child: const Text('제출'),
                ),
                ElevatedButton(
                  onPressed: _showExplanation ? nextQuestion : null,
                  child: const Text('다음'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
