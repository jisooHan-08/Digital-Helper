import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import random
import string

# Firebase 인증 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Firestore 클라이언트
db = firestore.client()

# 사용자 ID 자동 생성 함수 (예: 20250703_dijvn)
def generate_user_id():
    date_str = datetime.now().strftime("%Y%m%d")
    rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{date_str}_{rand_str}"

# 오답 예시 데이터 (보안 퀴즈 기준)
wrong_data = {
    "scenario_id": "security_quiz",
    "scenario_title": "보안 퀴즈",
    "step_index": 0,
    "question": "비밀번호는 자주 바꿔야 한다?",
    "selected": "아니오",
    "correct": "예",
    "timestamp": datetime.utcnow().isoformat() + "Z"
}

# 업로드 실행
def save_wrong_answer(data):
    user_id = generate_user_id()
    doc_ref = db.collection("test_security_quiz_mistake").document(user_id)
    doc_ref.set({
        "wrong_selections": firestore.ArrayUnion([data]),
        "user_id": user_id
    }, merge=True)
    print(f" 보안 퀴즈 오답 업로드 완료 (컬렉션: test_security_quiz_mistake, user_id: {user_id})")

# 실행
if __name__ == "__main__":
    save_wrong_answer(wrong_data)




