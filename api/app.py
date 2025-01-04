import re
from collections import Counter
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import parse_qs, urlparse

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

class handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if path == '/api/words':
            handle = query.get('handle', [None])[0]

            if not handle:
                self.send_error(400, "No handle provided")
                return

            posts = fetch_user_posts(handle)
            if not posts:
                self.send_error(404, "No posts found for this handle")
                return

            all_words = []
            stopwords = load_stopwords()

            for post in posts:
                text = post.get('post', {}).get('record', {}).get('text', '')
                if text:
                    extracted_words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
                    filtered_words = [word for word in extracted_words if word not in stopwords]
                    all_words.extend(filtered_words)

            word_counts = Counter(all_words)
            top_words = word_counts.most_common(5)

            response = {
                "handle": handle,
                "top_words": top_words
            }

            self.send_response(200)
            self._set_headers()
            self.wfile.write(json.dumps(response).encode())

        else:
            self.send_error(404, "Not Found")

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
