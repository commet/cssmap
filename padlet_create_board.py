import requests
import json

class PadletAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.padlet.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_padlet(self, title, description="", wall_type="wall"):
        """
        Create a new Padlet board
        
        Args:
            title (str): Title of the Padlet
            description (str): Description of the Padlet
            wall_type (str): Type of wall (wall, stream, grid, shelf, timeline, map, canvas)
        
        Returns:
            dict: Response from Padlet API
        """
        endpoint = f"{self.base_url}/padlets"
        
        data = {
            "title": title,
            "description": description,
            "wall_type": wall_type,
            "privacy": "secret",  # Can be: public, password, secret, private
            "comments": True,
            "reactions": True
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def get_my_padlets(self):
        """Get list of your Padlets"""
        endpoint = f"{self.base_url}/padlets"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def add_post_to_padlet(self, padlet_id, subject, body=""):
        """
        Add a post to an existing Padlet
        
        Args:
            padlet_id (str): ID of the Padlet
            subject (str): Title/subject of the post
            body (str): Content of the post
        
        Returns:
            dict: Response from Padlet API
        """
        endpoint = f"{self.base_url}/padlets/{padlet_id}/posts"
        
        data = {
            "subject": subject,
            "body": body
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

def main():
    # WARNING: Store API key securely in production (use environment variables)
    API_KEY = "pdltp_d271492999e5db6c2cb47a28ea8598a13d343d0a7d32880eeb87d4ea89074944205d6c"
    
    # Initialize Padlet API client
    padlet = PadletAPI(API_KEY)
    
    # Example 1: Create a new Padlet
    print("Creating a new Padlet...")
    new_padlet = padlet.create_padlet(
        title="My Test Padlet",
        description="This is a test padlet created via API",
        wall_type="wall"
    )
    
    if "error" in new_padlet:
        print(f"Error creating Padlet: {new_padlet['error']}")
    else:
        print(f"Successfully created Padlet!")
        print(f"Padlet ID: {new_padlet.get('id', 'N/A')}")
        print(f"Padlet URL: {new_padlet.get('url', 'N/A')}")
    
    # Example 2: Get list of your Padlets
    print("\n" + "="*50)
    print("Fetching your Padlets...")
    my_padlets = padlet.get_my_padlets()
    
    if "error" in my_padlets:
        print(f"Error fetching Padlets: {my_padlets['error']}")
    else:
        print(f"Found {len(my_padlets)} Padlet(s)")
        for p in my_padlets[:5]:  # Show first 5
            print(f"- {p.get('title', 'Untitled')} (ID: {p.get('id', 'N/A')})")
    
    # Example 3: Add a post to the newly created Padlet (if successful)
    if "error" not in new_padlet and new_padlet.get('id'):
        print("\n" + "="*50)
        print("Adding a post to the new Padlet...")
        new_post = padlet.add_post_to_padlet(
            padlet_id=new_padlet['id'],
            subject="Welcome Post",
            body="This is the first post on our new Padlet!"
        )
        
        if "error" in new_post:
            print(f"Error adding post: {new_post['error']}")
        else:
            print("Successfully added post to Padlet!")

if __name__ == "__main__":
    main()