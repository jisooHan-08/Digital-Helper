import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timezone
import random
import string

# 1. Firebase 인증 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# 2. 사용자 ID 생성 함수 (형식: 20250703_xxxxx)
def generate_user_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{date_part}_{random_part}"

user_id = generate_user_id()  # 사용자 ID 자동 생성

# 3. 오답 리스트 (보안 퀴즈 예시)
mistake_list = [
    {
        "scenario_id": "security_quiz",
        "scenario_title": "보안 퀴즈",
        "step_index": 0,
        "question": "비밀번호는 자주 바꿔야 한다?",
        "selected": "아니오",
        "correct": "예",
        "timestamp": datetime.now(timezone.utc).isoformat()
    },
    {
        "scenario_id": "security_quiz",
        "scenario_title": "보안 퀴즈",
        "step_index": 2,
        "question": "의심스러운 이메일은?",
        "selected": "열어본다",
        "correct": "삭제한다",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
]

# 4. 저장 함수
def save_multiple_wrong_answers(user_id, mistake_list):
    doc_ref = db.collection("security_quiz_mistakesbackup").document(user_id)
    doc_ref.set({
        "wrong_selections": firestore.ArrayUnion(mistake_list)
    }, merge=True)

# 5. 실행
user_id = "20250703_ab123"  
save_multiple_wrong_answers(user_id, mistake_list)
print(f" 사용자 ID {user_id}의 오답이 업로드되었습니다.")
