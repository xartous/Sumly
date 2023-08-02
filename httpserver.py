import http.server
import socketserver
import requests
import urllib.parse
from urllib.parse import parse_qs

PORT = 3000


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def do_GET(self):
        # Parse request path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = parse_qs(parsed_path.query)

        # Host URL and headers for external API
        HOST_URL = "https://textanalysis-text-summarization.p.rapidapi.com"

        payload = {}

        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": "660828d321msheaa256ed4acca10p15dc08jsn93bbcaf61f64",
            "X-RapidAPI-Host": "textanalysis-text-summarization.p.rapidapi.com"
        }

        # Forward request to external API if path starts with "/players" or "/teams"
        if path.startswith('/url') or path.startswith('/text'):
            search = query.get("search", [""])[0]  # Get search term or default to empty string
            url = HOST_URL
            if path.startswith('/url'):
                    url = url + '/text-summarizer-url'
                    payload = {
                        "url": search,
                        "sentnum": "5"
                    }
            elif path.startswith('/text'):
                    url = url + '/text-summarizer-text'
                    payload = {
                        "text": search,
                        "sentnum": "5"
                    }
            response = requests.post(url, data=payload, headers=headers)
            self.send_response(response.status_code, url)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)
        else:  # Handle other requests normally
            super().do_GET()


with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
