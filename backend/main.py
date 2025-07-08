from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 실제 사용하는 라우터만 import
from backend.routers.get import (
    get_hospital_kiosk_db_steps,
    get_security_quiz_feedback_message,
    get_top3_typing_mistake_stats,
    get_typing_encouragement,
    get_typing_feedback_message,
    get_hospital_kiosk_mistake_feedback,
    get_restaurant_kiosk_mistake_feedback,
    get_top3_restaurant_kiosk_mistakes_by_user,
    get_security_mistake_feedback,
    get_top3_security_mistakes,
    get_security_quiz_question,


)

from backend.routers.post import (
    post_security_education_mistake,
    post_typing_mistake_api,
    post_hospital_kiosk_mistake,
    post_restaurant_kiosk_mistake,
)

app = FastAPI()

# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"] 등 실제 프론트 주소만 허용 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GET 라우터 등록
app.include_router(get_hospital_kiosk_db_steps.router)
app.include_router(get_security_quiz_feedback_message.router)
app.include_router(get_top3_typing_mistake_stats.router)
app.include_router(get_typing_encouragement.router)
app.include_router(get_typing_feedback_message.router)
app.include_router(get_hospital_kiosk_mistake_feedback.router)
app.include_router(get_restaurant_kiosk_mistake_feedback.router)
app.include_router(get_top3_restaurant_kiosk_mistakes_by_user.router)
app.include_router(get_security_mistake_feedback.router)
app.include_router(get_top3_security_mistakes.router)
app.include_router(get_security_quiz_question.router)


# POST 라우터 등록
app.include_router(post_typing_mistake_api.router)
app.include_router(post_security_education_mistake.router)
app.include_router(post_hospital_kiosk_mistake.router)
app.include_router(post_restaurant_kiosk_mistake.router)

# 기본 루트 엔드포인트
@app.get("/")
def root():
    return {"message": "디지털 도우미 백엔드 API 서버입니다"}
