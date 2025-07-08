# get_restaurant_kiosk_mistake.py

import re
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 사용자 ID 자동 탐색 (형식: 2025xxxx_xxxxx)
def find_latest_user_id():
    pattern = r"^20\d{6}_[a-z0-9]{5}$"
    docs = db.collection("restaurant_kiosk_mistakesbackup_byuser").stream()
    matched_ids = [doc.id for doc in docs if re.match(pattern, doc.id)]
    matched_ids.sort(reverse=True)
    return matched_ids[0] if matched_ids else None

# 오답 조회 함수
def print_restaurant_mistakes(user_id):
    doc_ref = db.collection("restaurant_kiosk_mistakesbackup_byuser").document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        print(f"[오류] 사용자 ID {user_id}에 대한 오답 데이터가 없습니다.")
        return

    data = doc.to_dict()
    mistake_list = data.get("wrong_selections", [])

    print(f"[ 식당 키오스크 오답 목록 ] 사용자 ID: {user_id}")
    print("-" * 60)

    for m in mistake_list:
        question = m.get("question", "")
        selected = m.get("selected", "")
        correct = m.get("correct", "")
        step = m.get("step_index", "알 수 없음")

        print(f"Step: {step}")
        print(f"질문: {question}")
        print(f"선택한 답: {selected}")
        print(f"정답: {correct}")
        print("-" * 60)

# 실행
if __name__ == "__main__":
    user_id = find_latest_user_id()
    if user_id:
        print_restaurant_mistakes(user_id)
    else:
        print("[오류] 최근 사용자 ID를 찾을 수 없습니다.")
