"""Generate a fake Letterboxd export (diary.csv) for testing wrapped.py."""
import csv
import random
from datetime import date, timedelta
from pathlib import Path

FILMS = [
    ("Past Lives", 2023), ("Dune: Part Two", 2024), ("Paddington 2", 2017),
    ("Parasite", 2019), ("In the Mood for Love", 2000), ("Alien", 1979),
    ("The Godfather", 1972), ("Spirited Away", 2001), ("Whiplash", 2014),
    ("Heat", 1995), ("Aftersun", 2022), ("Mad Max: Fury Road", 2015),
    ("Before Sunrise", 1995), ("Oppenheimer", 2023), ("Perfect Days", 2023),
]

random.seed(1)
out = Path(__file__).parent / "sample_export"
out.mkdir(exist_ok=True)
seen = set()
with open(out / "diary.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Date", "Name", "Year", "Letterboxd URI", "Rating", "Rewatch", "Tags", "Watched Date"])
    for _ in range(60):
        name, yr = random.choice(FILMS)
        watched = date(2026, 1, 1) + timedelta(days=random.randint(0, 270))
        rating = random.choice(["", 2.5, 3, 3.5, 4, 4.5, 5])
        rewatch = "Yes" if name in seen else ""
        seen.add(name)
        uri = "https://boxd.it/" + name.lower().replace(" ", "")[:6]
        w.writerow([watched, name, yr, uri, rating, rewatch, "", watched])
print(f"Wrote {out / 'diary.csv'}")
