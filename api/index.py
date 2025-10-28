# api/index.py

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests

# --- CONFIGURATION ---
TARGET_API_BASE_URL = "https://tv-chi-eosin.vercel.app"

# You can specify allowed origins here. 
# '*' means allow all. For production, list specific domains.
ALLOWED_ORIGINS = ["*"] 
# Example for specific domains:
# ALLOWED_ORIGINS = ["https://your-frontend-domain.com", "http://localhost:3000"]

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}})

@app.route('/api/proxy/tv', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/api/proxy/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy_request(path):
    """
    Proxies requests from /api/proxy/* to the TARGET_API_BASE_URL/*
    """
    # 1. Construct the target URL (preserving query parameters)
    target_url = f"{TARGET_API_BASE_URL}/{path}"
    if request.query_string:
        target_url += f"?{request.query_string.decode('utf-8')}"

    # 2. Forward the request to the target API
    try:
        # Prepare headers to send (exclude hop-by-hop headers)
        headers = {k: v for k, v in request.headers.items() if k.lower() not in ('host', 'connection', 'content-length', 'transfer-encoding')}

        # Make the request to the original API
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data() if request.method in ['POST', 'PUT', 'PATCH'] else None,
            # Adjust timeout as necessary
            timeout=10 
        )

        # 3. Create the response for the client
        # Flask-CORS has already handled the necessary CORS headers automatically
        
        # Copy original headers (but ignore 'Content-Encoding' if not needed, as Vercel handles compression)
        response_headers = [(name, value) for name, value in response.headers.items() 
                            if name.lower() not in ('content-encoding', 'content-length', 'transfer-encoding', 'connection')]

        # Return the response directly
        return Response(response.content, status=response.status_code, headers=response_headers)

    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        return jsonify({"error": f"Proxy request failed: {str(e)}", "status_code": 500}), 500

# Vercel needs a handler function in vercel.json, which uses the app object
# No need to run app.run() here as Vercel's serverless environment handles it.
