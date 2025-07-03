import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
import datetime
import random
import string

# 1. Firebase 인증 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. JSON 파일들이 들어있는 폴더 경로
json_dir = "data"  # 현재 디렉토리 내부의 data 폴더

# 3. 컬렉션 자동 분류 함수
def infer_collection(filename):
    if filename.startswith("0."):
        return "main_screen_steps"
    elif filename.startswith("1-1"):
        return "restaurant_kiosk_steps"
    elif filename.startswith("1-2"):
        return "hospital_kiosk_steps"
    elif filename.startswith("2-"):
        return "typing_data"
    elif filename.startswith("3."):
        return "security_education"
    elif filename.startswith("4-0."):
        return "security_quiz"
    elif filename.startswith("4."):
        return "security_quiz"
    else:
        return "misc_data"

# 4. 고유 문서 ID 생성 함수
def generate_unique_doc_id():
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{now}_{rand}"

uploaded = 0
skipped = 0

# 5. 파일 업로드 반복
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

                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            doc_id = generate_unique_doc_id()
                            db.collection(collection).document(doc_id).set(item)
                        else:
                            print(f"⚠️ {file}의 항목이 dict가 아님. 건너뜀")
                            skipped += 1
                            continue
                else:
                    print(f"⚠️ {file}은 지원되지 않는 형식입니다.")
                    skipped += 1
                    continue

                print(f"✅ {collection}/{file} 업로드 완료")
                uploaded += 1

            except Exception as e:
                print(f"❌ {file} 업로드 실패: {e}")
                skipped += 1

print(f"\n총 {uploaded}개 업로드 완료, {skipped}개 실패")

