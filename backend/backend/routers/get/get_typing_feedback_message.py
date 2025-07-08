# get_typing_feedback_message.py
# 타자 연습 피드백 메시지 조회

from fastapi import APIRouter, HTTPException, Query
from firebase_init import db

router = APIRouter()

@router.get("/typing_feedback")
def get_typing_feedback(level: str = Query(...), accuracy: str = Query(...)):
    """
    레벨 + 정확도 기반 격려 메시지 조회 API
    예: /typing_feedback?level=beginner&accuracy=minor_mistake
    """
    doc_id = f"{level}_{accuracy}"
    doc = db.collection("typing_feedback_messages").document(doc_id).get()

    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code=404, detail="해당 조건의 피드백 메시지를 찾을 수 없습니다.")
