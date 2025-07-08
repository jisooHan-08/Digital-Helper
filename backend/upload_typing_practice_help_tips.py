# upload_typing_practice_help_tips.py

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

# JSON 경로 설정
json_path = os.path.join("..", "scenario", "data", "2-0. Typing_Practice_Help_Tips.json")

# JSON 로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 업로드
count = 0
for item in data:
    step = item.get("step")
    helper_message = item.get("helper_message")
    
    if step is not None and helper_message:
        doc_ref = db.collection("typing_practice_help_tips").document(f"step_{step}")
        doc_ref.set({
            "helper_message": helper_message
        })
        count += 1

print(f"[타자 연습 힌트] 총 {count}개 문서 업로드 완료 ")
