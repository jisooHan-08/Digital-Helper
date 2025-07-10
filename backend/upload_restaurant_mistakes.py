import os
import json
import random
import string
from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials, firestore

# 1. 사용자 ID 생성 함수 (형식: 20250708_xxxxx)
def generate_user_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{date_part}_{random_part}"

# 2. Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 3. 사용자 ID 생성
user_id = generate_user_id()

# 4. JSON 경로 설정 (Digital-Helper.new 구조 기준)
json_path = os.path.join("..", "scenario", "data", "Restaurant_Kiosk_Receipt_FullFlow_Sorted_WithImagePaths_AndMenuImages.json")

# 5. JSON 로드 및 오답 생성
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

mistake_list = []
for step in data:
    step_index = step.get("step")
    question = step.get("instruction")
    options = step.get("options")

    # 실제로 선택지를 가진 질문만 필터링
    if step_index and question and isinstance(options, list) and len(options) >= 2:
        mistake = {
            "scenario_id": "restaurant_kiosk",
            "scenario_title": "식당 키오스크",
            "step_index": step_index,
            "question": question,
            "selected": options[0],  # 오답 선택 예시
            "correct": options[-1],  # 마지막이 정답이라고 가정
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        mistake_list.append(mistake)

# 6. Firestore 저장
doc_ref = db.collection("restaurant_kiosk_mistakesbackup_byuser").document(user_id)
doc_ref.set({
    "wrong_selections": firestore.ArrayUnion(mistake_list)
}, merge=True)

print(f"사용자 ID {user_id}에 대해 식당 키오스크 오답 {len(mistake_list)}개 저장 완료")
