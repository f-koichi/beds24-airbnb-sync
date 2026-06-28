from datetime import date, datetime, timedelta
from icalendar import Calendar, Event
from beds24_client import get_daily_availability
from config import ROOM_MAPPING, SYNC_DAYS


def build_ical_for_room(room_id: int) -> bytes:
    room_name = ROOM_MAPPING.get(room_id, str(room_id))

    cal = Calendar()
    cal.add("prodid", "-//Beds24-AirBnB-Sync//EN")
    cal.add("version", "2.0")
    cal.add("x-wr-calname", f"Beds24 - {room_name}")

    availability = get_daily_availability(room_id, days=SYNC_DAYS)
    blocked_ranges = _blocked_ranges_from_availability(availability)

    for start, end in blocked_ranges:
        event = Event()
        event.add("uid", f"beds24-{room_id}-{start.isoformat()}@sync")
        event.add("dtstart", start)
        event.add("dtend", end + timedelta(days=1))
        event.add("summary", "Not Available")
        event.add("dtstamp", datetime.utcnow())
        cal.add_component(event)

    return cal.to_ical()


def _blocked_ranges_from_availability(availability: dict[date, int]) -> list[tuple[date, date]]:
    blocked = sorted(d for d, avail in availability.items() if avail <= 0)

    if not blocked:
        return []

    ranges = []
    start = prev = blocked[0]
    for d in blocked[1:]:
        if (d - prev).days == 1:
            prev = d
        else:
            ranges.append((start, prev))
            start = prev = d
    ranges.append((start, prev))
    return ranges
