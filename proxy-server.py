#!/usr/bin/env python3
"""
CarBuyer Proxy Server
Standalone proxy server for routing traffic between Customer and Admin services
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
from http.cookiejar import CookieJar
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
        # Determine target and path prefix
        if self.path.startswith('/admin'):
            target = ADMIN_SERVICE_URL
            prefix = 'admin'
        elif self.path.startswith('/employee'):
            target = ADMIN_SERVICE_URL
            prefix = 'employee'
        else:
            target = CUSTOMER_SERVICE_URL
            prefix = None
        
        url = target + self.path
        
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # Create request with cookie support
            req = urllib.request.Request(url, data=body, method=self.command)
            
            # Copy ALL headers including cookies
            for key, value in self.headers.items():
                if key.lower() not in ['host']:
                    req.add_header(key, value)
            
            # Use opener with cookie support
            opener = urllib.request.build_opener()
            with opener.open(req, timeout=30) as response:
                content = response.read()
                content_type = response.headers.get('Content-Type', '')
                
                # Rewrite HTML content to fix static file paths
                if prefix and 'text/html' in content_type:
                    content = content.decode('utf-8', errors='ignore')
                    content = content.replace('"/Public/', f'"/{prefix}/Public/')
                    content = content.replace("'/Public/", f"'/{prefix}/Public/")
                    content = content.encode('utf-8')
                
                self.send_response(response.status)
                # Forward ALL response headers including Set-Cookie
                for key, value in response.headers.items():
                    if key.lower() not in ['transfer-encoding', 'content-length']:
                        self.send_header(key, value)
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
        
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

