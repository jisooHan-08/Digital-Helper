from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import random
import string

from firebase_init import db

# 라우터 객체 생성
router = APIRouter()

# 요청 데이터 모델 정의
class TypingMistake(BaseModel):
    scenario_id: str
    step_index: int
    question: str
    selected: str

# 사용자 ID 생성 함수 (날짜 + 랜덤 5자리)
def generate_user_id():
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    return f"{date_part}_{random_part}"

# POST API: 타자연습 오답 업로드
@router.post("/upload_typing_mistake")
def upload_typing_mistake(mistake: TypingMistake):
    user_id = generate_user_id()

    data = {
        "scenario_id": mistake.scenario_id,
        "step_index": mistake.step_index,
        "question": mistake.question,
        "selected": mistake.selected,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    try:
        db.collection("typing_mistakes").document(user_id).set(data)
        return {
            "status": "ok",
            "user_id": user_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
