"""Test Padlet API connection"""
import os
from padlet_api_complete import PadletAPI

# 제공된 API 키 설정
API_KEY = "pdltp_d271492999e5db6c2cb47a28ea8598a13d343d0a7d32880eeb87d4ea89074944205d6c"
os.environ['PADLET_API_KEY'] = API_KEY

print(f"Testing with API Key: {API_KEY[:20]}...")

try:
    # API 클라이언트 초기화
    padlet_api = PadletAPI()
    board_id = "blwpq840o1u57awd"
    
    print(f"Fetching board: {board_id}")
    
    # 보드 데이터 가져오기
    board_data = padlet_api.get_board(board_id, include_posts=True)
    
    if 'error' in board_data:
        print(f"ERROR: {board_data['error']}")
        print(f"Status Code: {board_data.get('status_code', 'N/A')}")
    else:
        print("SUCCESS! Board data received")
        print(f"Board keys: {board_data.keys()}")
        
        # 전체 데이터 구조 출력
        import json
        print("\n=== Full Board Data ===")
        print(json.dumps(board_data, indent=2, ensure_ascii=False)[:2000])
        
        if 'data' in board_data:
            board_info = board_data['data']
            print(f"\n=== Board Info ===")
            print(f"Board ID: {board_info.get('id', 'N/A')}")
            if 'attributes' in board_info:
                attrs = board_info['attributes']
                print(f"Board title: {attrs.get('name', 'N/A')}")
                print(f"Board description: {attrs.get('description', 'N/A')}")
                print(f"Board type: {attrs.get('wall_type', 'N/A')}")
        
        if 'included' in board_data:
            all_items = board_data['included']
            print(f"\n=== Included Items ===")
            print(f"Total items: {len(all_items)}")
            
            # 타입별로 분류
            types = {}
            for item in all_items:
                item_type = item.get('type', 'unknown')
                if item_type not in types:
                    types[item_type] = []
                types[item_type].append(item)
            
            print(f"Item types found: {list(types.keys())}")
            for type_name, items in types.items():
                print(f"  {type_name}: {len(items)} items")
            
            # posts 상세 확인
            if 'posts' in types:
                posts = types['posts']
                print(f"\n=== Posts Details ===")
                for i, post in enumerate(posts[:3]):  # 처음 3개만
                    attrs = post.get('attributes', {})
                    print(f"\nPost {i+1}:")
                    print(f"  ID: {post.get('id')}")
                    print(f"  Subject: {attrs.get('subject', 'N/A')}")
                    print(f"  Body: {attrs.get('body', 'N/A')[:100]}...")
                
except Exception as e:
    print(f"EXCEPTION: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()