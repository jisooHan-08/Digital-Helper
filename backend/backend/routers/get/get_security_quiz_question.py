from fastapi import APIRouter, HTTPException, Query
from firebase_init import db

router = APIRouter()

@router.get("/security_quiz/question")
def get_security_quiz_question(
    quiz_id: int = Query(1, description="현재 문제 번호, 기본값은 1"),
    next: bool = Query(False, description="true면 다음 문제로 이동")
):
    # 시작 시 → 자동으로 1번부터 시작 / 다음 문제 이동 시 +1
    target_id = str(quiz_id + 1 if next else quiz_id)

    doc = db.collection("security_quiz_questions").document(target_id).get()

    if not doc.exists:
        return {
            "status": "end",
            "message": f"{'다음 문제' if next else '해당 문제'}를 찾을 수 없습니다."
        }

    data = doc.to_dict()
    return {
        "status": "ok",
        "quiz_id": target_id,
        "question": data.get("question"),
        "choices": data.get("choices"),
        "answer": data.get("answer"),
        "explanation": data.get("explanation")
    }
