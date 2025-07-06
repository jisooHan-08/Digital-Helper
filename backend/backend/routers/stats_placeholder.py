from fastapi import APIRouter, HTTPException
from collections import Counter
from firebase_init import db

router = APIRouter()

@router.get("/stats/typing_mistake_top3")
def get_typing_mistake_top3():
    try:
        # Firestore에서 모든 타자연습 오답 문서 가져오기
        docs = db.collection("typing_mistakes").stream()

        mistake_counter = Counter()

        for doc in docs:
            data = doc.to_dict()
            question = data.get("question")
            selected = data.get("selected")
            if question and selected:
                key = f"{question} → {selected}"
                mistake_counter[key] += 1

        # 가장 많이 틀린 항목 3개 추출
        top_3 = mistake_counter.most_common(3)

        result = {
            f"{i+1}) {item[0]}": f"{item[1]}회"
            for i, item in enumerate(top_3)
        }

        return {
            "category": "타자연습",
            "message": "가장 많이 틀린 항목 Top 3",
            "top_3_mistakes": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
