class CacheManager():
    def __init__(self):
        self.cache = {}
    
        
    def get(self, url: str) -> str:
        return self.cache.get(url)
    
    def set(self, url: str, response: str) -> None:
        self.cache[url] = response
        
    def clear(self):
        self.cache.clear()