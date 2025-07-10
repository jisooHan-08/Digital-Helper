import 'dart:convert';
import 'dart:io';

void main() async {
  final file = File('assat/data/hospital_kiosk.json'); // 파일명 확인해서 수정
  final jsonString = await file.readAsString();
  final List<dynamic> rawData = json.decode(jsonString);

  final List<dynamic> steps = rawData[0]['steps'];

  final stepMap = <int, Map<String, dynamic>>{};
  final referencedSteps = <int>{};

  for (var step in steps) {
    final stepId = step['step'];
    stepMap[stepId] = step;

    final next = step['next'];
    if (next is Map) {
      for (var v in next.values) {
        if (v is int) {
          referencedSteps.add(v);
        }
      }
    } else if (next is int) {
      referencedSteps.add(next);
    }

    final nextStep = step['next_step'];
    if (nextStep is int) {
      referencedSteps.add(nextStep);
    }
  }

  print('=== 병원 키오스크 Step 연결 테스트 시작 ===');
  for (var refStep in referencedSteps) {
    if (!stepMap.containsKey(refStep)) {
      print('❌ step $refStep 이(가) JSON에 없음');
    }
  }
  print('=== 테스트 종료 ===');
}
