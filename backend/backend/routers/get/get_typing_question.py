# routers/get/get_typing_question.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse  
from firebase_admin import firestore
from firebase_init import db

router = APIRouter()

MODE_COLLECTION_MAP = {
    "one": "typing_practice_one_letter_questions",
    "two": "typing_practice_two_letter_questions",
    "three": "typing_practice_three_letter_questions",
    "sentence": "typing_practice_sentence_questions",
    "paragraph": "typing_practice_paragraph_questions",
}

@router.get("/typing_question/{mode}/{step_id}")
def get_typing_question(mode: str, step_id: str):
    """
    타자 연습 문제 조회 API
    - mode: one, two, three, sentence, paragraph 중 하나
    - step_id: 예) step_1000, step_2001 등
    """
    try:
        if mode not in MODE_COLLECTION_MAP:
            raise HTTPException(status_code=400, detail="올바르지 않은 mode 값입니다.")

        collection_name = MODE_COLLECTION_MAP[mode]
        doc_ref = db.collection(collection_name).document(step_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="해당 문제(step)가 존재하지 않습니다.")

        return JSONResponse(
            content=doc.to_dict(),
            media_type="application/json; charset=utf-8"  # 한글 깨짐 방지
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
