import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import datetime
import random
import string

# Firebase 인증 초기화 (중복 방지)
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# JSON 파일들이 들어있는 폴더 경로
json_dir = "../scenario/data"

# 파일명에 따른 컬렉션명 추론
def infer_collection(filename):
    if filename.startswith("0."):
        return "main_screen_steps"
    elif filename.startswith("1-1"):
        return "restaurant_kiosk_steps"
    elif filename.startswith("1-2"):
        return "hospital_kiosk_steps"
    elif filename.startswith("2-0. Typing Practice Feedback Messages"):
        return "typing_feedback_messages"
    elif filename.startswith("2-0. Typing_Practice_Help_Tips"):
        return "typing_help_tips"
    elif filename.startswith(("2-1", "2-2", "2-3", "2-4", "2-5")):
        return "typing_data"  # 혹시 추후 레벨별로 나누고 싶으면 여기서 조정 가능
    elif filename.startswith("3."):
        return "security_education"
    elif filename.startswith("4-0."):
        return "security_quiz_feedback_messages"
    elif filename.startswith("4."):
        return "security_quiz"
    else:
        return "misc_data"

# 문서 ID 생성
def generate_unique_doc_id():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{now}_{rand}"

uploaded = 0
skipped = 0

# 업로드 시작
for file in os.listdir(json_dir):
    if file.endswith(".json") and file != "serviceAccountKey.json":
        path = os.path.join(json_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                collection = infer_collection(file)

                if isinstance(data, dict):
                    doc_id = generate_unique_doc_id()
                    db.collection(collection).document(doc_id).set(data)
                    print(f" {collection} ← {file} (1건 업로드 완료)")
                    uploaded += 1

                elif isinstance(data, list):
                    count = 0
                    for item in data:
                        if isinstance(item, dict):
                            doc_id = generate_unique_doc_id()
                            db.collection(collection).document(doc_id).set(item)
                            count += 1
                        else:
                            print(f"{file} 내 항목이 dict 아님. 건너뜀")
                            skipped += 1
                    print(f" {collection} ← {file} ({count}건 업로드 완료)")
                    uploaded += count

                else:
                    print(f" {file}은(는) 지원되지 않는 JSON 형식입니다.")
                    skipped += 1

            except Exception as e:
                print(f" {file} 업로드 실패: {e}")
                skipped += 1

# 결과 요약
print(f"\n 총 업로드 완료: {uploaded}건 /  실패 또는 건너뜀: {skipped}건")

