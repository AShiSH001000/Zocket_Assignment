from flask import Flask, jsonify
import recommendation

app = Flask(__name__)

# Root route
@app.route('/')
def home():
    return "Welcome to the Video Recommendation System! Use the /feed endpoint for recommendations."

# Favicon handler
@app.route('/favicon.ico')
def favicon():
    return "", 204

# Load data once when the app starts
viewed_posts, liked_posts, inspired_posts, rated_posts, users = recommendation.load_data()

@app.route('/feed', methods=['GET'])
def feed():
    """
    Endpoint to get the top recommended posts.
    """
    recommended_posts = recommendation.get_top_posts(viewed_posts, liked_posts, inspired_posts, rated_posts)
    return jsonify({"recommended_posts": recommended_posts})

@app.route('/recommend/user/<int:user_id>', methods=['GET'])
def recommend_for_user(user_id):
    """
    Recommend posts for a specific user.
    """
    recommended_posts = recommendation.recommend_posts(user_id, viewed_posts, liked_posts, inspired_posts, rated_posts)
    return jsonify({"user_id": user_id, "recommended_posts": recommended_posts})

@app.route('/user/posts/<int:user_id>', methods=['GET'])
def get_user_posts(user_id):
    """
    Get posts related to a specific user.
    """
    user_posts = recommendation.get_user_posts(user_id, viewed_posts, liked_posts, inspired_posts, rated_posts)
    return jsonify({"user_id": user_id, "posts": user_posts})

@app.route('/recommend/post/<int:post_id>', methods=['GET'])
def recommend_for_post(post_id):
    """
    Recommend posts similar to a specific post.
    """
    similar_posts = recommendation.recommend_for_post(post_id, viewed_posts, liked_posts, inspired_posts, rated_posts)
    return jsonify({"post_id": post_id, "recommended_posts": list(similar_posts)})

if __name__ == '__main__':
    app.run(debug=True)
