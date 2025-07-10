# get_top3_typing_mistake_stats.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from collections import Counter

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 사용자별 오답 통계 조회
def get_user_typing_mistake_stats(user_id: str):
    doc_ref = db.collection("typing_mistakesbackup_byuser").document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        print(f"[!] 사용자 ID {user_id}의 오답 데이터가 존재하지 않습니다.")
        return

    data = doc.to_dict()
    mistakes = data.get("wrong_selections", [])

    level_counters = {
        "한글자": Counter(),
        "두글자": Counter(),
        "세글자": Counter(),
        "문장": Counter(),
        "문단": Counter()
    }

    for m in mistakes:
        level = m.get("level")
        expected = m.get("expected")
        user_input = m.get("user_input")
        if level in level_counters and expected and user_input:
            key = f"{expected} (입력: {user_input})"
            level_counters[level][key] += 1

    for level, counter in level_counters.items():
        top3 = counter.most_common(3)
        if top3:
            print(f"\n[타자연습 - {level}] 가장 많이 틀린 항목:")
            for i, (desc, count) in enumerate(top3, 1):
                print(f"{i}) {desc} → {count}회")

# 오늘 날짜 기준 가장 최신 사용자 ID 찾기
def get_latest_user_id():
    today_prefix = datetime.now().strftime("%Y%m%d")
    docs = db.collection("typing_mistakesbackup_byuser").stream()
    matched_ids = [doc.id for doc in docs if doc.id.startswith(today_prefix)]
    return sorted(matched_ids, reverse=True)[0] if matched_ids else None

# 실행 테스트용
if __name__ == "__main__":
    latest_user = get_latest_user_id()
    if latest_user:
        get_user_typing_mistake_stats(latest_user)
    else:
        print("오늘 날짜로 시작하는 사용자 ID를 찾을 수 없습니다.")
