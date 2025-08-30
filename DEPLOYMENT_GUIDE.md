# 🚀 배포 가이드 - 헤맨만큼 내 땅이다

## 📊 배포 옵션 비교

### Option 1: **Streamlit Cloud** (추천) ⭐
**장점:**
- Python 코드 그대로 사용
- 실시간 데이터 연동
- 무료 (월 1GB 트래픽)
- GitHub 연동 자동 배포
- 모바일 반응형

**배포 방법:**
```bash
# 1. requirements.txt 업데이트
streamlit
plotly
fuzzywuzzy
python-Levenshtein
requests
python-dotenv
schedule

# 2. GitHub에 푸시
git add .
git commit -m "Add Streamlit app"
git push

# 3. streamlit.io/cloud 접속
# 4. "New app" → GitHub repo 연결
# 5. Main file: streamlit_app.py 선택
# 6. Deploy!
```

**환경변수 설정:**
Streamlit Cloud 대시보드에서 Secrets 추가:
```toml
PADLET_API_KEY = "your-api-key"
```

### Option 2: **Vercel** (정적 대시보드만)
**장점:**
- 매우 빠른 로딩
- 무료
- 커스텀 도메인

**제한사항:**
- Python 백엔드 불가
- 실시간 데이터 연동 어려움

**배포 방법:**
```bash
# 1. Vercel CLI 설치
npm i -g vercel

# 2. 프로젝트 루트에서
vercel

# 3. 설정 선택
# - Link to existing project? No
# - Project name: css-art-map
# - Directory: .
```

### Option 3: **Railway/Render** (풀스택)
**장점:**
- Python 백엔드 + 프론트엔드
- PostgreSQL 데이터베이스 포함
- 스케줄러 지원

**배포 방법:**
```bash
# Railway
railway login
railway init
railway up

# Render
# render.yaml 생성 후 GitHub 연동
```

## 🔗 사용자 입력 간소화 솔루션

### **최종 추천: Streamlit + 위치 자동완성**

**이유:**
1. **통합 환경**: 대시보드와 입력폼을 한 곳에서
2. **위치 자동완성**: Fuzzy matching으로 다양한 입력 처리
3. **즉각적 피드백**: 실시간 게시 확인
4. **모바일 최적화**: 반응형 디자인

**구현 완료 기능:**
- ✅ 위치명 자동 매칭 (국현 → 국립현대미술관)
- ✅ 감정 선택 UI
- ✅ 실시간 게시
- ✅ 성공/실패 피드백

### Google Forms 대안 분석

**Google Forms 한계:**
- ❌ 동적 자동완성 불가
- ❌ 실시간 검증 어려움
- ❌ 커스터마이징 제한

**대신 사용 가능한 서비스:**

#### 1. **Typeform** (유료)
```javascript
// Typeform Webhook 설정
{
  "form_response": {
    "answers": [
      {"field": "location", "text": "국제갤러리"},
      {"field": "emotion", "choice": "😍 감동"},
      {"field": "title", "text": "..."},
      {"field": "experience", "text": "..."}
    ]
  }
}
// → Lambda/Cloud Function → Padlet API
```

#### 2. **Airtable Forms** (무료 제한)
- 자동완성 지원
- 데이터베이스 직접 연동
- Zapier/Make 통합 가능

#### 3. **Tally Forms** (무료)
- 조건부 로직
- Webhook 지원
- 커스텀 도메인

## 📱 QR 코드 활용 전략

현장에서 쉽게 접근할 수 있도록:

```python
import qrcode

# QR 코드 생성
qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data('https://your-app.streamlit.app')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save('qr_code.png')
```

**QR 코드 배치 위치:**
- 프리즈/키아프 입구
- 주요 갤러리 앞
- CSS 부스
- 인쇄물/포스터

## 🔧 운영 체크리스트

### 배포 전:
- [ ] API 키 환경변수 설정
- [ ] 테스트 데이터 삭제
- [ ] 부적절한 단어 필터 업데이트
- [ ] 백업 스케줄 설정

### 배포 후:
- [ ] 모바일 테스트
- [ ] 로드 테스트 (100명 동시 접속)
- [ ] 모니터링 대시보드 설정
- [ ] 팀원 접근 권한 부여

### D-Day:
- [ ] 실시간 모니터링 시작
- [ ] 백업 주기 단축 (1시간 → 15분)
- [ ] 현장 QR 코드 배포
- [ ] 긴급 연락망 확인

## 💡 추가 개선 아이디어

1. **카카오톡 챗봇 연동**
   - 더 친숙한 인터페이스
   - 푸시 알림 가능

2. **Instagram 해시태그 수집**
   - #헤맨만큼내땅이다
   - 자동으로 Padlet에 추가

3. **AI 요약 리포트**
   - GPT API로 일일 하이라이트 생성
   - 인사이트 자동 추출

## 📞 문의

기술 지원이 필요하시면 연락주세요!

---
**"헤맨만큼 내 땅이다" - 당신의 발자취가 지도가 됩니다**