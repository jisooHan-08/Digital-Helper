# upload_image_path_mappings.py
# 이미지 파일 경로 저장 데이터

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
json_path = os.path.join("..", "scenario", "data", "corrected_images_by_filename.json")

# JSON 로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for filename, path in data.items():
    if filename and path:
        doc_ref = db.collection("image_path_mappings").document(filename)
        doc_ref.set({
            "path": path
        })
        count += 1

print(f"[이미지 경로 매핑] 총 {count}개 문서 업로드 완료 ")
