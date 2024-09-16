# Caching Proxy Server CLI app
This is a CLI tool that starts a caching proxy server, that will forward requests to the actual server and cache the responses. If the same request is made again, it will return the cached response instead of forwarding the request to the server.

## Architecture
The app is made up of the following components:

- **CLI**: Represents the user interface where commands such as starting the server and clearing the cache are issued.
- **Proxy Server (HTTPServer)**: The server that handles incoming requests and forwards them to the origin server if the cache is missed.
- **CacheManager**: Manages the in-memory cache, checking for cached responses and storing responses for future requests.
- **Origin Server**: The actual server that receives the request when it's not available in the cache.

Flow of information:

- User input in the CLI sends requests to the Proxy Server.
- Proxy Server checks the CacheManager for cached responses.
- If a response is cached, it is returned to the user (X-Cache: HIT).
- If the response is not cached, the Proxy Server forwards the request to the Origin Server (X-Cache: MISS).
- The response from the Origin Server is cached by the CacheManager and returned to the user.

View full architecture diagram [here](https://app.eraser.io/workspace/BqxLDyT4Ua2c2rxuYazq?elements=TJfCVrKTpIU9w2tlnZ3gug)
