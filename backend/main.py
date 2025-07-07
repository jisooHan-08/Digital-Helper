from fastapi import FastAPI
from backend.routers import upload_typing_mistake
from backend.routers import stats_placeholder
from backend.routers import upload_encouragement_message
from backend.routers import get_typing_encouragement
from backend.routers import get_security_feedback_by_question
from backend.routers import get_encouragement_message

app = FastAPI()

# 라우터 등록
app.include_router(upload_typing_mistake.router)
app.include_router(stats_placeholder.router)
app.include_router(upload_encouragement_message.router)
app.include_router(get_typing_encouragement.router)
app.include_router(get_security_feedback_by_question.router)
app.include_router(get_encouragement_message.router) 


@app.get("/")
def root():
    return {"message": "디지털 도우미 백엔드 API 서버입니다"}
