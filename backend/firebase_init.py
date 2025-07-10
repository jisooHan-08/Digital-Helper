import firebase_admin
from firebase_admin import credentials, firestore

# 중복 초기화 방지
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
