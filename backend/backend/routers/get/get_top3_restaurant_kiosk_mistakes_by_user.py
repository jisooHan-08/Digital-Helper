# 식당 키오스크 사용자별 오답 Top3
from fastapi import APIRouter, HTTPException, Request
from collections import Counter
from firebase_init import db

router = APIRouter()

@router.get("/restaurant-kiosk/mistake/top3")
def get_top3_restaurant_mistakes(request: Request):
    user_id = request.headers.get("user-id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user-id 헤더가 누락되었습니다.")

    doc = db.collection("restaurant_kiosk_mistakesbackup_byuser").document(user_id).get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail=f"{user_id}에 대한 오답 기록이 없습니다.")

    data = doc.to_dict()
    mistakes = data.get("wrong_selections", [])

    # 질문 + 선택 기준으로 카운트
    counter = Counter()
    for item in mistakes:
        question = item.get("question")
        selected = item.get("selected")
        if question and selected:
            key = f"{question} (선택: {selected})"
            counter[key] += 1

    # 상위 3개 추출
    top3 = counter.most_common(3)

    result = {
        "title": "[ 키오스크 연습(식당) ] 가장 많이 틀린 구간은?",
        "user_id": user_id,
        "top_3_mistakes": [
            f"{i+1}) {q} → {cnt}회" for i, (q, cnt) in enumerate(top3)
        ]
    }

    return result
