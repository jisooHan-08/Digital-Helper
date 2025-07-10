# upload_typing_feedback_messages.py

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

# JSON 파일 경로 (scenario/data 내부)
json_path = os.path.join("..", "scenario", "data", "2-0. Typing Practice Feedback Messages by Level.json")

# JSON 로드
with open(json_path, "r", encoding="utf-8") as f:
    typing_data = json.load(f)

# 업로드
collection = db.collection("typing_feedback_messages")
upload_count = 0

for level, feedback_types in typing_data.items():
    for accuracy, messages in feedback_types.items():
        doc_id = f"{level}_{accuracy}"
        collection.document(doc_id).set({
            "level": level,
            "accuracy": accuracy,
            "messages": messages
        })
        upload_count += 1

print(f" 타자연습 피드백 {upload_count}개 문서 Firestore 업로드 완료")

