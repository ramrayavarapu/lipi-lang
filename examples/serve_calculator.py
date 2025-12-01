#!/usr/bin/env python3
"""
Simple HTTP Server for Lipi Calculator UI
Serves the calculator_ui.html file on localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuration
PORT = 8000
CALCULATOR_HTML = "calculator_ui.html"

class CalculatorHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for the calculator"""

    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        # Redirect root to calculator UI
        if self.path == '/':
            self.path = f'/{CALCULATOR_HTML}'
        return super().do_GET()

def main():
    """Start the HTTP server"""

    # Check if calculator HTML exists
    html_path = Path(__file__).parent / CALCULATOR_HTML
    if not html_path.exists():
        print(f"❌ Error: {CALCULATOR_HTML} not found in {Path(__file__).parent}")
        print(f"   Please ensure {CALCULATOR_HTML} exists in the examples directory.")
        return

    # Create server
    with socketserver.TCPServer(("", PORT), CalculatorHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("🧮 LIPI CALCULATOR WEB SERVER")
        print("   లిపి కాలిక్యులేటర్ వెబ్ సర్వర్")
        print("=" * 60)
        print(f"\n✓ Server started successfully!")
        print(f"✓ Serving: {html_path}")
        print(f"\n🌐 Access the calculator at:")
        print(f"   http://localhost:{PORT}")
        print(f"   http://127.0.0.1:{PORT}")
        print(f"\n📝 Press Ctrl+C to stop the server")
        print("=" * 60)
        print()

        # Optionally open browser
        try:
            print("🌐 Opening calculator in your default browser...")
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            pass

        # Start serving
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n" + "=" * 60)
            print("👋 Server stopped. వీడ్కోలు! (Goodbye!)")
            print("=" * 60)

if __name__ == "__main__":
    main()
