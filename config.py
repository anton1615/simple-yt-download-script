import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")
COOKIE_FILE = os.environ.get("COOKIE_FILE", "cookies.txt")

if not YOUTUBE_API_KEY:
    print(
        "Warning: YOUTUBE_API_KEY not set. Please set it in .env file or environment variable."
    )
