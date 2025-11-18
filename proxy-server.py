#!/usr/bin/env python3
"""
CarBuyer Proxy Server
Standalone proxy server for routing traffic between Customer and Admin services
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import sys
import os

# Load configuration from .env file
def load_env():
    config = {}
    
    if not os.path.exists('.env'):
        print('\n✗ Error: .env file not found')
        print('  Please create .env file with:')
        print('  ADMIN_SERVICE_URL=http://YOUR_ADMIN_IP:3001')
        print('  CUSTOMER_SERVICE_URL=http://localhost:3000')
        print('  PROXY_PORT=3001')
        sys.exit(1)
    
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return config

config = load_env()
ADMIN_SERVICE_URL = config.get('ADMIN_SERVICE_URL', 'http://localhost:3001')
CUSTOMER_SERVICE_URL = config.get('CUSTOMER_SERVICE_URL', 'http://localhost:3000')
PROXY_PORT = int(config.get('PROXY_PORT', '3001'))

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.proxy_request()
    
    def do_POST(self):
        self.proxy_request()
    
    def do_PUT(self):
        self.proxy_request()
    
    def do_DELETE(self):
        self.proxy_request()
    
    def proxy_request(self):
        # Determine target based on path
        if self.path.startswith('/admin') or self.path.startswith('/employee'):
            target = ADMIN_SERVICE_URL
        else:
            target = CUSTOMER_SERVICE_URL
        
        url = target + self.path
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Create request
            req = urllib.request.Request(url, data=body, method=self.command)
            
            # Copy headers (skip host and connection)
            for key, value in self.headers.items():
                if key.lower() not in ['host', 'connection']:
                    req.add_header(key, value)
            
            # Send request and get response
            with urllib.request.urlopen(req, timeout=30) as response:
                self.send_response(response.status)
                for key, value in response.headers.items():
                    if key.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(key, value)
                self.end_headers()
                self.wfile.write(response.read())
        
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            error_msg = f'Bad Gateway: {str(e)}'.encode()
            self.wfile.write(error_msg)
    
    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")

if __name__ == '__main__':
    try:
        server = HTTPServer(('0.0.0.0', PROXY_PORT), ProxyHandler)
        print(f'✓ Proxy Server running on port {PROXY_PORT}')
        print(f'✓ Customer Service: {CUSTOMER_SERVICE_URL}')
        print(f'✓ Admin Service: {ADMIN_SERVICE_URL}')
        print('✓ Press Ctrl+C to stop')
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n✓ Server stopped')
        sys.exit(0)
    except PermissionError:
        print(f'\n✗ Error: Permission denied to bind port {PROXY_PORT}')
        print('  Run with sudo: sudo python3 proxy-server.py')
        sys.exit(1)

