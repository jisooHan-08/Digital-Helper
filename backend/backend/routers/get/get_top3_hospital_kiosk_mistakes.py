# 병원 키오스크 최다 오답 Top3
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse  
from firebase_admin import firestore
from collections import Counter

router = APIRouter()
db = firestore.client()

@router.get("/hospital-kiosk/mistake/top3")
def get_top3_mistakes(request: Request):
    user_id = request.headers.get("user-id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user-id 헤더가 누락되었습니다.")

    doc_ref = db.collection("hospital_kiosk_mistakesbackup_byuser").document(user_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail=f"{user_id}에 대한 오답 기록이 없습니다.")

    data = doc.to_dict()
    mistakes = data.get("wrong_selections", [])

    counter = Counter()
    for item in mistakes:
        question = item.get("question")
        selected = item.get("selected")
        if question and selected:
            key = f"{question} (선택: {selected})"
            counter[key] += 1

    top3 = counter.most_common(3)

    result = [f"{i+1}) {q} → {cnt}회" for i, (q, cnt) in enumerate(top3)]

    return JSONResponse(
        content={
            "title": "[ 키오스크 연습(병원) ] 가장 많이 틀린 구간은?",
            "user_id": user_id,
            "result": result
        },
        media_type="application/json; charset=utf-8"  # 한글 출력 보장
    )
