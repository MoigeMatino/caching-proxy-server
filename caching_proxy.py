import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urljoin

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        origin_url = self.headers['Origin-Url']
        full_url = urljoin(origin_url, self.path)

        # TODO: Check if response is cached
        cached_response = cache.get(full_url)
        if cached_response:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('X-Cache', 'HIT')  # Response from cache
            self.end_headers()
            self.wfile.write(cached_response.encode())
        else:
            # Forward the request to the origin server
            response = requests.get(full_url)
            # TODO: save response from origin server to cache
            # cache.set(full_url, response.text)  
            
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.send_header('X-Cache', 'MISS')  
            self.end_headers()
            self.wfile.write(response.content)
            
def start_server(port, origin):
    class CustomHandler(ProxyHandler):
        def __init__(self, *args, **kwargs):
            self.origin_url = origin
            super().__init__(*args, **kwargs)
    
    server = HTTPServer(('localhost', port), CustomHandler)
    print(f'Starting proxy on port {port}, forwarding to {origin}')
    server.serve_forever()

def clear_cache():
    #TODO: call clear_cache func
    print("Cache cleared!")