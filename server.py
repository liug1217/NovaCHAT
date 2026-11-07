"""NovaCHAT 開發伺服器（Phase 1）。

只用 Python 內建的東西，不用安裝套件。
    py server.py          （Windows）
    python3 server.py     （Mac / Linux）

啟動後：
    這台電腦：      http://localhost:8900/
    同 Wi-Fi 手機： http://<這台電腦的 IP>:8900/

目前只做「靜態網站 + /api/ping」。聊天的真後端（帳號 / 好友 / 群組 / 即時 / 推播）
是下一階段；為了不偽造尚未完成的功能，/api/chats 現在明確回 501（尚未實作）。
前端的資料層 Store 之後只要把 SEED 換成呼叫這些 API 即可。
"""

import json
import os
import socket
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

PORT = int(os.environ.get('NOVACHAT_PORT', '8900'))
HOST = os.environ.get('NOVACHAT_HOST', '0.0.0.0')
ROOT = os.path.dirname(os.path.abspath(__file__))

# 只開放網站本身的檔案
PUBLIC_FILES = {'/NovaCHAT.html', '/index.html', '/sw.js', '/manifest.json'}
PUBLIC_DIRS = ('/assets/',)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/ping':
            return self.send_json(200, {'ok': True, 'app': 'novachat', 'phase': 1})
        if path == '/api/chats':
            # 尚未實作（不偽造後端）。下一階段接真資料時改這裡。
            return self.send_json(501, {'error': 'not_implemented', 'hint': 'chat backend is Phase 2'})
        if path in ('/', '/index.html'):
            self.send_response(302)
            self.send_header('Location', '/NovaCHAT.html')
            self.end_headers()
            return
        if (path in PUBLIC_FILES or path.startswith(PUBLIC_DIRS)) and '..' not in path:
            return super().do_GET()
        return self.send_error(404)


def lan_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'


def main():
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    server.daemon_threads = True
    print('NovaCHAT 伺服器已啟動')
    print(f'  這台電腦：      http://localhost:{PORT}/')
    print(f'  同 Wi-Fi 手機： http://{lan_ip()}:{PORT}/')
    print('  按 Ctrl+C 關閉')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n已關閉')


if __name__ == '__main__':
    main()
