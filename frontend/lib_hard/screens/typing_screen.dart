import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class TypingPracticeItem {
  final String text;
  final String type;
  final String? hint;
  final List<String>? typingOrder;

  TypingPracticeItem({
    required this.text,
    required this.type,
    this.hint,
    this.typingOrder,
  });

  factory TypingPracticeItem.fromJson(Map<String, dynamic> json) {
    return TypingPracticeItem(
      text:
          json['text'] ??
          json['word'] ??
          json['sentence'] ??
          json['ui']?['text'] ??
          '',
      type: json['type'] ?? 'sentence',
      hint: json['ui']?['helper_message'],
      typingOrder: json['typing_order'] != null
          ? List<String>.from(json['typing_order'])
          : null,
    );
  }
}

class TypingScreen extends StatefulWidget {
  final String mode;

  TypingScreen({required this.mode});

  @override
  _TypingScreenState createState() => _TypingScreenState();
}

class _TypingScreenState extends State<TypingScreen> {
  List<TypingPracticeItem> allItems = [];
  bool isLoading = true;

  final TextEditingController controller = TextEditingController();
  String resultText = "";
  int currentIndex = 0;
  String userInput = "";
  Map<String, int> wrongAttempts = {};
  List<String> wrongHistory = [];

  // ✅ 오답 복습 관련 상태
  bool isReviewMode = false;
  int reviewIndex = 0;

  @override
  void initState() {
    super.initState();
    loadJsonFiles();
  }

  Future<void> loadJsonFiles() async {
    final Map<String, String> modeToFile = {
      'one-letter': 'assets/data/2-1. 50 One-letter Words.json',
      'two-letter': 'assets/data/2-2. 50 Two-letter Words.json',
      'three-letter': 'assets/data/2-3. 50 Three-letter Words.json',
      'sentence': 'assets/data/2-4. 30 One-sentence Practices.json',
      'paragraph': 'assets/data/2-5. 30 Paragraph Practices.json',
    };

    final selectedFile = modeToFile[widget.mode];

    if (selectedFile == null) {
      print('❌ 유효하지 않은 모드: ${widget.mode}');
      return;
    }

    try {
      final jsonStr = await rootBundle.loadString(selectedFile);
      final List<dynamic> jsonList = json.decode(jsonStr);
      final List<TypingPracticeItem> items = jsonList
          .map((e) => TypingPracticeItem.fromJson(e))
          .toList();

      setState(() {
        allItems = items;
        isLoading = false;
        currentIndex = 0;
      });

      print("✅ 로딩 성공: $selectedFile - ${items.length}개 항목");
    } catch (e) {
      print("❌ JSON 로딩 실패: $selectedFile - 오류: $e");
    }
  }

  void onTextChanged(String value) {
    setState(() {
      userInput = value;
    });
  }

  List<TextSpan> buildComparisonText(String target, String input) {
    List<TextSpan> spans = [];

    for (int i = 0; i < target.length; i++) {
      String char = target[i];

      if (i >= input.length) {
        spans.add(
          TextSpan(
            text: char,
            style: TextStyle(color: Colors.grey),
          ),
        );
      } else if (input[i] == char) {
        spans.add(
          TextSpan(
            text: char,
            style: TextStyle(color: Colors.green),
          ),
        );
      } else {
        spans.add(
          TextSpan(
            text: char,
            style: TextStyle(color: Colors.red),
          ),
        );
      }
    }
    return spans;
  }

  void checkInput() {
    final targetText = isReviewMode
        ? wrongHistory[reviewIndex]
        : allItems[currentIndex].text;

    if (userInput == targetText) {
      setState(() {
        resultText = "정답입니다!";
      });

      Future.delayed(Duration(milliseconds: 800), () {
        setState(() {
          userInput = '';
          resultText = '';
          controller.clear();

          if (isReviewMode) {
            if (reviewIndex < wrongHistory.length - 1) {
              reviewIndex++;
            } else {
              isReviewMode = false;
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text("🎉 오답 복습을 완료했습니다!"),
                  backgroundColor: Colors.green,
                ),
              );
            }
          }
        });
      });
    } else {
      setState(() {
        resultText = "틀렸습니다!";
        if (!isReviewMode) {
          wrongAttempts[targetText] = (wrongAttempts[targetText] ?? 0) + 1;
          wrongHistory.add(targetText);
        }
      });
    }
  }

  void goToNextStep() {
    if (currentIndex < allItems.length - 1) {
      setState(() {
        currentIndex++;
        userInput = '';
        resultText = '';
        controller.clear();
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("🎉 모든 단계를 마쳤어요! 정말 잘하셨어요! 🎉"),
          backgroundColor: Colors.green,
          duration: Duration(seconds: 3),
        ),
      );
    }
  }

  Widget buildTypingOrder(TypingPracticeItem item) {
    if (item.typingOrder == null || item.typingOrder!.isEmpty) {
      return Text("입력 순서 없음", style: TextStyle(color: Colors.grey));
    }
    return Text("입력 순서: ${item.typingOrder!.join(' → ')}");
  }

  void showWrongSortedDialog() {
    final sorted = wrongAttempts.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text("자주 틀린 순"),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: sorted
              .map((e) => Text("${e.key} - ${e.value}회 틀림"))
              .toList(),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text("닫기"),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading ||
        (!isReviewMode &&
            (allItems.isEmpty || currentIndex >= allItems.length))) {
      return Scaffold(
        appBar: AppBar(title: Text('타자 연습')),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final targetText = isReviewMode
        ? wrongHistory[reviewIndex]
        : allItems[currentIndex].text;

    return Scaffold(
      appBar: AppBar(title: Text('타자 연습')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                isReviewMode ? "오답 복습 중..." : "연습 문장:",
                style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 8),
              Text(
                targetText,
                style: TextStyle(fontSize: 28, color: Colors.blueAccent),
              ),
              SizedBox(height: 20),
              TextField(
                controller: controller,
                onChanged: onTextChanged,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: '입력하세요',
                ),
                onSubmitted: (_) => checkInput(),
              ),
              SizedBox(height: 20),
              if (targetText.length <= 3 && !isReviewMode) ...[
                Text(
                  "입력 순서:",
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                SizedBox(height: 8),
                buildTypingOrder(allItems[currentIndex]),
              ],
              SizedBox(height: 30),
              Text(
                "비교 결과:",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 10),
              RichText(
                text: TextSpan(
                  style: DefaultTextStyle.of(
                    context,
                  ).style.copyWith(fontSize: 20),
                  children: buildComparisonText(targetText, userInput),
                ),
              ),
              SizedBox(height: 20),
              ElevatedButton(onPressed: checkInput, child: Text("결과 확인")),
              SizedBox(height: 20),
              Text(
                resultText,
                style: TextStyle(fontSize: 20, color: Colors.red),
              ),
              SizedBox(height: 20),
              if (!isReviewMode)
                ElevatedButton(
                  onPressed: goToNextStep,
                  child: Text("다음 단계로 이동"),
                ),
              SizedBox(height: 12),
              if (!isReviewMode)
                ElevatedButton(
                  onPressed: () {
                    if (wrongHistory.isEmpty) {
                      ScaffoldMessenger.of(
                        context,
                      ).showSnackBar(SnackBar(content: Text("오답이 없습니다.")));
                      return;
                    }
                    setState(() {
                      isReviewMode = true;
                      reviewIndex = 0;
                      userInput = '';
                      resultText = '';
                      controller.clear();
                    });
                  },
                  child: Text("오답 다시 풀기"),
                ),
              SizedBox(height: 8),
              ElevatedButton(
                onPressed: showWrongSortedDialog,
                child: Text("틀린 순 정렬 보기"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
