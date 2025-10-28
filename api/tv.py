import requests

def handler(request, response):
    # Get 'search' query parameter
    search = request.args.get("search", "")
    if not search:
        response.status_code = 400
        return response.json({"error": "Missing 'search' query parameter"})

    # Your base API URL
    base_url = "https://tv-chi-eosin.vercel.app/tv"

    try:
        # Fetch data from the original API
        r = requests.get(base_url, params={"search": search})
        r.raise_for_status()
        data = r.json()

        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"

        return response.json(data)

    except Exception as e:
        response.status_code = 500
        return response.json({"error": str(e)})


# Required export for Vercel Python runtime
handler.is_async = False
