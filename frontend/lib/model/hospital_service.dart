// API 통신
import 'dart:convert';
import 'package:http/http.dart' as http;

class HospitalService {
  static Future<List<dynamic>> fetchHospitalSteps() async {
    final response = await http.get(
      Uri.parse('http://127.0.0.1:8000/hospital_kiosk/db_steps'),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data is Map && data['steps'] is List) {
        final stepsList = data['steps'];
        if (stepsList.isNotEmpty && stepsList[0]['scenario_data'] is List) {
          return stepsList[0]['scenario_data'];
        } else {
          throw Exception('scenario_data가 없음');
        }
      } else {
        throw Exception('steps가 리스트가 아님');
      }
    } else {
      throw Exception('데이터 로딩 실패: ${response.statusCode}');
    }
  }

  static Future<void> uploadMistake(int step, String selected) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:8000/hospital_kiosk/mistake-upload'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'step': step, 'wrong_answer': selected}),
    );

    if (response.statusCode != 200) {
      throw Exception('오답 업로드 실패');
    }
  }
}

//테스트용
void testStepFlow(List<dynamic> steps, int startStep) {
  Map<int, dynamic> stepMap = {for (var step in steps) step['step']: step};

  int current = startStep;
  Set<int> visited = {};

  print("=== 병원 키오스크 Step 연결 테스트 시작 ===");
  while (true) {
    if (visited.contains(current)) {
      print("🔁 순환 감지: $current");
      break;
    }

    visited.add(current);
    final currentStep = stepMap[current];

    if (currentStep == null) {
      print("❌ step $current 이(가) JSON에 없음");
      break;
    }

    print("✅ step $current → ${currentStep['type'] ?? '알 수 없음'}");

    final next = currentStep['next'];
    if (next == null || next is! Map || next.isEmpty) {
      print("⚠️ step $current 에 연결된 next 없음 → 종료");
      break;
    }

    final nextLabel = next.keys.first;
    final nextStepId = next[nextLabel];

    print("➡️ '$nextLabel' 선택 시 → step $nextStepId");

    current = nextStepId;
  }

  print("=== 테스트 종료 ===");
}

//테스트용

// ✅ 백엔드에서 JSON 받아오기
// ✅ 반환 타입은 List<dynamic> → 각 step이 map 구조로 들어있음
// 오답 업로드용 서비스 함수 추가
