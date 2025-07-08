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

# 4. JSON 파일 경로 설정 (Digital-Helper.new 구조 기준)
base_path = "../scenario/data"
file_map = {
    "한글자": "2-1. 50 One-letter Words.json",
    "두글자": "2-2. 50 Two-letter Words.json",
    "세글자": "2-3. 50 Three-letter Words.json",
    "문장": "2-4. 30 One-sentence Practices.json",
    "문단": "2-5. 30 Paragraph Practices.json"
}

# 5. 각 파일에서 오답 생성
mistake_list = []

for level, filename in file_map.items():
    file_path = os.path.join(base_path, filename)
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)
    
    if isinstance(data, list) and len(data) > 0:
        item = data[0]
        expected = (
            item.get("text") or 
            item.get("sentence") or 
            item.get("paragraph") or 
            ""
        )
        if expected:
            mistake = {
                "step": item.get("step", 0),
                "level": level,
                "expected": expected,
                "user_input": "오답입력",  # 실제 입력 대신 예시용 오답
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            mistake_list.append(mistake)

# 6. Firestore 저장
doc_ref = db.collection("typing_mistakesbackup_byuser").document(user_id)
doc_ref.set({
    "wrong_selections": firestore.ArrayUnion(mistake_list)
}, merge=True)

print(f" 사용자 ID {user_id} 에 대해 타자 연습 오답 {len(mistake_list)}개 저장 완료")
