"""
Flask API Server - SSE Enabled
"""

import os
import json
import time
from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from dotenv import load_dotenv
from instagram_scraper import InstagramScraper

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
PORT = int(os.getenv('PORT', 5000))
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', '')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', '')
PROXY_URL = os.getenv('PROXY_URL', None)
HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'mode': 'SSE'})

@app.route('/api/stream', methods=['GET'])
def stream_search():
    """
    SSE Endpoint for Real-Time Search
    Query Params: tags, gender, country, min_followers, max_followers, max_profiles
    """
    def generate():
        scraper = None
        try:
            # Parse Query Params
            tags = request.args.get('tags', '').split(',')
            tags = [t.strip() for t in tags if t.strip()]
            
            filters = {
                'gender': request.args.get('gender', 'both'),
                'country': request.args.get('country', ''),
                'min_followers': request.args.get('min_followers', 0),
                'max_followers': request.args.get('max_followers', 1000000000)
            }
            max_profiles = int(request.args.get('max_profiles', 20))
            
            if not tags:
                yield f"data: {json.dumps({'type': 'error', 'data': 'No tags provided'})}\n\n"
                return

            # Initialize Scraper
            yield f"data: {json.dumps({'type': 'log', 'data': 'Initializing browser...'})}\n\n"
            
            scraper = InstagramScraper(
                username=INSTAGRAM_USERNAME,
                password=INSTAGRAM_PASSWORD,
                proxy=PROXY_URL,
                headless=HEADLESS
            )
            
            if not scraper.start_browser():
                yield f"data: {json.dumps({'type': 'error', 'data': 'Failed to start browser'})}\n\n"
                return
                
            if not scraper.login():
                yield f"data: {json.dumps({'type': 'error', 'data': 'Login failed'})}\n\n"
                return
            
            # Run Search
            for event in scraper.search_tags(tags, filters, max_profiles):
                yield f"data: {json.dumps(event)}\n\n"
                
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'data': str(e)})}\n\n"
        finally:
            if scraper:
                scraper.close()
                
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    print(f'Server running on http://localhost:{PORT}')
    app.run(host='0.0.0.0', port=PORT, threaded=True)
