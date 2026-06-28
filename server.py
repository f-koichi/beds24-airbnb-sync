import time
import threading
from flask import Flask, Response, jsonify
from ical_generator import build_ical_for_room
from config import HOST, PORT, ROOM_MAPPING

app = Flask(__name__)

CACHE_TTL = 3600
_cache: dict[int, tuple[float, bytes]] = {}
_cache_lock = threading.Lock()


def _refresh_cache():
    for room_id in ROOM_MAPPING:
        try:
            data = build_ical_for_room(room_id)
            with _cache_lock:
                _cache[room_id] = (time.time(), data)
            print(f"Cache refreshed for {ROOM_MAPPING[room_id]} ({room_id})")
        except Exception as e:
            print(f"Cache refresh failed for {room_id}: {e}")


def _background_refresh():
    while True:
        _refresh_cache()
        time.sleep(CACHE_TTL)


@app.route("/")
def index():
    lines = ["<h1>Beds24 → AirBnB iCal Feeds</h1><ul>"]
    for room_id, name in ROOM_MAPPING.items():
        cached = "ready" if room_id in _cache else "loading..."
        lines.append(f'<li><a href="/ical/{room_id}">{name}</a> — /ical/{room_id} [{cached}]</li>')
    lines.append("</ul>")
    return "\n".join(lines)


@app.route("/ical/<int:room_id>")
def ical_feed(room_id: int):
    if room_id not in ROOM_MAPPING:
        return jsonify({"error": "Room not mapped to AirBnB"}), 404

    with _cache_lock:
        entry = _cache.get(room_id)

    if entry is None:
        return Response("Cache not ready, try again shortly", status=503)

    return Response(entry[1], mimetype="text/calendar", headers={
        "Content-Disposition": f"inline; filename=beds24-{room_id}.ics",
    })


if __name__ == "__main__":
    print("Building initial cache (this may take a few minutes)...")
    _refresh_cache()
    print("Cache ready! Starting server.")
    t = threading.Thread(target=_background_refresh, daemon=True)
    t.start()
    app.run(host=HOST, port=PORT)
