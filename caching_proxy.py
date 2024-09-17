import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urljoin
from cache_manager import CacheManager

cache = CacheManager()

class ProxyHandler(BaseHTTPRequestHandler):
    def __init__(self, origin_url, *args, **kwargs):
        self.origin_url = origin_url  
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        print(f"Received request for: {self.path}")
        
        # To ensure the origin url ends with a slash for proper construction
        # of full url
        if not self.origin_url.endswith('/'):
            self.origin_url += '/'
            
        full_url = urljoin(self.origin_url, self.path)

        # Check if response is cached
        cached_response = cache.get(full_url)
        if cached_response:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('X-Cache', 'HIT')  # Response from cache
            self.end_headers()
            self.wfile.write(cached_response.encode())
            print(f"CACHE HIT for {full_url}")
            print(f"Response Headers: X-Cache: HIT")
            
        else:
            # Forward the request to the origin server
            response = requests.get(full_url)
            
            # save response from origin server to cache
            cache.set(full_url, response.text)  
            
            self.send_response(response.status_code)
            for key, value in response.headers.items():
                self.send_header(key, value)
            self.send_header('X-Cache', 'MISS')  
            self.end_headers()
            self.wfile.write(response.content)
            print(f"CACHE MISS for {full_url}, response cached.")
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Content: {response.text[:100]}...")  
            
def start_server(port, origin):
    class CustomHandler(ProxyHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(origin, *args, **kwargs)
    
    server = HTTPServer(('localhost', port), CustomHandler)
    print(f'Starting proxy on port {port}, forwarding to {origin}')
    server.serve_forever()

def clear_cache():
    cache.clear()
    print("Cache cleared!")