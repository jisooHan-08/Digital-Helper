# get_hospital_kiosk_mistake_feedback.py
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Firebase init
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_mistake_feedback(user_id):
    doc = db.collection("hospital_kiosk_mistakesbackup_byuser").document(user_id).get()
    if not doc.exists:
        print("해당 사용자 ID에 대한 오답 기록이 없습니다.")
        return

    data = doc.to_dict()
    mistake_list = data.get("wrong_selections", [])

    print(f"[사용자 {user_id}] 병원 키오스크 오답 목록:")
    for item in mistake_list:
        print(f"Step: {item.get('step_index')}")
        print(f"문제: {item.get('question')}")
        print(f"선택: {item.get('selected')} / 정답: {item.get('correct')}")
        print("-")

# 예시 실행
if __name__ == "__main__":
    test_user_id = input("조회할 사용자 ID를 입력하세요: ")
    get_mistake_feedback(test_user_id)