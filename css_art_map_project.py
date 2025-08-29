import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from padlet_api_complete import PadletAPI, extract_board_id_from_url
from dotenv import load_dotenv

load_dotenv()

class CSSArtMapProject:
    """
    "헤맨만큼 내 땅이다" - CSS 미술 탐험 지도 프로젝트
    프리즈·키아프 기간 동안 미술애호가들의 전시 관람 경험을 기록하는 참여형 플랫폼
    """
    
    def __init__(self):
        self.api = PadletAPI()
        self.board_url = "https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd"
        self.board_id = extract_board_id_from_url(self.board_url)
        
        # 주요 전시 장소 좌표
        self.locations = {
            "코엑스": {"lat": 37.5116, "lng": 127.0594, "name": "COEX"},
            "프리즈서울": {"lat": 37.5116, "lng": 127.0594, "name": "Frieze Seoul"},
            "키아프": {"lat": 37.5116, "lng": 127.0594, "name": "KIAF"},
            "국제갤러리": {"lat": 37.5802, "lng": 126.9749, "name": "Kukje Gallery"},
            "리움미술관": {"lat": 37.5384, "lng": 126.9990, "name": "Leeum Museum"},
            "아트선재센터": {"lat": 37.5363, "lng": 126.9747, "name": "Art Sonje Center"},
            "갤러리현대": {"lat": 37.5789, "lng": 126.9770, "name": "Gallery Hyundai"},
            "페이스갤러리": {"lat": 37.5372, "lng": 127.0018, "name": "Pace Gallery"},
            "PKM갤러리": {"lat": 37.5794, "lng": 126.9742, "name": "PKM Gallery"},
            "삼청동": {"lat": 37.5830, "lng": 126.9830, "name": "Samcheong-dong"},
            "한남동": {"lat": 37.5345, "lng": 127.0045, "name": "Hannam-dong"},
            "성수동": {"lat": 37.5447, "lng": 127.0557, "name": "Seongsu-dong"}
        }
        
        # 감정 태그와 색상 매핑
        self.emotion_colors = {
            "😍": "red",     # 감동
            "😴": "blue",    # 피로
            "💸": "orange",  # 비쌈
            "🤔": "purple",  # 어려움
            "👍": "green"    # 추천
        }
    
    def post_visitor_experience(self, 
                               location_name: str,
                               title: str,
                               experience: str,
                               emotion: str = "👍",
                               image_url: Optional[str] = None) -> Dict:
        """
        방문자 경험을 지도에 게시
        
        Args:
            location_name: 장소명 (self.locations의 키)
            title: 게시물 제목
            experience: 경험 내용
            emotion: 감정 이모지
            image_url: 사진 URL (선택)
        
        Returns:
            생성된 게시물 정보
        """
        if location_name not in self.locations:
            return {"error": f"Unknown location: {location_name}"}
        
        location = self.locations[location_name]
        color = self.emotion_colors.get(emotion, "blue")
        
        # 게시물 생성
        post_data = self.api.create_post(
            board_id=self.board_id,
            subject=f"{emotion} {title}",
            body=f"{experience}\n\n📍 {location['name']}\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            color=color,
            attachment_url=image_url,
            map_props={
                "latitude": location["lat"],
                "longitude": location["lng"],
                "locationName": location["name"]
            }
        )
        
        return post_data
    
    def add_tip_comment(self, post_id: str, tip: str) -> Dict:
        """
        게시물에 팁이나 공감 댓글 추가
        
        Args:
            post_id: 댓글을 달 게시물 ID
            tip: 팁 또는 공감 내용
        
        Returns:
            생성된 댓글 정보
        """
        return self.api.create_comment(
            post_id=post_id,
            html_content=f"<p>{tip}</p>"
        )
    
    def batch_post_experiences(self, experiences: List[Dict]) -> List[Dict]:
        """
        여러 경험을 한번에 게시
        
        Args:
            experiences: 경험 정보 리스트
                [{"location": "코엑스", "title": "...", "experience": "...", "emotion": "😍"}, ...]
        
        Returns:
            생성된 게시물들의 정보
        """
        results = []
        for exp in experiences:
            result = self.post_visitor_experience(
                location_name=exp.get("location"),
                title=exp.get("title"),
                experience=exp.get("experience"),
                emotion=exp.get("emotion", "👍"),
                image_url=exp.get("image_url")
            )
            results.append(result)
            print(f"Posted: {exp.get('title')} at {exp.get('location')}")
        
        return results
    
    def get_popular_locations(self) -> Dict:
        """
        게시물이 많은 인기 장소 분석
        
        Returns:
            장소별 게시물 수와 감정 분포
        """
        board_data = self.api.get_board(self.board_id, include_posts=True)
        
        if "error" in board_data:
            return board_data
        
        # 게시물 분석 (실제 구현시 더 상세하게)
        stats = {
            "total_posts": 0,
            "locations": {},
            "emotions": {}
        }
        
        # 여기서 실제 데이터 분석 로직 구현
        # ...
        
        return stats


def example_scenarios():
    """실제 사용 시나리오 예제"""
    
    project = CSSArtMapProject()
    
    print("="*60)
    print("🎨 '헤맨만큼 내 땅이다' - CSS 미술 탐험 지도")
    print("="*60)
    
    # 시나리오 1: 지방에서 올라온 관람객
    print("\n📍 시나리오 1: 대구에서 올라온 김씨")
    experience1 = project.post_visitor_experience(
        location_name="코엑스",
        title="지방러의 첫 프리즈 도전기",
        experience="KTX 3시간, 지하철 40분... 벌써 지쳤지만 설레요! 대구에서는 이런 규모의 아트페어를 볼 수 없어서 더욱 기대됩니다. 입구부터 압도적이네요.",
        emotion="😅"
    )
    
    if "error" not in experience1:
        post_id = experience1.get("data", {}).get("id")
        print(f"✓ 게시물 생성: {post_id}")
        
        # 다른 사용자의 공감 댓글
        if post_id:
            project.add_tip_comment(
                post_id=post_id,
                tip="저도 부산에서 왔어요! 지방러끼리 파이팅해요 💪"
            )
            print("  └ 댓글 추가됨")
    
    # 시나리오 2: 감동받은 순간
    print("\n📍 시나리오 2: David Hockney 실물을 본 감동")
    experience2 = project.post_visitor_experience(
        location_name="프리즈서울",
        title="David Hockney 실물 감동",
        experience="TV로만 보던 작품을 실제로 보니 눈물이... 붓터치 하나하나가 살아있어요. 색감이 화면으로는 절대 전달될 수 없는 깊이가 있네요.",
        emotion="😍"
    )
    
    # 시나리오 3: 실용적인 팁 공유
    print("\n📍 시나리오 3: 줄 서기 포기 경험")
    experience3 = project.post_visitor_experience(
        location_name="국제갤러리",
        title="국제갤러리 줄 포기... VIP가 부럽다",
        experience="1시간 30분 예상 대기. 다리도 아프고 배도 고파서 포기했습니다. 평일 오전이 답인 것 같아요. 주말은 정말 피하세요!",
        emotion="😴"
    )
    
    if "error" not in experience3:
        post_id = experience3.get("data", {}).get("id")
        if post_id:
            # 꿀팁 댓글
            project.add_tip_comment(
                post_id=post_id,
                tip="평일 오전 10시 오픈 직후가 가장 한가해요! 점심시간도 의외로 괜찮습니다."
            )
            print("  └ 꿀팁 댓글 추가됨")
    
    # 시나리오 4: 예상외의 발견
    print("\n📍 시나리오 4: 숨은 명소 발견")
    experience4 = project.post_visitor_experience(
        location_name="삼청동",
        title="작은 갤러리의 큰 감동",
        experience="프리즈 인파를 피해 삼청동 작은 갤러리들을 돌았는데, 오히려 여기가 진짜네요. 천천히 작품을 감상할 수 있고, 갤러리스트가 직접 설명도 해주십니다.",
        emotion="👍"
    )
    
    # 시나리오 5: 초보자의 질문
    print("\n📍 시나리오 5: 미술 초보자의 첫 도전")
    experience5 = project.post_visitor_experience(
        location_name="리움미술관",
        title="미술 초보인데... 이게 맞나요?",
        experience="처음 와봤는데 어디서부터 봐야 할지 모르겠어요. 다들 뭔가 아는 듯한 표정으로 보시는데 저만 모르는 건가요? 초보자 가이드가 있으면 좋겠어요.",
        emotion="🤔"
    )
    
    # 배치 게시 예제
    print("\n📍 여러 경험 한번에 게시하기")
    batch_experiences = [
        {
            "location": "페이스갤러리",
            "title": "디지털 아트의 미래",
            "experience": "NFT 작품들이 생각보다 많네요. 시대가 변하고 있음을 실감합니다.",
            "emotion": "🤔"
        },
        {
            "location": "성수동",
            "title": "성수동 카페투어",
            "experience": "전시 보다가 지쳐서 카페 투어. 이것도 나름 예술 감상인가요? ㅎㅎ",
            "emotion": "😴"
        },
        {
            "location": "한남동",
            "title": "한남동 갤러리 밀집 지역",
            "experience": "걸어서 여러 갤러리를 둘러볼 수 있어 좋아요. 동선 짜기 최고!",
            "emotion": "👍"
        }
    ]
    
    # results = project.batch_post_experiences(batch_experiences)
    
    print("\n" + "="*60)
    print("✓ 모든 시나리오 실행 완료!")
    print("\n💡 이렇게 수집된 데이터는:")
    print("- 실시간으로 Padlet 지도에 표시됩니다")
    print("- 9/4 '관람객의 밤' 행사에서 활용됩니다")
    print("- 내년 프리즈를 위한 가이드맵이 됩니다")


if __name__ == "__main__":
    example_scenarios()