# [타자 연습용 격려 메시지 조회]
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_typing_feedback(level: str, accuracy: str):
    """
    타자 연습용 피드백 메시지 조회
    :param level: beginner / intermediate / advanced
    :param accuracy: correct / minor_mistake / major_mistake
    :return: 메시지 리스트 또는 오류 메시지
    """
    doc_id = f"{level}_{accuracy}"
    doc_ref = db.collection("typing_feedback_messages").document(doc_id)
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict().get("messages", [])
    else:
        return [f"'{doc_id}'에 해당하는 피드백 메시지가 없습니다."]

# 테스트 실행 예시 (자동 출력용으로 실제 구현 시 주석 처리 가능)
if __name__ == "__main__":
    messages = get_typing_feedback("beginner", "minor_mistake")
    print("타자 연습 피드백:", messages)
