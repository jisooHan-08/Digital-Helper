# [보안 퀴즈용 격려 메시지 조회]
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_security_quiz_feedback(result_type: str):
    """
    보안 퀴즈용 피드백 메시지 조회
    :param result_type: correct / almost_correct / wrong
    :return: 메시지 리스트 또는 오류 메시지
    """
    doc_ref = db.collection("security_quiz_feedback_messages").document(result_type)
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict().get("messages", [])
    else:
        return [f"'{result_type}' 유형의 피드백 메시지가 없습니다."]

# 테스트 실행 예시 (자동 출력용으로 실제 구현 시 주석 처리 가능)
if __name__ == "__main__":
    messages = get_security_quiz_feedback("wrong")
    print("보안 퀴즈 피드백:", messages)
