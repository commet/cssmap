import os
from supabase import create_client, Client

# Load environment variables
url = "https://sjcxowsvxcytrfqvgokx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqY3hvd3N2eGN5dHJmcXZnb2t4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjQ5NTE5MDMsImV4cCI6MjA0MDUyNzkwM30.JL0sEO1L0AFLE1H-NdMXAJKPIIu-B0D7h2YgFtFrYZI"

try:
    # Create Supabase client
    supabase: Client = create_client(url, key)
    print("SUCCESS: Supabase client connected!")
    
    # Test storage bucket access
    try:
        buckets = supabase.storage.list_buckets()
        print(f"SUCCESS: Found {len(buckets)} buckets")
        for bucket in buckets:
            print(f"  - {bucket.name}")
    except Exception as e:
        print(f"ERROR: Bucket list failed: {e}")
    
    # Test specific bucket
    try:
        files = supabase.storage.from_("gallery-photos").list()
        print(f"SUCCESS: gallery-photos bucket accessible! Files: {len(files)}")
    except Exception as e:
        print(f"ERROR: gallery-photos bucket access failed: {e}")
        
except Exception as e:
    print(f"ERROR: Supabase connection failed: {e}")