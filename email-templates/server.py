#!/usr/bin/env python3
"""
Simple HTTP server to test email templates on different devices
Automatically finds an available port and can kill existing servers
"""

import http.server
import socketserver
import socket
import os
import sys
import subprocess

# Get local IP address
def get_local_ip():
    try:
        # Connect to an external server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

# Find available port
def find_available_port(start_port=8000, max_port=9000):
    for port in range(start_port, max_port):
        try:
            # Try to bind to the port
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.bind(('', port))
            test_socket.close()
            return port
        except OSError:
            continue
    return None

# Kill existing Python servers on common ports
def kill_existing_servers():
    common_ports = [8000, 8080, 8888, 3000, 5000]
    killed_any = False

    for port in common_ports:
        try:
            # Find process using the port
            result = subprocess.run(
                ['lsof', '-t', '-i', f':{port}'],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                for pid in pids:
                    try:
                        subprocess.run(['kill', '-9', pid])
                        print(f"✅ Killed process {pid} on port {port}")
                        killed_any = True
                    except:
                        pass
        except:
            pass

    return killed_any

# Configuration
DIRECTORY = "/Users/lucianocosme/Projects/ucr-ento-social/email-templates"

# Check for --kill flag
if len(sys.argv) > 1 and sys.argv[1] == '--kill':
    print("🔍 Looking for existing servers to kill...")
    if kill_existing_servers():
        print("✅ Killed existing servers")
    else:
        print("ℹ️  No existing servers found")
    print()

# Find available port
PORT = find_available_port()
if PORT is None:
    print("❌ Could not find an available port!")
    print("   Try running: python3 server.py --kill")
    sys.exit(1)

# Change to the email-templates directory
os.chdir(DIRECTORY)

# Create handler
Handler = http.server.SimpleHTTPRequestHandler

# Get local IP
LOCAL_IP = get_local_ip()

print("\n" + "="*60)
print("📧 EMAIL TEMPLATE TEST SERVER")
print("="*60)
print(f"\n✅ Server starting on port {PORT}...")
print(f"\n📱 Access from your devices:")
print(f"   Computer: http://localhost:{PORT}/")
print(f"   Phone/Tablet: http://{LOCAL_IP}:{PORT}/")
print(f"\n📁 Serving files from: {DIRECTORY}")
print("\n" + "="*60)
print("\n🔗 Available templates:")
print(f"   http://{LOCAL_IP}:{PORT}/poll-announcement.html")
print("\n" + "="*60)
print("\n⚠️  Make sure your phone is on the same WiFi network!")
print("\n💡 Tips:")
print("   - Refresh browser with Ctrl+F5 to see changes")
print("   - Run 'python3 server.py --kill' to stop all servers")
print("\nPress Ctrl+C to stop the server\n")

# Start server with reuse address option
class ReuseAddrServer(socketserver.TCPServer):
    allow_reuse_address = True

try:
    with ReuseAddrServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n✅ Server stopped")
    sys.exit(0)