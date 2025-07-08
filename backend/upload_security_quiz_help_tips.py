# upload_security_quiz_help_tips.py

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
json_path = os.path.join("..", "scenario", "data", "4-0. Security_Education_Quiz_Help_Tips.json")

#  JSON 로드 및 업로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for item in data:
    step = item.get("step")
    helper_message = item.get("helper_message")

    if step and helper_message:
        doc_ref = db.collection("security_quiz_help_tips").document(str(step))
        doc_ref.set({
            "helper_message": helper_message
        })
        count += 1

print(f"[보안 퀴즈 힌트] 총 {count}개 도움말 업로드 완료 ")
