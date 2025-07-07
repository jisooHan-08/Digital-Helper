import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import random
import string

# 사용자 ID 생성 함수 (예: 20250703_a1b2c)
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

# 오답 데이터 1건 예시 (병원 키오스크)
mistake = {
    "scenario_id": "hospital_kiosk",
    "scenario_title": "병원 키오스크",
    "step_index": 101,
    "question": "진료과를 선택해주세요.",
    "selected": "피부과",
    "correct": "내과",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "user_id": user_id
}

# Firestore 업로드 (단일 문서로 저장)
doc_ref = db.collection("test_hospital_kiosk_mistakes").document(user_id)
doc_ref.set({
    "mistakes": [mistake],
    "user_id": user_id
})

print(f" 병원 키오스크 오답이 업로드되었습니다. (user_id: {user_id})")
