from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from firebase_init import db
from firebase_admin import firestore

router = APIRouter()

class TypingMistake(BaseModel):
    scenario_id: str
    step_index: int
    question: str
    selected: str

@router.post("/upload_typing_mistake")
def upload_typing_mistake(request: Request, mistake: TypingMistake):
    user_id = request.headers.get("user-id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user-id 헤더가 누락되었습니다.")

    data = {
        "scenario_id": mistake.scenario_id,
        "step_index": mistake.step_index,
        "question": mistake.question,
        "selected": mistake.selected,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        db.collection("typing_mistakesbackup_byuser").document(user_id).set({
            "wrong_selections": firestore.ArrayUnion([data])
        }, merge=True)

        return {"status": "ok", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

