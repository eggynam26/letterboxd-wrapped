"""Look up movie poster URLs on TMDB, caching results in posters_cache.json.

Needs TMDB_API_KEY in your environment or in a .env file next to this script.
"""
import json
import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

CACHE_FILE = Path(__file__).parent / "posters_cache.json"
SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
IMAGE_BASE = "https://image.tmdb.org/t/p/w342"


def load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}


def lookup_poster(name: str, year: int, key: str) -> str | None:
    """Return a full poster URL for one film, or None if TMDB has no match."""
    r = requests.get(SEARCH_URL, params={"api_key": key, "query": name, "year": year}, timeout=10)
    r.raise_for_status()
    results = r.json()["results"]
    if not results or not results[0].get("poster_path"):
        return None
    return IMAGE_BASE + results[0]["poster_path"]


def get_posters(diary: pd.DataFrame) -> list[str]:
    """Return poster URLs for every unique film in the diary, in watch order."""
    load_dotenv(Path(__file__).parent / ".env")
    key = os.environ.get("TMDB_API_KEY")
    cache = load_cache()

    films = diary.sort_values("Watched Date").drop_duplicates(subset=["Name", "Year"])
    posters = []
    for name, year in zip(films["Name"], films["Year"]):
        cache_key = f"{name} ({year})"
        if cache_key not in cache:
            if not key:
                print("No TMDB_API_KEY set, skipping posters.")
                break
            try:
                cache[cache_key] = lookup_poster(name, int(year), key)
            except requests.RequestException as e:
                print(f"Couldn't look up {cache_key}: {e}")
                continue
        if cache[cache_key]:
            posters.append(cache[cache_key])

    CACHE_FILE.write_text(json.dumps(cache, indent=2))
    return posters
