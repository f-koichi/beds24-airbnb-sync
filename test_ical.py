import os
os.environ.setdefault("BEDS24_API_TOKEN", "test")

from datetime import date
from icalendar import Calendar
from ical_generator import _blocked_ranges_from_availability, build_ical_for_room
from unittest.mock import patch


def test_blocked_ranges():
    avail = {
        date(2026, 7, 1): 0,
        date(2026, 7, 2): 0,
        date(2026, 7, 3): 1,
        date(2026, 7, 5): 0,
    }
    ranges = _blocked_ranges_from_availability(avail)
    assert ranges == [
        (date(2026, 7, 1), date(2026, 7, 2)),
        (date(2026, 7, 5), date(2026, 7, 5)),
    ]


def test_no_blocked():
    avail = {date(2026, 7, 1): 1, date(2026, 7, 2): 1}
    assert _blocked_ranges_from_availability(avail) == []


@patch("ical_generator.get_daily_availability")
def test_ical_output(mock_avail):
    mock_avail.return_value = {
        date(2026, 7, 1): 0,
        date(2026, 7, 2): 0,
        date(2026, 7, 3): 1,
    }
    ical_bytes = build_ical_for_room(497200)
    cal = Calendar.from_ical(ical_bytes)
    events = [c for c in cal.walk() if c.name == "VEVENT"]
    assert len(events) == 1
    assert str(events[0]["summary"]) == "Not Available"


if __name__ == "__main__":
    test_blocked_ranges()
    test_no_blocked()
    test_ical_output()
    print("All tests passed!")
