from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, quote
import urllib.request
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse query parameters
            query = self.path.split('?', 1)[1] if '?' in self.path else ''
            params = parse_qs(query)
            search = params.get('search', [''])[0]
            
            if not search:
                self._send_response(400, {
                    "error": "Missing 'search' parameter",
                    "usage": "?search=YourChannel"
                })
                return
            
            # Fetch from original API
            url = f"https://tv-chi-eosin.vercel.app/tv?search={quote(search)}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            self._send_response(200, data)
            
        except urllib.error.HTTPError as e:
            self._send_response(e.code, {"error": f"API error: {e.code}"})
        except Exception as e:
            self._send_response(500, {"error": str(e)})
    
    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def _send_response(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self._set_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
