"""
지금 바로 실행 가능한 Padlet API 테스트
실행 결과를 직접 웹사이트에서 확인하세요!
"""

import os
from datetime import datetime
from padlet_api_complete import PadletAPI, extract_board_id_from_url
from dotenv import load_dotenv

load_dotenv()

def test_padlet_api():
    """실제로 작동하는지 테스트"""
    
    print("\n" + "="*60)
    print("🚀 Padlet API 실제 테스트 시작!")
    print("="*60)
    
    # API 초기화
    try:
        api = PadletAPI()
        print("✅ API 연결 성공")
    except Exception as e:
        print(f"❌ API 연결 실패: {e}")
        print("\n💡 해결방법:")
        print("1. .env 파일에 API 키가 있는지 확인")
        print("2. PADLET_API_KEY=pdltp_xxx... 형식인지 확인")
        return
    
    # 보드 정보
    board_url = "https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd"
    board_id = extract_board_id_from_url(board_url)
    
    print(f"\n📌 대상 보드:")
    print(f"   URL: {board_url}")
    print(f"   ID: {board_id}")
    
    # 선택 메뉴
    print("\n무엇을 테스트하시겠습니까?")
    print("1. 보드 정보 조회 (읽기만)")
    print("2. 테스트 게시물 작성 (지도에 추가)")
    print("3. 현재 게시물 통계 보기")
    print("0. 취소")
    
    choice = input("\n선택 (0-3): ")
    
    if choice == "1":
        # 보드 정보 조회
        print("\n📊 보드 정보 조회 중...")
        board_data = api.get_board(board_id, include_posts=True)
        
        if "error" not in board_data:
            board_info = board_data.get("data", {}).get("attributes", {})
            print(f"\n✅ 보드 정보:")
            print(f"   제목: {board_info.get('title', 'N/A')}")
            print(f"   설명: {board_info.get('description', 'N/A')}")
            print(f"   작성자: {board_info.get('builder', {}).get('fullName', 'N/A')}")
            
            posts = board_data.get("data", {}).get("relationships", {}).get("posts", {}).get("data", [])
            print(f"   현재 게시물 수: {len(posts)}개")
            
            print(f"\n💡 웹사이트에서 확인: {board_url}")
        else:
            print(f"❌ 오류: {board_data['error']}")
            if board_data.get('status_code') == 403:
                print("   → 권한 문제: Padlet 유료 구독 또는 보드 관리자 권한 필요")
    
    elif choice == "2":
        # 테스트 게시물 작성
        print("\n✍️ 테스트 게시물을 작성합니다...")
        print("어느 위치에 게시하시겠습니까?")
        print("1. 코엑스 (프리즈/키아프)")
        print("2. 국제갤러리 (삼청동)")
        print("3. 리움미술관 (한남동)")
        
        loc_choice = input("선택 (1-3): ")
        
        locations = {
            "1": {"name": "코엑스", "lat": 37.5116, "lng": 127.0594},
            "2": {"name": "국제갤러리", "lat": 37.5802, "lng": 126.9749},
            "3": {"name": "리움미술관", "lat": 37.5384, "lng": 126.9990}
        }
        
        if loc_choice in locations:
            loc = locations[loc_choice]
            
            # 게시물 작성
            timestamp = datetime.now().strftime("%H:%M")
            result = api.create_post(
                board_id=board_id,
                subject=f"🧪 API 테스트 - {timestamp}",
                body=f"Claude Code에서 작성한 테스트 게시물입니다.\n위치: {loc['name']}\n시간: {timestamp}",
                color="blue",
                map_props={
                    "latitude": loc["lat"],
                    "longitude": loc["lng"],
                    "locationName": loc["name"]
                }
            )
            
            if "error" not in result:
                print(f"\n✅ 게시물 작성 성공!")
                print(f"   위치: {loc['name']}")
                print(f"   시간: {timestamp}")
                print(f"\n🌐 지금 확인하세요:")
                print(f"   {board_url}")
                print(f"\n   → 지도에서 파란색 핀을 찾아보세요!")
            else:
                print(f"❌ 작성 실패: {result['error']}")
                if result.get('status_code') == 403:
                    print("   → 쓰기 권한이 필요합니다")
    
    elif choice == "3":
        # 통계 보기
        print("\n📈 게시물 통계 분석 중...")
        board_data = api.get_board(board_id, include_posts=True)
        
        if "error" not in board_data:
            included = board_data.get("included", [])
            
            # 간단한 통계
            total_posts = 0
            locations_count = {}
            recent_posts = []
            
            for item in included:
                if item.get("type") == "post":
                    total_posts += 1
                    
                    # 위치 정보
                    map_props = item.get("attributes", {}).get("mapProps", {})
                    loc_name = map_props.get("locationName", "Unknown")
                    locations_count[loc_name] = locations_count.get(loc_name, 0) + 1
                    
                    # 최근 게시물
                    content = item.get("attributes", {}).get("content", {})
                    subject = content.get("subject", "")
                    if subject:
                        recent_posts.append(subject)
            
            print(f"\n📊 현재 통계:")
            print(f"   총 게시물: {total_posts}개")
            
            if locations_count:
                print(f"\n   인기 장소:")
                for loc, count in sorted(locations_count.items(), key=lambda x: x[1], reverse=True)[:5]:
                    print(f"   • {loc}: {count}개")
            
            if recent_posts:
                print(f"\n   최근 게시물:")
                for post in recent_posts[:3]:
                    print(f"   • {post[:50]}...")
        else:
            print(f"❌ 통계 조회 실패: {board_data['error']}")
    
    print("\n" + "="*60)
    print("테스트 완료!")
    print("="*60)


if __name__ == "__main__":
    test_padlet_api()