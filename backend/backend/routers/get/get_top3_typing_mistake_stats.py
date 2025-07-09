# 타자연습 최다 오답 Top3
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse  
from collections import Counter
from firebase_init import db

router = APIRouter()

@router.get("/stats/typing_mistake_top3")
def get_typing_mistake_top3():
    try:
        docs = db.collection("typing_mistakesbackup_byuser").stream()
        mistake_counter = Counter()

        for doc in docs:
            data = doc.to_dict()
            wrong_list = data.get("wrong_selections", [])

            for item in wrong_list:
                question = item.get("question")
                selected = item.get("selected")
                if question and selected:
                    key = f"{question} → {selected}"
                    mistake_counter[key] += 1

        top_3 = mistake_counter.most_common(3)
        result = {
            f"{i+1}) {item[0]}": f"{item[1]}회"
            for i, item in enumerate(top_3)
        }

        response_data = {
            "category": "타자연습",
            "message": "가장 많이 틀린 항목 Top 3",
            "top_3_mistakes": result
        }

        return JSONResponse(
            content=response_data,
            media_type="application/json; charset=utf-8"  # 한글 인코딩 
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

