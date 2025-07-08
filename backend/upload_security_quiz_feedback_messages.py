# upload_security_quiz_feedback_messages.py

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
json_path = os.path.join("..", "scenario", "data", "4-0. Security_Quiz_Feedback_Messages.json")

# JSON 로드
with open(json_path, "r", encoding="utf-8") as f:
    security_data = json.load(f)

# 내부 키 접근
feedback_dict = security_data.get("security_quiz_feedback", {})

# 업로드
collection = db.collection("security_quiz_feedback_messages")
upload_count = 0

for result_type, messages in feedback_dict.items():
    collection.document(result_type).set({
        "result_type": result_type,
        "messages": messages
    })
    upload_count += 1

print(f" 보안퀴즈 피드백 {upload_count}개 문서 Firestore 업로드 완료")
