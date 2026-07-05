import requests
from datetime import date, timedelta
from config import BEDS24_API_KEY

API_BASE = "https://api.beds24.com/json"


def _auth() -> dict:
    return {"apiKey": BEDS24_API_KEY}


def get_properties() -> list[dict]:
    resp = requests.post(
        f"{API_BASE}/getProperties",
        json={"authentication": _auth()},
    )
    resp.raise_for_status()
    return resp.json().get("getProperties", [])


def get_daily_availability(room_id: int, days: int = 365) -> dict[date, int]:
    today = date.today()
    result = {}

    for i in range(days):
        d = today + timedelta(days=i)
        resp = requests.post(
            f"{API_BASE}/getAvailabilities",
            json={
                "authentication": _auth(),
                "roomId": str(room_id),
                "checkIn": d.strftime("%Y%m%d"),
                "checkOut": (d + timedelta(days=1)).strftime("%Y%m%d"),
            },
        )
        resp.raise_for_status()
        data = resp.json()
        room_data = data.get(str(room_id), {})
        avail = int(room_data.get("roomsavail", 1))
        result[d] = avail

    return result
