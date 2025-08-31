"""
사용자 친화적 입력 시스템
Google Forms 대신 자체 웹폼 또는 Typeform 연동
"""

import streamlit as st
from typing import Dict, List, Optional
import json

class UserFriendlyInputSystem:
    """사용자가 쉽게 경험을 입력할 수 있는 시스템"""
    
    def __init__(self):
        pass  # CSSArtMapProject 의존성 제거
        
        # 장소명 변형 매핑 (자동완성용)
        self.location_aliases = {
            "코엑스": ["coex", "코엑스", "코액스", "삼성역"],
            "프리즈서울": ["frieze", "프리즈", "frieze seoul", "프리즈 서울"],
            "키아프": ["kiaf", "키아프", "kiaf seoul"],
            "국제갤러리": ["국제", "kukje", "kukje gallery", "국제 갤러리"],
            "리움미술관": ["리움", "leeum", "리움", "삼성미술관"],
            "아트선재센터": ["아트선재", "art sonje", "선재"],
            "갤러리현대": ["현대갤러리", "gallery hyundai", "현대"],
            "페이스갤러리": ["pace", "페이스", "pace gallery"],
            "PKM갤러리": ["pkm", "피케이엠"],
            "삼청동": ["삼청", "삼청동길", "북촌"],
            "한남동": ["한남", "한남동", "이태원"],
            "성수동": ["성수", "성수동", "뚝섬"]
        }
        
        # 모든 가능한 입력값 리스트 생성
        self.all_location_inputs = []
        for key, aliases in self.location_aliases.items():
            self.all_location_inputs.append(key)
            self.all_location_inputs.extend(aliases)
    
    def match_location(self, user_input: str) -> Optional[str]:
        """
        사용자 입력을 실제 장소명으로 매칭
        간단한 문자열 매칭 사용
        """
        # 정확히 일치하는 경우 먼저 체크
        user_input_lower = user_input.lower().strip()
        
        for location, aliases in self.location_aliases.items():
            if user_input_lower == location.lower():
                return location
            for alias in aliases:
                if user_input_lower == alias.lower():
                    return location
        
        # 부분 문자열 매칭
        for location, aliases in self.location_aliases.items():
            if user_input_lower in location.lower() or location.lower() in user_input_lower:
                return location
            for alias in aliases:
                if user_input_lower in alias.lower() or alias.lower() in user_input_lower:
                    return location
        
        return None
    
    def create_streamlit_form(self):
        """Streamlit 웹 폼 생성"""
        st.set_page_config(
            page_title="헤맨만큼 내 땅이다 - 경험 공유",
            page_icon="🎨",
            layout="centered"
        )
        
        st.title("🎨 헤맨만큼 내 땅이다")
        st.subtitle("프리즈·키아프 관람 경험을 공유해주세요")
        
        with st.form("experience_form"):
            # 1. 장소 입력 (자동완성 지원)
            location_input = st.selectbox(
                "📍 어느 장소를 방문하셨나요?",
                options=[""] + list(self.location_aliases.keys()),
                help="장소명을 선택하거나 직접 입력하세요"
            )
            
            # 직접 입력 옵션
            if location_input == "":
                location_text = st.text_input(
                    "직접 입력",
                    placeholder="예: 국제갤러리, 리움, coex..."
                )
            else:
                location_text = location_input
            
            # 2. 감정 선택
            emotion = st.select_slider(
                "😊 어떤 감정을 느끼셨나요?",
                options=["😍 감동", "👍 추천", "🤔 어려움", "💸 비쌈", "😴 피로"],
                value="👍 추천"
            )
            emotion_emoji = emotion.split()[0]
            
            # 3. 제목
            title = st.text_input(
                "✏️ 한 줄 요약",
                placeholder="예: David Hockney 실물을 드디어 보다!"
            )
            
            # 4. 상세 경험
            experience = st.text_area(
                "📝 자세한 경험을 들려주세요",
                placeholder="어떤 작품이 인상적이었나요? 대기시간은? 꿀팁이 있다면?",
                height=150
            )
            
            # 5. 이미지 URL (선택)
            image_url = st.text_input(
                "📷 사진 URL (선택사항)",
                placeholder="https://..."
            )
            
            # 제출 버튼
            submitted = st.form_submit_button("🚀 경험 공유하기")
            
            if submitted:
                # 장소 매칭
                matched_location = self.match_location(location_text)
                
                if not matched_location:
                    st.error(f"❌ '{location_text}'를 찾을 수 없습니다. 다시 확인해주세요.")
                    st.info("💡 사용 가능한 장소: " + ", ".join(self.location_aliases.keys()))
                elif not title or not experience:
                    st.error("❌ 제목과 경험을 모두 입력해주세요.")
                else:
                    # 결과 표시 (Padlet 연동 부분은 제거)
                    st.success(f"✅ 성공적으로 저장되었습니다! 📍 {matched_location}")
                    st.balloons()
                    
                    # 저장된 데이터 표시
                    st.info(f"""
                    📍 장소: {matched_location}
                    {emotion_emoji} 감정: {emotion}
                    ✏️ 제목: {title}
                    📝 경험: {experience}
                    """)
    
    def create_google_forms_webhook(self):
        """
        Google Forms → Webhook → Padlet 연동
        Google Apps Script 사용
        """
        gas_code = '''
        // Google Apps Script 코드
        function onFormSubmit(e) {
          var response = e.response;
          var itemResponses = response.getItemResponses();
          
          // 응답 파싱
          var location = itemResponses[0].getResponse();
          var emotion = itemResponses[1].getResponse();
          var title = itemResponses[2].getResponse();
          var experience = itemResponses[3].getResponse();
          
          // 웹훅 엔드포인트로 전송
          var payload = {
            'location': location,
            'emotion': emotion,
            'title': title,
            'experience': experience
          };
          
          var options = {
            'method': 'post',
            'contentType': 'application/json',
            'payload': JSON.stringify(payload)
          };
          
          UrlFetchApp.fetch('YOUR_WEBHOOK_URL', options);
        }
        '''
        return gas_code
    
    def create_typeform_integration(self):
        """
        Typeform 통합 설정
        더 나은 UX와 조건부 로직 지원
        """
        typeform_config = {
            "title": "헤맨만큼 내 땅이다 - 경험 공유",
            "fields": [
                {
                    "type": "dropdown",
                    "title": "어느 장소를 방문하셨나요?",
                    "choices": list(self.location_aliases.keys()),
                    "required": True,
                    "properties": {
                        "alphabetical_order": False,
                        "randomize": False
                    }
                },
                {
                    "type": "opinion_scale",
                    "title": "방문 경험은 어떠셨나요?",
                    "properties": {
                        "start_at_one": False,
                        "steps": 5,
                        "labels": {
                            "left": "😴 피로",
                            "center": "🤔 보통",
                            "right": "😍 감동"
                        }
                    }
                },
                {
                    "type": "short_text",
                    "title": "한 줄로 요약한다면?",
                    "required": True
                },
                {
                    "type": "long_text",
                    "title": "자세한 경험을 들려주세요",
                    "required": True
                }
            ],
            "logic": [
                {
                    "type": "field",
                    "field": "location",
                    "condition": "is",
                    "value": "프리즈서울",
                    "action": {
                        "type": "jump",
                        "to": "frieze_specific_questions"
                    }
                }
            ]
        }
        return typeform_config


def main():
    """실행 예제"""
    system = UserFriendlyInputSystem()
    
    print("사용자 친화적 입력 시스템 옵션:")
    print("\n1. Streamlit 웹 앱")
    print("   - 실시간 자동완성")
    print("   - 즉각적인 피드백")
    print("   - 모바일 친화적")
    
    print("\n2. Google Forms + Webhook")
    print("   - 익숙한 인터페이스")
    print("   - 제한적 자동완성")
    print("   - Apps Script 필요")
    
    print("\n3. Typeform")
    print("   - 최고의 UX")
    print("   - 조건부 로직")
    print("   - 유료 기능 포함")
    
    # 위치 매칭 테스트
    test_inputs = ["국현", "mmca", "리움", "pace", "프리즈"]
    print("\n위치 자동 매칭 테스트:")
    for test in test_inputs:
        matched = system.match_location(test)
        print(f"  '{test}' → '{matched}'")


if __name__ == "__main__":
    main()