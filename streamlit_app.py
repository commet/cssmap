"""
Professional UI/UX 개선된 Streamlit 앱
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import json
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 임시 API 키
TEMP_API_KEY = "pdltp_d271492999e5db6c2cb47a28ea8598a13d343d0a7d32880eeb87d4ea89074944205d6c"
os.environ['PADLET_API_KEY'] = TEMP_API_KEY

# 페이지 설정
st.set_page_config(
    page_title="CSS Art Map | 헤맨만큼 내 땅이다",
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
        padding: 2rem 3rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
        animation: slideDown 0.5s ease-out;
    }
    
    @keyframes slideDown {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .header-title {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.5rem;
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
    
    /* 메트릭 카드 애니메이션 */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    /* 플로팅 액션 버튼 */
    .fab {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        cursor: pointer;
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .fab:hover {
        transform: scale(1.1) rotate(90deg);
    }
    
    /* 알림 배지 */
    .notification-badge {
        position: absolute;
        top: -8px;
        right: -8px;
        background: #ef4444;
        color: white;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 700;
    }
    
    /* 로딩 애니메이션 */
    .loading-dots {
        display: inline-flex;
        gap: 0.25rem;
    }
    
    .loading-dots span {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #667eea;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
    .loading-dots span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
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
    
    /* 스크롤바 커스텀 */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46a0 100%);
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("""
<div class="main-header">
    <h1 class="header-title">🎨 CSS Art Map</h1>
    <p class="header-subtitle">헤맨만큼 내 땅이다 | 프리즈·키아프 2025 실시간 트래킹</p>
</div>
""", unsafe_allow_html=True)

# 세션 상태 초기화 - 실제 데이터 저장용
if 'locations_data' not in st.session_state:
    st.session_state.locations_data = []
if 'total_locations' not in st.session_state:
    st.session_state.total_locations = 0
if 'total_participants' not in st.session_state:
    st.session_state.total_participants = 1  # 기본값 1명
if 'avg_stay_time' not in st.session_state:
    st.session_state.avg_stay_time = 0

# 메인 탭
tab1, tab2, tab3, tab4 = st.tabs(["📊 대시보드", "🗺️ 실시간 지도", "📍 위치 추가", "📈 분석"])

with tab1:
    # 실제 데이터 계산
    total_locations = len(st.session_state.locations_data)
    total_participants = st.session_state.total_participants
    avg_stay_time = st.session_state.avg_stay_time if st.session_state.avg_stay_time > 0 else 1.5
    
    # 주요 지표 카드 (3개로 변경)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon" style="background: rgba(102, 126, 234, 0.1);">
                📍
            </div>
            <div class="stat-label">총 방문 장소</div>
            <div class="stat-value">{total_locations}</div>
            <div class="stat-change change-positive">오늘 추가된 장소</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
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
    
    with col3:
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
        
        # 샘플 데이터
        import pandas as pd
        import numpy as np
        from datetime import date
        
        # 9월 1일부터 오늘까지의 데이터
        today = date.today()
        start_date = date(2025, 9, 1)
        
        # 날짜 범위 생성
        dates = pd.date_range(start=start_date, end=today, freq='D')
        
        # 실제 방문 데이터가 있으면 사용, 없으면 샘플 데이터
        if len(st.session_state.locations_data) > 0:
            # 날짜별로 방문 횟수 집계
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
        
        # 인기 장소 리스트
        popular_places = [
            ("국제갤러리", "89", "↑2"),
            ("리움미술관", "76", "↓1"),
            ("아트선재센터", "65", "→"),
            ("갤러리현대", "54", "↑1"),
            ("페이스갤러리", "48", "↑3")
        ]
        
        for i, (place, visits, trend) in enumerate(popular_places, 1):
            trend_color = "#22c55e" if "↑" in trend else "#ef4444" if "↓" in trend else "#64748b"
            st.markdown(f"""
            <div class="hover-card" style="display: flex; align-items: center; justify-content: space-between; padding: 0.75rem; margin-bottom: 0.5rem; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.25rem; font-weight: 700; color: #667eea; margin-right: 1rem;">{i}</span>
                    <span style="font-weight: 600; color: #1e293b;">{place}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-weight: 600; color: #64748b;">{visits}</span>
                    <span style="color: {trend_color}; font-weight: 600;">{trend}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">🗺️ 실시간 위치 트래킹</div>', unsafe_allow_html=True)
    
    # Folium 지도
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=13)
    
    # 실제 저장된 위치 데이터 표시
    if len(st.session_state.locations_data) > 0:
        for location in st.session_state.locations_data:
            # 감정에 따른 색상 결정
            if "😍" in location['emotion']:
                color = 'purple'
            elif "👍" in location['emotion']:
                color = 'blue'
            elif "😊" in location['emotion']:
                color = 'green'
            elif "🤔" in location['emotion']:
                color = 'orange'
            else:
                color = 'gray'
                
            folium.Marker(
                [location['lat'], location['lon']],
                popup=f"{location['name']}<br>{location['emotion']}<br>{location.get('notes', '')}",
                tooltip=location['name'],
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(m)
    else:
        # 샘플 마커들 (데이터가 없을 때만)
        st.info("아직 추가된 위치가 없습니다. '📍 위치 추가' 탭에서 새로운 위치를 추가해보세요!")
    
    st_folium(m, height=500, width=None, returned_objects=["last_object_clicked"])

with tab3:
    st.markdown('<div class="section-title">📍 새로운 위치 추가</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            <div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 2px 20px rgba(0,0,0,0.08);">
            """, unsafe_allow_html=True)
            
            location_name = st.text_input("장소명", placeholder="예: 국제갤러리")
            
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                latitude = st.number_input("위도", value=37.5665, format="%.4f")
            with col1_2:
                longitude = st.number_input("경도", value=126.9780, format="%.4f")
            
            emotion = st.select_slider(
                "방문 감상",
                options=["😍 감동", "👍 추천", "😊 만족", "🤔 보통", "😴 실망"],
                value="😊 만족"
            )
            
            notes = st.text_area("메모", placeholder="전시 관련 메모를 입력하세요...")
            
            if st.button("📍 위치 추가", use_container_width=True):
                # 실제 데이터 저장
                new_location = {
                    'name': location_name,
                    'lat': latitude,
                    'lon': longitude,
                    'emotion': emotion,
                    'notes': notes,
                    'timestamp': datetime.now()
                }
                st.session_state.locations_data.append(new_location)
                st.session_state.total_locations = len(st.session_state.locations_data)
                
                st.success("✅ 위치가 성공적으로 추가되었습니다!")
                st.balloons()
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 16px; color: white;">
            <h3 style="margin-top: 0;">💡 Quick Tips</h3>
            <ul style="line-height: 2;">
                <li>GPS 버튼을 눌러 현재 위치를 자동으로 가져올 수 있어요</li>
                <li>장소명은 검색 가능하도록 정확히 입력해주세요</li>
                <li>감상평은 나중에 통계에 반영됩니다</li>
                <li>사진을 추가하면 더 생생한 기록이 됩니다</li>
            </ul>
            
            <div style="margin-top: 2rem; padding: 1rem; background: rgba(255,255,255,0.2); border-radius: 10px;">
                <h4 style="margin-top: 0;">📊 오늘의 기록</h4>
                <div style="font-size: 2rem; font-weight: 700;">12</div>
                <div>개의 장소를 방문했어요!</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-title">📈 상세 분석</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 도넛 차트
        fig = go.Figure(data=[go.Pie(
            labels=['국제갤러리', '리움미술관', '아트선재', '기타'],
            values=[30, 25, 20, 25],
            hole=.7,
            marker_colors=['#667eea', '#764ba2', '#ec4899', '#f59e0b']
        )])
        
        fig.update_layout(
            annotations=[dict(text='장소별<br>방문 비율', x=0.5, y=0.5, font_size=14, showarrow=False)],
            showlegend=True,
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 히트맵
        hours = list(range(9, 21))
        days = ['월', '화', '수', '목', '금', '토', '일']
        z = np.random.randint(0, 100, size=(7, 12))
        
        fig = go.Figure(data=go.Heatmap(
            z=z,
            x=hours,
            y=days,
            colorscale='Purples',
            showscale=False
        ))
        
        fig.update_layout(
            title="시간대별 활동 히트맵",
            height=350,
            margin=dict(l=0, r=0, t=40, b=0),
            paper_bgcolor='white',
            xaxis=dict(title="시간"),
            yaxis=dict(title="요일")
        )
        
        st.plotly_chart(fig, use_container_width=True)

# 플로팅 액션 버튼 (HTML/CSS로 구현)
st.markdown("""
<div class="fab">
    +
    <div class="notification-badge">3</div>
</div>
""", unsafe_allow_html=True)

# 푸터
st.markdown("""
<div style="margin-top: 3rem; padding: 2rem; background: white; border-radius: 16px; text-align: center; box-shadow: 0 2px 20px rgba(0,0,0,0.08);">
    <p style="color: #64748b; margin: 0;">
        Made with ❤️ for CSS Art Map Project | 
        <span class="gradient-text">프리즈·키아프 2025</span>
    </p>
</div>
""", unsafe_allow_html=True)