import os

class Creds:
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    API_HASH = os.environ.get("API_HASH", "")
    API_ID = os.environ.get("API_ID", "")