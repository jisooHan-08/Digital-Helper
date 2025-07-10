# get_top3_hospital_kiosk_mistakes.py
from collections import Counter
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 가장 최근 사용자 ID 찾기
def get_latest_user_id():
    today_prefix = datetime.now().strftime("%Y%m%d")
    docs = db.collection("hospital_kiosk_mistakesbackup_byuser").stream()
    matched_ids = [doc.id for doc in docs if doc.id.startswith(today_prefix)]
    return sorted(matched_ids, reverse=True)[0] if matched_ids else None

# 사용자별 병원 키오스크 오답 통계 출력
def get_top3_hospital_mistakes_by_user(user_id: str):
    doc = db.collection("hospital_kiosk_mistakesbackup_byuser").document(user_id).get()
    if not doc.exists:
        print(f"[!] 사용자 ID {user_id} 에 대한 오답 데이터가 없습니다.")
        return

    data = doc.to_dict()
    counter = Counter()

    for m in data.get("wrong_selections", []):
        question = m.get("question")
        selected = m.get("selected")
        if question and selected:
            key = f"{question} (선택: {selected})"
            counter[key] += 1

    print(f"\n[ 키오스크 연습(병원) ] 가장 많이 틀린 구간은?")
    for i, (desc, count) in enumerate(counter.most_common(3), start=1):
        print(f"{i}) {desc} → {count}회")

# 실행
if __name__ == "__main__":
    latest_user = get_latest_user_id()
    if latest_user:
        get_top3_hospital_mistakes_by_user(latest_user)
    else:
        print("오늘 날짜로 시작하는 사용자 ID를 찾을 수 없습니다.")
