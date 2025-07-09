# 식당 시나리오 단계별 전체 반환
# restaurant_kiosk_fullflow 내에 저장된 각 step 문서를 불러와  
# helper_message, text, buttons, type, next 등의 흐름 정보 제공

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse  
from firebase_init import db

router = APIRouter()

@router.get("/restaurant-kiosk/steps")
def get_restaurant_kiosk_steps():
    """
    restaurant_kiosk_fullflow 컬렉션에 있는 전체 step 데이터를 리스트 형태로 반환
    """
    try:
        docs = db.collection("restaurant_kiosk_fullflow").stream()
        steps = []

        for doc in docs:
            data = doc.to_dict()
            data["step_id"] = doc.id  # 문서 ID를 step_id로 저장
            steps.append(data)

        if not steps:
            raise HTTPException(status_code=404, detail="식당 키오스크 시나리오가 없습니다.")

        return JSONResponse(
            content={"steps": steps},
            media_type="application/json; charset=utf-8"  # 한글 깨짐 방지
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
