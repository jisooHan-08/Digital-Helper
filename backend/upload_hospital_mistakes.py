# upload_hospital_mistakes.py

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
json_path = os.path.join("..", "scenario", "data", "hospital_kiosk.json")


# 5. JSON 로드 및 오답 데이터 생성
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

mistake_list = []

for step in data:
    step_index = step.get("step")
    instruction = step.get("instruction") or step.get("ui", {}).get("text")
    ui = step.get("ui", {})
    buttons = ui.get("buttons", [])
    options = ui.get("options", [])

    # 선택형 인터페이스인지 확인
    choices = buttons if buttons else options
    if step_index and instruction and isinstance(choices, list) and len(choices) >= 2:
        mistake = {
            "scenario_id": "hospital_kiosk",
            "scenario_title": "병원 키오스크",
            "step_index": step_index,
            "question": instruction,
            "selected": choices[0],    # 첫 번째 선택지를 오답으로 가정
            "correct": choices[-1],    # 마지막 선택지를 정답으로 가정
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        mistake_list.append(mistake)

# 6. Firestore에 저장
doc_ref = db.collection("hospital_kiosk_mistakesbackup_byuser").document(user_id)
doc_ref.set({
    "wrong_selections": firestore.ArrayUnion(mistake_list)
}, merge=True)

print(f"[병원 키오스크] 사용자 {user_id} - 오답 {len(mistake_list)}개 업로드 완료")

