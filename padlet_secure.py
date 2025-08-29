import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PadletAPI:
    def __init__(self, api_key=None):
        # Get API key from environment variable if not provided
        self.api_key = api_key or os.getenv('PADLET_API_KEY')
        if not self.api_key:
            raise ValueError("Padlet API key not found. Set PADLET_API_KEY environment variable.")
        
        self.base_url = "https://api.padlet.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_padlet(self, title, description="", wall_type="wall", privacy="secret"):
        """
        Create a new Padlet board with enhanced options
        
        Args:
            title (str): Title of the Padlet
            description (str): Description of the Padlet
            wall_type (str): Type of wall (wall, stream, grid, shelf, timeline, map, canvas)
            privacy (str): Privacy setting (public, password, secret, private)
        
        Returns:
            dict: Response from Padlet API
        """
        endpoint = f"{self.base_url}/padlets"
        
        data = {
            "title": title,
            "description": description,
            "wall_type": wall_type,
            "privacy": privacy,
            "comments": True,
            "reactions": True,
            "attribution": True
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"error": f"HTTP Error: {e}", "status_code": e.response.status_code}
        except requests.exceptions.RequestException as e:
            return {"error": f"Request Error: {e}"}
    
    def create_multiple_padlets(self, padlet_configs):
        """
        Create multiple Padlets at once
        
        Args:
            padlet_configs (list): List of dictionaries with Padlet configurations
        
        Returns:
            list: List of created Padlets
        """
        created_padlets = []
        
        for config in padlet_configs:
            result = self.create_padlet(**config)
            created_padlets.append({
                "config": config,
                "result": result
            })
        
        return created_padlets
    
    def delete_padlet(self, padlet_id):
        """Delete a Padlet by ID"""
        endpoint = f"{self.base_url}/padlets/{padlet_id}"
        
        try:
            response = requests.delete(endpoint, headers=self.headers)
            response.raise_for_status()
            return {"success": True, "message": "Padlet deleted successfully"}
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def update_padlet(self, padlet_id, **kwargs):
        """Update an existing Padlet"""
        endpoint = f"{self.base_url}/padlets/{padlet_id}"
        
        try:
            response = requests.patch(endpoint, headers=self.headers, json=kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

def main():
    # Initialize API (will read from environment variable)
    try:
        padlet = PadletAPI()
    except ValueError as e:
        print(f"Error: {e}")
        print("\nTo use this script:")
        print("1. Create a .env file in the same directory")
        print("2. Add your API key: PADLET_API_KEY=your_api_key_here")
        return
    
    # Example: Create multiple Padlets with different configurations
    padlet_configs = [
        {
            "title": "Project Ideas Board",
            "description": "Share and discuss project ideas",
            "wall_type": "wall",
            "privacy": "secret"
        },
        {
            "title": "Team Timeline",
            "description": "Track our project milestones",
            "wall_type": "timeline",
            "privacy": "secret"
        },
        {
            "title": "Resource Library",
            "description": "Useful resources and links",
            "wall_type": "shelf",
            "privacy": "secret"
        }
    ]
    
    print("Creating multiple Padlets...")
    results = padlet.create_multiple_padlets(padlet_configs)
    
    for result in results:
        config = result['config']
        response = result['result']
        
        print(f"\n{'='*50}")
        print(f"Padlet: {config['title']}")
        
        if "error" in response:
            print(f"❌ Error: {response['error']}")
        else:
            print(f"✅ Successfully created!")
            print(f"   ID: {response.get('id', 'N/A')}")
            print(f"   URL: {response.get('url', 'N/A')}")
            print(f"   Type: {config['wall_type']}")

if __name__ == "__main__":
    main()