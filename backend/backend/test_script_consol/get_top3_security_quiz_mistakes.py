# get_top3_security_quiz_mistakes.py

from collections import Counter
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

# 최신 사용자 ID 탐색 함수 (형식: 20xxxxxx_xxxxx)
def find_latest_user_id():
    pattern = r"^20\d{6}_[a-z0-9]{5}$"
    docs = db.collection("security_quiz_mistakesbackup").stream()
    matched_ids = [doc.id for doc in docs if re.match(pattern, doc.id)]
    matched_ids.sort(reverse=True)
    return matched_ids[0] if matched_ids else None

# 통계 출력 함수
def print_top3_security_mistakes(user_id):
    doc = db.collection("security_quiz_mistakesbackup").document(user_id).get()
    if not doc.exists:
        print(f"[오류] 사용자 {user_id}의 오답 데이터가 없습니다.")
        return

    data = doc.to_dict()
    counter = Counter()

    for mistake in data.get("wrong_selections", []):
        question = mistake.get("question")
        selected = mistake.get("selected")
        if question and selected:
            key = f"{question} → {selected}"
            counter[key] += 1

    print(f"[ 보안 퀴즈 오답 TOP 3 ] 사용자 ID: {user_id}")
    for i, (desc, count) in enumerate(counter.most_common(3), 1):
        print(f"{i}) {desc} → {count}회")

# 실행 테스트용
if __name__ == "__main__":
    user_id = find_latest_user_id()
    if user_id:
        print_top3_security_mistakes(user_id)
    else:
        print("[오류] 형식에 맞는 사용자 ID를 찾을 수 없습니다.")
