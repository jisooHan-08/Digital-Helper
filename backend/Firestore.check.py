import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 전체 컬렉션 이름 리스트 조회
collections = db.collections()
print("현재 Firestore에 존재하는 컬렉션 목록:")

for col in collections:
    print(f" - {col.id}")
