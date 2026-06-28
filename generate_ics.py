"""Generate static .ics files for each room and upload to a public host."""
import os
from beds24_client import get_daily_availability
from ical_generator import build_ical_for_room
from config import ROOM_MAPPING

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "ics_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

for room_id, name in ROOM_MAPPING.items():
    print(f"Generating iCal for {name} ({room_id})...")
    data = build_ical_for_room(room_id)
    path = os.path.join(OUTPUT_DIR, f"{room_id}.ics")
    with open(path, "wb") as f:
        f.write(data)
    print(f"  Saved to {path} ({len(data)} bytes)")

print(f"\nAll files saved to {OUTPUT_DIR}")
