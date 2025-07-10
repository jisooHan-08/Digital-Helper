# upload_all_typing_practice_questions.py

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

# 업로드할 JSON 파일 목록
typing_files = {
    "one_letter": "../scenario/data/2-1. 50 One-letter Words.json",
    "two_letter": "../scenario/data/2-2. 50 Two-letter Words.json",
    "three_letter": "../scenario/data/2-3. 50 Three-letter Words.json",
    "sentence": "../scenario/data/2-4. 30 One-sentence Practices.json",
    "paragraph": "../scenario/data/2-5. 30 Paragraph Practices.json"
}

# 각 파일에 대한 Firestore 컬렉션 이름
# 예: typing_practice_oneletter_questions
for level, path in typing_files.items():
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    collection_name = f"typing_practice_{level}_questions"
    collection_ref = db.collection(collection_name)

    count = 0
    for item in data:
        step = item.get("step")
        if step is None:
            continue

        # 그대로 전체 저장
        doc_ref = collection_ref.document(f"step_{step}")
        doc_ref.set(item)
        count += 1

    print(f"[{collection_name}] 총 {count}개 문서 업로드 완료 ")
