#!/usr/bin/env python3

import argparse
from caching_proxy import clear_cache, start_server

def parse_args():
    parser = argparse.ArgumentParser(description='Start the caching proxy server.')
    parser.add_argument('-p', '--port', type=int, required=True, help='Port on which the server runs')
    parser.add_argument('-o', '--origin', type=str, required=True, help='Origin server URL')
    parser.add_argument('-cc', '--clear-cache', action='store_true', help='Clear the cache')

    return parser

def main():
    parser = parse_args()
    args = parser.parse_args()

    
    print(f'Starting caching proxy server on port {args.port} with origin {args.origin}')
    if args.clear_cache:
        print('Clearing cache')
        clear_cache()
        print('cache cleared')
    else:
        print(f'Starting server on port {args.port} with origin {args.origin}')
        start_server(args.port, args.origin)
        print("Server started.")
        
if __name__ == '__main__':
    main()
