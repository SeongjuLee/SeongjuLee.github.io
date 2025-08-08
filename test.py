#!/usr/bin/env python3
"""
Simple HTTP server to preview the portfolio website locally.
Usage: python main.py
"""

import http.server
import socketserver
import webbrowser
import os
import signal
import sys
from pathlib import Path

class GracefulHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging for cleaner output
        pass

def signal_handler(signum, frame):
    """Handle interrupt signals gracefully"""
    print("\n🛑 Received interrupt signal. Shutting down gracefully...")
    sys.exit(0)

def main():
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Check if index.html exists
    index_path = current_dir / "index.html"
    if not index_path.exists():
        print("❌ Error: index.html not found in the current directory")
        print(f"Expected location: {index_path}")
        return
    
    # Set up the server
    PORT = 8000
    
    # Change to the directory containing the HTML file
    os.chdir(current_dir)
    
    # Create the server with graceful shutdown
    Handler = GracefulHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            # Allow reuse of the address
            httpd.allow_reuse_address = True
            
            print(f"🚀 Starting local server...")
            print(f"📁 Serving files from: {current_dir}")
            print(f"🌐 Server running at: http://localhost:{PORT}")
            print(f"📄 Main page: http://localhost:{PORT}/index.html")
            print("\n" + "="*50)
            print("💡 Tips:")
            print("   - Press Ctrl+C to stop the server")
            print("   - Your browser should open automatically")
            print("   - If not, manually visit: http://localhost:8000")
            print("="*50 + "\n")
            
            # Try to open the browser automatically
            try:
                webbrowser.open(f"http://localhost:{PORT}")
                print("✅ Browser opened automatically!")
            except Exception as e:
                print(f"⚠️  Could not open browser automatically: {e}")
                print("   Please manually visit: http://localhost:8000")
            
            # Start the server
            print("🔄 Server is running... (Press Ctrl+C to stop)")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user (Ctrl+C)")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Error: Port {PORT} is already in use")
            print("   Try using a different port or stop the existing server")
            print("   You can kill the process using: lsof -ti:8000 | xargs kill -9")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 