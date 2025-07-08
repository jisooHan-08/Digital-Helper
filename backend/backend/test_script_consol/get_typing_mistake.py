# get_typing_mistake.py
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 사용자 오답 조회 함수
def get_typing_mistakes_by_user(user_id: str):
    doc_ref = db.collection("typing_mistakesbackup_byuser").document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        print(f"[!] 사용자 ID {user_id}에 대한 오답 기록이 없습니다.")
        return

    data = doc.to_dict()
    mistakes = data.get("wrong_selections", [])

    print(f"\n[ 사용자 오답 기록 - ID: {user_id} ]")
    print("-" * 60)
    for i, m in enumerate(mistakes, 1):
        step = m.get("step")
        level = m.get("level")
        expected = m.get("expected")
        user_input = m.get("user_input")
        timestamp = m.get("timestamp")
        print(f"{i}) STEP: {step} | 레벨: {level}")
        print(f"    정답: {expected}")
        print(f"    입력: {user_input}")
        print(f"    시간: {timestamp}")
        print("-" * 60)

# 실행 테스트 (예시 사용자 ID)
if __name__ == "__main__":
    test_user_id = "20250707_27546"  # 테스트용 사용자 ID (업로드된 ID 사용)
    get_typing_mistakes_by_user(test_user_id)
