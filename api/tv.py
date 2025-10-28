import json
import requests

def handler(request, context):
    # Enable CORS
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }

    if request["method"] == "OPTIONS":
        return {"status": 200, "body": "", "headers": headers}

    search = request["query"].get("search", "")
    if not search:
        return {"status": 400, "body": json.dumps({"error": "Missing search parameter"}), "headers": headers}

    try:
        # Forward the request to the original API
        url = f"https://tv-chi-eosin.vercel.app/tv?search={search}"
        resp = requests.get(url, timeout=10)
        data = resp.json()
    except Exception as e:
        return {"status": 500, "body": json.dumps({"error": str(e)}), "headers": headers}

    return {"status": 200, "body": json.dumps(data), "headers": headers}
