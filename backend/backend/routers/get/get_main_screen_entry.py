# get_main_screen_entry.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse  
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

        # 문자열 변환 처리
        context = data.get("context", "")
        instruction = data.get("instruction", "")
        helper_message = data.get("helper_message", "")
        options = data.get("options", [])
        next_step = {str(k): v for k, v in data.get("next_step", {}).items()}

        return JSONResponse(
            content={
                "context": context,
                "instruction": instruction,
                "helper_message": helper_message,
                "options": options,
                "next_step": next_step,
            },
            media_type="application/json; charset=utf-8"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")

