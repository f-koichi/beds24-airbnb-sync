import os
from dotenv import load_dotenv

load_dotenv()

BEDS24_API_KEY = os.environ["BEDS24_API_TOKEN"]
BEDS24_API_BASE = "https://api.beds24.com/json"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))
SYNC_DAYS = int(os.getenv("SYNC_DAYS", "30"))

ROOM_MAPPING = {
    497200: "Nutshell",
    497201: "Hut-nest",
    497202: "Hut-roof",
}
