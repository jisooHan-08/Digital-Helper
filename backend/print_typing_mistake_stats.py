from firebase_admin import firestore, credentials, initialize_app
from collections import Counter, defaultdict
from datetime import datetime

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)
db = firestore.client()

# 틀린 글자에 <span> 씌우기
def highlight_mistakes(correct, typed):
    result = []
    for c, t in zip(correct, typed):
        if c != t:
            result.append(f'<span style="color:red">{t}</span>')
        else:
            result.append(t)
    # 남은 글자도 처리
    if len(typed) > len(correct):
        for t in typed[len(correct):]:
            result.append(f'<span style="color:red">{t}</span>')
    return ''.join(result)

# 틀린 글자 수 계산
def count_wrong_chars(correct, typed):
    count = 0
    for c, t in zip(correct, typed):
        if c != t:
            count += 1
    count += abs(len(correct) - len(typed))
    return count

# 통계 수집 함수
def get_typing_stats():
    collection = "test_typing_mistakes"
    docs = db.collection(collection).stream()

    stats = {
        "1": Counter(),
        "2": Counter(),
        "3": Counter(),
        "sentence": Counter(),
        "paragraph": Counter()
    }

    wrong_chars = {
        "sentence": defaultdict(int),
        "paragraph": defaultdict(int)
    }

    for doc in docs:
        data = doc.to_dict()
        mistakes = data.get("mistakes", [])
        for m in mistakes:
            mode = m.get("mode")
            correct = m.get("correct", "")
            typed = m.get("typed", "")
            key = typed

            if mode in ["1", "2", "3"]:
                stats[mode][key] += 1
            elif mode in ["sentence", "paragraph"]:
                stats[mode][key] += 1
                wrong_chars[mode][key] = count_wrong_chars(correct, typed)

    return stats, wrong_chars

# 출력 함수
def print_stats():
    stats, wrong_chars = get_typing_stats()

    print("\n[타자연습 ( 1 글자 )] 가장 많이 틀린 단어는?")
    for i, (k, v) in enumerate(stats["1"].most_common(3), 1):
        print(f"{i}) {k} → {v}회")
    print("=" * 50)

    print("\n[타자연습 ( 2 글자 )] 가장 많이 틀린 단어는?")
    for i, (k, v) in enumerate(stats["2"].most_common(3), 1):
        print(f"{i}) {k} → {v}회")
    print("=" * 50)

    print("\n[타자연습 ( 3 글자 )] 가장 많이 틀린 단어는?")
    for i, (k, v) in enumerate(stats["3"].most_common(3), 1):
        print(f"{i}) {k} → {v}회")
    print("=" * 50)

    print("\n[타자연습 ( 한 문장 )] 가장 많이 틀린 문장은?")
    for i, (k, v) in enumerate(stats["sentence"].most_common(3), 1):
        error = wrong_chars["sentence"][k]
        print(f"{i}) {k} → {v}회 ( 틀린 글자수 : {error} )")
    print("=" * 50)

    print("\n[타자연습 ( 한 문단 )] 틀린 글자가 가장 많은 문단은?")
    for i, (k, v) in enumerate(stats["paragraph"].most_common(3), 1):
        error = wrong_chars["paragraph"][k]
        print(f"{i}) {k} → {v}회 ( 틀린 글자수 : {error} )")
    print("=" * 50)

if __name__ == "__main__":
    print_stats()
