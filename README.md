# Letterboxd Wrapped

Turns your Letterboxd data into a scrollable, Spotify-Wrapped style page.

## Quick start
1. letterboxd.com → Settings → Data → **Export your data**, unzip it.
2. `pip install pandas jinja2`
3. `python wrapped.py ~/Downloads/letterboxd-export --year 2026 --user Chris`
4. Open `wrapped.html`.

Try it without your data: `python make_sample_data.py && python wrapped.py sample_export --year 2026`.

## Files
- `wrapped.py`: loads `diary.csv`, computes stats with pandas, renders the page.
- `template.html`: Jinja2 template, one full-screen "slide" per stat.
- `make_sample_data.py`: writes a fake export to `sample_export/`.

## Getting the data: options
| Source | Pros | Cons |
|---|---|---|
| CSV export (used here) | Complete, official, no scraping | Manual download |
| RSS `letterboxd.com/USERNAME/rss/` | Automatable, no login | Only the ~50 most recent entries |
| Scrape `letterboxd.com/USERNAME/films/diary/` with requests + BeautifulSoup | Fully automated, can grab extra page data | Fragile HTML, check ToS, sleep 1–2s between requests |

## Next steps
- **Genres, directors, actors, runtime (total hours):** the export doesn't include these. Look each film up on the free TMDB API (`/search/movie?query=Name&year=Year`, then `/movie/{id}?append_to_response=credits`), cache results to a JSON file, and join on Name + Year.
- **Interactive version:** swap the template for Streamlit if you'd rather have filters and charts.
