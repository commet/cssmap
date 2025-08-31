import requests
import json
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any

load_dotenv()

# Streamlit secrets 지원
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

class PadletAPI:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Padlet API client with API key"""
        # 1. 직접 전달된 API 키
        # 2. Streamlit secrets
        # 3. 환경변수
        # 4. .env 파일
        self.api_key = api_key
        
        if not self.api_key and HAS_STREAMLIT:
            try:
                self.api_key = st.secrets.get("PADLET_API_KEY")
            except:
                pass
        
        if not self.api_key:
            self.api_key = os.getenv('PADLET_API_KEY')
            
        if not self.api_key:
            raise ValueError("Padlet API key not found. Set PADLET_API_KEY in Streamlit secrets or environment variable.")
        
        self.base_url = "https://api.padlet.dev/v1"
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/vnd.api+json"
        }
    
    def get_board(self, board_id: str, include_posts: bool = True, include_sections: bool = True) -> Dict[str, Any]:
        """
        Get board information by ID
        
        Args:
            board_id: 16-character board ID from Padlet URL
            include_posts: Include all posts data
            include_sections: Include all sections data
        
        Returns:
            Board object with optional posts and sections
        """
        includes = []
        if include_posts:
            includes.append("posts")
        if include_sections:
            includes.append("sections")
        
        params = {"include": ",".join(includes)} if includes else {}
        endpoint = f"{self.base_url}/boards/{board_id}"
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def create_post(self, board_id: str, subject: str = "", body: str = "", 
                   attachment_url: str = None, color: str = None,
                   section_id: str = None, map_props: Dict = None, 
                   canvas_props: Dict = None) -> Dict[str, Any]:
        """
        Create a new post on a Padlet board
        
        Args:
            board_id: Board ID where post will be created
            subject: Post title/subject
            body: Post body content
            attachment_url: URL of attachment
            color: Post color (red, orange, green, blue, purple)
            section_id: Section ID to post in (for boards with sections)
            map_props: Map properties {"latitude": float, "longitude": float, "locationName": str}
            canvas_props: Canvas properties {"left": int, "top": int, "width": int}
        
        Returns:
            Created post object
        """
        endpoint = f"{self.base_url}/boards/{board_id}/posts"
        
        # Build content object
        content = {}
        if subject:
            content["subject"] = subject
        if body:
            content["body"] = body
        if attachment_url:
            content["attachment"] = {"url": attachment_url}
        
        # Build attributes
        attributes = {"content": content}
        if color:
            attributes["color"] = color
        if map_props:
            attributes["mapProps"] = map_props
        if canvas_props:
            attributes["canvasProps"] = canvas_props
        
        # Build data object
        data = {
            "data": {
                "type": "post",
                "attributes": attributes
            }
        }
        
        # Add section relationship if provided
        if section_id:
            data["data"]["relationships"] = {
                "section": {
                    "data": {"id": section_id}
                }
            }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def create_comment(self, post_id: str, html_content: str = None, 
                      attachment_url: str = None) -> Dict[str, Any]:
        """
        Create a comment on a post
        
        Args:
            post_id: The post ID to comment on
            html_content: HTML content of the comment
            attachment_url: URL of attachment
        
        Returns:
            Created comment object
        """
        endpoint = f"{self.base_url}/posts/{post_id}/comments"
        
        attributes = {}
        if html_content:
            attributes["htmlContent"] = html_content
        if attachment_url:
            attributes["attachment"] = {"url": attachment_url}
        
        data = {
            "data": {
                "type": "comment",
                "attributes": attributes
            }
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def get_current_user(self, include_boards: bool = False, 
                        include_organizations: bool = False) -> Dict[str, Any]:
        """
        Get current user information
        
        Args:
            include_boards: Include user's boards
            include_organizations: Include user's organizations
        
        Returns:
            User object with optional boards and organizations
        """
        includes = []
        if include_boards:
            includes.append("boards")
        if include_organizations:
            includes.append("organizations")
        
        params = {"include": ",".join(includes)} if includes else {}
        endpoint = f"{self.base_url}/me"
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def create_ai_board(self, instructions: str, role: str = "teacher", 
                       workspace_id: str = None) -> Dict[str, Any]:
        """
        Create an AI-generated board with natural language instructions
        
        Args:
            instructions: Natural language instructions (max 2000 chars)
            role: Role context for board creation
            workspace_id: Optional workspace ID
        
        Returns:
            Status URL to poll for board creation progress
        """
        endpoint = f"{self.base_url}/ai-recipe-boards"
        
        attributes = {
            "boardCreationInstructions": instructions,
            "role": role
        }
        if workspace_id:
            attributes["workspaceId"] = workspace_id
        
        data = {
            "data": {
                "type": "ai_recipe_board",
                "attributes": attributes
            }
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def get_ai_board_status(self, status_key: str) -> Dict[str, Any]:
        """
        Check AI board creation status
        
        Args:
            status_key: Status key from create_ai_board response
        
        Returns:
            Status object with board data when complete
        """
        endpoint = f"{self.base_url}/ai-recipe-boards/status/{status_key}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}


def extract_board_id_from_url(url: str) -> Optional[str]:
    """
    Extract 16-character board ID from Padlet URL
    Example: https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd -> blwpq840o1u57awd
    """
    # The board ID is typically the last 16 characters after the final hyphen
    parts = url.rstrip('/').split('/')
    if parts:
        last_part = parts[-1]
        # Find the last hyphen and get everything after it
        if '-' in last_part:
            potential_id = last_part.split('-')[-1]
            if 16 <= len(potential_id) <= 22:  # Board IDs are 16-22 chars
                return potential_id
    return None


def main():
    """Example usage of Padlet API for CSS map board"""
    
    # Initialize API
    padlet = PadletAPI()
    
    # Your CSS map board URL
    board_url = "https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd"
    board_id = extract_board_id_from_url(board_url)
    
    if not board_id:
        print("Could not extract board ID from URL")
        return
    
    print(f"Board ID: {board_id}")
    print("="*60)
    
    # 1. Get current user info
    print("\n1. Getting current user information...")
    user_info = padlet.get_current_user(include_boards=True)
    
    if "error" not in user_info:
        user_data = user_info.get("data", {}).get("attributes", {})
        print(f"✓ Logged in as: {user_data.get('name', 'Unknown')}")
        print(f"  Username: {user_data.get('username', 'N/A')}")
        print(f"  Email: {user_data.get('email', 'N/A')}")
    else:
        print(f"✗ Error: {user_info['error']}")
        if user_info.get('status_code') == 401:
            print("  Note: Check your API key")
        return
    
    # 2. Get board information with all posts
    print("\n2. Getting board information...")
    board_info = padlet.get_board(board_id, include_posts=True, include_sections=True)
    
    if "error" not in board_info:
        board_data = board_info.get("data", {}).get("attributes", {})
        print(f"✓ Board: {board_data.get('title', 'Unknown')}")
        print(f"  Description: {board_data.get('description', 'N/A')}")
        print(f"  Created by: {board_data.get('builder', {}).get('fullName', 'Unknown')}")
        
        # Show existing posts count
        posts = board_info.get("data", {}).get("relationships", {}).get("posts", {}).get("data", [])
        print(f"  Current posts: {len(posts)}")
    else:
        print(f"✗ Error: {board_info['error']}")
        if board_info.get('status_code') == 403:
            print("  Note: You need admin access to this board")
        return
    
    # 3. Create a post with map location
    print("\n3. Creating a new post on the map...")
    
    # Example locations for CSS meeting points
    locations = [
        {
            "name": "서울시청",
            "latitude": 37.5665,
            "longitude": 126.9780,
            "locationName": "서울시청 앞 광장"
        },
        {
            "name": "강남역",
            "latitude": 37.4979,
            "longitude": 127.0276,
            "locationName": "강남역 11번 출구"
        },
        {
            "name": "홍대입구",
            "latitude": 37.5563,
            "longitude": 126.9235,
            "locationName": "홍대입구역 9번 출구"
        }
    ]
    
    # Create a post for the first location
    location = locations[0]
    new_post = padlet.create_post(
        board_id=board_id,
        subject=f"CSS 모임 장소 - {location['name']}",
        body=f"다음 CSS 모임 장소 후보입니다.\n위치: {location['locationName']}\n\n참석 가능하신 분들은 댓글로 알려주세요!",
        color="blue",
        map_props={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "locationName": location["locationName"]
        }
    )
    
    if "error" not in new_post:
        post_data = new_post.get("data", {})
        post_id = post_data.get("id")
        print(f"✓ Post created successfully!")
        print(f"  Post ID: {post_id}")
        
        # 4. Add a comment to the post
        if post_id:
            print("\n4. Adding a comment to the post...")
            comment = padlet.create_comment(
                post_id=post_id,
                html_content="<p>좋은 장소네요! 👍 저는 참석 가능합니다.</p>"
            )
            
            if "error" not in comment:
                print("✓ Comment added successfully!")
            else:
                print(f"✗ Error adding comment: {comment['error']}")
    else:
        print(f"✗ Error creating post: {new_post['error']}")
        if new_post.get('status_code') == 403:
            print("  Note: You need admin/write access to this board")
    
    # 5. Example: Create an AI-generated board (optional)
    print("\n5. AI Board Creation Example (skipped - requires workspace)")
    print("  To create AI boards, you need a workspace ID")
    
    print("\n" + "="*60)
    print("✓ API test complete!")


if __name__ == "__main__":
    main()