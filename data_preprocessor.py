import pandas as pd

# File paths
DATA_DIR = "data/"
FILES = {
    "viewed": "viewed_posts.csv",
    "liked": "liked_posts.csv",
    "inspired": "inspired_posts.csv",
    "rated": "rated_posts.csv",
    "metadata": "video_metadata.csv",
}

def merge_data():
    # Load interaction files
    viewed = pd.read_csv(DATA_DIR + FILES["viewed"])
    liked = pd.read_csv(DATA_DIR + FILES["liked"])
    inspired = pd.read_csv(DATA_DIR + FILES["inspired"])
    rated = pd.read_csv(DATA_DIR + FILES["rated"])

    # Load metadata
    metadata = pd.read_csv(DATA_DIR + FILES["metadata"])

    # Combine interaction data
    interactions = pd.concat([viewed, liked, inspired, rated], ignore_index=True)

    # Merge interactions with metadata on 'video_id' or relevant key
    merged_data = pd.merge(interactions, metadata, on="video_id", how="left")

    # Save merged data
    merged_data.to_csv("posts_data.csv", index=False)
    print("Merged data saved to 'posts_data.csv'.")

if __name__ == "__main__":
    merge_data()
