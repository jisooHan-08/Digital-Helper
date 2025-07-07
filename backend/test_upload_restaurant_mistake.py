import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import random
import string

# 사용자 ID 생성 함수 (예: 20250703_x9z8a)
def generate_user_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{date_part}_{random_part}"

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 사용자 ID 생성
user_id = generate_user_id()

# 오답 데이터 1건 예시 (식당 키오스크)
mistake = {
    "scenario_id": "restaurant_kiosk",
    "scenario_title": "식당 키오스크",
    "step_index": 203,
    "question": "사이드 메뉴를 선택해주세요.",
    "selected": "콜라",
    "correct": "감자튀김",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "user_id": user_id
}

# Firestore 업로드
doc_ref = db.collection("test_restaurant_kiosk_mistakes").document(user_id)
doc_ref.set({
    "mistakes": [mistake],
    "user_id": user_id
})

print(f" 식당 키오스크 오답이 업로드되었습니다. (user_id: {user_id})")
