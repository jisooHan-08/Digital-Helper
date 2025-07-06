from fastapi import APIRouter, HTTPException, Query
from firebase_init import db

router = APIRouter()

# GET 
@router.get("/encouragement")
def get_encouragement_by_step(step: int = Query(..., description="시나리오 단계 번호")):
    try:
        docs = db.collection("encouragement_messages").where("step", "==", step).stream()
        results = [doc.to_dict() for doc in docs]

        if not results:
            raise HTTPException(status_code=404, detail="404: 해당 step에 대한 격려 메시지가 없습니다.")

        return results[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
