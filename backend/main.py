from fastapi import FastAPI

# 실제 사용하는 라우터들만 임포트
from backend.backend.routers import encouragement_message_api
from backend.backend.routers.get import get_security_quiz_feedback_message, get_top3_typing_mistake_stats, get_typing_encouragement, get_typing_feedback_message
from backend.backend.routers.post import post_typing_mistake_api
from backend.routers import (
    get_typing_mistake,
    get_hospital_kiosk_mistake_feedback,
    get_restaurant_kiosk_mistake_feedback,
    get_restaurant_kiosk_mistake,
    get_top3_hospital_kiosk_mistakes,
    get_top3_restaurant_kiosk_mistakes_by_user,
    get_top3_security_quiz_mistakes,
    get_security_quiz_encouragement_messages
)

app = FastAPI()

# 라우터 등록
app.include_router(post_typing_mistake_api.router)
app.include_router(encouragement_message_api.router)
app.include_router(get_typing_encouragement.router)
app.include_router(get_security_quiz_feedback_message.router)
app.include_router(get_typing_feedback_message.router)
app.include_router(get_typing_mistake.router)
app.include_router(get_top3_typing_mistake_stats.router)
app.include_router(get_hospital_kiosk_mistake_feedback.router)
app.include_router(get_restaurant_kiosk_mistake_feedback.router)
app.include_router(get_restaurant_kiosk_mistake.router)
app.include_router(get_top3_hospital_kiosk_mistakes.router)
app.include_router(get_top3_restaurant_kiosk_mistakes_by_user.router)
app.include_router(get_security_quiz_feedback_message.router)
app.include_router(get_top3_security_quiz_mistakes.router)
app.include_router(get_security_quiz_encouragement_messages.router)

@app.get("/")
def root():
    return {"message": "디지털 도우미 백엔드 API 서버입니다"}
