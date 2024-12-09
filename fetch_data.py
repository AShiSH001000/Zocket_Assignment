import requests
import pandas as pd
import os
import time

# Directory to save data
base_dir = "data"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Headers for API request
headers = {
    "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
}

# API URLs
apis = {
    "viewed_posts": "https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    "liked_posts": "https://api.socialverseapp.com/posts/like?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    "inspired_posts": "https://api.socialverseapp.com/posts/inspire?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    "rated_posts": "https://api.socialverseapp.com/posts/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if",
    "all_posts": "https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000",
    "users": "https://api.socialverseapp.com/users/get_all?page=1&page_size=1000",
}

# Function to fetch data and save it to CSV
def fetch_and_save(api_name, url):
    all_data = []
    page = 1

    while True:
        paginated_url = f"{url.split('?')[0]}?page={page}&page_size=1000"
        response = requests.get(paginated_url, headers=headers)

        # Debugging output
        print(f"Fetching {api_name} - Page {page}: Status Code {response.status_code}")
        if response.status_code != 200:
            print(f"Error {response.status_code}: {response.text}")
            break

        try:
            data = response.json()
            print(f"Data keys for {api_name}: {list(data.keys())}")
            # Extract the posts or users based on the API
            if api_name in ["viewed_posts", "liked_posts", "inspired_posts", "rated_posts"]:
                posts = data.get("posts", [])
            elif api_name == "all_posts":
                posts = data.get("posts", [])
            elif api_name == "users":
                posts = data.get("users", [])
            else:
                posts = []
            print(f"Number of posts fetched for {api_name}: {len(posts)}")
        except Exception as e:
            print(f"Error parsing JSON for {api_name}: {e}")
            break

        if not posts:
            print(f"No more data for {api_name}.")
            break

        # Extract specific fields from the data and append to all_data
        if api_name in ["viewed_posts", "liked_posts", "inspired_posts", "rated_posts"]:
            for post in posts:
                all_data.append({
                    "id": post.get("id"),
                    "post_id": post.get("post_id"),
                    "user_id": post.get("user_id"),
                    "viewed_at": post.get("viewed_at") if api_name == "viewed_posts" else None,
                    "liked_at": post.get("liked_at") if api_name == "liked_posts" else None,
                    "inspired_at": post.get("inspired_at") if api_name == "inspired_posts" else None,
                    "rated_at": post.get("rated_at") if api_name == "rated_posts" else None
                })
        elif api_name == "users":
            for user in posts:
                all_data.append({
                    "user_id": user.get("user_id"),
                    "username": user.get("username"),
                    "email": user.get("email")
                })

        page += 1
        time.sleep(1)  # Adding a delay to avoid overloading the server

    if all_data:
        # Save the data to CSV
        df = pd.DataFrame(all_data)
        csv_path = os.path.join(base_dir, f"{api_name}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Data for {api_name} saved to {csv_path}.")
    else:
        print(f"No data available for {api_name}.")

# Fetch data for each API and save
for api_name, api_url in apis.items():
    print(f"Fetching data for {api_name}...")
    fetch_and_save(api_name, api_url)
    print(f"Completed fetching data for {api_name}.\n")
