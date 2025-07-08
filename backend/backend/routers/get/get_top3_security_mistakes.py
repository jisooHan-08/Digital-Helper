# 보안 퀴즈 최다 오답 Top3
from fastapi import APIRouter, HTTPException, Request
from collections import Counter
from firebase_init import db

router = APIRouter()

@router.get("/security_education/mistake/top3")
def get_top3_security_mistakes(request: Request):
    user_id = request.headers.get("user-id")

    if not user_id:
        raise HTTPException(status_code=400, detail="user-id 헤더가 누락되었습니다.")

    doc = db.collection("security_quiz_mistakesbackup_byuser").document(user_id).get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail=f"{user_id}에 대한 오답 기록이 없습니다.")

    data = doc.to_dict()
    wrong_cases = data.get("wrong_cases", [])

    # mistake 필드 기준으로 카운트
    counter = Counter()
    for item in wrong_cases:
        mistake = item.get("mistake")
        if mistake:
            counter[mistake] += 1

    top3 = counter.most_common(3)

    result = {
        "title": "[보안퀴즈] 가장 자주 틀린 문제는?",
        "user_id": user_id,
        "top_3_mistakes": [
            f"{i+1}) {mistake} → {cnt}회" for i, (mistake, cnt) in enumerate(top3)
        ]
    }

    return result
