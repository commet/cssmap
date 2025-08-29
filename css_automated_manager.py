"""
CSS "헤맨만큼 내 땅이다" 자동화 관리 시스템
실시간 데이터 수집, 분석, 모더레이션을 위한 통합 도구
"""

import os
import json
import time
import schedule
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from collections import Counter, defaultdict
import re
from padlet_api_complete import PadletAPI, extract_board_id_from_url
from dotenv import load_dotenv

load_dotenv()

class CSSArtMapAutomation:
    """
    자동화된 Padlet 관리 시스템
    - 실시간 모니터링
    - 자동 백업
    - 통계 생성
    - 콘텐츠 모더레이션
    """
    
    def __init__(self):
        self.api = PadletAPI()
        self.board_url = "https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd"
        self.board_id = extract_board_id_from_url(self.board_url)
        
        # 데이터 저장 경로
        self.data_dir = "css_art_map_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 부적절한 단어 필터 (예시)
        self.blocked_words = [
            "광고", "홍보", "판매", "할인",
            "욕설1", "욕설2"  # 실제 운영시 추가
        ]
        
        # 통계 추적
        self.stats = {
            "total_posts": 0,
            "total_comments": 0,
            "popular_locations": Counter(),
            "emotion_distribution": Counter(),
            "peak_hours": Counter(),
            "active_users": set()
        }
    
    def backup_board_data(self) -> str:
        """
        현재 보드 데이터를 JSON으로 백업
        
        Returns:
            백업 파일 경로
        """
        print(f"\n🔄 백업 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 보드 데이터 가져오기
        board_data = self.api.get_board(self.board_id, include_posts=True, include_sections=True)
        
        if "error" in board_data:
            print(f"❌ 백업 실패: {board_data['error']}")
            return None
        
        # 백업 파일명 (시간별)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.data_dir, f"backup_{timestamp}.json")
        
        # JSON 저장
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(board_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 백업 완료: {backup_file}")
        return backup_file
    
    def analyze_board_activity(self) -> Dict:
        """
        보드 활동 분석 및 통계 생성
        
        Returns:
            분석 결과 딕셔너리
        """
        print(f"\n📊 활동 분석 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        board_data = self.api.get_board(self.board_id, include_posts=True)
        
        if "error" in board_data:
            return {"error": board_data["error"]}
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "total_posts": 0,
            "posts_by_location": defaultdict(int),
            "posts_by_emotion": defaultdict(int),
            "posts_by_hour": defaultdict(int),
            "most_active_time": None,
            "trending_keywords": [],
            "engagement_rate": 0
        }
        
        posts = board_data.get("data", {}).get("relationships", {}).get("posts", {}).get("data", [])
        analysis["total_posts"] = len(posts)
        
        # 실제 포스트 데이터가 included에 있다면 분석
        included = board_data.get("included", [])
        post_contents = []
        
        for item in included:
            if item.get("type") == "post":
                attributes = item.get("attributes", {})
                content = attributes.get("content", {})
                
                # 텍스트 수집
                subject = content.get("subject", "")
                body = content.get("bodyHtml", "")
                post_contents.append(f"{subject} {body}")
                
                # 위치 분석
                map_props = attributes.get("mapProps", {})
                if map_props.get("locationName"):
                    analysis["posts_by_location"][map_props["locationName"]] += 1
                
                # 시간대 분석
                created_at = attributes.get("createdAt", "")
                if created_at:
                    try:
                        post_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        hour = post_time.hour
                        analysis["posts_by_hour"][hour] += 1
                    except:
                        pass
                
                # 감정 분석 (이모지 찾기)
                emotions = ["😍", "😴", "💸", "🤔", "👍"]
                for emotion in emotions:
                    if emotion in subject or emotion in body:
                        analysis["posts_by_emotion"][emotion] += 1
        
        # 키워드 추출 (간단한 버전)
        all_text = " ".join(post_contents)
        words = re.findall(r'[가-힣]+', all_text)  # 한글 단어만 추출
        word_freq = Counter(words)
        
        # 불용어 제거 및 상위 키워드
        stopwords = {"있습니다", "있어요", "합니다", "해요", "이", "가", "을", "를", "의", "에", "와", "과"}
        filtered_words = [(word, count) for word, count in word_freq.most_common(20) 
                         if word not in stopwords and len(word) > 1]
        analysis["trending_keywords"] = filtered_words[:10]
        
        # 가장 활발한 시간대
        if analysis["posts_by_hour"]:
            peak_hour = max(analysis["posts_by_hour"].items(), key=lambda x: x[1])
            analysis["most_active_time"] = f"{peak_hour[0]}시"
        
        # 결과 저장
        analysis_file = os.path.join(self.data_dir, f"analysis_{datetime.now().strftime('%Y%m%d')}.json")
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 분석 완료:")
        print(f"  - 총 게시물: {analysis['total_posts']}")
        print(f"  - 인기 장소: {dict(list(analysis['posts_by_location'].items())[:3])}")
        print(f"  - 주요 감정: {dict(analysis['posts_by_emotion'])}")
        print(f"  - 트렌딩 키워드: {[w[0] for w in analysis['trending_keywords'][:5]]}")
        
        return analysis
    
    def moderate_content(self) -> List[Dict]:
        """
        부적절한 콘텐츠 감지 및 플래그
        
        Returns:
            문제가 있는 게시물 리스트
        """
        print(f"\n🔍 콘텐츠 모더레이션: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        board_data = self.api.get_board(self.board_id, include_posts=True)
        
        if "error" in board_data:
            return []
        
        flagged_posts = []
        included = board_data.get("included", [])
        
        for item in included:
            if item.get("type") == "post":
                post_id = item.get("id")
                attributes = item.get("attributes", {})
                content = attributes.get("content", {})
                
                subject = content.get("subject", "")
                body = content.get("bodyHtml", "")
                full_text = f"{subject} {body}".lower()
                
                # 부적절한 단어 체크
                for blocked_word in self.blocked_words:
                    if blocked_word.lower() in full_text:
                        flagged_posts.append({
                            "post_id": post_id,
                            "reason": f"금지 단어 포함: {blocked_word}",
                            "subject": subject,
                            "created_at": attributes.get("createdAt")
                        })
                        break
                
                # 스팸 패턴 체크 (연속된 특수문자, URL 남발 등)
                if full_text.count("http") > 3:
                    flagged_posts.append({
                        "post_id": post_id,
                        "reason": "과도한 링크 포함",
                        "subject": subject,
                        "created_at": attributes.get("createdAt")
                    })
        
        if flagged_posts:
            print(f"⚠️ 검토 필요 게시물 {len(flagged_posts)}개 발견")
            for post in flagged_posts:
                print(f"  - {post['subject'][:30]}... ({post['reason']})")
        else:
            print("✅ 모든 콘텐츠 정상")
        
        return flagged_posts
    
    def generate_daily_report(self) -> str:
        """
        일일 리포트 생성
        
        Returns:
            리포트 텍스트
        """
        print(f"\n📈 일일 리포트 생성: {datetime.now().strftime('%Y-%m-%d')}")
        
        analysis = self.analyze_board_activity()
        
        report = f"""
========================================
🎨 헤맨만큼 내 땅이다 - 일일 리포트
날짜: {datetime.now().strftime('%Y년 %m월 %d일')}
========================================

📊 오늘의 통계
-----------------
• 총 게시물 수: {analysis.get('total_posts', 0)}개
• 가장 활발한 시간: {analysis.get('most_active_time', 'N/A')}

🏆 인기 장소 TOP 3
-----------------"""
        
        for i, (location, count) in enumerate(list(analysis.get('posts_by_location', {}).items())[:3], 1):
            report += f"\n{i}. {location}: {count}개 게시물"
        
        report += "\n\n😊 감정 분포\n-----------------"
        emotions_map = {
            "😍": "감동",
            "😴": "피로", 
            "💸": "비싼",
            "🤔": "어려움",
            "👍": "추천"
        }
        
        for emotion, count in analysis.get('posts_by_emotion', {}).items():
            report += f"\n• {emotion} {emotions_map.get(emotion, '')}: {count}개"
        
        report += "\n\n🔥 트렌딩 키워드\n-----------------"
        for keyword, count in analysis.get('trending_keywords', [])[:5]:
            report += f"\n• {keyword} ({count}회)"
        
        report += "\n\n========================================\n"
        
        # 리포트 저장
        report_file = os.path.join(self.data_dir, f"daily_report_{datetime.now().strftime('%Y%m%d')}.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(report)
        return report
    
    def auto_respond_to_questions(self):
        """
        초보자 질문에 자동 응답 (도움말 댓글)
        """
        print(f"\n💬 자동 응답 체크: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        board_data = self.api.get_board(self.board_id, include_posts=True)
        
        if "error" in board_data:
            return
        
        included = board_data.get("included", [])
        
        for item in included:
            if item.get("type") == "post":
                content = item.get("attributes", {}).get("content", {})
                body = content.get("bodyHtml", "")
                
                # 질문 패턴 감지
                if any(keyword in body for keyword in ["처음", "초보", "어디부터", "모르겠", "도와"]):
                    post_id = item.get("id")
                    
                    # 이미 응답했는지 체크 (실제 구현시 DB 필요)
                    # 여기서는 예시로만
                    
                    help_message = """
                    <p>안녕하세요! 처음 오신 분을 위한 팁을 드릴게요 😊</p>
                    <ul>
                        <li>평일 오전이 가장 한가합니다</li>
                        <li>프리즈는 코엑스, 키아프는 같은 장소입니다</li>
                        <li>삼청동 작은 갤러리들도 놓치지 마세요</li>
                        <li>편한 신발은 필수입니다!</li>
                    </ul>
                    <p>즐거운 관람 되세요! 🎨</p>
                    """
                    
                    # 도움말 댓글 달기 (중복 방지 로직 필요)
                    # self.api.create_comment(post_id, help_message)
                    print(f"  ℹ️ 초보자 질문 감지: {content.get('subject', '')[:30]}...")
    
    def run_scheduled_tasks(self):
        """
        정기 작업 스케줄링
        """
        print("\n⏰ 자동화 시스템 시작")
        print("="*50)
        
        # 매 시간 백업
        schedule.every().hour.do(self.backup_board_data)
        
        # 30분마다 통계 분석
        schedule.every(30).minutes.do(self.analyze_board_activity)
        
        # 10분마다 모더레이션
        schedule.every(10).minutes.do(self.moderate_content)
        
        # 매일 오후 9시 일일 리포트
        schedule.every().day.at("21:00").do(self.generate_daily_report)
        
        # 15분마다 자동 응답 체크
        schedule.every(15).minutes.do(self.auto_respond_to_questions)
        
        print("스케줄 설정 완료:")
        print("• 매시간: 데이터 백업")
        print("• 30분마다: 활동 분석")
        print("• 10분마다: 콘텐츠 모더레이션")
        print("• 매일 21시: 일일 리포트")
        print("• 15분마다: 자동 응답")
        print("="*50)
        
        # 즉시 한 번 실행
        self.backup_board_data()
        self.analyze_board_activity()
        self.moderate_content()
        
        # 스케줄 루프
        while True:
            schedule.run_pending()
            time.sleep(60)  # 1분마다 체크


class EventDayManager:
    """
    9월 4일 '관람객의 밤' 행사 당일 특별 관리
    """
    
    def __init__(self):
        self.automation = CSSArtMapAutomation()
        self.api = self.automation.api
        self.board_id = self.automation.board_id
    
    def create_live_event_post(self, message: str, location: str = "코엑스") -> Dict:
        """
        행사 현장에서 실시간 게시물 생성
        
        Args:
            message: 현장 메시지
            location: 행사 장소
        
        Returns:
            생성된 게시물
        """
        locations = {
            "코엑스": {"lat": 37.5116, "lng": 127.0594}
        }
        
        loc = locations.get(location, locations["코엑스"])
        
        return self.api.create_post(
            board_id=self.board_id,
            subject=f"🔴 LIVE: 관람객의 밤 현장",
            body=f"{message}\n\n#관람객의밤 #CSS2025 #실시간",
            color="red",
            map_props={
                "latitude": loc["lat"],
                "longitude": loc["lng"],
                "locationName": f"관람객의 밤 - {location}"
            }
        )
    
    def get_live_statistics(self) -> Dict:
        """
        행사용 실시간 통계 (큰 화면 표출용)
        
        Returns:
            시각화 가능한 통계 데이터
        """
        analysis = self.automation.analyze_board_activity()
        
        # 화면 표출용 포맷
        display_stats = {
            "title": "🎨 헤맨만큼 내 땅이다 - LIVE",
            "update_time": datetime.now().strftime("%H:%M:%S"),
            "metrics": {
                "총 참여자": f"{analysis.get('total_posts', 0)}명",
                "오늘 참여": f"{analysis.get('posts_today', 0)}명",
                "실시간 활동": "🟢 활발"
            },
            "top_locations": [
                {"name": loc, "count": count, "bar_width": count * 10}
                for loc, count in list(analysis.get('posts_by_location', {}).items())[:5]
            ],
            "emotions": {
                "😍 감동": analysis.get('posts_by_emotion', {}).get('😍', 0),
                "👍 추천": analysis.get('posts_by_emotion', {}).get('👍', 0),
                "🤔 고민": analysis.get('posts_by_emotion', {}).get('🤔', 0),
                "😴 피로": analysis.get('posts_by_emotion', {}).get('😴', 0)
            },
            "trending_now": [kw[0] for kw in analysis.get('trending_keywords', [])[:3]]
        }
        
        return display_stats
    
    def create_event_summary(self) -> str:
        """
        행사 종료 후 요약 생성
        
        Returns:
            행사 요약 텍스트
        """
        stats = self.get_live_statistics()
        
        summary = f"""
🎉 관람객의 밤 - 참여 요약
========================

📊 참여 통계
• 총 {stats['metrics']['총 참여자']} 참여
• 가장 인기있던 장소: {stats['top_locations'][0]['name'] if stats['top_locations'] else 'N/A'}

😊 관람객들의 감정
• 감동 {stats['emotions']['😍 감동']}개
• 추천 {stats['emotions']['👍 추천']}개
• 고민 {stats['emotions']['🤔 고민']}개

🔥 오늘의 키워드
{', '.join(stats['trending_now'])}

감사합니다! 내년에 또 만나요 🎨
"""
        return summary


def main():
    """메인 실행 함수"""
    
    print("""
    ╔══════════════════════════════════════════════╗
    ║  🎨 CSS "헤맨만큼 내 땅이다" 관리 시스템     ║
    ╚══════════════════════════════════════════════╝
    
    선택하세요:
    1. 자동화 시스템 실행 (24/7 모니터링)
    2. 일회성 백업 실행
    3. 현재 통계 분석
    4. 일일 리포트 생성
    5. 행사 당일 모드 (9/4)
    0. 종료
    """)
    
    choice = input("선택 (0-5): ")
    
    automation = CSSArtMapAutomation()
    
    if choice == "1":
        automation.run_scheduled_tasks()
    elif choice == "2":
        automation.backup_board_data()
    elif choice == "3":
        automation.analyze_board_activity()
    elif choice == "4":
        automation.generate_daily_report()
    elif choice == "5":
        event = EventDayManager()
        print("\n🔴 행사 당일 모드 활성화")
        
        while True:
            print("\n1. 실시간 통계 보기")
            print("2. 현장 메시지 게시")
            print("3. 행사 요약 생성")
            print("0. 종료")
            
            event_choice = input("선택: ")
            
            if event_choice == "1":
                stats = event.get_live_statistics()
                print(json.dumps(stats, ensure_ascii=False, indent=2))
            elif event_choice == "2":
                msg = input("현장 메시지: ")
                event.create_live_event_post(msg)
                print("✅ 게시 완료")
            elif event_choice == "3":
                print(event.create_event_summary())
            elif event_choice == "0":
                break
    
    print("\n👋 프로그램을 종료합니다.")


if __name__ == "__main__":
    main()