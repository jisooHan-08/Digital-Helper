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
      text: json['text'] ?? json['word'] ?? json['sentence'] ?? '',
      type: json['type'] ?? 'sentence',
      hint: json['hint'],
      typingOrder: json['typing_order'] != null
          ? List<String>.from(json['typing_order'])
          : null,
    );
  }
}
