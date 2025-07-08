import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class QuizScreen extends StatefulWidget {
  const QuizScreen({Key? key}) : super(key: key);

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  int currentQuizId = 1;
  String question = '';
  List<String> choices = [];
  String correctAnswer = '';
  String explanation = '';
  String? selectedAnswer;
  bool isAnswerSubmitted = false;

  @override
  void initState() {
    super.initState();
    loadQuizDataFromAPI();
  }

  Future<void> loadQuizDataFromAPI() async {
    try {
      final response = await http.get(
        Uri.parse(
          'http://localhost:8000/security_quiz/question?quiz_id=$currentQuizId',
        ),
      );

      if (response.statusCode == 200) {
        final Map<String, dynamic> json = jsonDecode(response.body);
        if (json["status"] == "ok") {
          setState(() {
            question = json["question"];
            choices = List<String>.from(json["choices"]);
            correctAnswer = json["answer"];
            explanation = json["explanation"];
            selectedAnswer = null;
            isAnswerSubmitted = false;
          });
        } else if (json["status"] == "end") {
          setState(() {
            question = "퀴즈가 종료되었습니다.";
            choices = [];
            correctAnswer = '';
            explanation = '';
          });
        }
      } else {
        throw Exception("서버 오류");
      }
    } catch (e) {
      print('퀴즈 로딩 실패: $e');
    }
  }

  void submitAnswer(String choice) {
    setState(() {
      selectedAnswer = choice;
      isAnswerSubmitted = true;
    });
  }

  void goToNextQuiz() {
    setState(() {
      currentQuizId += 1;
    });
    loadQuizDataFromAPI();
  }

  Widget buildChoiceButton(String choice) {
    final isCorrect = choice == correctAnswer;
    final isSelected = choice == selectedAnswer;

    Color getColor() {
      if (!isAnswerSubmitted) return Colors.blue;
      if (isSelected && isCorrect) return Colors.green;
      if (isSelected && !isCorrect) return Colors.red;
      return Colors.grey;
    }

    return ElevatedButton(
      style: ElevatedButton.styleFrom(backgroundColor: getColor()),
      onPressed: isAnswerSubmitted ? null : () => submitAnswer(choice),
      child: Text(choice),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('보안 퀴즈')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: question.isEmpty
            ? const Center(child: CircularProgressIndicator())
            : Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Q$currentQuizId. $question',
                    style: const TextStyle(fontSize: 20),
                  ),
                  const SizedBox(height: 20),
                  ...choices.map(buildChoiceButton).toList(),
                  const SizedBox(height: 30),
                  if (isAnswerSubmitted)
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          selectedAnswer == correctAnswer
                              ? "정답입니다!"
                              : "오답입니다  정답: $correctAnswer",
                          style: TextStyle(
                            fontSize: 18,
                            color: selectedAnswer == correctAnswer
                                ? Colors.green
                                : Colors.red,
                          ),
                        ),
                        const SizedBox(height: 10),
                        Text(
                          '해설: $explanation',
                          style: const TextStyle(fontSize: 16),
                        ),
                        const SizedBox(height: 20),
                        ElevatedButton(
                          onPressed: goToNextQuiz,
                          child: const Text('다음 문제'),
                        ),
                      ],
                    ),
                ],
              ),
      ),
    );
  }
}
