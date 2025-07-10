# upload_main_screen_entry.py
# 앱의 메인 화면 진입 시 보여줄 안내 메시지 및 선택지 데이터

import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

#  Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

#  JSON 경로 설정
json_path = os.path.join("..", "scenario", "data", "0. On Entering the Main Screen.json")

#  JSON 로드 및 Firestore 업로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# step 값 사용해서 문서 ID 지정
step = data.get("step", 0)
doc_ref = db.collection("main_screen_entry").document(f"step_{step}")
doc_ref.set(data)

print(f"[메인 화면 진입 데이터] step_{step} 업로드 완료 ")
