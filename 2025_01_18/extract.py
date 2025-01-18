import json
import requests
import os

def fetch_dog_data(file_name="dogs.json"):
    """Fetch random dog image data and save it to a file."""
    url = "https://dog.ceo/api/breeds/image/random"

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Save data to a file
        with open(file_path, "w") as f:
            json.dump(data, f)
        
        print("✅ Data fetched and saved to file.")
    except requests.RequestException as e:
        print(f"❌ Error fetching data: {e}")
