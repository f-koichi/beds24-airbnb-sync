"""Periodically regenerate ICS files and serve them via HTTP."""
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from beds24_client import get_daily_availability
from ical_generator import build_ical_for_room
from config import ROOM_MAPPING, HOST, PORT

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "ics_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

UPDATE_INTERVAL = 3600


def regenerate_one(room_id, name):
    try:
        data = build_ical_for_room(room_id)
        path = os.path.join(OUTPUT_DIR, f"{room_id}.ics")
        with open(path, "wb") as f:
            f.write(data)
        print(f"[OK] {name} ({room_id}) - {len(data)} bytes")
    except Exception as e:
        print(f"[ERROR] {name} ({room_id}): {e}")


def regenerate_ics():
    with ThreadPoolExecutor(max_workers=3) as executor:
        for room_id, name in ROOM_MAPPING.items():
            executor.submit(regenerate_one, room_id, name)


def update_loop():
    while True:
        print(f"\n--- Updating ICS files ({time.strftime('%Y-%m-%d %H:%M:%S')}) ---")
        regenerate_ics()
        print(f"--- Next update in {UPDATE_INTERVAL // 60} minutes ---")
        time.sleep(UPDATE_INTERVAL)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=OUTPUT_DIR, **kwargs)

    def log_message(self, format, *args):
        print(f"[HTTP] {args[0]}")


if __name__ == "__main__":
    print("=== Beds24 → AirBnB Sync Server ===")
    print("Starting update thread (ICS generation runs in background)...")
    t = threading.Thread(target=update_loop, daemon=True)
    t.start()
    print(f"Serving on {HOST}:{PORT}")
    server = TCPServer((HOST, PORT), Handler)
    server.serve_forever()
