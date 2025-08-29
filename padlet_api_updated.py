import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

class PadletAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('PADLET_API_KEY')
        if not self.api_key:
            raise ValueError("Padlet API key not found")
        
        self.base_url = "https://api.padlet.dev"
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/vnd.api+json"
        }
    
    def get_board(self, board_id):
        """
        Get board information
        
        Args:
            board_id (str): The ID of the Padlet board
        
        Returns:
            dict: Board information
        """
        endpoint = f"{self.base_url}/board/{board_id}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def create_post(self, board_id, subject, body="", location=None, attachment_url=None):
        """
        Create a new post on a Padlet board
        
        Args:
            board_id (str): The ID of the Padlet board
            subject (str): Title of the post
            body (str): Content of the post
            location (dict): Location data for map boards {"lat": float, "lng": float, "name": str}
            attachment_url (str): URL of attachment to include
        
        Returns:
            dict: Created post information
        """
        endpoint = f"{self.base_url}/post"
        
        data = {
            "data": {
                "type": "post",
                "attributes": {
                    "boardId": board_id,
                    "subject": subject,
                    "body": body
                }
            }
        }
        
        # Add location for map boards
        if location:
            data["data"]["attributes"]["location"] = {
                "latitude": location.get("lat"),
                "longitude": location.get("lng"),
                "name": location.get("name", "")
            }
        
        # Add attachment if provided
        if attachment_url:
            data["data"]["attributes"]["attachment"] = {
                "url": attachment_url
            }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def create_comment(self, post_id, content):
        """
        Create a comment on a post
        
        Args:
            post_id (str): The ID of the post
            content (str): Comment content
        
        Returns:
            dict: Created comment information
        """
        endpoint = f"{self.base_url}/comment"
        
        data = {
            "data": {
                "type": "comment",
                "attributes": {
                    "postId": post_id,
                    "body": content
                }
            }
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def get_current_user(self):
        """Get current user information"""
        endpoint = f"{self.base_url}/user/current"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}

def extract_board_id_from_url(url):
    """
    Extract board ID from Padlet URL
    Example: https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd -> blwpq840o1u57awd
    """
    parts = url.split('/')
    if len(parts) > 0:
        last_part = parts[-1]
        if '-' in last_part:
            return last_part.split('-')[-1]
    return None

def main():
    # Initialize API
    padlet = PadletAPI()
    
    # Your map board URL
    board_url = "https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd"
    board_id = extract_board_id_from_url(board_url)
    
    if not board_id:
        print("Could not extract board ID from URL")
        return
    
    print(f"Board ID: {board_id}")
    
    # Example 1: Get board information
    print("\n" + "="*50)
    print("Getting board information...")
    board_info = padlet.get_board(board_id)
    
    if "error" in board_info:
        print(f"Error: {board_info['error']}")
        if board_info.get('status_code') == 403:
            print("Note: You need admin access to this board or a paid Padlet subscription")
    else:
        print(f"Board retrieved successfully!")
        print(json.dumps(board_info, indent=2))
    
    # Example 2: Create a post with location (for map board)
    print("\n" + "="*50)
    print("Creating a post on the map...")
    
    # Seoul location as example
    location_data = {
        "lat": 37.5665,
        "lng": 126.9780,
        "name": "서울시청"
    }
    
    new_post = padlet.create_post(
        board_id=board_id,
        subject="CSS 모임 장소",
        body="여기서 다음 CSS 모임을 진행할 예정입니다!",
        location=location_data
    )
    
    if "error" in new_post:
        print(f"Error creating post: {new_post['error']}")
    else:
        print("Post created successfully!")
        post_id = new_post.get("data", {}).get("id")
        
        # Example 3: Add a comment to the post
        if post_id:
            print("\n" + "="*50)
            print("Adding a comment...")
            
            comment = padlet.create_comment(
                post_id=post_id,
                content="좋은 장소네요! 참석하겠습니다."
            )
            
            if "error" in comment:
                print(f"Error creating comment: {comment['error']}")
            else:
                print("Comment added successfully!")
    
    # Example 4: Get current user info
    print("\n" + "="*50)
    print("Getting current user info...")
    user_info = padlet.get_current_user()
    
    if "error" in user_info:
        print(f"Error: {user_info['error']}")
    else:
        print("User info retrieved!")
        print(json.dumps(user_info, indent=2))

if __name__ == "__main__":
    main()