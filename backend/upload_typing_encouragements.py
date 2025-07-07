import os
import json
from firebase_admin import credentials, firestore, initialize_app

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

# JSON 경로 
filename = "2-0. Typing Practice Feedback Messages by Level.json"
json_path = os.path.join("data", filename)

# JSON 파일 열기
try:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"[오류] JSON 파일을 찾을 수 없습니다: {json_path}")
    exit()

# Firestore 업로드
collection = db.collection("typing_encouragements")

for level, result_dict in data.items():
    for result_type, messages in result_dict.items():
        doc_id = f"{level}_{result_type}"
        doc_data = {
            "level": level,
            "result": result_type,
            "messages": messages
        }
        collection.document(doc_id).set(doc_data)
        print(f"[업로드 완료] {doc_id}: {len(messages)}개 메시지")

