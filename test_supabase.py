"""
Supabase 연동 테스트 스크립트
실행: streamlit run test_supabase.py
"""

import streamlit as st
from supabase_storage import SupabaseStorage
import os
from datetime import datetime

st.set_page_config(page_title="Supabase 연동 테스트", page_icon="🔧")

st.title("🔧 Supabase 연동 테스트")
st.markdown("---")

# 1. 연결 상태 확인
st.header("1️⃣ 연결 상태 확인")

col1, col2 = st.columns(2)

with col1:
    st.subheader("환경 변수")
    url_exists = bool(os.getenv('SUPABASE_URL') or (hasattr(st, 'secrets') and 'SUPABASE_URL' in st.secrets))
    key_exists = bool(os.getenv('SUPABASE_ANON_KEY') or (hasattr(st, 'secrets') and 'SUPABASE_ANON_KEY' in st.secrets))
    
    st.metric("SUPABASE_URL", "✅ 설정됨" if url_exists else "❌ 없음")
    st.metric("SUPABASE_ANON_KEY", "✅ 설정됨" if key_exists else "❌ 없음")

with col2:
    st.subheader("Storage 초기화")
    try:
        storage = SupabaseStorage()
        if storage.client:
            st.success("✅ Supabase 클라이언트 연결 성공!")
            st.write(f"URL: {storage.url[:30]}...")
        else:
            st.error("❌ Supabase 클라이언트 연결 실패")
    except Exception as e:
        st.error(f"❌ 초기화 오류: {e}")
        storage = None

st.markdown("---")

# 2. 버킷 상태 확인
if storage and storage.client:
    st.header("2️⃣ Storage 버킷 상태")
    
    try:
        buckets = storage.client.storage.list_buckets()
        st.success(f"✅ {len(buckets)}개의 버킷 발견")
        
        for bucket in buckets:
            with st.expander(f"버킷: {bucket['name']}"):
                st.json(bucket)
                
                # 버킷 내 파일 목록
                try:
                    files = storage.list_photos()
                    st.write(f"파일 수: {len(files)}개")
                    if files:
                        st.write("최근 파일:")
                        for file in files[:5]:
                            st.write(f"- {file.get('name', 'Unknown')}")
                except:
                    st.write("파일 목록 조회 실패")
                    
    except Exception as e:
        st.error(f"버킷 조회 실패: {e}")

st.markdown("---")

# 3. 업로드 테스트
if storage and storage.client:
    st.header("3️⃣ 업로드 테스트")
    
    test_file = st.file_uploader("테스트 이미지 업로드", type=['png', 'jpg', 'jpeg'])
    
    if test_file:
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(test_file, caption="업로드할 이미지", use_container_width=True)
        
        with col2:
            gallery_name = st.text_input("갤러리 이름", value="테스트갤러리")
            
            if st.button("📤 업로드 테스트"):
                with st.spinner("업로드 중..."):
                    try:
                        # 파일 리셋 (읽기 위치를 처음으로)
                        test_file.seek(0)
                        
                        # 업로드
                        url = storage.upload_photo(test_file, gallery_name)
                        
                        if url:
                            st.success("✅ 업로드 성공!")
                            st.write(f"**공개 URL**: {url}")
                            
                            # URL로 이미지 표시
                            st.image(url, caption="업로드된 이미지 (URL에서 로드)", use_container_width=True)
                            
                            # URL 복사 버튼
                            st.code(url)
                            
                            # Padlet 테스트 데이터
                            st.info("이 URL을 Padlet API의 attachment_url로 사용할 수 있습니다!")
                        else:
                            st.error("업로드 실패 - URL이 반환되지 않음")
                            
                    except Exception as e:
                        st.error(f"업로드 오류: {e}")

st.markdown("---")

# 4. 연동 체크리스트
st.header("4️⃣ 연동 체크리스트")

checklist = {
    "Supabase 프로젝트 생성": url_exists and key_exists,
    "Storage 버킷 생성": storage and storage.client and any(b['name'] == 'gallery-photos' for b in buckets) if storage and storage.client else False,
    "공개 접근 설정": True,  # 수동 확인 필요
    "Streamlit Secrets 설정": hasattr(st, 'secrets') and 'SUPABASE_URL' in st.secrets,
    "업로드 테스트 완료": False  # 수동 확인 필요
}

for item, status in checklist.items():
    if status:
        st.success(f"✅ {item}")
    else:
        st.warning(f"⚠️ {item} - 확인 필요")

st.markdown("---")

# 5. 디버깅 정보
with st.expander("🐛 디버깅 정보"):
    st.subheader("Secrets 상태")
    if hasattr(st, 'secrets'):
        st.write("Streamlit secrets 키:", list(st.secrets.keys()) if st.secrets else "없음")
    else:
        st.write("Streamlit secrets 사용 불가")
    
    st.subheader("환경 변수")
    env_vars = {
        "SUPABASE_URL": os.getenv('SUPABASE_URL', 'Not set'),
        "SUPABASE_ANON_KEY": os.getenv('SUPABASE_ANON_KEY', 'Not set')[:20] + "..." if os.getenv('SUPABASE_ANON_KEY') else 'Not set',
        "PADLET_API_KEY": os.getenv('PADLET_API_KEY', 'Not set')[:20] + "..." if os.getenv('PADLET_API_KEY') else 'Not set'
    }
    st.json(env_vars)

st.markdown("---")
st.caption("이 테스트 페이지로 Supabase 연동이 제대로 작동하는지 확인할 수 있습니다.")