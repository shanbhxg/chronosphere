import re
from collections import Counter
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_stopwords():
    try:
        with open('stopwords/stopwords.txt', 'r', encoding='utf-16-le') as f:
            return set(f.read().splitlines())
    except Exception as e:
        print(f"Error loading stopwords: {e}")
        return set()

def fetch_user_posts(handle):
    url = 'https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed'
    params = {
        'actor': handle,
        'filter': 'posts_and_author_threads'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('feed', [])
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

@app.route('/api/words', methods=['GET'])
def get_words():
    handle = request.args.get('handle')
    if not handle:
        return jsonify({"error": "No handle provided"}), 400

    posts = fetch_user_posts(handle)
    if not posts:
        return jsonify({"error": "No posts found for this handle"}), 404

    all_words = []
    stopwords = load_stopwords()

    for post in posts:
        text = post.get('post', {}).get('record', {}).get('text', '')
        if text:
            # Extract words, only alphabetic characters
            extracted_words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
            # Remove stopwords
            filtered_words = [word for word in extracted_words if word not in stopwords]
            all_words.extend(filtered_words)

    # Count word frequencies
    word_counts = Counter(all_words)

    # Get the top 5 most common words
    top_words = word_counts.most_common(5)

    return jsonify({
        "handle": handle,
        "top_words": top_words
    })

if __name__ == '__main__':
    app.run(debug=True)
