import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import random
import string

# 1. 사용자 ID 생성 함수 (날짜 + 랜덤문자 5자리)
def generate_user_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{date_part}_{random_part}"

user_id = generate_user_id()

# 2. Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 3. 식당 키오스크 오답 예시 리스트
mistake_list = [
    {
        "scenario_id": "restaurant_kiosk",
        "scenario_title": "식당 키오스크",
        "step_index": 102,
        "question": "원하는 메뉴를 선택해주세요.",
        "selected": "음료",       #  사용자가 잘못 누른 선택
        "correct": "메인 메뉴",    #  올바른 선택
        "timestamp": datetime.now(timezone.utc).isoformat()
    },
    {
        "scenario_id": "restaurant_kiosk",
        "scenario_title": "식당 키오스크",
        "step_index": 107,
        "question": "결제 수단을 선택해주세요.",
        "selected": "현금",
        "correct": "카드",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
]

# 4. 저장 함수
def save_restaurant_kiosk_mistakes(user_id, mistake_list):
    doc_ref = db.collection("restaurant_kiosk_mistakesbackup_byuser").document(user_id)
    doc_ref.set({
        "wrong_selections": firestore.ArrayUnion(mistake_list)
    }, merge=True)

# 5. 실행
save_restaurant_kiosk_mistakes(user_id, mistake_list)
print(f" 사용자 ID {user_id} 에 대해 식당 키오스크 오답 {len(mistake_list)}개 저장 완료")
