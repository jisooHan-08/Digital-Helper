# get_typing_result_summary.py
# result_type: correct, minor_mistake, major_mistake 중 하나
# 해당 결과에 해당하는 문제 목록만 필터링해서 반환

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse  
from firebase_init import db

router = APIRouter()

@router.get("/typing_review_by_result/{user_id}/{result_type}")
def get_typing_review_by_result(user_id: str, result_type: str):
    try:
        doc = db.collection("typing_result_by_user").document(user_id).get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail="해당 사용자 기록이 없습니다.")

        data = doc.to_dict()
        result_list = data.get("result_list", [])
        filtered = [item for item in result_list if item.get("result") == result_type]

        return JSONResponse(
            content={
                "status": "success",
                "result_type": result_type,
                "count": len(filtered),
                "problems": filtered
            },
            media_type="application/json; charset=utf-8"  # 한글 깨짐 방지
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
