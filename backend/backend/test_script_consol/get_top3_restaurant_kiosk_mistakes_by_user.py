# get_top3_restaurant_kiosk_mistakes_by_user.py

import re
from collections import Counter
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 사용자 ID 자동 탐색 (최신순)
def find_latest_user_id():
    pattern = r"^20\d{6}_[a-z0-9]{5}$"
    docs = db.collection("restaurant_kiosk_mistakesbackup_byuser").stream()
    matched_ids = [doc.id for doc in docs if re.match(pattern, doc.id)]
    matched_ids.sort(reverse=True)
    return matched_ids[0] if matched_ids else None

# 통계 출력 함수
def print_top3_mistakes(user_id):
    doc_ref = db.collection("restaurant_kiosk_mistakesbackup_byuser").document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        print(f"[오류] 사용자 ID {user_id}에 대한 오답 정보가 없습니다.")
        return

    data = doc.to_dict()
    counter = Counter()

    for mistake in data.get("wrong_selections", []):
        question = mistake.get("question")
        selected = mistake.get("selected")
        if question and selected:
            key = f"{question} (선택: {selected})"
            counter[key] += 1

    print(f"[ 식당 키오스크 ] 사용자 ID: {user_id}의 가장 많이 틀린 구간은?")
    for i, (desc, count) in enumerate(counter.most_common(3), start=1):
        print(f"{i}) {desc} → {count}회")

# 실행 테스트용
if __name__ == "__main__":
    user_id = find_latest_user_id()
    if user_id:
        print_top3_mistakes(user_id)
    else:
        print("[오류] 조건에 맞는 사용자 ID를 찾을 수 없습니다.")
