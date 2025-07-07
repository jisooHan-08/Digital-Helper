import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import random
import string

# 1. 사용자 ID 생성 함수 (오늘 날짜 + 랜덤 문자열 5자리)
def generate_user_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{date_part}_{random_part}"

user_id = generate_user_id()

# 2. Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 3. 오답 리스트 (예시: 단어/문장/문단 단계별)
mistake_list = [
    {
        "step": 1001,
        "level": "한글자",
        "expected": "가",
        "user_input": "나",
        "timestamp": datetime.now(timezone.utc).isoformat()
    },
    {
        "step": 4005,
        "level": "문장",
        "expected": "나는 오늘 학교에 갔다.",
        "user_input": "나는 오늘 학교 갔다.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    },
    {
        "step": 5003,
        "level": "문단",
        "expected": "오늘은 비가 오는 날이다. 창문을 열어두면 시원한 바람이 들어온다.",
        "user_input": "오늘 비가 오는 날이다. 창문 열어두면 바람이 들어온다.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
]

# 4. 저장 함수
def save_typing_mistakes(user_id, mistake_list):
    doc_ref = db.collection("typing_mistakesbackup_byuser").document(user_id)
    doc_ref.set({
        "wrong_selections": firestore.ArrayUnion(mistake_list)
    }, merge=True)

# 5. 실행
save_typing_mistakes(user_id, mistake_list)
print(f" 사용자 ID {user_id} 에 대해 오답 {len(mistake_list)}개 저장 완료")
