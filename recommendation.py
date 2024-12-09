import pandas as pd

def load_data():
    """
    Load data from CSV files into data structures.
    """

    viewed_posts_df = pd.read_csv('data/viewed_posts.csv', encoding='utf-8')  
    liked_posts_df = pd.read_csv('data/liked_posts.csv', encoding='utf-8')    
    inspired_posts_df = pd.read_csv('data/inspired_posts.csv', encoding='utf-8') 
    rated_posts_df = pd.read_csv('data/rated_posts.csv', encoding='utf-8')   
    users_df = pd.read_csv('data/users.csv', encoding='ISO-8859-1')  

    viewed_posts = viewed_posts_df.to_dict(orient='records')
    liked_posts = liked_posts_df.to_dict(orient='records')
    inspired_posts = inspired_posts_df.to_dict(orient='records')
    rated_posts = rated_posts_df.to_dict(orient='records')
    users = users_df.to_dict(orient='records')
    
    return viewed_posts, liked_posts, inspired_posts, rated_posts, users

def get_top_posts(viewed_posts, liked_posts, inspired_posts, rated_posts):

    viewed_posts_df = pd.DataFrame(viewed_posts)
    

    post_view_counts = viewed_posts_df['post_id'].value_counts().reset_index()
    post_view_counts.columns = ['post_id', 'views']
    

    top_posts = post_view_counts.sort_values(by='views', ascending=False).head(5)
    return top_posts.to_dict(orient='records')

def recommend_posts(user_id, viewed_posts, liked_posts, inspired_posts, rated_posts):

    return get_top_posts(viewed_posts, liked_posts, inspired_posts, rated_posts)

def get_user_posts(user_id, viewed_posts, liked_posts, inspired_posts, rated_posts):
    """
    Get posts related to a specific user.
    """

    user_viewed = [post for post in viewed_posts if post['user_id'] == user_id]
    user_liked = [post for post in liked_posts if post['user_id'] == user_id]
    user_inspired = [post for post in inspired_posts if post['user_id'] == user_id]
    user_rated = [post for post in rated_posts if post['user_id'] == user_id]

    return {
        "viewed": user_viewed,
        "liked": user_liked,
        "inspired": user_inspired,
        "rated": user_rated
    }

def recommend_for_post(post_id, viewed_posts, liked_posts, inspired_posts, rated_posts):
    """
    Recommend posts similar to a given post. Currently, this is a placeholder.
    """

    post_viewers = {post['user_id'] for post in viewed_posts if post['post_id'] == post_id}
    similar_posts = {post['post_id'] for post in viewed_posts if post['user_id'] in post_viewers and post['post_id'] != post_id}
    return similar_posts
