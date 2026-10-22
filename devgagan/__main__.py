# Clean startup file — chor-code (stealer) hata diya gaya hai.
# Ye file saare modules load karke bot ko chalati hai + Koyeb ke liye
# ek chhota health-check port kholti hai.

import asyncio
import importlib
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from devgagan import app, loop
from devgagan.modules import ALL_MODULES


class _Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive")

    def log_message(self, *args):
        pass


def _start_health_server():
    port = int(os.environ.get("PORT", "8000"))
    try:
        HTTPServer(("0.0.0.0", port), _Health).serve_forever()
    except Exception as e:
        print(f"Health server error: {e}", flush=True)


async def _run():
    for module_name in ALL_MODULES:
        importlib.import_module(f"devgagan.modules.{module_name}")
    print("Bot started successfully - saare modules load ho gaye", flush=True)
    await asyncio.Event().wait()


if __name__ == "__main__":
    threading.Thread(target=_start_health_server, daemon=True).start()
    try:
        loop.run_until_complete(_run())
    except KeyboardInterrupt:
        pass
