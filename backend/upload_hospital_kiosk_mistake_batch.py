import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import random
import string

# 1. 사용자 ID 생성 함수
def generate_user_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{date_part}_{random_part}"

user_id = generate_user_id()

# 2. Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 3. 병원 키오스크 오답 예시
mistake_list = [
    {
        "scenario_id": "hospital_kiosk",
        "scenario_title": "병원 키오스크",
        "step_index": 214,
        "question": "접수된 정보가 맞는지 확인하고 입력완료 버튼을 눌러주세요.",
        "selected": "뒤로가기 버튼 누름",
        "correct": "입력완료 버튼 누름",
        "timestamp": datetime.now(timezone.utc).isoformat()
    },
    {
        "scenario_id": "hospital_kiosk",
        "scenario_title": "병원 키오스크",
        "step_index": 219,
        "question": "카드를 클릭하면 결제됩니다.",
        "selected": "현금 버튼 클릭",
        "correct": "카드 버튼 클릭",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
]

# 4. 저장 함수
def save_hospital_kiosk_mistakes(user_id, mistake_list):
    doc_ref = db.collection("hospital_kiosk_mistakesbackup_byuser").document(user_id)
    doc_ref.set({
        "wrong_selections": firestore.ArrayUnion(mistake_list)
    }, merge=True)

# 5. 실행
save_hospital_kiosk_mistakes(user_id, mistake_list)
print(f" 사용자 ID {user_id} 에 대해 병원 키오스크 오답 {len(mistake_list)}개 저장 완료")
