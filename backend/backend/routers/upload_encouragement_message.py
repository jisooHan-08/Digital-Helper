from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from firebase_init import db

router = APIRouter()

# 요청 데이터 모델
class EncouragementMessage(BaseModel):
    step: int
    type: str
    messages: list[str]

# POST API: 격려 메시지 업로드
@router.post("/upload_encouragement_message")
def upload_encouragement_message(data: EncouragementMessage):
    try:
        doc_id = f"{data.type}_{data.step}"
        db.collection("encouragement_messages").document(doc_id).set(data.dict())
        return {"status": "ok", "doc_id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# GET API: 격려 메시지 조회
@router.get("/encouragement/{type}/{step}")
def get_encouragement_message(type: str, step: int):
    try:
        doc_id = f"{type}_{step}"
        doc = db.collection("encouragement_messages").document(doc_id).get()

        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="격려 메시지를 찾을 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
