"""Letterboxd Wrapped: turn your Letterboxd data export into a Spotify-Wrapped style page.

Usage:
    1. On letterboxd.com go to Settings > Data > Export your data, then unzip it.
    2. pip install pandas jinja2
    3. python wrapped.py path/to/export_folder --year 2026
    4. Open wrapped.html in a browser.
"""
import argparse
from pathlib import Path

import pandas as pd
from jinja2 import Template

from posters import get_posters


def load_diary(export_dir: Path, year: int | None) -> pd.DataFrame:
    """diary.csv has one row per logged watch: Date, Name, Year, Letterboxd URI,
    Rating, Rewatch, Tags, Watched Date."""
    diary = pd.read_csv(export_dir / "diary.csv")
    diary["Watched Date"] = pd.to_datetime(diary["Watched Date"])
    diary["Rewatch"] = diary["Rewatch"].fillna("").eq("Yes")
    if year:
        diary = diary[diary["Watched Date"].dt.year == year]
    return diary


def compute_stats(diary: pd.DataFrame) -> dict:
    rated = diary.dropna(subset=["Rating"])
    by_month = diary.groupby(diary["Watched Date"].dt.strftime("%b"), sort=False).size()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    by_month = by_month.reindex(months, fill_value=0)
    weekday = diary["Watched Date"].dt.day_name().value_counts()
    decade = (diary["Year"] // 10 * 10).value_counts()

    top = rated.sort_values(["Rating", "Watched Date"], ascending=[False, True]).head(5)
    return {
        "total": len(diary),
        "unique": diary["Letterboxd URI"].nunique(),
        "rewatches": int(diary["Rewatch"].sum()),
        "avg_rating": round(rated["Rating"].mean(), 2) if len(rated) else None,
        "by_month": by_month.to_dict(),
        "max_month": int(by_month.max()) or 1,
        "busiest_month": by_month.idxmax(),
        "fav_weekday": weekday.idxmax() if len(weekday) else None,
        "fav_decade": f"{int(decade.idxmax())}s" if len(decade) else None,
        "rating_dist": rated["Rating"].value_counts().sort_index().to_dict(),
        "top_films": top[["Name", "Year", "Rating"]].to_dict("records"),
        "first": diary.sort_values("Watched Date").iloc[0].to_dict() if len(diary) else None,
    }


TEMPLATE = Template((Path(__file__).parent / "template.html").read_text())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("export_dir", type=Path)
    p.add_argument("--year", type=int, default=None)
    p.add_argument("--user", default="you")
    p.add_argument("--out", type=Path, default=Path("wrapped.html"))
    p.add_argument("--no-posters", action="store_true", help="skip the TMDB poster lookup")
    args = p.parse_args()

    diary = load_diary(args.export_dir, args.year)
    if diary.empty:
        raise SystemExit("No diary entries found for that year.")
    stats = compute_stats(diary)
    stats["posters"] = [] if args.no_posters else get_posters(diary)
    args.out.write_text(TEMPLATE.render(s=stats, user=args.user, year=args.year or "All time"))
    print(f"Wrote {args.out} ({stats['total']} films)")


if __name__ == "__main__":
    main()
