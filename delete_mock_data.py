#!/usr/bin/env python3
"""
Padlet Post Cleanup Script

This script connects to the Padlet API to identify posts that need to be removed:
1. Posts located in Antarctica (latitude -75 to -90)
2. Posts containing "리나 갤러리" or "Lina Gallery" in subject/body

Board ID: blwpq840o1u57awd (CSS map board)
Board URL: https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd
"""

import requests
import json
import os
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PadletCleanup:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Padlet API client with API key"""
        self.api_key = api_key or os.getenv('PADLET_API_KEY')
        
        # Use provided API key if no environment variable
        if not self.api_key:
            self.api_key = "pdltp_d271492999e5db6c2cb47a28ea8598a13d343d0a7d32880eeb87d4ea89074944205d6c"
        
        if not self.api_key:
            raise ValueError("Padlet API key not found. Set PADLET_API_KEY in environment variable or .env file.")
        
        self.base_url = "https://api.padlet.dev/v1"
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/vnd.api+json"
        }
        
        # Target criteria
        self.target_board_id = "blwpq840o1u57awd"  # CSS map board
        self.antarctica_lat_range = (-90, -75)  # Antarctica latitude range
        self.target_text_patterns = [
            "리나 갤러리",  # Korean
            "Lina Gallery", # English
            "lina gallery", # Case insensitive
            "리나갤러리"    # Without space
        ]
    
    def get_board_with_posts(self, board_id: str) -> Dict[str, Any]:
        """Get board information with all posts included"""
        endpoint = f"{self.base_url}/boards/{board_id}"
        params = {"include": "posts"}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "status_code": getattr(e.response, 'status_code', None)}
    
    def check_api_capabilities(self) -> Dict[str, Any]:
        """Check what API endpoints are available, particularly DELETE operations"""
        print("Checking Padlet API capabilities...")
        
        # Test if DELETE endpoint exists for posts (this will likely fail)
        test_post_id = "test"
        delete_endpoint = f"{self.base_url}/posts/{test_post_id}"
        
        try:
            # We'll use a HEAD request to check if the endpoint exists without actually deleting
            response = requests.head(delete_endpoint, headers=self.headers)
            delete_available = response.status_code != 404
        except:
            delete_available = False
        
        return {
            "delete_posts_available": delete_available,
            "base_url": self.base_url,
            "api_key_configured": bool(self.api_key),
            "note": "Public Padlet API typically doesn't support DELETE operations for posts"
        }
    
    def is_in_antarctica(self, latitude: float) -> bool:
        """Check if latitude is in Antarctica range"""
        return self.antarctica_lat_range[0] <= latitude <= self.antarctica_lat_range[1]
    
    def contains_target_text(self, text: str) -> bool:
        """Check if text contains any target patterns (case insensitive)"""
        if not text:
            return False
        
        text_lower = text.lower()
        for pattern in self.target_text_patterns:
            if pattern.lower() in text_lower:
                return True
        return False
    
    def analyze_post(self, post_data: Dict[str, Any], included_posts: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Analyze a single post to see if it matches removal criteria"""
        post_id = post_data.get("id")
        
        # Find the full post data in included section
        full_post = None
        for included_post in included_posts:
            if included_post.get("id") == post_id and included_post.get("type") == "post":
                full_post = included_post
                break
        
        if not full_post:
            return None
        
        attributes = full_post.get("attributes", {})
        content = attributes.get("content", {})
        map_props = attributes.get("mapProps", {})
        
        # Extract post information
        subject = content.get("subject", "")
        body = content.get("body", "")
        latitude = map_props.get("latitude")
        longitude = map_props.get("longitude")
        location_name = map_props.get("locationName", "")
        
        # Check removal criteria
        reasons = []
        
        # Check Antarctica location
        if latitude is not None and self.is_in_antarctica(latitude):
            reasons.append(f"Located in Antarctica (lat: {latitude})")
        
        # Check text content
        text_fields = [subject, body, location_name]
        for field_name, field_value in zip(["subject", "body", "location"], text_fields):
            if self.contains_target_text(field_value):
                reasons.append(f"Contains target text in {field_name}: '{field_value}'")
        
        if reasons:
            return {
                "id": post_id,
                "subject": subject,
                "body": body,
                "latitude": latitude,
                "longitude": longitude,
                "location_name": location_name,
                "created_at": attributes.get("createdAt"),
                "updated_at": attributes.get("updatedAt"),
                "reasons": reasons,
                "full_content": content
            }
        
        return None
    
    def find_posts_to_remove(self) -> Dict[str, Any]:
        """Find all posts that match removal criteria"""
        print(f"Analyzing board {self.target_board_id}...")
        
        # Get board data with posts
        board_data = self.get_board_with_posts(self.target_board_id)
        
        if "error" in board_data:
            return {
                "error": board_data["error"],
                "status_code": board_data.get("status_code")
            }
        
        # Extract board info
        board_info = board_data.get("data", {}).get("attributes", {})
        posts_refs = board_data.get("data", {}).get("relationships", {}).get("posts", {}).get("data", [])
        included_data = board_data.get("included", [])
        
        print(f"Board: {board_info.get('title', 'Unknown')}")
        print(f"Total posts: {len(posts_refs)}")
        
        # Analyze each post
        posts_to_remove = []
        all_posts_summary = []
        
        for post_ref in posts_refs:
            analysis = self.analyze_post(post_ref, included_data)
            
            if analysis:
                posts_to_remove.append(analysis)
            
            # Also collect summary for all posts
            full_post = None
            for included_post in included_data:
                if (included_post.get("id") == post_ref.get("id") and 
                    included_post.get("type") == "post"):
                    full_post = included_post
                    break
            
            if full_post:
                attrs = full_post.get("attributes", {})
                content = attrs.get("content", {})
                map_props = attrs.get("mapProps", {})
                
                all_posts_summary.append({
                    "id": post_ref.get("id"),
                    "subject": content.get("subject", "")[:50] + "..." if len(content.get("subject", "")) > 50 else content.get("subject", ""),
                    "latitude": map_props.get("latitude"),
                    "longitude": map_props.get("longitude"),
                    "created_at": attrs.get("createdAt")
                })
        
        return {
            "board_info": {
                "id": self.target_board_id,
                "title": board_info.get("title"),
                "description": board_info.get("description"),
                "total_posts": len(posts_refs)
            },
            "posts_to_remove": posts_to_remove,
            "all_posts_summary": all_posts_summary,
            "removal_criteria": {
                "antarctica_range": self.antarctica_lat_range,
                "text_patterns": self.target_text_patterns
            }
        }
    
    def attempt_delete_post(self, post_id: str) -> Dict[str, Any]:
        """Attempt to delete a post (likely to fail as public API doesn't support this)"""
        endpoint = f"{self.base_url}/posts/{post_id}"
        
        try:
            response = requests.delete(endpoint, headers=self.headers)
            if response.status_code == 204:
                return {"success": True, "message": "Post deleted successfully"}
            elif response.status_code == 404:
                return {"success": False, "message": "DELETE endpoint not found (expected)"}
            else:
                return {"success": False, "message": f"Unexpected response: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": str(e)}


def run_demonstration_mode():
    """Demonstration mode showing what the script would find and API limitations"""
    print("This demonstrates what the script would find when connected to the Padlet API.")
    print("API Research Summary:")
    print("- Padlet API Documentation: https://docs.padlet.dev/reference/introduction")
    print("- Available endpoints: GET (board info, posts) and POST (create posts/comments)")
    print("- NO DELETE endpoints available in public API")
    print("- API requires paid Padlet subscription")
    print("- Base URL: https://api.padlet.dev")
    
    print("\nTarget Board: blwpq840o1u57awd (CSS map board)")
    print("URL: https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd")
    
    print("\nSearch Criteria:")
    print("1. Geographic: Posts with latitude between -90 and -75 (Antarctica)")
    print("2. Text content: Posts containing any of these terms:")
    print("   - '리나 갤러리' (Korean)")
    print("   - 'Lina Gallery' (English)")
    print("   - 'lina gallery' (case insensitive)")
    print("   - '리나갤러리' (Korean without space)")
    
    # Mock example of what might be found
    print("\nExample of posts that would be flagged for removal:")
    print("-" * 50)
    
    mock_posts = [
        {
            "id": "mock_001",
            "subject": "리나 갤러리 작품 전시",
            "body": "갤러리에서 전시 중인 작품들입니다.",
            "latitude": None,
            "longitude": None,
            "reasons": ["Contains target text in subject: '리나 갤러리 작품 전시'"]
        },
        {
            "id": "mock_002", 
            "subject": "Antarctic Research Station",
            "body": "Research facility in Antarctica",
            "latitude": -82.5,
            "longitude": 45.2,
            "reasons": ["Located in Antarctica (lat: -82.5)"]
        },
        {
            "id": "mock_003",
            "subject": "Visit to Lina Gallery",
            "body": "Great art exhibition at the gallery downtown",
            "latitude": 37.5665,
            "longitude": 126.9780,
            "reasons": ["Contains target text in subject: 'Visit to Lina Gallery'"]
        }
    ]
    
    for i, post in enumerate(mock_posts, 1):
        print(f"{i}. Post ID: {post['id']}")
        print(f"   Subject: {post['subject']}")
        print(f"   Body: {post['body']}")
        if post['latitude']:
            print(f"   Location: {post['latitude']}, {post['longitude']}")
        print(f"   Reasons for flagging:")
        for reason in post['reasons']:
            print(f"     - {reason}")
        print()
    
    print("=" * 60)
    print("MANUAL DELETION INSTRUCTIONS")
    print("=" * 60)
    print("Since the Padlet API does not provide DELETE endpoints, manual deletion is required:")
    print("\n1. Go to the board: https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd")
    print("2. For each flagged post:")
    print("   - Click on the post to open it")
    print("   - Click the three-dot menu (...) in the top right of the post")
    print("   - Select 'Delete' from the dropdown menu")
    print("   - Confirm deletion")
    print("\n3. Alternative bulk deletion (if you are the board owner):")
    print("   - Click the three-dot menu (...) in the board header")
    print("   - Select 'Clear posts' to remove all posts at once")
    print("   - Note: This removes ALL posts, not just the flagged ones")
    
    print("\n4. With API key, this script would:")
    print("   - Connect to board 'blwpq840o1u57awd'")
    print("   - Retrieve all posts with their content and location data")
    print("   - Analyze each post against the removal criteria")
    print("   - Generate a detailed list of posts to remove")
    print("   - Provide the exact post IDs for manual deletion")
    
    print("\nTo run with real data:")
    print("1. Obtain a Padlet API key (requires paid subscription)")
    print("2. Set PADLET_API_KEY environment variable")
    print("3. Run this script again")


def main():
    """Main function to run the cleanup analysis"""
    print("Starting Padlet Mock Data Cleanup Analysis")
    print("=" * 60)
    
    try:
        # Initialize cleanup tool
        cleanup = PadletCleanup()
        
        # Check API capabilities first
        print("\n1. API Capabilities Check:")
        api_capabilities = cleanup.check_api_capabilities()
        
        for key, value in api_capabilities.items():
            print(f"   {key}: {value}")
        
        # Find posts to remove
        print("\n2. Analyzing Posts:")
        results = cleanup.find_posts_to_remove()
        
        if "error" in results:
            print(f"Error: {results['error']}")
            if results.get("status_code") == 401:
                print("   Make sure PADLET_API_KEY is set correctly")
            elif results.get("status_code") == 403:
                print("   Make sure you have access to this board")
            return
        
        # Display results
        board_info = results["board_info"]
        posts_to_remove = results["posts_to_remove"]
        all_posts = results["all_posts_summary"]
        
        print(f"\nBoard Information:")
        print(f"   Title: {board_info['title']}")
        print(f"   ID: {board_info['id']}")
        print(f"   Total Posts: {board_info['total_posts']}")
        
        print(f"\nPosts Found for Removal: {len(posts_to_remove)}")
        
        if posts_to_remove:
            print("\n" + "=" * 60)
            print("POSTS TO REMOVE:")
            print("=" * 60)
            
            for i, post in enumerate(posts_to_remove, 1):
                print(f"\n{i}. Post ID: {post['id']}")
                print(f"   Subject: {post['subject']}")
                print(f"   Body: {post['body'][:100]}..." if len(post['body']) > 100 else f"   Body: {post['body']}")
                if post['latitude'] is not None:
                    print(f"   Location: {post['latitude']}, {post['longitude']} ({post['location_name']})")
                print(f"   Created: {post['created_at']}")
                print(f"   Reasons for removal:")
                for reason in post['reasons']:
                    print(f"     - {reason}")
            
            # Test delete capability (will likely fail)
            print(f"\n3. Testing Delete Capability:")
            first_post_id = posts_to_remove[0]['id']
            delete_result = cleanup.attempt_delete_post(first_post_id)
            print(f"   Attempted to delete post {first_post_id}: {delete_result['message']}")
            
        else:
            print("No posts found matching removal criteria!")
        
        # Show summary of all posts for reference
        print(f"\nAll Posts Summary:")
        print("-" * 60)
        for i, post in enumerate(all_posts[:10], 1):  # Show first 10
            location_str = f"({post['latitude']}, {post['longitude']})" if post['latitude'] else "No location"
            print(f"{i}. {post['id']}: {post['subject']} {location_str}")
        
        if len(all_posts) > 10:
            print(f"   ... and {len(all_posts) - 10} more posts")
        
        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        
        if posts_to_remove:
            print("1. The Padlet public API does not provide DELETE endpoints for posts")
            print("2. Manual deletion is required through the Padlet web interface:")
            print("   - Go to: https://padlet.com/CSS2025/css_-1_map-blwpq840o1u57awd")
            print("   - Click on each post identified above")
            print("   - Use the delete option in the post menu")
            print("\n3. Post IDs to delete manually:")
            for post in posts_to_remove:
                print(f"   - {post['id']} ({post['subject']})")
        else:
            print("No action needed - no mock posts found!")
    
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nTo fix this:")
        print("1. Create a .env file in the project directory")
        print("2. Add: PADLET_API_KEY=your_actual_api_key")
        print("3. Or set the PADLET_API_KEY environment variable")
        
        # Run demonstration mode
        print("\n" + "=" * 60)
        print("RUNNING DEMONSTRATION MODE")
        print("=" * 60)
        run_demonstration_mode()
    
    except Exception as e:
        print(f"Unexpected Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()