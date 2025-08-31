#!/usr/bin/env python3
"""
환경변수 테스트 스크립트
"""

import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 키 확인
api_key = os.getenv('PADLET_API_KEY')

if api_key:
    print("[SUCCESS] API key loaded successfully!")
    print(f"   Key starts with: {api_key[:10]}...")
    print(f"   Key length: {len(api_key)}")
else:
    print("[ERROR] API key not found.")
    print("   Check if .env file exists.")
    print("   Format should be: PADLET_API_KEY=pdltp_xxx...")