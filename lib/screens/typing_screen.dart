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

  @override
  void initState() {
    super.initState();
    loadJsonFiles();
  }

  Future<void> loadJsonFiles() async {
    final List<String> assetPaths = [
      'assets/data/2-1. 50 One-letter Words.json',
      'assets/data/2-2. 50 Two-letter Words.json',
      'assets/data/2-3. 50 Three-letter Words.json',
      'assets/data/2-4. 30 One-sentence Practices.json',
      'assets/data/2-5. 30 Paragraph Practices.json',
      'assets/data/2-0. Typing_Practice_Help_Tips.json',
    ];

    List<TypingPracticeItem> items = [];

    for (final path in assetPaths) {
      try {
        final jsonStr = await rootBundle.loadString(path);
        final List<dynamic> jsonList = json.decode(jsonStr);
        items.addAll(jsonList.map((e) => TypingPracticeItem.fromJson(e)));
        print("✅ 로딩 성공: $path");
      } catch (e) {
        print("❌ JSON 로딩 실패: $path - 오류: $e");
      }
    }

    setState(() {
      allItems = items;
      isLoading = false;
      print("총 로딩된 문제 수: ${allItems.length}");
    });
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
    final targetText = allItems[currentIndex].text;
    if (userInput == targetText) {
      setState(() {
        resultText = "정답입니다!";
      });
    } else {
      setState(() {
        resultText = "틀렸습니다!";
        wrongAttempts[targetText] = (wrongAttempts[targetText] ?? 0) + 1;
        wrongHistory.add(targetText);
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
          content: Text(
            "🎉 모든 단계를 마쳤어요! 정말 잘하셨어요! 🎉",
            style: TextStyle(fontSize: 16),
          ),
          backgroundColor: Colors.green,
          duration: Duration(seconds: 3),
          behavior: SnackBarBehavior.floating,
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

  void showWrongHistoryDialog() {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text("오답 다시보기"),
        content: SizedBox(
          width: double.maxFinite,
          child: ListView(children: wrongHistory.map((e) => Text(e)).toList()),
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
    if (isLoading) {
      return Scaffold(
        appBar: AppBar(title: Text('타자 연습')),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (isLoading || allItems.isEmpty || currentIndex >= allItems.length) {
      return Scaffold(
        appBar: AppBar(title: Text('타자 연습')),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final targetText = allItems[currentIndex].text;

    return Scaffold(
      appBar: AppBar(title: Text('타자 연습')),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                "연습 문장:",
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
              if (targetText.length <= 3) ...[
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
              ElevatedButton(onPressed: goToNextStep, child: Text("다음 단계로 이동")),
              SizedBox(height: 12),
              ElevatedButton(
                onPressed: showWrongHistoryDialog,
                child: Text("오답 다시 보기"),
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
