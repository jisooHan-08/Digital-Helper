from firebase_admin import firestore, credentials, initialize_app
from collections import Counter, defaultdict

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

def get_security_quiz_stats():
    collection = "test_security_quiz_mistake"
    docs = db.collection(collection).stream()

    counter = Counter()
    explanations = dict()

    for doc in docs:
        data = doc.to_dict()
        mistakes = data.get("wrong_selections", [])
        for item in mistakes:
            question = item.get("question", "")
            explanation = item.get("explanation", "")
            if question:
                counter[question] += 1
                explanations[question] = explanation  # 항상 마지막 값으로 갱신

    return counter.most_common(3), explanations

def print_security_stats():
    print("\n[보안퀴즈] 가장 자주 틀린 문제는?")
    stats, explanations = get_security_quiz_stats()
    for i, (question, count) in enumerate(stats, 1):
        explanation = explanations.get(question, "해설 정보 없음")
        print(f"{i}) {question} → {count}회")
        print(f"해당 문제 해설: {explanation}\n")

if __name__ == "__main__":
    print_security_stats()
