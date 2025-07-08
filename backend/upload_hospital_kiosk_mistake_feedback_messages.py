# upload_hospital_kiosk_mistake_feedback_messages.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import json
import random
import string

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 사용자 ID 생성 함수
def generate_user_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{date_part}_{random_part}"

# JSON 경로 및 로드
with open("../scenario/data/병원키오스크_영수증기능포함_이미지경로적용본.json", encoding="utf-8") as f:
    scenario_data = json.load(f)

user_id = generate_user_id()
mistake_list = []

# 예시로 일부 항목을 임의 오답으로 처리
for step in scenario_data:
    step_index = step.get("step")
    question = step.get("instruction") or step.get("ui", {}).get("text")
    buttons = step.get("ui", {}).get("buttons")
    
    if step_index and question and buttons:
        mistake = {
            "scenario_id": "hospital_kiosk",
            "scenario_title": "병원 키오스크",
            "step_index": step_index,
            "question": question,
            "selected": buttons[0],  # 실제 선택값 (예: 사용자가 틀린 선택을 했다고 가정)
            "correct": buttons[-1],  # 마지막 버튼이 정답이라고 가정
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        mistake_list.append(mistake)

# Firestore 저장
ref = db.collection("hospital_kiosk_mistakesbackup_byuser").document(user_id)
ref.set({"wrong_selections": firestore.ArrayUnion(mistake_list)}, merge=True)
print(f"{len(mistake_list)}개 오답 저장 완료 (user_id: {user_id})")