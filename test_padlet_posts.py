"""Test Padlet posts data structure"""
import os
from padlet_api_complete import PadletAPI
from datetime import datetime
import sys
import json

# 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

# API 키 설정
API_KEY = "pdltp_d271492999e5db6c2cb47a28ea8598a13d343d0a7d32880eeb87d4ea89074944205d6c"
os.environ['PADLET_API_KEY'] = API_KEY

try:
    # API 클라이언트 초기화
    padlet_api = PadletAPI()
    board_id = "blwpq840o1u57awd"
    
    print(f"Fetching board: {board_id}")
    
    # 보드 데이터 가져오기
    board_data = padlet_api.get_board(board_id, include_posts=True)
    
    if 'included' in board_data:
        posts = [item for item in board_data['included'] if item.get('type') == 'post']
        
        print(f"\n총 {len(posts)}개의 포스트 발견")
        print("="*50)
        
        for i, post in enumerate(posts[:5], 1):  # 처음 5개만 상세 출력
            attrs = post.get('attributes', {})
            
            # attributes 전체 키 확인
            print(f"\n포스트 {i}:")
            print(f"  ID: {post.get('id')}")
            print(f"  Available attributes: {list(attrs.keys())}")
            
            # content 내부 확인
            content = attrs.get('content', {})
            print(f"  Content keys: {list(content.keys()) if content else 'Empty'}")
            if content:
                print(f"    제목: {content.get('subject', 'N/A')}")
                print(f"    내용: {content.get('body', 'N/A')[:200] if content.get('body') else 'N/A'}")
                print(f"    첨부: {content.get('attachment', 'N/A')}")
            
            # mapProps 확인 (위치 정보)
            map_props = attrs.get('mapProps', {})
            if map_props:
                print(f"  Map Properties: {map_props}")
                print(f"    위도: {map_props.get('latitude', 'N/A')}")
                print(f"    경도: {map_props.get('longitude', 'N/A')}")
                print(f"    장소명: {map_props.get('locationName', 'N/A')}")
            print(f"  생성일: {attrs.get('created_at', 'N/A')}")
            print(f"  수정일: {attrs.get('updated_at', 'N/A')}")
            print(f"  색상: {attrs.get('color', 'N/A')}")
            
            # attachment 확인
            attachment = attrs.get('attachment')
            if attachment:
                print(f"  첨부파일: {attachment.get('type', 'N/A')} - {attachment.get('url', 'N/A')[:50]}...")
            
            print("-"*40)
        
        # 전체 통계
        print(f"\n=== 전체 통계 ===")
        posts_with_location = [p for p in posts if p.get('attributes', {}).get('location', {}).get('latitude')]
        print(f"위치 정보가 있는 포스트: {len(posts_with_location)}개")
        
        # 감정 이모지 통계
        emotions = {'😍': 0, '👍': 0, '😴': 0, '💸': 0, '🤔': 0}
        for post in posts:
            body = post.get('attributes', {}).get('body', '')
            for emoji in emotions:
                if emoji in body:
                    emotions[emoji] += 1
        
        print("\n감정 이모지 통계:")
        for emoji, count in emotions.items():
            print(f"  {emoji}: {count}개")
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()