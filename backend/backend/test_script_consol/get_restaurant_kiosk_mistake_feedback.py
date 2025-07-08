# get_restaurant_kiosk_mistake_feedback.py

import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 저장된 사용자 ID 문서 찾기
docs = db.collection("restaurant_kiosk_mistakesbackup_byuser").order_by("__name__", direction=firestore.Query.DESCENDING).limit(1).stream()
latest_doc = next(docs, None)

if latest_doc is None:
    print(" 저장된 식당 키오스크 오답 데이터가 없습니다.")
else:
    user_id = latest_doc.id
    data = latest_doc.to_dict()
    wrong_selections = data.get("wrong_selections", [])

    if not wrong_selections:
        print(f" 사용자 ID '{user_id}'에 저장된 오답이 없습니다.")
    else:
        print(f"[🍽 식당 키오스크] 사용자 {user_id}의 오답 피드백 조회 결과\n")

        for idx, mistake in enumerate(wrong_selections, start=1):
            selected = mistake.get("selected")
            question = mistake.get("question")

            # 선택한 오답에 대해 피드백 메시지 조회
            fb_doc = db.collection("restaurant_kiosk_feedback_messages").document(selected)
            fb_data = fb_doc.get()

            print(f"{idx}) 질문: {question}")
            print(f" 선택: {selected}")

            if fb_data.exists:
                messages = fb_data.to_dict().get("messages", [])
                for i, msg in enumerate(messages, start=1):
                    print(f" 피드백 {i}: {msg}")
            else:
                print(" 해당 선택에 대한 피드백 메시지가 없습니다.")

            print()
