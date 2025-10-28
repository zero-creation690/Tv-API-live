import requests
import json

def handler(request, response):
    # --- Enable CORS ---
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    # --- Handle preflight request ---
    if request.method == "OPTIONS":
        return response.status(200).send("")

    search = request.query.get("search")
    if not search:
        return response.status(400).json({"error": "Missing search parameter"})

    try:
        # Call your original API
        url = f"https://tv-chi-eosin.vercel.app/tv?search={search}"
        r = requests.get(url, timeout=10)
        data = r.json()
        return response.status(200).json(data)
    except Exception as e:
        return response.status(500).json({"error": str(e)})
