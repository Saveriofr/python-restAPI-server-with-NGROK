#!/usr/bin/env python3
"""An example HTTP server with GET and POST endpoints.
Using pyngrok to open a direct link from outside"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time
from pyngrok import ngrok

# start ngrok
url = ngrok.connect(8001).public_url
print(url)

# Sample blog post data similar to
# https://ordina-jworks.github.io/frontend/2019/03/04/vue-with-typescript.html#4-how-to-write-your-first-component
_g_posts = []

class _RequestHandler(BaseHTTPRequestHandler):
    # Borrowing from https://gist.github.com/nitaku/10d0662536f37a087e1b
    def _set_headers(self):
        self.send_response(HTTPStatus.OK.value)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps(_g_posts).encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        message['date_ms'] = int(time.time()) * 1000
        _g_posts.append(message)
        self._set_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        print(message)
        with open("webhook.json", "w") as file:
            file.write(str(message))

    def do_OPTIONS(self):
        # Send allow-origin header for preflight POST XHRs.
        self.send_response(HTTPStatus.NO_CONTENT.value)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()


def run_server():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
