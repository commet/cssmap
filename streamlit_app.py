"""
Streamlit 기반 통합 대시보드 & 입력 시스템
실행: streamlit run streamlit_app.py
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from user_input_system import UserFriendlyInputSystem
from css_automated_manager import CSSArtMapAutomation
from padlet_api_complete import PadletAPI, extract_board_id_from_url

# 페이지 설정
st.set_page_config(
    page_title="헤맨만큼 내 땅이다",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 20px;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .big-number {
        font-size: 3rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'automation' not in st.session_state:
    st.session_state.automation = CSSArtMapAutomation()
if 'input_system' not in st.session_state:
    st.session_state.input_system = UserFriendlyInputSystem()

# 사이드바 메뉴
st.sidebar.title("🎨 헤맨만큼 내 땅이다")
st.sidebar.markdown("**프리즈·키아프 2025**")

page = st.sidebar.radio(
    "메뉴",
    ["📊 실시간 대시보드", "✏️ 경험 공유하기", "🗺️ 지도 보기", "⚙️ 관리자"]
)

# 페이지별 내용
if page == "📊 실시간 대시보드":
    st.title("📊 실시간 대시보드")
    st.markdown("---")
    
    # 자동 새로고침
    auto_refresh = st.checkbox("자동 새로고침 (10초)", value=True)
    if auto_refresh:
        st.empty()
        import time
        time.sleep(10)
        st.experimental_rerun()
    
    # 데이터 가져오기
    with st.spinner("데이터 로딩 중..."):
        analysis = st.session_state.automation.analyze_board_activity()
    
    if "error" not in analysis:
        # 주요 지표
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div>총 참여자</div>
                <div class="big-number">{}</div>
            </div>
            """.format(analysis.get("total_posts", 0)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div>오늘 게시물</div>
                <div class="big-number">+{}</div>
            </div>
            """.format(len([p for h, p in analysis.get("posts_by_hour", {}).items() if h >= 0])), unsafe_allow_html=True)
        
        with col3:
            most_active = analysis.get("most_active_time", "N/A")
            st.markdown(f"""
            <div class="metric-card">
                <div>피크 시간</div>
                <div class="big-number">{most_active}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            top_location = list(analysis.get("posts_by_location", {}).keys())[0] if analysis.get("posts_by_location") else "N/A"
            st.markdown(f"""
            <div class="metric-card">
                <div>인기 장소</div>
                <div style="font-size: 1.5rem; font-weight: bold;">{top_location}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 차트들
        col1, col2 = st.columns(2)
        
        with col1:
            # 감정 분포
            st.subheader("😊 감정 분포")
            emotions = analysis.get("posts_by_emotion", {})
            if emotions:
                fig = px.pie(
                    values=list(emotions.values()),
                    names=list(emotions.keys()),
                    color_discrete_sequence=px.colors.sequential.Purples
                )
                fig.update_traces(textinfo='label+percent')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("아직 데이터가 없습니다")
        
        with col2:
            # 장소별 게시물
            st.subheader("📍 장소별 활동")
            locations = analysis.get("posts_by_location", {})
            if locations:
                # 상위 5개만
                top_locations = dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5])
                fig = px.bar(
                    x=list(top_locations.values()),
                    y=list(top_locations.keys()),
                    orientation='h',
                    color=list(top_locations.values()),
                    color_continuous_scale="Purples"
                )
                fig.update_layout(showlegend=False, xaxis_title="게시물 수", yaxis_title="")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("아직 데이터가 없습니다")
        
        # 시간대별 활동
        st.subheader("⏰ 시간대별 활동")
        hours = analysis.get("posts_by_hour", {})
        if hours:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(hours.keys()),
                y=list(hours.values()),
                mode='lines+markers',
                line=dict(color='#764ba2', width=3),
                marker=dict(color='#667eea', size=10),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.2)'
            ))
            fig.update_layout(
                xaxis_title="시간",
                yaxis_title="게시물 수",
                xaxis=dict(tickmode='linear', tick0=0, dtick=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 트렌딩 키워드
        st.subheader("🔥 트렌딩 키워드")
        keywords = analysis.get("trending_keywords", [])
        if keywords:
            cols = st.columns(5)
            for i, (word, count) in enumerate(keywords[:5]):
                with cols[i]:
                    st.metric(word, f"{count}회")
    else:
        st.error(f"데이터를 불러올 수 없습니다: {analysis.get('error')}")

elif page == "✏️ 경험 공유하기":
    st.title("✏️ 경험 공유하기")
    st.markdown("프리즈·키아프 관람 경험을 공유해주세요")
    st.markdown("---")
    
    with st.form("experience_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # 장소 선택
            location = st.selectbox(
                "📍 방문 장소",
                options=list(st.session_state.input_system.location_aliases.keys()),
                help="방문하신 장소를 선택해주세요"
            )
            
            # 감정 선택
            emotion_map = {
                "😍 감동적이었어요": "😍",
                "👍 추천해요": "👍", 
                "🤔 어려웠어요": "🤔",
                "💸 비쌌어요": "💸",
                "😴 피곤했어요": "😴"
            }
            emotion_choice = st.radio(
                "😊 느낀 감정",
                options=list(emotion_map.keys())
            )
            emotion = emotion_map[emotion_choice]
        
        with col2:
            # 제목
            title = st.text_input(
                "📝 한 줄 요약",
                placeholder="예: David Hockney 실물에 압도당하다!"
            )
            
            # 경험
            experience = st.text_area(
                "💭 상세 경험",
                placeholder="작품, 대기시간, 꿀팁 등을 자유롭게 적어주세요",
                height=120
            )
        
        # 제출
        submitted = st.form_submit_button("🚀 공유하기", use_container_width=True)
        
        if submitted:
            if not title or not experience:
                st.error("제목과 경험을 모두 입력해주세요!")
            else:
                with st.spinner("게시 중..."):
                    result = st.session_state.input_system.project.post_visitor_experience(
                        location_name=location,
                        title=title,
                        experience=experience,
                        emotion=emotion
                    )
                    
                    if "error" not in result:
                        st.success("✅ 성공적으로 공유되었습니다!")
                        st.balloons()
                        st.info(f"🔗 [지도에서 보기]({st.session_state.input_system.project.board_url})")
                    else:
                        st.error(f"오류: {result['error']}")

elif page == "🗺️ 지도 보기":
    st.title("🗺️ 지도 보기")
    st.markdown("---")
    
    # Padlet 지도 임베드
    padlet_url = "https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd"
    
    st.markdown(f"""
    ### 🎨 CSS 미술 탐험 지도
    
    Padlet 지도에서 실시간으로 업데이트되는 관람 경험을 확인하세요.
    
    [🔗 전체 화면으로 보기]({padlet_url})
    """)
    
    # iframe으로 임베드 (Padlet이 iframe을 허용한다면)
    st.components.v1.iframe(padlet_url, height=800)

elif page == "⚙️ 관리자":
    st.title("⚙️ 관리자 도구")
    st.markdown("---")
    
    # 비밀번호 체크 (실제로는 더 안전한 방법 사용)
    password = st.text_input("관리자 비밀번호", type="password")
    
    if password == "css2025admin":  # 실제로는 환경변수 사용
        st.success("✅ 관리자 모드")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 데이터 백업", use_container_width=True):
                with st.spinner("백업 중..."):
                    backup_file = st.session_state.automation.backup_board_data()
                    if backup_file:
                        st.success(f"백업 완료: {backup_file}")
        
        with col2:
            if st.button("🔍 콘텐츠 모더레이션", use_container_width=True):
                with st.spinner("검사 중..."):
                    flagged = st.session_state.automation.moderate_content()
                    if flagged:
                        st.warning(f"검토 필요: {len(flagged)}개 게시물")
                        for post in flagged:
                            st.write(f"- {post.get('id')}: {post.get('reason')}")
                    else:
                        st.success("모든 콘텐츠 정상")
        
        with col3:
            if st.button("📊 일일 리포트", use_container_width=True):
                with st.spinner("리포트 생성 중..."):
                    report = st.session_state.automation.generate_daily_report()
                    st.success("리포트 생성 완료")
                    st.json(report)
    elif password:
        st.error("❌ 비밀번호가 틀렸습니다")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; opacity: 0.7;">
    🎨 헤맨만큼 내 땅이다 - CSS 2025<br>
    프리즈·키아프 기간: 2025.9.1-7
</div>
""", unsafe_allow_html=True)