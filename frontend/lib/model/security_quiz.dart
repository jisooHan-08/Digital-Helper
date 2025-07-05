class SecurityQuiz {
  final int id;
  final String question;
  final List<String> options;
  final int answerIndex;
  final String explanation;
  final String type; // OX or multiple

  SecurityQuiz({
    required this.id,
    required this.question,
    required this.options,
    required this.answerIndex,
    required this.explanation,
    required this.type,
  });

  factory SecurityQuiz.fromJson(Map<String, dynamic> json) {
    final options =
        (json['choices'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList() ??
        [];
    final answerText = json['answer'] ?? '';
    final answerIndex = options.indexOf(answerText);

    return SecurityQuiz(
      id: json['quiz_id'] ?? 0,
      question: json['question'] ?? '',
      options: options,
      answerIndex: answerIndex >= 0 ? answerIndex : 0,
      explanation: json['explanation'] ?? '',
      type: 'multiple', // 필요한 경우 나중에 'ox' 분기 가능
    );
  }
}

class SecurityHint {
  final String step;
  final String helperMessage;

  SecurityHint({required this.step, required this.helperMessage});

  factory SecurityHint.fromJson(Map<String, dynamic> json) {
    return SecurityHint(
      step: json['step'] ?? '',
      helperMessage: json['helper_message'] ?? '',
    );
  }
}
