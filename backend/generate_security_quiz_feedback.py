import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# 1. Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. 피드백 메시지 리스트 (예시 2개, 원할 경우 확장 가능)
feedback_messages = [
    {
        "question": "비밀번호는 자주 바꿔야 한다?",
        "correct_answer": "예",
        "feedback": "비밀번호를 주기적으로 변경하면 해킹 피해를 예방할 수 있습니다."
    },
    {
        "question": "의심스러운 이메일은?",
        "correct_answer": "삭제한다",
        "feedback": "의심스러운 이메일은 열지 말고 바로 삭제하는 것이 안전합니다."
    }
]

# 3. Firestore에 업로드
def upload_feedback_messages(feedback_messages):
    collection_ref = db.collection("security_quiz_feedback_messages")
    for item in feedback_messages:
        doc_id = f"{item['question'][:10]}_{item['correct_answer']}"
        collection_ref.document(doc_id).set({
            "question": item["question"],
            "correct_answer": item["correct_answer"],
            "feedback": item["feedback"],
            "created_at": datetime.now().isoformat()
        })
    print(f"보안 퀴즈 피드백 메시지 {len(feedback_messages)}개 업로드 완료")

# 4. 실행
upload_feedback_messages(feedback_messages)
