import firebase_admin
from firebase_admin import credentials, firestore
import re

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# 사용자 ID 자동 탐색 (형식: 20250703_xxxxx)
def find_latest_user_id():
    pattern =  r"^20250703_[a-zA-Z0-9]{5}$"
    collection_ref = db.collection("security_quiz_mistakesbackup")
    docs = collection_ref.stream()

    matched_ids = []
    for doc in docs:
        if re.match(pattern, doc.id):
            matched_ids.append(doc.id)

    if not matched_ids:
        return None

    matched_ids.sort(reverse=True)
    return matched_ids[0]

# 오답 + 피드백 출력 함수 (누락 로그 포함)
def print_user_feedback(user_id):
    mistake_doc = db.collection("security_quiz_mistakesbackup").document(user_id).get()
    if not mistake_doc.exists:
        print(f"사용자 ID {user_id}에 대한 오답 정보가 없습니다.")
        return

    mistake_data = mistake_doc.to_dict()
    mistake_list = mistake_data.get("wrong_selections", [])

    feedback_ref = db.collection("security_quiz_feedback_messages")
    feedback_docs = feedback_ref.stream()

    feedback_dict = {}
    for doc in feedback_docs:
        item = doc.to_dict()
        feedback_dict[item["question"]] = item.get("feedback", "")

    missing_feedback_questions = []

    print(f"\n사용자 {user_id}의 오답 피드백 목록:")
    print("-" * 60)

    for m in mistake_list:
        question = m.get("question", "")
        correct = m.get("correct", "")
        selected = m.get("selected", "")
        feedback = feedback_dict.get(question)

        if feedback:
            print(f"문제: {question}")
            print(f"틀린 답: {selected}")
            print(f"정답: {correct}")
            print(f"피드백: {feedback}")
        else:
            print(f"문제: {question}")
            print(f"틀린 답: {selected}")
            print(f"정답: {correct}")
            print(f"피드백: 피드백 메시지가 등록되지 않았습니다.")
            missing_feedback_questions.append(question)

        print("-" * 60)

    if missing_feedback_questions:
        print("\n아래 질문들은 피드백 메시지가 등록되어 있지 않습니다:")
        for q in missing_feedback_questions:
            print(f"- {q}")

# 실행
if __name__ == "__main__":
    user_id = find_latest_user_id()
    if user_id:
        print_user_feedback(user_id)
    else:
        print(" 해당 형식에 맞는 사용자 ID를 찾을 수 없습니다.")
