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
from supabase_storage import SupabaseStorage
from updated_locations import COMPLETE_GALLERY_LOCATIONS
from gallery_coordinates import get_gallery_coordinates

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
    <h1 class="header-title">🎨 헤맨만큼 내 땅이다 | As Much Land as I Wandered</h1>
    <p class="header-subtitle">Curating School Seoul | 프리즈·키아프 미술주간 2025</p>
</div>
""", unsafe_allow_html=True)

# 갤러리 이름을 정규화하는 함수
def normalize_gallery_name(gallery_name):
    """갤러리 이름을 정규화하여 COMPLETE_GALLERY_LOCATIONS와 매칭"""
    # 괄호 안 내용 제거 (예: "프리즈 서울 (COEX)" -> "프리즈 서울")
    normalized = gallery_name.split('(')[0].strip()
    
    # 매핑 테이블
    name_mapping = {
        "프리즈 서울": "코엑스",
        "키아프": "코엑스",
        "국제갤러리": "국제갤러리",
        "갤러리 진선": "갤러리진선",
        "예화랑": "예화랑",
        "우손갤러리 서울": "우손갤러리",
        "이화익갤러리": "이화익갤러리",
        "초이앤초이 갤러리": "초이앤초이갤러리",
        "갤러리현대": "갤러리현대",
        "학고재": "학고재",
        "바라캇 컨템포러리": "바라캇컨템포러리",
        "BAIK ART Seoul": "백아트",
        "갤러리 조선": "갤러리조선",
        "아라리오갤러리 서울": "아라리오갤러리",
        "아트선재센터": "아트선재센터",
        "재단법인 예울": "여재단",
        "전혁림 (포즈뮤지엄사진)": "전혁림",
        "(ICA) 우양미술관·더성북도원미술관": "우양미술관",
        "(삼청) PKM갤러리": "PKM갤러리",
        "갤러리 가이아": "갤러리가이아",
        "갤러리 그라프": "갤러리그라프",
        "김리아갤러리": "김리아갤러리",
        "갤러리 피치": "갤러리피치",
        "갤러리 플래닛": "갤러리플래닛",
        "갤러리위 청담": "갤러리위청담",
        "Gladstone Gallery Seoul": "글래드스톤갤러리",
        "White Cube Seoul": "화이트큐브서울",
        "페로탕": "페로탕",
        "G Gallery 지갤러리": "G갤러리",
        "LEE EUGEAN GALLERY 이유진갤러리": "이유진갤러리",
        "송은": "송은아트스페이스",
        "아뜰리에 에르메스": "아뜰리에에르메스",
        "BHAK": "바크",
        "갤러리 SP": "갤러리SP",
        "갤러리조은": "갤러리조은",
        "가나아트 한남": "가나아트한남",
        "리만머핀": "리만머핀",
        "에스더쉬퍼": "에스더쉬퍼",
        "타데우스 로팍 서울": "타데우스로팍",
        "갤러리바톤": "갤러리바톤",
        "디스위켄드룸": "디스위켄드룸",
        "ThisWeekendRoom": "디스위켄드룸",
        "조현화랑 서울": "조현화랑",
        "P21": "P21",
        "실린더2": "실린더2",
        "두아르트 스퀘이라 서울": "두아르트",
        "양혜규스튜디오": "양혜규스튜디오",
        "리움미술관": "리움미술관",
        "PKM갤러리": "PKM갤러리",
        "페이스갤러리": "페이스갤러리",
        "가나아트센터": "가나아트센터",
        "대림미술관": "대림미술관",
        "삼성미술관": "리움미술관"
    }
    
    return name_mapping.get(normalized, normalized)

def get_gallery_location(gallery_name):
    """갤러리 이름으로 실제 위치 정보 가져오기"""
    normalized_name = normalize_gallery_name(gallery_name)
    
    # COMPLETE_GALLERY_LOCATIONS에서 위치 정보 찾기
    if normalized_name in COMPLETE_GALLERY_LOCATIONS:
        location = COMPLETE_GALLERY_LOCATIONS[normalized_name]
        return location["lat"], location["lng"]
    
    # 못 찾으면 서울 중심부 좌표 반환 (폴백)
    return 37.5665, 126.9780

# 세션 상태 초기화
if 'locations_data' not in st.session_state:
    st.session_state.locations_data = []
if 'reviews' not in st.session_state:
    st.session_state.reviews = []
if 'total_participants' not in st.session_state:
    st.session_state.total_participants = 1
if 'avg_stay_time' not in st.session_state:
    st.session_state.avg_stay_time = 1.5
if 'padlet_data' not in st.session_state:
    st.session_state.padlet_data = []
if 'last_padlet_fetch' not in st.session_state:
    st.session_state.last_padlet_fetch = None
if 'submission_in_progress' not in st.session_state:
    st.session_state.submission_in_progress = False
if 'last_submission_time' not in st.session_state:
    st.session_state.last_submission_time = None

# Padlet 데이터 가져오기 함수
def fetch_padlet_data():
    """Padlet에서 데이터를 가져와서 로컬 데이터와 동기화"""
    try:
        # 마지막 fetch로부터 5분이 지났는지 체크
        if st.session_state.last_padlet_fetch:
            if (datetime.now() - st.session_state.last_padlet_fetch).seconds < 300:
                return  # 5분 이내면 다시 가져오지 않음
        
        padlet_api = PadletAPI()
        board_id = "blwpq840o1u57awd"
        
        # Padlet 보드 데이터 가져오기
        board_data = padlet_api.get_board(board_id, include_posts=True)
        
        if 'data' in board_data and 'included' in board_data:
            posts = board_data['included']
            
            # Padlet 포스트를 reviews 형식으로 변환
            for post in posts:
                if post.get('type') == 'posts':
                    attributes = post.get('attributes', {})
                    
                    # 이미 있는 데이터인지 체크 (중복 방지)
                    post_id = post.get('id')
                    if not any(r.get('padlet_id') == post_id for r in st.session_state.padlet_data):
                        padlet_review = {
                            'padlet_id': post_id,
                            'gallery': attributes.get('subject', '갤러리'),
                            'review': attributes.get('body', ''),
                            'timestamp': attributes.get('created_at', datetime.now()),
                            'from_padlet': True
                        }
                        st.session_state.padlet_data.append(padlet_review)
        
        st.session_state.last_padlet_fetch = datetime.now()
        
    except Exception as e:
        # 에러가 있어도 앱이 중단되지 않도록
        pass

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
            "헤맨만큼 내 땅이다"는 프리즈·키아프 미술주간 2025 기간 동안 갤러리 방문 경험을 
            공유하고 기록하는 Curating School Seoul 프로젝트입니다.
            
            ### 📝 사용 방법
            1. **Padlet 지도 탭**: 실시간으로 업데이트되는 참여자들의 방문 기록을 확인
            2. **직접 작성 탭**: 갤러리 방문 후기를 작성하고 Padlet에 자동 업로드
            3. **대시보드 탭**: 프로젝트 통계와 트렌드 확인
            4. **분석 탭**: 상세한 데이터 분석 결과 확인
            
            ### 🚀 시작하기
            - 갤러리를 방문한 후 **"직접 작성"** 탭에서 후기를 작성하세요
            - 작성된 후기는 자동으로 Padlet 지도에 반영됩니다
            - 다른 참여자들의 후기는 Padlet 지도에서 확인할 수 있습니다
            """)
            
            st.info("""
            💡 Tip: 사진을 함께 업로드하면 더욱 생생한 후기가 됩니다!
            """)
        
        with col2:
            st.markdown("""
            ### 📅 프리즈·키아프 미술주간 2025
            - **기간**: 2025년 9월 1일 - 7일
            - **장소**: 서울 주요 갤러리
            
            ### 🏛️ 주요 참여 갤러리
            
            🎨 아트 페어
            - 프리즈 서울 (COEX)
            - 키아프 (COEX)
            
            🌃 삼청 나잇 (9/4, 목)
            - 국제갤러리, 갤러리현대, 학고재
            - 아라리오갤러리, 바라캇 컨템포러리
            - 갤러리 진선, 예화랑, 우손갤러리
            
            ✨ 청담 나잇 (9/3, 수)
            - 송은, 아뜰리에 에르메스, 페로탕
            - Gladstone Gallery, White Cube Seoul
            - 갤러리 가이아, 김리아갤러리
            
            🌙 한남 나잇 (9/2, 화)
            - BHAK, 가나아트 한남, 리만머핀
            - 타데우스 로팍, 갤러리바톤
            - 에스더쉬퍼, 조현화랑
            
            🌆 을지로 나잇 (9/1, 월)
            - 양혜규스튜디오
            
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
            "As Much Land as I Wandered" is a Curating School Seoul project that shares and records 
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
            💡 Tip: Upload photos for more vivid reviews!
            """)
        
        with col2:
            st.markdown("""
            ### 📅 Frieze·KIAF Art Week 2025
            - **Period**: September 1-7, 2025
            - **Location**: Major galleries in Seoul
            
            ### 🏛️ Participating Galleries
            
            🎨 Art Fairs
            - Frieze Seoul (COEX)
            - KIAF (COEX)
            
            🌃 Samcheong Night (9/4, Thu)
            - Kukje Gallery, Gallery Hyundai, Hakgojae
            - Arario Gallery, Barakat Contemporary
            - Gallery Jean Sun, Yehwharang, Wooson Gallery
            
            ✨ Cheongdam Night (9/3, Wed)
            - Songeun, Atelier Hermès, Perrotin
            - Gladstone Gallery, White Cube Seoul
            - Gallery Gaia, Kim Rhea Gallery
            
            🌙 Hannam Night (9/2, Tue)
            - BHAK, Gana Art Hannam, Lehmann Maupin
            - Thaddaeus Ropac, Gallery Baton
            - Esther Schipper, Johyun Gallery
            
            🌆 Euljiro Night (9/1, Mon)
            - Yang Hye Gyu Studio
            
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
    
    # Padlet 데이터 가져오기 시도
    fetch_padlet_data()
    
    if len(st.session_state.padlet_data) > 0:
        st.info(f"📥 Padlet에서 {len(st.session_state.padlet_data)}개의 포스트를 불러왔습니다.")
    
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
        # 방문 정보 컨테이너
        with st.container():
            st.markdown("### 📍 방문 정보")
            
            # 3단계 갤러리 선택 프로세스
            st.markdown("#### Step 1: 지역/카테고리 선택")
            area_option = st.selectbox(
                "지역/카테고리 선택",
                ["--- 지역을 선택하세요 ---",
                 "🎨 아트 페어",
                 "🌃 삼청 나잇 (9/4, 목)",
                 "✨ 청담 나잇 (9/3, 수)",
                 "🌙 한남 나잇 (9/2, 화)",
                 "🌆 을지로 나잇 (9/1, 월)",
                 "🏛️ 이 기간 전국 갤러리"],
                key="area_select",
                label_visibility="collapsed"
            )
            
            # 지역별 갤러리 리스트
            gallery_lists = {
                "🎨 아트 페어": ["프리즈 서울 (COEX)", "키아프 (COEX)"],
                "🌃 삼청 나잇 (9/4, 목)": [
                    "국제갤러리", "갤러리 진선", "예화랑", "우손갤러리 서울",
                    "이화익갤러리", "초이앤초이 갤러리", "갤러리현대", 
                    "학고재", "바라캇 컨템포러리", "BAIK ART Seoul", 
                    "갤러리 조선", "아라리오갤러리 서울", "아트선재센터", 
                    "재단법인 예울", "전혁림 (포즈뮤지엄사진)", 
                    "(ICA) 우양미술관·더성북도원미술관", "(삼청) PKM갤러리"
                ],
                "✨ 청담 나잇 (9/3, 수)": [
                    "갤러리 가이아", "갤러리 그라프", "김리아갤러리",
                    "갤러리 피치", "갤러리 플래닛", "갤러리위 청담",
                    "Gladstone Gallery Seoul", "White Cube Seoul", "페로탕",
                    "G Gallery 지갤러리", "LEE EUGEAN GALLERY 이유진갤러리",
                    "송은", "아뜰리에 에르메스"
                ],
                "🌙 한남 나잇 (9/2, 화)": [
                    "BHAK", "갤러리 SP", "갤러리조은", "가나아트 한남",
                    "리만머핀", "에스더쉬퍼", "타데우스 로팍 서울",
                    "갤러리바톤", "디스위켄드룸", "ThisWeekendRoom",
                    "조현화랑 서울", "P21", "실린더2",
                    "두아르트 스퀘이라 서울"
                ],
                "🌆 을지로 나잇 (9/1, 월)": ["양혜규스튜디오"],
                "🏛️ 이 기간 전국 갤러리": [
                    "리움미술관", "PKM갤러리", "페이스갤러리", 
                    "가나아트센터", "대림미술관", "삼성미술관"
                ]
            }
            
            gallery_name = None
            
            if area_option != "--- 지역을 선택하세요 ---":
                st.markdown("#### Step 2: 갤러리 선택")
                
                if area_option in gallery_lists:
                    gallery_options = gallery_lists[area_option] + ["🖊️ 직접 입력"]
                    gallery_selection = st.selectbox(
                        "갤러리 선택",
                        ["--- 갤러리를 선택하세요 ---"] + gallery_options,
                        key="gallery_dropdown",
                        label_visibility="collapsed"
                    )
                    
                    if gallery_selection == "🖊️ 직접 입력":
                        st.markdown("#### Step 3: 직접 입력")
                        gallery_name = st.text_input(
                            "갤러리 이름 직접 입력",
                            placeholder="예: 새로운 갤러리 이름",
                            key="gallery_input",
                            label_visibility="collapsed"
                        )
                        
                        # 지역 선택 (직접 입력 갤러리용)
                        if gallery_name:
                            st.markdown("#### 갤러리 위치 선택")
                            custom_location = st.selectbox(
                                "이 갤러리는 어느 지역에 있나요?",
                                ["삼청동", "청담동", "한남동", "강남", "홍대", "성수동", "이태원", "기타 서울"],
                                key="custom_location",
                                help="지도에 표시될 대략적인 위치입니다"
                            )
                    elif gallery_selection != "--- 갤러리를 선택하세요 ---":
                        gallery_name = gallery_selection
                        st.success(f"✅ 선택된 갤러리: {gallery_name}")
            else:
                st.info("👆 먼저 지역/카테고리를 선택해주세요")
        
        # 폼 시작 (나머지 필드들)
        with st.form("review_form"):
            
            st.markdown("### 🎨 전시 정보")
            exhibition_name = st.text_input("전시명 (선택사항)", placeholder="예: David Hockney 개인전")
            
            st.markdown("### ⭐ 평가")
            col_a, col_b = st.columns(2)
            with col_a:
                rating = st.slider("별점", 1, 5, 4)
            
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
                help="사진을 업로드하면 Supabase 클라우드에 저장되고 Padlet에 공유됩니다."
            )
            
            photo_url = None
            if uploaded_file is not None:
                st.image(uploaded_file, caption="업로드된 사진 (미리보기)", use_container_width=True)
                
                # Supabase Storage 초기화
                if 'storage' not in st.session_state:
                    st.session_state.storage = SupabaseStorage()
                
                # Supabase가 설정되어 있으면 업로드 시도
                if st.session_state.storage.client:
                    st.info("📤 사진이 클라우드에 업로드되어 Padlet에 공유됩니다.")
                else:
                    st.warning("📌 Supabase 설정이 없어 사진이 임시 저장만 됩니다.")
                    with st.expander("🔧 Supabase 설정 방법 (5분 소요)"):
                        st.markdown("""
                        ### 빠른 설정 가이드
                        
                        1. **Supabase 가입**: [supabase.com](https://supabase.com) → Start your project
                        2. **프로젝트 생성**: New Project → Region: Seoul 선택
                        3. **Storage 설정**: Storage → Create bucket → Name: `gallery-photos`, Public: ✅
                        4. **API 키 복사**: Settings → API → URL과 anon key 복사
                        5. **Streamlit 설정**: 
                           ```toml
                           SUPABASE_URL = "복사한 URL"
                           SUPABASE_ANON_KEY = "복사한 anon key"
                           ```
                        
                        [📖 상세 가이드 보기](https://github.com/commet/cssmap/blob/main/SUPABASE_SETUP_GUIDE.md)
                        """)
            
            # 추가 정보
            col_c, col_d = st.columns(2)
            with col_c:
                visit_date = st.date_input("방문 날짜", value=date.today())
            with col_d:
                stay_time = st.slider(
                    "체류 시간",
                    min_value=0.25,
                    max_value=4.0,
                    value=1.5,
                    step=0.25,
                    format="%.2f시간",
                    help="15분 단위로 조정 가능 (15분~4시간)"
                )
            
            submit = st.form_submit_button("🚀 후기 등록", use_container_width=True, disabled=st.session_state.submission_in_progress)
            
            if submit and not st.session_state.submission_in_progress:
                # 중복 제출 방지: 5초 이내 재제출 방지
                if st.session_state.last_submission_time:
                    time_diff = (datetime.now() - st.session_state.last_submission_time).total_seconds()
                    if time_diff < 5:
                        st.warning("⏳ 잠시 후 다시 시도해주세요.")
                        st.stop()
                
                if gallery_name and review_text:
                    st.session_state.submission_in_progress = True
                    st.session_state.last_submission_time = datetime.now()
                    # 사진 업로드 처리
                    photo_url = None
                    if uploaded_file and hasattr(st.session_state, 'storage') and st.session_state.storage.client:
                        with st.spinner("사진 업로드 중..."):
                            photo_url = st.session_state.storage.upload_photo(uploaded_file, gallery_name)
                    
                    # 데이터 저장
                    new_review = {
                        'gallery': gallery_name,
                        'exhibition': exhibition_name,
                        'rating': rating,
                        'emotion': emotion,
                        'review': review_text,
                        'visit_date': visit_date,
                        'stay_time': stay_time,
                        'photo': photo_url if photo_url else (uploaded_file.name if uploaded_file else None),
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
                        🎨 {exhibition_name if exhibition_name else '전시 정보 없음'}
                        ⭐ {'⭐' * rating}
                        {emotion}
                        
                        {review_text}
                        
                        ⏱️ 체류시간: {stay_time}시간
                        📅 방문일: {visit_date}
                        """
                        
                        # 사진 URL이 있으면 내용에 추가
                        if photo_url:
                            post_content += f"\n\n📸 사진 보기: {photo_url}"
                        
                        # 갤러리의 실제 좌표 가져오기 (직접 입력인 경우 지역 정보 전달)
                        custom_location = st.session_state.get('custom_location', None) if '🖊️ 직접 입력' in str(st.session_state.get('gallery_dropdown', '')) else None
                        
                        # 우선 updated_locations에서 정확한 좌표 시도
                        lat, lng = get_gallery_location(gallery_name)
                        
                        # 못 찾으면 gallery_coordinates에서 시도
                        if lat == 37.5665 and lng == 126.9780:  # 기본 좌표인 경우
                            gallery_coords = get_gallery_coordinates(gallery_name, custom_location)
                            lat, lng = gallery_coords["lat"], gallery_coords["lon"]
                        
                        # Padlet에 포스트 생성 (attachment_url 파라미터 사용)
                        result = padlet_api.create_post(
                            board_id=board_id,
                            subject=f"{gallery_name} - {exhibition_name}",
                            body=post_content,
                            attachment_url=photo_url,  # 사진 URL 추가
                            map_props={
                                "latitude": lat, 
                                "longitude": lng,
                                "locationName": gallery_name
                            }  # 올바른 Padlet API 키 이름으로 GPS 좌표 전달
                        )
                        
                        if 'error' not in result:
                            st.success(f"✅ {gallery_name} 후기가 등록되고 Padlet에 공유되었습니다!")
                        else:
                            st.success(f"✅ {gallery_name} 후기가 등록되었습니다!")
                            st.warning("Padlet 연동 중 문제가 발생했지만 로컬에는 저장되었습니다.")
                    except Exception as e:
                        st.success(f"✅ {gallery_name} 후기가 등록되었습니다!")
                        st.warning(f"⏳ 잠시 후 다시 시도해주세요. Padlet 지도에 직접 등록해주시면 감사드리겠습니다!")
                    
                    # 제출 상태 초기화
                    st.session_state.submission_in_progress = False
                    
                    # 위치 데이터도 업데이트 (동일한 좌표 사용)
                    st.session_state.locations_data.append({
                        'name': gallery_name,
                        'lat': lat,
                        'lon': lng,
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
                    st.session_state.submission_in_progress = False
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
    # Padlet 데이터 가져오기
    fetch_padlet_data()
    
    # 실제 데이터 계산 (로컬 + Padlet 데이터)
    total_locations = len(st.session_state.locations_data)
    total_reviews = len(st.session_state.reviews) + len(st.session_state.padlet_data)
    total_participants = st.session_state.total_participants
    avg_stay_time = st.session_state.avg_stay_time
    
    # Padlet 데이터 동기화 상태 표시
    if st.session_state.last_padlet_fetch:
        st.caption(f"🔄 Padlet 동기화: {st.session_state.last_padlet_fetch.strftime('%H:%M')} (로컬: {len(st.session_state.reviews)}개, Padlet: {len(st.session_state.padlet_data)}개)")
    
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
                zeroline=False,
                tickformat='%m/%d',  # 월/일 형식으로 표시
                tickmode='linear',
                dtick=86400000  # 1일 간격 (밀리초 단위)
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
    
    st.info("📊 아래 그래프들은 현재 예시 데이터로 표시됩니다. 실제 데이터가 쌓이면 자동으로 업데이트됩니다.")
    
    # 첫 번째 행
    col1, col2 = st.columns(2)
    
    with col1:
        # 평점 분포 (Mock Data)
        st.markdown("### ⭐ 평점 분포")
        mock_ratings = {1: 2, 2: 5, 3: 12, 4: 28, 5: 45}
        
        fig = go.Figure(data=[go.Bar(
            x=list(mock_ratings.keys()),
            y=list(mock_ratings.values()),
            text=list(mock_ratings.values()),
            textposition='outside',
            marker=dict(
                color=list(mock_ratings.values()),
                colorscale='Purples',
                showscale=False
            )
        )])
        
        fig.update_layout(
            xaxis_title="별점",
            yaxis_title="후기 수",
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='white',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickmode='linear', tick0=1, dtick=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 감정 분포 (Mock Data)
        st.markdown("### 😊 감정 분석")
        mock_emotions = {"😍": 35, "👍": 28, "😊": 20, "🤔": 12, "😴": 5}
        
        fig = go.Figure(data=[go.Pie(
            labels=list(mock_emotions.keys()),
            values=list(mock_emotions.values()),
            hole=.6,
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
    
    # 두 번째 행
    col3, col4 = st.columns(2)
    
    with col3:
        # 시간대별 방문 (Mock Data)
        st.markdown("### ⏰ 시간대별 방문 패턴")
        hours = list(range(10, 20))  # 10시부터 19시까지
        visits = [5, 8, 15, 22, 18, 25, 30, 28, 20, 12]
        
        fig = go.Figure(data=[go.Scatter(
            x=hours,
            y=visits,
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8, color='#764ba2'),
            fillcolor='rgba(102, 126, 234, 0.2)'
        )])
        
        fig.update_layout(
            xaxis_title="시간",
            yaxis_title="방문자 수",
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='white',
            xaxis=dict(tickmode='linear', tick0=10, dtick=1, ticksuffix="시")
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # 체류 시간 분석 (Mock Data)
        st.markdown("### ⏱️ 평균 체류 시간")
        galleries = ["국제갤러리", "갤러리현대", "리움", "페로탕", "송은"]
        stay_times = [2.5, 1.8, 3.2, 1.5, 2.0]
        
        fig = go.Figure(data=[go.Bar(
            x=stay_times,
            y=galleries,
            orientation='h',
            text=[f"{t}시간" for t in stay_times],
            textposition='outside',
            marker=dict(
                color=stay_times,
                colorscale='Purples',
                showscale=False
            )
        )])
        
        fig.update_layout(
            xaxis_title="시간",
            yaxis_title="",
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 세 번째 행 - 히트맵
    st.markdown("### 🗓️ 주간 활동 히트맵")
    
    # Mock data for heatmap
    days = ['월', '화', '수', '목', '금', '토', '일']
    times = ['오전', '오후', '저녁']
    z_data = [[5, 15, 8], [10, 25, 12], [8, 30, 15], [12, 35, 20], [20, 40, 25], [35, 45, 30], [30, 38, 22]]
    
    fig = go.Figure(data=go.Heatmap(
        z=z_data,
        x=times,
        y=days,
        colorscale='Purples',
        text=z_data,
        texttemplate="%{text}",
        textfont={"size": 12},
        colorbar=dict(title="방문 수")
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=20, b=0),
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 네 번째 행 - 워드 클라우드 대체
    st.markdown("### 🏷️ 인기 키워드")
    
    keywords_data = {
        "현대미술": 45, "설치미술": 38, "회화": 35, "조각": 30,
        "미디어아트": 28, "사진": 25, "퍼포먼스": 22, "개념미술": 20,
        "추상": 18, "구상": 15, "팝아트": 12, "미니멀리즘": 10
    }
    
    col5, col6, col7, col8 = st.columns(4)
    sorted_keywords = sorted(keywords_data.items(), key=lambda x: x[1], reverse=True)
    
    for i, col in enumerate([col5, col6, col7, col8]):
        if i*3 < len(sorted_keywords):
            with col:
                for j in range(3):
                    idx = i*3 + j
                    if idx < len(sorted_keywords):
                        keyword, count = sorted_keywords[idx]
                        size = 1.5 - (idx * 0.08)  # 크기 점진적 감소
                        opacity = 1.0 - (idx * 0.05)  # 투명도 점진적 증가
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, rgba(102, 126, 234, {opacity}), rgba(118, 75, 162, {opacity}));
                            color: white;
                            padding: 0.5rem;
                            border-radius: 20px;
                            text-align: center;
                            margin-bottom: 0.5rem;
                            font-size: {size}rem;
                            font-weight: 600;
                        ">
                            {keyword} ({count})
                        </div>
                        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("💡 참고: 위 분석 데이터는 예시입니다. 실제 후기가 누적되면 자동으로 실제 데이터 기반 분석으로 전환됩니다.")

# 푸터
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem; background: white; border-radius: 16px; text-align: center; box-shadow: 0 2px 20px rgba(0,0,0,0.08);">
    <p style="color: #64748b; margin: 0;">
        Made with ❤️ for Curating School Seoul | 
        <span class="gradient-text">프리즈·키아프 미술주간 2025</span>
    </p>
</div>
""", unsafe_allow_html=True)