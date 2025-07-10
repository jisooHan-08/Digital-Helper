# upload_security_phishing_examples.py
# 피싱 사례 전체 업로드

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# JSON 경로
json_path = os.path.join("..", "scenario", "data", "3. Security Education - Phishing Examples.json")

# JSON 로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for item in data:
    case_id = item.get("case_id")
    if case_id is not None:
        doc_ref = db.collection("security_phishing_examples").document(f"case_{case_id}")
        doc_ref.set(item)
        count += 1

print(f"[보안 피싱 사례] 총 {count}건 업로드 완료 ")
