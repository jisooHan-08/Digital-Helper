# upload_security_quiz_mistakes.py

import os
import json
import random
import string
from datetime import datetime, timezone
import firebase_admin
from firebase_admin import credentials, firestore

# 1. 사용자 ID 자동 생성 (형식: 20250708_xxxxx)
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
json_path = os.path.join("..", "scenario", "data", "4. 50 Security Quiz Questions - Base.json")

# 5. JSON 로드 및 오답 데이터 생성
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

mistake_list = []

for item in data:
    quiz_id = item.get("quiz_id")
    question = item.get("question")
    options = item.get("choices", [])
    correct = item.get("answer")

    # 정답/선택지/문항 모두 존재하는 경우만
    if quiz_id and question and correct and isinstance(options, list) and len(options) >= 2:
        wrong_option = next((opt for opt in options if opt != correct), None)
        if wrong_option:
            mistake = {
                "quiz_id": quiz_id,
                "question": question,
                "selected": wrong_option,
                "correct": correct,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            mistake_list.append(mistake)

# 6. Firestore에 저장
doc_ref = db.collection("security_quiz_mistakesbackup_byuser").document(user_id)
doc_ref.set({
    "wrong_answers": firestore.ArrayUnion(mistake_list)
}, merge=True)

print(f"[보안퀴즈] 사용자 {user_id} - 오답 {len(mistake_list)}개 업로드 완료")

