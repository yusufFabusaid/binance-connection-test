
import json
import os
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer

BINANCE_URL = "https://fapi.binance.com/fapi/v1/exchangeInfo"


class Handler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):

        if self.path == "/":
            self.send_json(200, {
                "service": "Binance Connection Test",
                "status": "running",
                "test_url": "/test"
            })
            return

        if self.path != "/test":
            self.send_json(404, {"error": "Not found"})
            return

        request = urllib.request.Request(
            BINANCE_URL,
            headers={"User-Agent": "Binance-Connectivity-Test/1.0"}
        )

        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                data = json.loads(response.read().decode("utf-8"))

                self.send_json(200, {
                    "reachable": True,
                    "http_status": response.status,
                    "endpoint": BINANCE_URL,
                    "symbols_count": len(data.get("symbols", [])),
                    "message": "Binance API connection successful"
                })

        except urllib.error.HTTPError as error:
            self.send_json(200, {
                "reachable": False,
                "http_status": error.code,
                "endpoint": BINANCE_URL,
                "error": error.read(500).decode(
                    "utf-8", errors="replace"
                )
            })

        except Exception as error:
            self.send_json(200, {
                "reachable": False,
                "error_type": type(error).__name__,
                "error": str(error)
            })


port = int(os.environ.get("PORT", 10000))

server = HTTPServer(("0.0.0.0", port), Handler)

print(f"Server running on port {port}", flush=True)

server.serve_forever()
