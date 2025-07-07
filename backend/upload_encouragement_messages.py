import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# 예시 격려 메시지들
encouragement_data = {
    201: "잘하고 있어요! 계속 진행해봐요.",
    202: "멋져요! 금방 익숙해질 거예요.",
    203: "차근차근 해보면 다 할 수 있어요.",
    204: "지금처럼만 하면 충분해요!",
    205: "훌륭해요! 자신감을 가져요!"
}

# Firestore 업로드
collection = db.collection("encouragement_messages")

for step, message in encouragement_data.items():
    doc_id = str(step)
    collection.document(doc_id).set({
        "step": step,
        "message": message
    })

print("격려 메시지 업로드 완료 ")
