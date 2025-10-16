#!/usr/bin/env python3
"""
Fast threaded local web server for testing static websites
Auto-finds available port and shows local IP for mobile testing
Uses ThreadingHTTPServer for parallel request handling (much faster on mobile)
"""

import http.server
import socketserver
import socket
import sys

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def find_available_port(start_port=8000, max_port=9000):
    for port in range(start_port, max_port):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind(('', port))
            test_socket.close()
            return port
        except OSError:
            continue
    return None

class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

PORT = find_available_port()
if PORT is None:
    print("\nError: Could not find an available port between 8000-9000")
    print("Try: lsof -ti:8000 | xargs kill -9\n")
    sys.exit(1)

LOCAL_IP = get_local_ip()
Handler = http.server.SimpleHTTPRequestHandler

print(f"\nFast server running at:")
print(f"  Computer:  http://localhost:{PORT}/")
print(f"  Mobile:    http://{LOCAL_IP}:{PORT}/")
print(f"\nPress Ctrl+C to stop\n")

try:
    with ThreadedHTTPServer(("0.0.0.0", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\nServer stopped")
    sys.exit(0)