# 📚 Streamlit Cloud 배포 단계별 가이드

## 🔵 1단계: Streamlit Cloud 접속 및 로그인

1. 브라우저에서 **https://share.streamlit.io** 접속
2. **"Continue with GitHub"** 버튼 클릭
3. GitHub 계정으로 로그인
4. Streamlit이 GitHub 접근 권한 요청하면 **"Authorize streamlit"** 클릭

---

## 🔵 2단계: 새 앱 만들기

1. 로그인 후 대시보드에서 **"New app"** 버튼 클릭
2. 배포 옵션 선택:
   - **"From existing repo"** 선택 (이미 GitHub에 코드가 있으므로)

---

## 🔵 3단계: Repository 설정

다음 정보를 입력:

### Repository
- **Repository**: `commet/cssmap` 선택
  - 드롭다운에서 자동으로 나타남
  - 안 보이면 직접 입력

### Branch
- **Branch**: `main` 선택

### Main file path
- **Main file path**: `streamlit_app.py` 입력

### App URL (선택사항)
- 원하는 URL 설정 가능
- 예: `css-art-map` 입력하면
- 최종 URL: `https://css-art-map.streamlit.app`

---

## 🔵 4단계: Deploy 클릭

1. 모든 설정 확인 후 **"Deploy!"** 버튼 클릭
2. 배포 시작 - 보통 2-5분 소요
3. 화면에 로그가 표시되며 진행 상황 확인 가능

---

## 🔵 5단계: 환경변수(Secrets) 설정

### 앱이 배포되면:

1. 오른쪽 상단 **"⋮"** (세 점) 메뉴 클릭
2. **"Settings"** 선택
3. 왼쪽 메뉴에서 **"Secrets"** 탭 클릭
4. 텍스트 박스에 다음 입력:
```
PADLET_API_KEY = "여기에_실제_API_키_입력"
```
5. **"Save"** 버튼 클릭
6. 앱이 자동으로 재시작됨

---

## 🔵 6단계: 앱 테스트

1. 배포 완료 후 나타나는 URL 클릭
2. 또는 대시보드에서 앱 이름 클릭
3. 테스트 항목:
   - [ ] 페이지 정상 로드
   - [ ] GPS 위치 추가 기능
   - [ ] 지도 표시
   - [ ] KMZ 다운로드
   - [ ] Padlet 업로드 (API 키 설정 후)

---

## 🎯 배포 완료 후

### 앱 URL 공유
```
https://[your-app-name].streamlit.app
```
이 URL을 팀원들과 공유

### 앱 관리
- **View logs**: 실시간 로그 확인
- **Reboot app**: 앱 재시작
- **Delete app**: 앱 삭제

### 자동 업데이트
- GitHub에 push하면 자동으로 재배포
- 보통 1-2분 내 반영

---

## ⚠️ 문제 해결

### 배포 실패 시
1. **Logs** 확인하여 에러 메시지 확인
2. 주요 체크 사항:
   - `requirements.txt` 파일 존재 여부
   - `streamlit_app.py` 파일명 정확한지
   - Python 버전 호환성

### 앱이 느린 경우
- 무료 플랜 제한: 1GB 메모리, 1GB 트래픽/월
- 사용자가 많으면 유료 플랜 고려

### Secrets 관련 오류
- Secrets 형식 확인 (KEY = "value")
- 저장 후 앱 재시작 대기

---

## 📱 모바일 접속

배포된 URL은 모바일에서도 작동:
1. 스마트폰 브라우저에서 URL 입력
2. GPS 권한 허용
3. 바로 사용 가능

---

## 🎉 축하합니다!

이제 CSS Art Map이 온라인에 배포되었습니다!
누구나 URL로 접속하여 사용할 수 있습니다.