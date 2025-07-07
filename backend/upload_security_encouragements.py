import os
import json
from firebase_admin import credentials, firestore, initialize_app

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

# JSON 파일 경로
filename = "4-0. Security_Quiz_Feedback_Messages.json"
json_path = os.path.join("data", filename)

# JSON 파일 열기
try:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"[오류] JSON 파일을 찾을 수 없습니다: {json_path}")
    exit()

# Firestore 업로드
collection = db.collection("security_quiz_encouragements")
feedback = data.get("security_quiz_feedback", {})

for result_type, messages in feedback.items():
    doc_data = {
        "result": result_type,
        "messages": messages
    }
    collection.document(result_type).set(doc_data)
    print(f"[업로드 완료] {result_type}: {len(messages)}개 메시지")
