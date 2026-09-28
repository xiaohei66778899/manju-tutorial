#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的 HTTP server,所有响应加 Cache-Control: no-store,避免浏览器缓存。
替代 python -m http.server,行为一致,只是强制不缓存。
"""
import http.server
import socketserver
import os
import sys
import urllib.parse

PORT = 18080
DIR = r"E:\AIGC\课件\12小说"

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 强制不缓存 + UTF-8
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        # HTML / JS / CSS / 视频默认 charset
        path = self.path
        if path.endswith(".html"):
            self.send_header("Content-Type", "text/html; charset=utf-8")
        elif path.endswith(".js"):
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
        elif path.endswith(".css"):
            self.send_header("Content-Type", "text/css; charset=utf-8")
        elif path.endswith(".mp4"):
            self.send_header("Content-Type", "video/mp4")
        elif path.endswith(".mov"):
            self.send_header("Content-Type", "video/quicktime")
        elif path.endswith(".webm"):
            self.send_header("Content-Type", "video/webm")
        elif path.endswith(".json"):
            self.send_header("Content-Type", "application/json; charset=utf-8")
        # 支持视频 Range 请求(浏览器视频拖拽需要)
        if any(path.endswith(ext) for ext in ('.mp4', '.mov', '.webm', '.ogv')):
            self.send_header("Accept-Ranges", "bytes")
        super().end_headers()

    def log_message(self, format, *args):
        sys.stderr.write("[%s] %s\n" % (self.log_date_time_string(), format % args))

class ThreadingNoCacheServer(http.server.ThreadingHTTPServer):
    """多线程版本:避免单线程被慢请求/僵尸 socket 阻塞整个服务"""
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    os.chdir(DIR)
    with ThreadingNoCacheServer(("127.0.0.1", PORT), NoCacheHandler) as httpd:
        print(f"Threading no-cache server started: http://127.0.0.1:{PORT} (root: {DIR})")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopping...")
            httpd.shutdown()