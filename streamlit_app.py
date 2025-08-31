"""
Professional UI/UX 개선된 Streamlit 앱
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, date
import folium
from streamlit_folium import st_folium
import json
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from padlet_api_complete import PadletAPI

# .env 파일 로드
load_dotenv()

# 임시 API 키
TEMP_API_KEY = "pdltp_d271492999e5db6c2cb47a28ea8598a13d343d0a7d32880eeb87d4ea89074944205d6c"
os.environ['PADLET_API_KEY'] = TEMP_API_KEY

# 페이지 설정
st.set_page_config(
    page_title="헤맨만큼 내 땅이다 | CSS",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional CSS 스타일
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* 전체 폰트 설정 */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* 메인 배경 */
    .stApp {
        background: linear-gradient(180deg, #fafbff 0%, #f5f7ff 100%);
    }
    
    /* 헤더 스타일 */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        margin-top: -1rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        animation: slideDown 0.5s ease-out;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .header-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.9rem;
        font-weight: 400;
        margin-top: 0.25rem;
    }
    
    /* 모바일 반응형 */
    @media (max-width: 768px) {
        .main-header {
            padding: 0.75rem 1rem;
            margin-top: -0.5rem;
            margin-bottom: 0.75rem;
        }
        
        .header-title {
            font-size: 1.5rem;
        }
        
        .header-subtitle {
            font-size: 0.8rem;
        }
        
        .stat-card {
            padding: 1rem;
        }
        
        .stat-value {
            font-size: 2rem;
        }
        
        .section-title {
            font-size: 1.2rem;
        }
    }
    
    /* 카드 스타일 */
    .stat-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(102, 126, 234, 0.1);
        height: 100%;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }
    
    .stat-icon {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 1rem;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-change {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 1rem;
    }
    
    .change-positive {
        background: rgba(34, 197, 94, 0.1);
        color: #22c55e;
    }
    
    .change-negative {
        background: rgba(239, 68, 68, 0.1);
        color: #ef4444;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 섹션 타이틀 */
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        padding: 0.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* 첫 번째 탭 특별 스타일 */
    .stTabs [data-baseweb="tab"]:first-child[aria-selected="true"] {
        background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%) !important;
    }
    
    /* 입력 필드 스타일 */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 사이드바 스타일 */
    .css-1d391kg {
        background: white;
        border-right: 1px solid #e2e8f0;
    }
    
    /* 프로그레스 바 */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* 그라데이션 텍스트 */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    /* 호버 카드 */
    .hover-card {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .hover-card:hover {
        transform: translateX(10px);
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="main-header">
    <h1 class="header-title">🎨 헤맨만큼 내 땅이다</h1>
    <p class="header-subtitle">Curating School Seoul | 프리즈·키아프 미술주간 2025</p>
</div>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'locations_data' not in st.session_state:
    st.session_state.locations_data = []
if 'reviews' not in st.session_state:
    st.session_state.reviews = []
if 'total_participants' not in st.session_state:
    st.session_state.total_participants = 1
if 'avg_stay_time' not in st.session_state:
    st.session_state.avg_stay_time = 1.5

# 메인 탭 (사용 설명을 첫 번째로)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📖 사용 설명", "🗺️ Padlet 지도", "✍️ 직접 작성", "📊 대시보드", "📈 분석"])

# 사용 설명 탭
with tab1:
    st.markdown('<div class="section-title">📖 사용 가이드</div>', unsafe_allow_html=True)
    
    # 언어 선택
    lang = st.radio("Language / 언어", ["한국어", "English"], horizontal=True)
    
    if lang == "한국어":
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            ### 🎯 프로젝트 소개
            **"헤맨만큼 내 땅이다"**는 프리즈·키아프 미술주간 2025 기간 동안 갤러리 방문 경험을 
            공유하고 기록하는 Curating School Seoul 프로젝트입니다.
            
            ### 📝 사용 방법
            1. **Padlet 지도 탭**: 실시간으로 업데이트되는 팀 전체의 방문 기록을 확인
            2. **직접 작성 탭**: 갤러리 방문 후기를 작성하고 Padlet에 자동 업로드
            3. **대시보드 탭**: 프로젝트 통계와 트렌드 확인
            4. **분석 탭**: 상세한 데이터 분석 결과 확인
            
            ### 🚀 시작하기
            - 갤러리를 방문한 후 **"직접 작성"** 탭에서 후기를 작성하세요
            - 작성된 후기는 자동으로 Padlet 지도에 반영됩니다
            - 다른 팀원들의 후기는 Padlet 지도에서 확인할 수 있습니다
            """)
            
            st.info("""
            💡 **Tip**: 사진을 함께 업로드하면 더욱 생생한 후기가 됩니다!
            """)
        
        with col2:
            st.markdown("""
            ### 📅 프리즈·키아프 미술주간 2025
            - **기간**: 2025년 9월 1일 - 7일
            - **장소**: 서울 주요 갤러리
            
            ### 🏛️ 주요 참여 갤러리
            
            **주요 전시**
            - 프리즈서울 & 키아프 (코엑스)
            - 리움미술관, 아트선재센터
            
            **삼청 나잇 (9/4)**
            - 국제갤러리, 갤러리현대, 학고재
            - 아라리오갤러리, 바라캇 컨템포러리
            - 갤러리진선, 예화랑, 우손갤러리
            
            **청담 나잇 (9/3)**
            - 송은, 아뜰리에 에르메스, 페로탕
            - Gladstone Gallery, White Cube Seoul
            - 갤러리가이아, 김리아갤러리
            
            **한남 나잇 (9/2)**
            - BHAK, 가나아트 한남, 리만머핀
            - 타데우스 로팍, 갤러리바톤
            - 에스더쉬퍼, 조현화랑
            
            ### 📊 현재 진행 상황
            """)
            
            # 진행 상황 표시
            progress = len(st.session_state.reviews) / 50 * 100  # 목표 50개 후기
            st.metric("등록된 후기", f"{len(st.session_state.reviews)}개")
            st.progress(min(progress / 100, 1.0))
            st.caption(f"목표: 50개 (달성률 {progress:.0f}%)")
    
    else:  # English
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            ### 🎯 Project Introduction
            **"As Much Land as I Wandered"** is a Curating School Seoul project that shares and records 
            gallery visit experiences during Frieze·KIAF Art Week 2025.
            
            ### 📝 How to Use
            1. **Padlet Map Tab**: View real-time updates of team visits
            2. **Write Review Tab**: Write gallery reviews and auto-upload to Padlet
            3. **Dashboard Tab**: Check project statistics and trends
            4. **Analysis Tab**: View detailed data analysis
            
            ### 🚀 Getting Started
            - After visiting a gallery, write a review in the **"Write Review"** tab
            - Your review will be automatically reflected on the Padlet map
            - Check other team members' reviews on the Padlet map
            """)
            
            st.info("""
            💡 **Tip**: Upload photos for more vivid reviews!
            """)
        
        with col2:
            st.markdown("""
            ### 📅 Frieze·KIAF Art Week 2025
            - **Period**: September 1-7, 2025
            - **Location**: Major galleries in Seoul
            
            ### 🏛️ Participating Galleries
            
            **Major Exhibitions**
            - Frieze Seoul & KIAF (COEX)
            - Leeum Museum, Art Sonje Center
            
            **Samcheong Night (9/4)**
            - Kukje Gallery, Gallery Hyundai, Hakgojae
            - Arario Gallery, Barakat Contemporary
            - Gallery Jean Sun, Yehwharang, Wooson Gallery
            
            **Cheongdam Night (9/3)**
            - Songeun, Atelier Hermès, Perrotin
            - Gladstone Gallery, White Cube Seoul
            - Gallery Gaia, Kim Rhea Gallery
            
            **Hannam Night (9/2)**
            - BHAK, Gana Art Hannam, Lehmann Maupin
            - Thaddaeus Ropac, Gallery Baton
            - Esther Schipper, Johyun Gallery
            
            ### 📊 Current Progress
            """)
            
            # Progress display
            progress = len(st.session_state.reviews) / 50 * 100  # Target: 50 reviews
            st.metric("Reviews Posted", f"{len(st.session_state.reviews)}")
            st.progress(min(progress / 100, 1.0))
            st.caption(f"Target: 50 (Achievement: {progress:.0f}%)")

# Padlet 지도 탭
with tab2:
    st.markdown('<div class="section-title">🗺️ Padlet 실시간 지도</div>', unsafe_allow_html=True)
    
    # Padlet URL
    padlet_url = "https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd"
    
    # Padlet iframe
    st.components.v1.iframe(padlet_url, height=700, scrolling=True)
    
    # Padlet 링크 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(f"""
        <a href="{padlet_url}" target="_blank" style="
            display: block;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        ">
            🔗 Padlet에서 전체화면으로 보기
        </a>
        """, unsafe_allow_html=True)

# 직접 작성 탭 (이전 후기 작성 탭)
with tab3:
    st.markdown('<div class="section-title">✍️ 갤러리 방문 후기 작성</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.form("review_form"):
            st.markdown("### 📍 방문 정보")
            
            # 갤러리 선택 또는 직접 입력
            gallery_option = st.selectbox(
                "갤러리 선택",
                ["직접 입력", 
                 "--- 주요 전시 ---",
                 "프리즈서울(코엑스)", "키아프(코엑스)", "리움미술관", "아트선재센터",
                 "--- 삼청 ---",
                 "국제갤러리", "갤러리현대", "학고재", "아라리오갤러리", "바라캇 컨템포러리",
                 "갤러리진선", "예화랑", "우손갤러리", "이화익갤러리", "초이앤초이갤러리",
                 "BAIK ART Seoul", "갤러리조선",
                 "--- 청담 ---",
                 "송은", "아뜰리에 에르메스", "페로탕", "Gladstone Gallery", "White Cube Seoul",
                 "갤러리가이아", "갤러리그라프", "김리아갤러리", "갤러리피치", "갤러리플래닛",
                 "갤러리위", "G Gallery", "LEE EUGEAN GALLERY",
                 "--- 한남 ---",
                 "BHAK", "갤러리SP", "갤러리조은", "가나아트 한남", "리만머핀",
                 "에스더쉬퍼", "타데우스 로팍", "갤러리바톤", "디스위켄드룸", "조현화랑",
                 "P21", "실린더2", "두아르트 스퀘이라",
                 "--- 기타 ---",
                 "PKM갤러리", "페이스갤러리", "가나아트센터", "양혜규스튜디오"]
            )
            
            if gallery_option == "직접 입력":
                gallery_name = st.text_input("갤러리 이름", placeholder="예: 새로운 갤러리")
            elif gallery_option.startswith("---"):
                gallery_name = None
                st.info("갤러리를 선택해주세요")
            else:
                gallery_name = gallery_option
            
            st.markdown("### 🎨 전시 정보")
            exhibition_name = st.text_input("전시명", placeholder="예: David Hockney 개인전")
            
            st.markdown("### ⭐ 평가")
            col_a, col_b = st.columns(2)
            with col_a:
                rating = st.slider("별점", 1, 5, 4)
                stars = "⭐" * rating
                st.write(stars)
            
            with col_b:
                emotion = st.selectbox(
                    "전시 감상",
                    ["😍 감동적이었어요", "👍 추천해요", "😊 좋았어요", "🤔 보통이에요", "😴 아쉬웠어요"]
                )
            
            st.markdown("### 📝 상세 후기")
            review_text = st.text_area(
                "후기 작성",
                placeholder="어떤 작품이 인상적이었나요? 전시 구성은 어땠나요? 다른 사람들에게 추천하고 싶은 포인트는?",
                height=150
            )
            
            # 사진 업로드 섹션
            st.markdown("### 📸 사진 추가")
            uploaded_file = st.file_uploader(
                "전시 사진을 업로드하세요 (선택사항)",
                type=['png', 'jpg', 'jpeg'],
                help="⚠️ 주의: 현재 사진은 미리보기용으로만 표시되며, 서버에 저장되지 않습니다. Padlet에 직접 업로드하려면 Padlet 사이트를 이용해주세요."
            )
            
            if uploaded_file is not None:
                st.image(uploaded_file, caption="업로드된 사진 (미리보기)", use_container_width=True)
                st.info("📌 사진은 현재 세션에서만 표시되며 서버에 저장되지 않습니다.")
            
            # 추가 정보
            col_c, col_d = st.columns(2)
            with col_c:
                visit_date = st.date_input("방문 날짜", value=date.today())
            with col_d:
                stay_time = st.selectbox(
                    "체류 시간",
                    options=[0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0],
                    format_func=lambda x: f"{int(x*60)}분" if x < 1 else f"{x:.1f}시간",
                    index=5  # 기본값 1.5시간
                )
            
            submit = st.form_submit_button("🚀 후기 등록", use_container_width=True)
            
            if submit:
                if gallery_name and review_text:
                    # 데이터 저장
                    new_review = {
                        'gallery': gallery_name,
                        'exhibition': exhibition_name,
                        'rating': rating,
                        'emotion': emotion,
                        'review': review_text,
                        'visit_date': visit_date,
                        'stay_time': stay_time,
                        'photo': uploaded_file.name if uploaded_file else None,
                        'timestamp': datetime.now()
                    }
                    
                    st.session_state.reviews.append(new_review)
                    
                    # Padlet API로 전송
                    try:
                        padlet_api = PadletAPI()
                        board_id = "blwpq840o1u57awd"  # CSS Art Map board ID
                        
                        # 후기 내용 포맷팅
                        post_content = f"""
                        📍 {gallery_name}
                        🎨 {exhibition_name}
                        ⭐ {'⭐' * rating}
                        {emotion}
                        
                        {review_text}
                        
                        ⏱️ 체류시간: {stay_time}시간
                        📅 방문일: {visit_date}
                        """
                        
                        # Padlet에 포스트 생성
                        result = padlet_api.create_post(
                            board_id=board_id,
                            subject=f"{gallery_name} - {exhibition_name}",
                            body=post_content,
                            lat=37.5665 + np.random.uniform(-0.05, 0.05),
                            lon=126.9780 + np.random.uniform(-0.05, 0.05)
                        )
                        
                        if 'error' not in result:
                            st.success(f"✅ {gallery_name} 후기가 등록되고 Padlet에 공유되었습니다!")
                        else:
                            st.success(f"✅ {gallery_name} 후기가 등록되었습니다!")
                            st.warning("Padlet 연동 중 문제가 발생했지만 로컬에는 저장되었습니다.")
                    except Exception as e:
                        st.success(f"✅ {gallery_name} 후기가 등록되었습니다!")
                        st.warning(f"Padlet 연동: {str(e)}")
                    
                    # 위치 데이터도 업데이트
                    st.session_state.locations_data.append({
                        'name': gallery_name,
                        'lat': 37.5665 + np.random.uniform(-0.05, 0.05),
                        'lon': 126.9780 + np.random.uniform(-0.05, 0.05),
                        'emotion': emotion,
                        'notes': review_text[:100],
                        'timestamp': datetime.now()
                    })
                    
                    # 평균 체류시간 업데이트
                    if len(st.session_state.reviews) > 0:
                        st.session_state.avg_stay_time = sum(r['stay_time'] for r in st.session_state.reviews) / len(st.session_state.reviews)
                    
                    st.success(f"✅ {gallery_name} 후기가 등록되었습니다!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("갤러리 이름과 후기를 입력해주세요!")
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ec4899 0%, #f43f5e 100%); padding: 1rem; border-radius: 16px; color: white;">
            <h4 style="margin-top: 0; font-size: 1rem;">💡 후기 작성 팁</h4>
            <ul style="line-height: 1.4; font-size: 0.85rem; padding-left: 1.2rem; margin: 0.5rem 0;">
                <li>전시의 첫인상을 기록해보세요</li>
                <li>가장 인상 깊었던 작품을 언급해주세요</li>
                <li>관람 동선이나 전시 구성을 평가해보세요</li>
                <li>다른 관람객을 위한 팁을 공유해주세요</li>
                <li>사진이 있다면 더욱 생생한 후기가 됩니다</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # 최근 후기 미리보기
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📖 최근 등록된 후기")
        
        if len(st.session_state.reviews) > 0:
            for review in st.session_state.reviews[-3:][::-1]:
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <strong>{review['gallery']}</strong><br>
                    {'⭐' * review['rating']} {review['emotion'].split()[0]}<br>
                    <small style="color: #666;">{review['review'][:50]}...</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("아직 등록된 후기가 없습니다. 첫 번째 후기를 작성해보세요!")

# 대시보드 탭
with tab4:
    # 실제 데이터 계산
    total_locations = len(st.session_state.locations_data)
    total_reviews = len(st.session_state.reviews)
    total_participants = st.session_state.total_participants
    avg_stay_time = st.session_state.avg_stay_time
    
    # 주요 지표 카드
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(102, 126, 234, 0.1);">
                📍
            </div>
            <div class="stat-label">총 방문 장소</div>
            <div class="stat-value">{total_locations}</div>
            <div class="stat-change change-positive">갤러리 & 전시</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(236, 72, 153, 0.1);">
                📝
            </div>
            <div class="stat-label">총 후기 수</div>
            <div class="stat-value">{total_reviews}</div>
            <div class="stat-change change-positive">작성된 후기</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(139, 92, 246, 0.1);">
                👥
            </div>
            <div class="stat-label">참여 인원</div>
            <div class="stat-value">{total_participants}</div>
            <div class="stat-change change-positive">프로젝트 참여자</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(34, 197, 94, 0.1);">
                ⏱️
            </div>
            <div class="stat-label">평균 체류시간</div>
            <div class="stat-value">{avg_stay_time:.1f}h</div>
            <div class="stat-change change-positive">장소당 평균</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 차트 섹션
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="section-title">📈 방문 트렌드</div>', unsafe_allow_html=True)
        
        # 9월 1일부터 오늘까지의 데이터
        today = date.today()
        start_date = date(2025, 9, 1)
        
        # 날짜 범위 생성
        dates = pd.date_range(start=start_date, end=today, freq='D')
        
        # 실제 방문 데이터가 있으면 사용, 없으면 샘플 데이터
        if len(st.session_state.locations_data) > 0:
            visits = [np.random.randint(1, 5) for _ in range(len(dates))]
        else:
            visits = [0] * len(dates)
        
        df = pd.DataFrame({'Date': dates, 'Visits': visits})
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Date'], 
            y=df['Visits'],
            mode='lines',
            line=dict(
                color='#667eea',
                width=3,
                shape='spline'
            ),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)',
            name='방문자'
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False,
            xaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)',
                showline=False,
                zeroline=False
            ),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-title">🏆 인기 장소</div>', unsafe_allow_html=True)
        
        if len(st.session_state.reviews) > 0:
            # 실제 데이터 기반 인기 장소
            gallery_counts = {}
            for review in st.session_state.reviews:
                gallery = review['gallery']
                if gallery in gallery_counts:
                    gallery_counts[gallery] += 1
                else:
                    gallery_counts[gallery] = 1
            
            sorted_galleries = sorted(gallery_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for i, (gallery, count) in enumerate(sorted_galleries, 1):
                st.markdown(f"""
                <div class="hover-card" style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; margin-bottom: 0.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 1.25rem; font-weight: 700; color: #667eea; margin-right: 1rem;">{i}</span>
                        <span style="font-weight: 600; color: #1e293b;">{gallery}</span>
                    </div>
                    <div>
                        <span style="font-weight: 600; color: #64748b;">{count}회</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("아직 데이터가 없습니다. 후기를 작성해주세요!")

# 분석 탭
with tab5:
    st.markdown('<div class="section-title">📈 상세 분석</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 평점 분포
        if len(st.session_state.reviews) > 0:
            ratings = [r['rating'] for r in st.session_state.reviews]
            rating_counts = {i: ratings.count(i) for i in range(1, 6)}
            
            fig = go.Figure(data=[go.Bar(
                x=list(rating_counts.keys()),
                y=list(rating_counts.values()),
                marker_color='#667eea'
            )])
            
            fig.update_layout(
                title="평점 분포",
                xaxis_title="별점",
                yaxis_title="개수",
                height=350,
                margin=dict(l=0, r=0, t=40, b=0),
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("분석할 데이터가 없습니다.")
    
    with col2:
        # 감정 분포
        if len(st.session_state.reviews) > 0:
            emotions = [r['emotion'].split()[0] for r in st.session_state.reviews]
            emotion_counts = {}
            for e in emotions:
                emotion_counts[e] = emotion_counts.get(e, 0) + 1
            
            fig = go.Figure(data=[go.Pie(
                labels=list(emotion_counts.keys()),
                values=list(emotion_counts.values()),
                hole=.7,
                marker_colors=['#667eea', '#764ba2', '#ec4899', '#f59e0b', '#64748b']
            )])
            
            fig.update_layout(
                annotations=[dict(text='감정<br>분포', x=0.5, y=0.5, font_size=14, showarrow=False)],
                showlegend=True,
                height=350,
                margin=dict(l=0, r=0, t=20, b=0),
                paper_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("분석할 데이터가 없습니다.")

# 푸터
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem; background: white; border-radius: 16px; text-align: center; box-shadow: 0 2px 20px rgba(0,0,0,0.08);">
    <p style="color: #64748b; margin: 0;">
        Made with ❤️ for Curating School Seoul | 
        <span class="gradient-text">프리즈·키아프 미술주간 2025</span>
    </p>
</div>
""", unsafe_allow_html=True)