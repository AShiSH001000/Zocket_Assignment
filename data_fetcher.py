import requests
import pandas as pd

API_HEADERS = {
    "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
}

# Fetch data using APIs
def fetch_data(api_url, output_file):
    page = 1
    all_data = []
    while True:
        response = requests.get(f"{api_url}&page={page}&page_size=1000", headers=API_HEADERS)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        all_data.extend(data)
        page += 1
    
    # Save to CSV
    df = pd.DataFrame(all_data)
    df.to_csv(output_file, index=False)
    print(f"Saved data to {output_file}")

# Fetch all data
if __name__ == "__main__":
    fetch_data("https://api.socialverseapp.com/posts/view", "data/viewed_posts.csv")
    fetch_data("https://api.socialverseapp.com/posts/like", "data/liked_posts.csv")
    fetch_data("https://api.socialverseapp.com/posts/inspire", "data/inspired_posts.csv")
    fetch_data("https://api.socialverseapp.com/posts/rating", "data/rated_posts.csv")
    fetch_data("https://api.socialverseapp.com/posts/summary/get", "data/video_metadata.csv")
