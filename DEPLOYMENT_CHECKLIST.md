# 🚀 Streamlit Cloud 배포 체크리스트

## 1️⃣ GitHub 업로드
```bash
git add .
git commit -m "Ready for Streamlit deployment"
git push origin main
```

## 2️⃣ Streamlit Cloud 설정
- [ ] https://share.streamlit.io 접속
- [ ] GitHub로 로그인
- [ ] "New app" 클릭
- [ ] Repository 선택
- [ ] Branch: main
- [ ] Main file: streamlit_app.py
- [ ] Deploy 클릭

## 3️⃣ 환경변수 설정
Secrets 탭에서:
```
PADLET_API_KEY = "your-key-here"
```

## 4️⃣ 배포 확인
- [ ] 앱 URL 접속 테스트
- [ ] GPS 기능 테스트
- [ ] KMZ 다운로드 테스트
- [ ] Padlet 업로드 테스트

## 📱 공유 URL
```
https://[your-app-name].streamlit.app
```

## 🔧 문제 해결
- 로그 확인: Manage app > Logs
- 재배포: GitHub push 시 자동
- 리소스: 무료 플랜 1GB/월