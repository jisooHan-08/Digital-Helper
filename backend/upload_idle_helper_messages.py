# upload_idle_helper_messages.py
# 사용자가 아무 동작 없이 일정 시간 멈춰 있을 때 보여주는 도움말 메시지 시스템 데이터

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
json_path = os.path.join("..", "scenario", "data", "0. 1min Help System on Inactivity.json")

# JSON 로드 및 업로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

messages = data.get("idle_helper_messages", {})
count = 0

for key, message in messages.items():
    if key and message:
        doc_ref = db.collection("idle_helper_messages").document(str(key))
        doc_ref.set({
            "message": message
        })
        count += 1

print(f"[대기 중 힌트 메시지] 총 {count}개 문서 업로드 완료 ")
