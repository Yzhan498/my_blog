# comment_service.py

from flask import Flask, jsonify
import requests
import sqlite3
conn = sqlite3.connect(':memory:')

app = Flask(__name__)

#define list comments
comments = [{'comment_id': 1, 'user_id': 1, 'comment': 'Amazing comment!'}, {'comment_id': 2, 'user_id': 2, 'comment': 'Amazing comment!'}]

@app.route('/comment/<int:id>')
def comment(id):
    filtered_comment = [comment for comment in comments if comment['comment_id'] == id]
    comment_info = None
    if len(filtered_comment) > 0: 
        comment_info =  filtered_comment[0]

# Get comment info from User Service and Post Service
    if comment_info:
        response = requests.get(f'http://userservicey.azurewebsites.net/user/{comment_info["user_id"]},postserviceying.azurewebsites.net/post/{comment_info["comment_id"]}')
        if response.status_code == 200:
            comment_info['comment_id']=response.json()

    return jsonify(comment_info)

if __name__ == '__main__':
    app.run(port=5002)




