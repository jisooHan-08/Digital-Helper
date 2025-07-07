from firebase_admin import firestore, credentials, initialize_app
from collections import Counter

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

def get_sorted_restaurant_mistakes():
    collection_name = "test_restaurant_kiosk_mistakes"
    docs = db.collection(collection_name).stream()

    counter = Counter()

    for doc in docs:
        data = doc.to_dict()
        mistakes = data.get("mistakes", [])
        for m in mistakes:
            question = m.get("question", "")
            selected = m.get("selected", "")
            if question and selected:
                key = f"{question} (선택: {selected})"
                counter[key] += 1

    return counter.most_common(3)

def print_mistake_stats():
    print("\n[ 키오스크 연습(식당) ] 가장 많이 틀린 구간은?")
    top_mistakes = get_sorted_restaurant_mistakes()
    for i, (desc, count) in enumerate(top_mistakes, start=1):
        print(f"{i}) {desc} → {count}회")

if __name__ == "__main__":
    print_mistake_stats()
