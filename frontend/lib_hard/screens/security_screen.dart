import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;

class PhishingCase {
  final int caseId;
  final String title;
  final String description;
  final String phishingType;
  final List<String> redFlags;
  final String preventiveTip;
  final String level;

  PhishingCase({
    required this.caseId,
    required this.title,
    required this.description,
    required this.phishingType,
    required this.redFlags,
    required this.preventiveTip,
    required this.level,
  });

  factory PhishingCase.fromJson(Map<String, dynamic> json) {
    return PhishingCase(
      caseId: json['case_id'],
      title: json['title'],
      description: json['description'],
      phishingType: json['phishing_type'],
      redFlags: List<String>.from(json['red_flags']),
      preventiveTip: json['preventive_tip'],
      level: json['level'],
    );
  }
}

class SecurityScreen extends StatefulWidget {
  @override
  _SecurityScreenState createState() => _SecurityScreenState();
}

class _SecurityScreenState extends State<SecurityScreen> {
  late Future<List<PhishingCase>> _casesFuture;
  List<int> _completedIds = [];

  @override
  void initState() {
    super.initState();
    _casesFuture = loadPhishingCases();
  }

  Future<List<PhishingCase>> loadPhishingCases() async {
    final String jsonString = await rootBundle.loadString(
      'assets/data/3. Security Education - Phishing Examples.json',
    );
    final List<dynamic> jsonData = json.decode(jsonString);
    return jsonData.map((e) => PhishingCase.fromJson(e)).toList();
  }

  Color getLevelColor(String level) {
    switch (level.toLowerCase()) {
      case 'high':
        return Colors.red;
      case 'medium':
        return Colors.orange;
      case 'low':
        return Colors.green;
      default:
        return Colors.black;
    }
  }

  void _navigateToDetail(int index, List<PhishingCase> cases) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => PhishingDetailScreen(
          phishingCase: cases[index],
          onNext: index < cases.length - 1
              ? () => _navigateToDetail(index + 1, cases)
              : null,
          onComplete: () {
            setState(() {
              _completedIds.add(cases[index].caseId);
            });
          },
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('보안 교육 사례')),
      body: FutureBuilder<List<PhishingCase>>(
        future: _casesFuture,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            final cases = snapshot.data!;
            return ListView.builder(
              itemCount: cases.length,
              itemBuilder: (context, index) {
                final item = cases[index];
                final isCompleted = _completedIds.contains(item.caseId);
                return ListTile(
                  title: Text(item.title),
                  subtitle: Text(item.phishingType),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        item.level.toUpperCase(),
                        style: TextStyle(
                          color: getLevelColor(item.level),
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (isCompleted)
                        Padding(
                          padding: const EdgeInsets.only(left: 8.0),
                          child: Icon(Icons.check_circle, color: Colors.green),
                        ),
                    ],
                  ),
                  onTap: () => _navigateToDetail(index, cases),
                );
              },
            );
          } else if (snapshot.hasError) {
            return Center(child: Text('불러오는 중 오류 발생'));
          } else {
            return Center(child: CircularProgressIndicator());
          }
        },
      ),
    );
  }
}

class PhishingDetailScreen extends StatefulWidget {
  final PhishingCase phishingCase;
  final VoidCallback? onNext;
  final VoidCallback onComplete;

  PhishingDetailScreen({
    required this.phishingCase,
    this.onNext,
    required this.onComplete,
  });

  @override
  State<PhishingDetailScreen> createState() => _PhishingDetailScreenState();
}

class _PhishingDetailScreenState extends State<PhishingDetailScreen> {
  bool _completed = false;

  void _showSnackBar() {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text('🎉 교육을 완료하셨습니다! 잘하셨어요!')));
    setState(() {
      _completed = true;
    });
    widget.onComplete(); // 완료 리스트에 추가
  }

  void _showAlertDialog() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('⚠️ 피싱 경고'),
        content: Text('이 링크는 위험할 수 있습니다. 절대 클릭하지 마세요!'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: Text('확인')),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final caseData = widget.phishingCase;

    return Scaffold(
      appBar: AppBar(title: Text(caseData.title)),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Card(
          elevation: 4,
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Text(caseData.description, style: TextStyle(fontSize: 16)),
              SizedBox(height: 16),
              Text("📌 피싱 유형: ${caseData.phishingType}"),
              Text("🚨 위험도: ${caseData.level.toUpperCase()}"),
              SizedBox(height: 16),
              Text("🚩 위험 신호", style: TextStyle(fontWeight: FontWeight.bold)),
              ...caseData.redFlags.map((e) => Text("- $e")),
              SizedBox(height: 16),
              Text("✅ 예방 방법", style: TextStyle(fontWeight: FontWeight.bold)),
              Text(caseData.preventiveTip),
              SizedBox(height: 24),
              GestureDetector(
                onTap: _showAlertDialog,
                child: Text(
                  '📎 링크 시뮬레이션 클릭하기',
                  style: TextStyle(
                    color: Colors.blue,
                    decoration: TextDecoration.underline,
                  ),
                ),
              ),
              SizedBox(height: 24),
              if (!_completed)
                ElevatedButton(
                  onPressed: _showSnackBar,
                  child: Text("이 사례 학습 완료"),
                ),
              if (_completed && widget.onNext != null)
                ElevatedButton(
                  onPressed: widget.onNext,
                  child: Text("➡ 다음 학습하기"),
                ),
              if (_completed && widget.onNext == null)
                Text(
                  "🎊 모든 사례 학습을 완료했습니다!",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
              SizedBox(height: 24),

              // ✅ 학습 종료 버튼
              OutlinedButton(
                onPressed: () {
                  Navigator.popUntil(
                    context,
                    (route) => route.settings.name == 'SecurityScreen',
                  );
                },
                child: Text("📚 학습 종료하기"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
