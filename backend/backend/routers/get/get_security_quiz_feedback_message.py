# get_security_quiz_feedback_message.py
# 보안 퀴즈 피드백 메시지 관련 조회 API (Firestore에서 읽기 전용)
# 사용자의 오답 기록이나 정답/오답 유형에 따라 피드백 메시지를 조회하는 기능만 수행

from fastapi import APIRouter, HTTPException
from firebase_init import db

router = APIRouter()

# [기능 1] 사용자가 틀린 질문을 기준으로 오답 기록 조회
# 사용 목적: 사용자가 어떤 문제에서 오답을 냈는지 확인할 때
# 검색 기준: "security_quiz_mistakesbackup_byuser" 컬렉션에서 질문 텍스트로 조회
@router.get("/security_feedback_by_question/{question}")
def get_feedback_by_question(question: str):
    try:
        docs = db.collection("security_quiz_mistakesbackup_byuser").where("question", "==", question).stream()
        for doc in docs:
            return doc.to_dict()
        raise HTTPException(status_code=404, detail="해당 질문에 대한 피드백이 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# [기능 2] 결과 유형(corrrect / wrong 등)별로 피드백 메시지를 조회
# 사용 목적: 정답/오답 여부에 따라 해당 피드백 멘트를 보여줄 때
# 예시 호출: /security_feedback/correct 또는 /security_feedback/wrong

@router.get("/security_feedback/{result_type}")
def get_feedback_by_result_type(result_type: str):
    """
    결과 타입 기반 피드백 메시지 조회 API
    예: /security_feedback/correct
    """
    try:
        doc = db.collection("security_quiz_mistakesbackup_byuser").document(result_type).get()
        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="해당 결과 타입의 메시지를 찾을 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
