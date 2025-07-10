//화면 흐름 제어
import 'package:flutter/material.dart';
import '../model/hospital_service.dart';
import '../widgets/step_renderer.dart';

class HospitalKioskScreen extends StatefulWidget {
  @override
  _HospitalKioskScreenState createState() => _HospitalKioskScreenState();
}

class _HospitalKioskScreenState extends State<HospitalKioskScreen> {
  List<dynamic> _steps = [];
  int _currentStepId = 200;

  @override
  void initState() {
    super.initState();
    loadSteps();
  }

  Future<void> loadSteps() async {
    final loadedSteps = await HospitalService.fetchHospitalSteps();
    setState(() {
      _steps = loadedSteps;
    });

    //테스트용
    testStepFlow(loadedSteps, 200);
  }

  void goToStep(int stepId) {
    setState(() {
      _currentStepId = stepId;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_steps.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text("병원 키오스크")),
        body: Center(child: CircularProgressIndicator()),
      );
    }

    final currentStep = _steps.firstWhere(
      (s) => s['step'] == _currentStepId,
      orElse: () => null,
    );

    // ✅ currentStep이 null이면 에러 방지
    if (currentStep == null) {
      return Scaffold(
        appBar: AppBar(title: Text("병원 키오스크")),
        body: Center(child: Text("단계를 찾을 수 없습니다.")),
      );
    }

    // ✅ type이 '종료'이면 자동 종료 다이얼로그 표시
    if (currentStep['type'] == '종료') {
      WidgetsBinding.instance.addPostFrameCallback((_) {
        showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: Text("이용 종료"),
            content: Text("이용해 주셔서 감사합니다."),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop(); // 다이얼로그 닫기
                  Navigator.of(context).pop(); // 홈으로
                },
                child: Text("확인"),
              ),
            ],
          ),
        );
      });
    }

    return Scaffold(
      appBar: AppBar(
        title: Text('병원 키오스크'),
        actions: [
          IconButton(
            icon: Icon(Icons.home),
            onPressed: () {
              showDialog(
                context: context,
                builder: (_) => AlertDialog(
                  title: Text("홈으로 돌아가시겠습니까?"),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.of(context).pop(),
                      child: Text("취소"),
                    ),
                    TextButton(
                      onPressed: () {
                        Navigator.of(context).pop(); // 다이얼로그 닫기
                        Navigator.of(context).pop(); // 홈으로 이동
                      },
                      child: Text("확인"),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
      body: StepRenderer(stepData: currentStep, onNext: goToStep),
    );
  }
}
