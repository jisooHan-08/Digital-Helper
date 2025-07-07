from fastapi import APIRouter, HTTPException
from firebase_init import db

router = APIRouter()

# GET API: 질문 텍스트로 피드백 메시지 조회
@router.get("/security_feedback_by_question/{question}")
def get_feedback_by_question(question: str):
    try:
        # Firestore에서 "question" 필드가 일치하는 문서를 찾음
        docs = db.collection("security_quiz_feedback_messages").where("question", "==", question).stream()
        
        for doc in docs:
            return doc.to_dict()
        
        # 아무 문서도 없을 경우
        raise HTTPException(status_code=404, detail="404: 해당 질문에 대한 피드백이 없습니다.")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
