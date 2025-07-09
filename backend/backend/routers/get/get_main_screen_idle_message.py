# get_main_screen_idle_message.py
# 앱 실행 중 아무 입력 없이 2분 이상 멈춰 있을 경우 안내 메시지를 랜덤으로 제공하는 라우터

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse  
from firebase_init import db
import random

router = APIRouter()

@router.get("/main-screen-idle-message")
def get_main_screen_idle_message():
    try:
        doc_ids = ["0", "default"]
        chosen_id = random.choice(doc_ids)

        doc_ref = db.collection("idle_helper_messages").document(chosen_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"{chosen_id} 문서가 존재하지 않습니다.")

        data = doc.to_dict()

        return JSONResponse(
            content={
                "source": chosen_id,
                "message": data.get("message", "")
            },
            media_type="application/json; charset=utf-8"  # 인코딩 명시
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")

