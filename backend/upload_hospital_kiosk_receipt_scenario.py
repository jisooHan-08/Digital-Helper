# upload_hospital_kiosk_receipt_scenario.py

import firebase_admin
from firebase_admin import credentials, firestore
import json
import os
from datetime import datetime
import random
import string

# 1. Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. JSON 파일 경로 (백엔드 기준 상대경로)
json_path = os.path.join("..", "scenario", "data", "병원키오스크_영수증기능포함_이미지경로적용본.json")

# 3. JSON 로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 4. 컬렉션 이름 지정
collection_name = "hospital_kiosk_fullflow"

# 5. 문서 ID 생성 함수
def generate_doc_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{date_part}_{random_part}"

# 6. 업로드 실행
doc_id = generate_doc_id()
doc_ref = db.collection(collection_name).document(doc_id)
doc_ref.set({
    "source_filename": "병원키오스크_영수증기능포함_이미지경로적용본.json",
    "uploaded_at": datetime.utcnow().isoformat() + "Z",
    "scenario_data": data
})

print(f"병원 키오스크 전체 시나리오 업로드 완료! 문서 ID: {doc_id}")
