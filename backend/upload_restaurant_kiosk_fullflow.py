# upload_restaurant_kiosk_fullflow.py

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
json_path = os.path.join("..", "scenario", "data", "Restaurant_Kiosk_Receipt_FullFlow_Sorted_WithImagePaths_AndMenuImages.json")

# JSON 로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for i, item in enumerate(data):
    # 메뉴 레이아웃 전용 문서로 구분
    if i == 0 and "menu_items" in item:
        doc_ref = db.collection("restaurant_kiosk_fullflow").document("menu_layout")
        doc_ref.set(item)
        count += 1
        continue

    step = item.get("step")
    if step is not None:
        doc_ref = db.collection("restaurant_kiosk_fullflow").document(f"step_{step}")
        doc_ref.set(item)
        count += 1

print(f"[식당 키오스크 전체 시나리오] 총 {count}개 문서 업로드 완료 ")
