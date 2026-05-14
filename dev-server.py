#!/usr/bin/env python3
"""
Dev server multi-thread avec :
- ThreadingHTTPServer : traite plusieurs requetes en parallele (sinon le hero video
  de 66 Mo bloque tout)
- Range requests (pour <video> en streaming)
- Headers no-cache (pour voir tout de suite les changements d'assets)

Usage : python dev-server.py
Port  : 8765
"""
import os
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = 8765


class NoCacheHandler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".mp4":  "video/mp4",
        ".webm": "video/webm",
        ".js":   "application/javascript",
        ".css":  "text/css",
        ".svg":  "image/svg+xml",
        ".woff2": "font/woff2",
    }

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        # Less noisy logs
        if args and isinstance(args[0], str) and args[0].startswith(("GET", "HEAD")):
            return
        super().log_message(format, *args)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with ThreadingHTTPServer(("", PORT), NoCacheHandler) as httpd:
        print(f"Dev server (multi-thread, no-cache) http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
