# get_main_screen_entry.py

from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from firebase_init import db  

router = APIRouter()

@router.get("/main-screen-entry")
def get_main_screen_entry():
    try:
        doc_ref = db.collection("main_screen_entry").document("step_0")
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="step_0 문서가 존재하지 않습니다.")

        data = doc.to_dict()
        return {
            "context": data.get("context"),
            "instruction": data.get("instruction"),
            "helper_message": data.get("helper_message"),
            "options": data.get("options"),
            "next_step": data.get("next_step"),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
