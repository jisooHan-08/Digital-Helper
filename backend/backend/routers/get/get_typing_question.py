# routers/get/get_typing_question.py

from fastapi import APIRouter, HTTPException
from firebase_admin import firestore
from firebase_init import db  # 이미 initialize_app() 되어 있다고 가정

router = APIRouter()

# mode => 컬렉션 이름 매핑
MODE_COLLECTION_MAP = {
    "one": "typing_practice_one_letter_questions",
    "two": "typing_practice_two_letter_questions",
    "three": "typing_practice_three_letter_questions",
    "sentence": "typing_practice_sentence_questions",
    "paragraph": "typing_practice_paragraph_questions",
}

# 특정 타자 연습 문제(step)를 가져오는 라우터
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

        return doc.to_dict()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
