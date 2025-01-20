import json
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load .env file from the correct directory
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# print("JSONBIN_API_KEY:", os.getenv("JSONBIN_API_KEY"))
# print("JSONBIN_COLLECTION_ID:", os.getenv("JSONBIN_COLLECTION_ID"))

def upload_to_jsonbin(file_name="dogs.json"):
    """Upload data from a file to JSONBin."""
    api_url = "https://api.jsonbin.io/v3/b"
    custom_name = f"dog_{datetime.now().strftime('%Y%m%d')}"

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": os.getenv("JSONBIN_API_KEY"),
        "X-Collection-Id": os.getenv("JSONBIN_COLLECTION_ID"),
        "X-Bin-Name": custom_name,
    }
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()

        print("✅ Data uploaded to JSONBin.")
        print(response.json())
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error reading the file: {e}")
    except requests.RequestException as e:
        print(f"❌ Error uploading data: {e}")
