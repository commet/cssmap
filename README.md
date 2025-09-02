# 🎨 헤맨만큼 내 땅이다 - CSS Art Map Project

프리즈·키아프 기간 동안 미술애호가들의 전시 관람 경험을 Padlet 지도에 기록하고 공유하는 참여형 플랫폼

## 📌 프로젝트 개요

"헤맨만큼 내 땅이다"는 2025년 9월 1-7일 프리즈·키아프 기간 동안 관람객들이 자신의 전시 경험을 온라인 지도에 실시간으로 기록하고 공유하는 인터랙티브 프로젝트입니다.

### 주요 기능
- 🗺️ **위치 기반 경험 공유**: Padlet 지도에 감정과 함께 경험 기록
- 📊 **실시간 통계**: 인기 장소, 감정 분포, 트렌딩 키워드 분석  
- 🤖 **자동화 시스템**: 24/7 모니터링, 백업, 모더레이션
- 💬 **커뮤니티 상호작용**: 댓글, 팁 공유, 공감

## 🚀 시작하기

### 필수 요구사항
- Python 3.8+
- Padlet API 키 (유료 구독 필요)
- 보드 관리자 권한

### 설치

```bash
# 1. 저장소 클론
git clone https://github.com/commet/cssmap.git
cd cssmap

# 2. 패키지 설치
pip install -r requirements.txt

# 3. 환경 변수 설정
# .env 파일 생성 후 API 키 입력
PADLET_API_KEY=your_api_key_here
```

## 💻 사용법

### 📺 사용 안내 영상: https://buly.kr/1xzE29j

### 1. 테스트 실행
```bash
python test_padlet_now.py
```

### 2. 실제 시나리오 실행
```bash
python css_art_map_project.py
```

### 3. 자동화 시스템 시작
```bash
python css_automated_manager.py
# 옵션 1: 24/7 모니터링
# 옵션 3: 현재 통계 분석
# 옵션 4: 일일 리포트
# 옵션 5: 행사 당일 모드
```

### 4. 대시보드 보기
브라우저에서 `simple_dashboard.html` 열기

## 📁 프로젝트 구조

```
cssmap/
├── padlet_api_complete.py      # Padlet API 클라이언트
├── css_art_map_project.py      # 실제 사용 시나리오
├── css_automated_manager.py    # 자동화 관리 시스템
├── test_padlet_now.py          # 즉시 테스트 도구
├── simple_dashboard.html       # 웹 대시보드
├── requirements.txt            # 패키지 의존성
├── .env                       # API 키 (gitignore)
└── README.md                  # 프로젝트 문서
```

## 🗓️ 운영 계획

### Phase 1: 사전 준비 (8/29-31)
- 시스템 테스트 및 검증
- 초기 데이터 시딩

### Phase 2: 행사 기간 (9/1-3)
- 24시간 자동 데이터 수집
- 실시간 통계 생성
- 콘텐츠 모더레이션

### Phase 3: 행사 당일 (9/4)
- "관람객의 밤" 라이브 모드
- 실시간 대시보드 운영
- 현장 인터랙션

### Phase 4: 사후 분석 (9/5-7)
- 최종 리포트 생성
- 데이터 아카이빙
- 인사이트 도출

## 📊 주요 통계 지표

- 총 참여자 수
- 인기 장소 TOP 5
- 감정 분포 (😍 😴 💸 🤔 👍)
- 시간대별 활동량
- 트렌딩 키워드

## 🔒 보안 및 개인정보

- API 키는 절대 커밋하지 않습니다
- 개인정보는 수집하지 않습니다
- 부적절한 콘텐츠는 자동 필터링됩니다

## 🤝 기여하기

이슈와 PR을 환영합니다!

## 📝 라이선스

MIT License

## 📧 문의

CSS 2025 Team

---

**"헤맨만큼 내 땅이다" - 당신의 발자취가 지도가 됩니다**