// 병원 키오스크 step별 UI 렌더링
import 'package:flutter/material.dart';
import '../model/hospital_service.dart';

class StepRenderer extends StatefulWidget {
  final Map<String, dynamic> stepData;
  final Function(int) onNext;

  const StepRenderer({required this.stepData, required this.onNext});

  @override
  State<StepRenderer> createState() => _StepRendererState();
}

class _StepRendererState extends State<StepRenderer> {
  final TextEditingController _textController = TextEditingController();
  bool _checkboxChecked = false;

  @override
  void initState() {
    super.initState();

    final ui = widget.stepData['ui'] ?? {};
    final options = [
      ...(ui['options'] is List ? ui['options'] : []),
      ...(ui['buttons'] is List ? ui['buttons'] : []),
    ];
    final nextStep = widget.stepData['next_step'];

    // 자동 이동: 버튼/옵션 없고 next_step 있으면 3초 후 자동 이동
    if (options.isEmpty && nextStep != null) {
      Future.delayed(Duration(seconds: 3), () {
        widget.onNext(nextStep);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final ui = widget.stepData['ui'] ?? {};
    final validation = widget.stepData['validation'] ?? {};
    final helper = widget.stepData['helper_message'] ?? '';
    final options = [
      ...(ui['options'] is List ? ui['options'] : []),
      ...(ui['buttons'] is List ? ui['buttons'] : []),
    ];

    void handleNext(dynamic labelOrButton) async {
      if (validation['checkbox'] == true && !_checkboxChecked) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text("체크박스를 먼저 체크해주세요.")));
        return;
      }

      final answer = widget.stepData['answer'];
      if (answer != null) {
        final selected = labelOrButton is String
            ? labelOrButton
            : labelOrButton['label'] ?? labelOrButton['button_text'];

        if (selected != answer) {
          try {
            await HospitalService.uploadMistake(
              widget.stepData['step'],
              selected,
            );
          } catch (e) {
            print("오답 업로드 실패: $e");
          }

          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text("틀렸습니다. 다시 시도하세요.")));
          return;
        }
      }

      final checkboxLabel = ui['checkbox'];
      final label = labelOrButton is String
          ? labelOrButton
          : labelOrButton['label'] ?? labelOrButton['button_text'];

      dynamic nextStep;
      if (_checkboxChecked && checkboxLabel != null) {
        nextStep = widget.stepData['next']?[checkboxLabel];
      }
      nextStep ??= widget.stepData['next']?[label];
      nextStep ??= widget.stepData['next_step'];

      print("👉 클릭한 버튼: $label");
      print("🔎 nextMap: ${widget.stepData['next']}");
      print("➡️ 이동할 nextStep: $nextStep");

      if (nextStep == null) {
        await showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: Text("미션 완료 🎊"),
            content: Text("축하합니다! 미션을 모두 완료했어요."),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                  Navigator.of(context).pop();
                },
                child: Text("확인"),
              ),
            ],
          ),
        );
        return;
      }

      widget.onNext(nextStep);
    }

    return SingleChildScrollView(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (ui['text'] != null)
            Text(ui['text'], style: TextStyle(fontSize: 18)),
          if (ui['text_input'] != null)
            TextField(
              controller: _textController,
              decoration: InputDecoration(labelText: ui['text_input']),
            ),
          if (ui['checkbox'] != null)
            Row(
              children: [
                Checkbox(
                  value: _checkboxChecked,
                  onChanged: (v) =>
                      setState(() => _checkboxChecked = v ?? false),
                ),
                Expanded(child: Text(ui['checkbox'])),
              ],
            ),
          if (ui['image'] != null) Image.asset(ui['image']),
          if (ui['images'] != null && ui['images'] is List)
            ...List.generate(ui['images'].length, (i) {
              final img = ui['images'][i];
              final path = img is String ? img : img['image'];
              return Column(
                children: [
                  Image.asset(path),
                  if (img is Map && img['message'] != null)
                    Text(img['message']),
                ],
              );
            }),
          if (ui['info'] != null && ui['info'] is Map) ...[
            Text(
              "접수 정보",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            ...ui['info'].entries.map<Widget>((entry) {
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 2),
                child: Row(
                  children: [
                    Text(
                      '${entry.key}: ',
                      style: TextStyle(fontWeight: FontWeight.bold),
                    ),
                    Text(entry.value.toString()),
                  ],
                ),
              );
            }).toList(),
          ],
          SizedBox(height: 20),
          Text(helper, style: TextStyle(color: Colors.grey)),
          SizedBox(height: 20),
          ...List.generate(options.length, (i) {
            final item = options[i];
            final label = item is String
                ? item
                : item['label'] ?? item['button_text'] ?? '선택';

            return Padding(
              padding: const EdgeInsets.symmetric(vertical: 4),
              child: ElevatedButton(
                onPressed: () => handleNext(label),
                child: Text(label),
              ),
            );
          }),
        ],
      ),
    );
  }
}
