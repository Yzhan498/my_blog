# comment_service.py

from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Mock in-memory data store
comments = {
    1: {
        "id": 1,
        "text": "Amazing comment!",
        "user_id": 1,
        "post_id": 2
    },
    2: {
        "id": 2,
        "text": "I did not know that!",
        "user_id": 2,
        "post_id": 2
    },
}

# Endpoint to retrieve comment information
@app.route('/comment/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    if comment_id not in comments:
        return jsonify({"message": "Comment not found"}), 404
    
    comment = comments[comment_id]
    
    # Fetch user details from user_service
    user_id = comment["user_id"]
    user_response = requests.get(f'http://userservicey.azurewebsites.net/users/{user_id}')
    if user_response.status_code != 200:
        return jsonify({"message": "User not found"}), 404
    user_details = user_response.json()
    
    # Fetch post details from post_service
    post_id = comment["post_id"]
    post_response = requests.get(f'http://postservicey.azurewebsites.net/post/{post_id}')
    if post_response.status_code != 200:
        return jsonify({"message": "Post not found"}), 404
    post_details = post_response.json()
    
    # Combine comment, user, and post details into a JSON response
    comment_info = {
        "comment": comment,
        "user": user_details,
        "post": post_details
    }
    
    return jsonify(comment_info), 200

if __name__ == '__main__':
    app.run(debug=True)  # Replace with your production settings


