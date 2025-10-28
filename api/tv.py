from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/tv', methods=['GET'])
def get_tv():
    search = request.args.get('search', '')
    if not search:
        return jsonify({"error": "Missing search parameter"}), 400

    # Original API URL
    original_api = f"https://tv-chi-eosin.vercel.app/tv?search={search}"
    try:
        response = requests.get(original_api)
        data = response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(data)

# For Vercel deployment
def handler(request, context):
    return app(request.environ, context)
