# 병원 키오스크 시나리오 단계 조회
# routers/get/get_hospital_kiosk_db_steps.py
from fastapi import APIRouter, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore

router = APIRouter()

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 1. 전체 병원 키오스크 step 조회
@router.get("/hospital_kiosk/db_steps")
def get_all_hospital_steps():
    docs = db.collection("hospital_kiosk_fullflow").stream()
    all_steps = [doc.to_dict() for doc in docs]
    
    if not all_steps:
        raise HTTPException(status_code=404, detail="시나리오 데이터가 존재하지 않습니다.")

    # step_index 기준으로 정렬
    sorted_steps = sorted(all_steps, key=lambda x: x.get("step_index", 0))
    return {"steps": sorted_steps}

# 2. 특정 step_index로 조회
@router.get("/hospital_kiosk/db_steps/{step_index}")
def get_hospital_step(step_index: int):
    docs = db.collection("hospital_kiosk_fullflow").where("step_index", "==", step_index).stream()
    step_list = [doc.to_dict() for doc in docs]
    
    if not step_list:
        raise HTTPException(status_code=404, detail=f"{step_index}번 step이 존재하지 않습니다.")
    
    return step_list[0]  # 정확히 하나만 존재해야 하므로
