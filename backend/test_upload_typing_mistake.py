import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import random
import string

# 사용자 ID 생성 함수 (예: 20250703_k1l2m)
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

# 오답 데이터 1건 예시 (타자 연습)
mistake = {
    "step": 4002,
    "level": "문장",
    "expected": "오늘은 날씨가 맑습니다.",
    "user_input": "오늘 날씨가 맑습니다.",
    "timestamp": datetime.now(timezone.utc).isoformat(),
    "user_id": user_id
}

# Firestore 업로드
doc_ref = db.collection("test_typing_mistakes").document(user_id)
doc_ref.set({
    "mistakes": [mistake],
    "user_id": user_id
})

print(f" 타자 오답이 업로드되었습니다. (user_id: {user_id})")
