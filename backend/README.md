 디지털 적응 도우미 앱 백엔드 작업 내역 정리
 백엔드 코드는 Firebase Firestore를 기반으로 사용자 오답 데이터를 업로드하고, 통계를 출력하는 기능을 제공합니다.

 
== 개발 환경 및 기반 ==
개발 툴: VS Code
언어: Python
데이터베이스: Firebase Firestore
연동 모듈: firebase_admin, firestore, datetime, random, string

1. Firebase Firestore 연동
   모든 .py 파일과 같은 디렉토리에 위치해야 Firebase가 정상 작동
   모든 파일에 firebase_admin 초기화 코드 포함
   초기설정 내용
      - 사용자 ID 자동 생성 형식:
         20250703_xxxxx (날짜 + 5자리 랜덤 문자열)
      -timestamp 기록:
        UTC 기준 ISO 8601 형식으로 저장됨
        (datetime.utcnow().isoformat() + "Z")

2. 오답 데이터 업로드 기능 - 오답 저장 (총 9개)
( 파일명	 / 설명	/ Firestore 컬렉션 저장명 )
( test_upload_hospital_mistake.py	/ 병원 키오스크 오답 업로드	 / test_hospital_kiosk_mistakes)
( test_upload_restaurant_mistake.py	/ 식당 키오스크 오답 업로드	 / test_restaurant_kiosk_mistakes)
( test_upload_typing_mistake.py	/ 타자 연습 오답 업로드	 / test_typing_mistakes)
( test_upload_sec_quiz_mistake.py	/ 보안 퀴즈 오답 업로드 / test_security_quiz_mistake)

( upload_all.py	/ 위 4개를 한 번에 실행하는 통합 업로드 / - ) 	
( upload_hospital_kiosk_mistake_batch.py	/ 병원 오답 일괄 업로드	 /  - ) 
( upload_restaurant_kiosk_mistake_batch.py	/ 식당 오답 일괄 업로드		 /  - ) 
( upload_typing_mistake_batch.py	/ 타자연습 오답 일괄 업로드		 /  - ) 
( upload_mistake_batch.py	/ 통합 일괄 업로드		 /  - ) 

이때 사용자 ID는 20250703_xxxxx 형식으로 자동 생성
     모든 업로드에 UTC 기반 timestamp 포함됨
     Firestore에는 각 오답을 ArrayUnion 형식으로 누적 저장

3. 오답 통계 출력 기능
   ( 파일명 / 설명 / 출력 형식 )

( `print_hospital_mistake_stats.py` / 병원 키오스크 오답 상위 3개 출력 / [키오스크 연습(병원)]가장 많이 틀린 구간은?...) 
( `print_restaurant_mistake_stats.py` / 식당 키오스크 오답 상위 3개 출력 / [ 키오스크 연습(식당) ] 가장 많이 틀린 구간은?...)
( `print_typing_mistake_stats.py` / 타자 연습 (1글자부터 3글자까지 /문장/문단) 오답 통계 / 카테고리별 3개 + 틀린 글자수 + 문장/문단은 틀린 글자 빨간색 표시)
( `print_security_quiz_stats.py` / 보안 퀴즈 문제별 오답 순위(1위부터 3위까지) 및 해설 출력 / 문제 + 해설 형태로 정리 출력)

   이때 통계는 누적 데이터 기준으로 자동 계산
        출력 포맷은 팀 내부 결정사항에 맞춰 구성됨
         - `print_hospital_mistake_stats.py`  
            → 병원 키오스크에서 가장 많이 틀린 질문 출력 (상위 3개)

        - `print_restaurant_mistake_stats.py`  
            → 식당 키오스크에서 가장 많이 틀린 질문 출력

        - `print_typing_mistake_stats.py`  
           → 1글자, 2글자, 3글자, 문장, 문단 오답 통계 출력  
           → 문장/문단은 틀린 글자수 계산되고, 틀린 글자 빨간색 표시까지 지원

        - `print_security_quiz_stats.py`  
           → 자주 틀린 보안 퀴즈 문제 상위 3개 출력 + 각 문제의 해설 제공

  => Firestore에 실제로 저장된 오답 통계 관련 컬렉션
       저장된 컬렉션:
           test_hospital_kiosk_mistakes
 
           test_restaurant_kiosk_mistakes

           test_typing_mistakes

           test_security_quiz_mistake
모든 업로드는 Firestore 콘솔에서 정상 확인 완료

4. 오답 피드백 기능 (보안 퀴즈, 키오스크( 병원, 식당 ), 타자 연습 포함)
    - `generate_security_quiz_feedback.py`  
     → 보안 퀴즈 오답 데이터를 분석하여 문제별 해설(피드백)을 자동 생성  
     → 생성된 피드백은 Firestore에 저장되어 사용자별 조회가 가능함
   - `get_security_quiz_feedback_for_user.py`  
     → 특정 사용자의 보안 퀴즈 오답 데이터를 기반으로 해설을 조회함  
     → 추후 웹 API 혹은 서비스 화면으로 연동 가능
  - `print_hospital_mistake_stats.py`, `print_restaurant_mistake_stats.py`
     → 키오스크(병원, 식당)오답 데이터를 분석하여 통계 기반 피드백을 제공
     → 가장 많이 틀린 구간을 상위 3개 항목 기준으로 출력하며, 사용자 학습 개선에 활용 가능
  -`print_typing_mistake_stats.py`
     → 타자 연습 오답 데이터를 분석하여 통계 기반 피드백을 제공
     → 타자 연습의 경우 카테고리별(1~3글자/문장/문단) 오답률 분석 및 틀린 글자 시각화 포함
    
→ 각 연습 유형별 오답 피드백은 Firestore 저장 데이터를 기반으로 하며, 누적 데이터에 따라 자동 갱신됨

5. 격려 메시지 출력 기능 구현 (총 3종)
   : 격려 메시지는 모든 기능에 공통 적용됨: 키오스크(병원, 식당), 타자 연습, 보안 퀴즈

   - 업로드 파일: upload_encouragement_message.py, upload_typing_encouragements.py
                 upload_security_encouragements.py

출력 API 구현 완료:

  - GET /encouragement?step=... : 시나리오 기반 격려 메시지 조회

  - GET /typing_encouragement/{level}/{result} : 타자 연습 레벨 및 결과 기반 격려 메시지 조회

  - GET /security_encouragement/{result} : 보안 퀴즈 결과 기반 격려 메시지 조회


6. .gitignore 설정
   유출되면 안 되는 비공개 키 제외 성공

7. FastAPI 기반 API 구현

  앱 연동을 위한 백엔드 API를 FastAPI로 구현 완료

  전체 테스트 주소: http://127.0.0.1:8000/docs  - (Swagger UI)

  [완성된 주요 API 목록 (총 10개)]

    - 병원 키오스크 오답 업로드: POST /upload_hospital_mistake
      (POST http://127.0.0.1:8000/upload_hospital_mistake)
    - 식당 키오스크 오답 업로드: POST /upload_restaurant_mistake
      (http://127.0.0.1:8000/upload_restaurant_mistake)
    - 타자 연습 오답 업로드: POST /upload_typing_mistake
      (POST http://127.0.0.1:8000/upload_typing_mistake)
    - 보안 퀴즈 오답 업로드: POST /upload_security_quiz_mistake
      (http://127.0.0.1:8000/upload_security_quiz_mistake)
    - 격려 메시지 업로드: POST /upload_encouragement_message
      (http://127.0.0.1:8000/upload_encouragement_message)
    - 타자 격려 메시지 업로드: POST /upload_typing_encouragements
      (http://127.0.0.1:8000/upload_typing_encouragements)
    - 보안 격려 메시지 업로드: POST /upload_security_encouragements
      (http://127.0.0.1:8000/upload_security_encouragements)
    - 타자 연습 통계 조회: GET /stats/typing_mistake_top3
      (GET http://127.0.0.1:8000/stats/typing_mistake_top3)
    - 보안 퀴즈 통계 조회 및 해설: GET /security_quiz_stats
      (GET http://127.0.0.1:8000/security_quiz_stats)
    - 격려 메시지 조회: GET /encouragement?step=...
      (http://127.0.0.1:8000/encouragement?step=201)
→ FastAPI 문서 자동 생성 페이지에서 모든 테스트 확인 가능: http://127.0.0.1:8000/docs 

7. 그 외 수행한 백엔드 주요 작업

   - GitHub 업로드 완료
   -전체 backend 디렉토리 구조 정리 및 commit
   -업로드 메시지에 작업 내역 명시
   -README.md 작성 예정 (내 역할 기준)
   -VSCode로 Firebase 업로드 정상 실행 확인 (터미널 결과까지 검증)
   -오류 발생 시 DeprecationWarning, 파일 경로 문제 디버깅
   -Firestore 콘솔에서 업로드 확인 및 컬렉션 구조 점검 완료



   

