"""
Supabase Storage Integration for CSS Art Map
사진 업로드 및 저장을 위한 Supabase 연동
"""

import os
from supabase import create_client, Client
from typing import Optional
import streamlit as st
from datetime import datetime
import uuid

class SupabaseStorage:
    def __init__(self):
        """Supabase 클라이언트 초기화"""
        # Supabase 설정 (환경변수 또는 Streamlit secrets에서 가져오기)
        self.url = self._get_config('SUPABASE_URL')
        self.key = self._get_config('SUPABASE_ANON_KEY')
        
        if self.url and self.key:
            self.client: Client = create_client(self.url, self.key)
            self.bucket_name = "gallery-photos"  # 버킷 이름
            self._ensure_bucket_exists()
        else:
            self.client = None
            st.warning("⚠️ Supabase 설정이 필요합니다. 사진 업로드 기능이 비활성화됩니다.")
    
    def _get_config(self, key: str) -> Optional[str]:
        """설정값 가져오기 (Streamlit secrets 우선, 그 다음 환경변수)"""
        # Streamlit secrets
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
        # 환경변수
        return os.getenv(key)
    
    def _ensure_bucket_exists(self):
        """버킷이 존재하는지 확인하고 없으면 생성"""
        try:
            buckets = self.client.storage.list_buckets()
            bucket_names = [b['name'] for b in buckets]
            
            if self.bucket_name not in bucket_names:
                # 버킷 생성 (공개 버킷으로 설정)
                self.client.storage.create_bucket(
                    self.bucket_name,
                    options={"public": True}
                )
                st.info(f"✅ 스토리지 버킷 '{self.bucket_name}' 생성 완료")
        except Exception as e:
            st.error(f"버킷 확인/생성 실패: {e}")
    
    def upload_photo(self, file, gallery_name: str, user_id: str = None) -> Optional[str]:
        """
        사진을 Supabase Storage에 업로드
        
        Args:
            file: Streamlit file_uploader로 받은 파일
            gallery_name: 갤러리 이름
            user_id: 사용자 ID (선택사항)
        
        Returns:
            업로드된 파일의 공개 URL 또는 None
        """
        if not self.client:
            return None
        
        try:
            # 파일명 생성 (timestamp + uuid + 원본 확장자)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            file_extension = file.name.split('.')[-1]
            
            # 갤러리 이름에서 특수문자 제거
            safe_gallery_name = "".join(c for c in gallery_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_gallery_name = safe_gallery_name.replace(' ', '_')
            
            # 파일 경로 생성
            file_path = f"{safe_gallery_name}/{timestamp}_{unique_id}.{file_extension}"
            
            # 파일 읽기
            file_bytes = file.read()
            
            # Supabase에 업로드
            response = self.client.storage.from_(self.bucket_name).upload(
                path=file_path,
                file=file_bytes,
                file_options={"content-type": file.type}
            )
            
            # 공개 URL 가져오기
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(file_path)
            
            return public_url
            
        except Exception as e:
            st.error(f"사진 업로드 실패: {e}")
            return None
    
    def delete_photo(self, file_path: str) -> bool:
        """
        Supabase Storage에서 사진 삭제
        
        Args:
            file_path: 삭제할 파일 경로
        
        Returns:
            성공 여부
        """
        if not self.client:
            return False
        
        try:
            self.client.storage.from_(self.bucket_name).remove([file_path])
            return True
        except Exception as e:
            st.error(f"사진 삭제 실패: {e}")
            return False
    
    def list_photos(self, gallery_name: str = None) -> list:
        """
        업로드된 사진 목록 가져오기
        
        Args:
            gallery_name: 특정 갤러리의 사진만 가져올 경우
        
        Returns:
            파일 정보 리스트
        """
        if not self.client:
            return []
        
        try:
            if gallery_name:
                safe_gallery_name = "".join(c for c in gallery_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_gallery_name = safe_gallery_name.replace(' ', '_')
                files = self.client.storage.from_(self.bucket_name).list(safe_gallery_name)
            else:
                files = self.client.storage.from_(self.bucket_name).list()
            
            return files
        except Exception as e:
            st.error(f"사진 목록 가져오기 실패: {e}")
            return []


# 사용 예시
if __name__ == "__main__":
    st.title("Supabase Storage 테스트")
    
    # Supabase 설정 안내
    st.info("""
    ### Supabase 설정 방법:
    1. [Supabase](https://supabase.com)에서 무료 프로젝트 생성
    2. Settings → API에서 URL과 anon key 복사
    3. Streamlit secrets에 추가:
       ```
       SUPABASE_URL = "your-project-url"
       SUPABASE_ANON_KEY = "your-anon-key"
       ```
    """)
    
    # 스토리지 초기화
    storage = SupabaseStorage()
    
    # 파일 업로드 테스트
    uploaded_file = st.file_uploader("사진 업로드 테스트", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        gallery_name = st.text_input("갤러리 이름", "테스트 갤러리")
        
        if st.button("업로드"):
            with st.spinner("업로드 중..."):
                url = storage.upload_photo(uploaded_file, gallery_name)
                
                if url:
                    st.success("✅ 업로드 성공!")
                    st.write(f"URL: {url}")
                    st.image(url, caption="업로드된 이미지")
                else:
                    st.error("업로드 실패")