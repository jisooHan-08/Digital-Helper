# get_main_screen_idle_message.py
# 앱 실행 중 아무 입력 없이 2분 이상 멈춰 있을 경우 안내 메시지를 랜덤으로 제공하는 라우터

from fastapi import APIRouter, HTTPException
from firebase_init import db
import random

router = APIRouter()

@router.get("/main-screen-idle-message")
def get_main_screen_idle_message():
    try:
        # Firestore에서 사용할 두 개의 문서 ID (사전 정의된 메시지)
        doc_ids = ["0", "default"]

        # ID 중 하나를 무작위로 선택
        chosen_id = random.choice(doc_ids)

        # 선택된 문서를 Firestore에서 가져옴
        doc_ref = db.collection("idle_helper_messages").document(chosen_id)
        doc = doc_ref.get()

        # 문서가 존재하지 않으면 오류 반환
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"{chosen_id} 문서가 존재하지 않습니다.")

        data = doc.to_dict()

        # 메시지 필드만 추출하여 반환
        return {
            "source": chosen_id,
            "message": data.get("message", "")
        }

    except Exception as e:
        # 예외 발생 시 500 오류 반환
        raise HTTPException(status_code=500, detail=f"오류 발생: {str(e)}")
