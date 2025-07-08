# get_security_quiz_feedback_message.py

from fastapi import APIRouter, HTTPException
from firebase_init import db

router = APIRouter()

# 1. 질문 텍스트로 피드백 메시지 조회
@router.get("/security_feedback_by_question/{question}")
def get_feedback_by_question(question: str):
    try:
        docs = db.collection("security_quiz_mistakesbackup_byuser").where("question", "==", question).stream()
        for doc in docs:
            return doc.to_dict()
        raise HTTPException(status_code=404, detail="해당 질문에 대한 피드백이 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2. 결과 타입 기반 피드백 메시지 조회
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
