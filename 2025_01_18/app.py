from extract import fetch_dog_data
from loading import upload_to_jsonbin

if __name__ == "__main__":
    print("📥 Fetching data from Dog API...")
    fetch_dog_data()  # Extract data

    print("\n📤 Uploading data to JSONBin...")
    upload_to_jsonbin()  # Load data
