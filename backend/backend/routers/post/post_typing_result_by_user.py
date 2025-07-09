# post_typing_result_by_user.py - [전체 결과 요약 저장용 API]
# 각 문제에 대해 step, level, result(correct/minor_mistake/major_mistake)와 함께 저장
# 사용자가 타자 연습을 완료한 뒤, 여러 문제들의 결과를 한 번에 Firestore에 저장
# 사용자의 전체 연습 결과를 분석 및 통계 목적으로 저장 - (post_typing_mistake_api.py)와 병행 사용

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse  
from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime, timezone

from firebase_init import db  # Firebase 초기화 포함된 모듈

router = APIRouter()

# 1. 개별 문제 결과 구조 정의
class TypingResultItem(BaseModel):
    step: int  # 문제 step 번호
    level: Literal["beginner", "intermediate", "advanced"]  # 난이도
    result: Literal["correct", "minor_mistake", "major_mistake"]  # 결과 분류

# 2. 전체 업로드 구조 정의
class TypingResultUploadRequest(BaseModel):
    user_id: str  # 사용자 자동 생성 ID
    result_list: List[TypingResultItem]  # 여러 문제의 결과 리스트

# 3. 결과 저장 라우터
@router.post("/typing_result_by_user")
def upload_typing_result(data: TypingResultUploadRequest):
    """
    타자 연습 결과 업로드 API
    - 기존 결과에 누적 저장됨
    - user_id는 자동 생성한 ID 기반
    """
    try:
        doc_ref = db.collection("typing_result_by_user").document(data.user_id)

        # 기존 데이터 불러오기
        existing_doc = doc_ref.get()
        existing_data = existing_doc.to_dict() if existing_doc.exists else {}
        result_list = existing_data.get("result_list", [])

        # 새로운 결과 추가
        for item in data.result_list:
            result_list.append({
                "step": item.step,
                "level": item.level,
                "result": item.result,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        # Firestore에 저장
        doc_ref.set({
            "user_id": data.user_id,
            "result_list": result_list
        })

        return JSONResponse(  # 한글 깨짐 방지
            content={
                "status": "success",
                "user_id": data.user_id,
                "total_results": len(result_list),
                "message": "타자 연습 결과가 저장되었습니다."
            },
            media_type="application/json; charset=utf-8"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
