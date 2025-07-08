# upload_security_quiz_questions.py

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
json_path = os.path.join("..", "scenario", "data", "4. 50 Security Quiz Questions - Base.json")

# JSON 로드 및 업로드
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

count = 0
for item in data:
    quiz_id = item.get("quiz_id")
    question = item.get("question")
    choices = item.get("choices")
    answer = item.get("answer")
    explanation = item.get("explanation")

    if quiz_id and question and choices and answer:
        doc_ref = db.collection("security_quiz_questions").document(str(quiz_id))  
        doc_ref.set({
            "question": question,
            "choices": choices,
            "answer": answer,
            "explanation": explanation
        })
        count += 1

print(f"[보안 퀴즈 문제] 총 {count}개 문항 업로드 완료 ")
