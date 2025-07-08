from fastapi import APIRouter, HTTPException
from firebase_init import db

router = APIRouter()

@router.get("/typing_encouragement/{level}/{result}")
def get_typing_encouragement(level: str, result: str):
    doc_id = f"{level}_{result}"
    try:
        doc_ref = db.collection("typing_encouragements").document(doc_id)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="격려 메시지를 찾을 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
