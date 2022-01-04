from os import environ
from dotenv import load_dotenv

load_dotenv()

# Social Tokens
GITHUB_KEY = environ.get("GITHUB_KEY", "orchid")
GITHUB_SECRET = environ.get("GITHUB_SECRET", "orchid")

SPOTIFY_KEY = environ.get("SPOTIFY_KEY", "orchid")
SPOTIFY_SECRET = environ.get("SPOTIFY_SECRET", "orchid")