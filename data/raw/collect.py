import requests
import pandas as pd
import time
import os
from typing import List, Dict


from app.config import (
    TMDB_API_KEY as API_KEY,
    TMDB_BASE_URL as BASE_URL,
    START_YEAR,
    END_YEAR,
    VOTE_COUNT_MIN,
    REQUEST_DELAY,
    RAW_MOVIES_CSV as OUTPUT_FILE
)
CHECKPOINT_FILE = "checkpoint_movies.csv"


session = requests.Session()
session.params = {"api_key": API_KEY}


def load_genres() -> Dict[int, str]:
    r = session.get(f"{BASE_URL}/genre/movie/list", params={"language": "en-US"})
    r.raise_for_status()
    return {g["id"]: g["name"] for g in r.json()["genres"]}

GENRE_MAP = load_genres()


def discover_movies(year: int) -> List[Dict]:
    movies = []
    page = 1

    while True:
        r = session.get(
            f"{BASE_URL}/discover/movie",
            params={
                "language": "en-US",
                "primary_release_date.gte": f"{year}-01-01",
                "primary_release_date.lte": f"{year}-12-31",
                "vote_count.gte": VOTE_COUNT_MIN,
                "sort_by": "release_date.asc",
                "page": page
            }
        )

        if r.status_code != 200:
            print(f"[WARN] Discover failed | Year {year} Page {page}")
            break

        data = r.json()
        movies.extend(data["results"])

        if page >= data["total_pages"]:
            break

        page += 1
        time.sleep(REQUEST_DELAY)

    return movies


def fetch_movie_details(movie_id: int) -> Dict:
    r = session.get(f"{BASE_URL}/movie/{movie_id}", params={"language": "en-US"})
    r.raise_for_status()
    return r.json()

def fetch_credits(movie_id: int):
    r = session.get(f"{BASE_URL}/movie/{movie_id}/credits")
    r.raise_for_status()
    data = r.json()

    director = next(
        (c["name"] for c in data["crew"] if c.get("job") == "Director"),
        None
    )

    cast = [c["name"] for c in data["cast"][:5]]
    return director, cast

def fetch_keywords(movie_id: int) -> List[str]:
    r = session.get(f"{BASE_URL}/movie/{movie_id}/keywords")
    if r.status_code != 200:
        return []
    return [k["name"] for k in r.json().get("keywords", [])]


records = []
collected_ids = set()

if os.path.exists(CHECKPOINT_FILE):
    df_ckpt = pd.read_csv(CHECKPOINT_FILE)
    records = df_ckpt.to_dict(orient="records")
    collected_ids = set(df_ckpt["id"].astype(int))
    print(f"[INFO] Resumed {len(collected_ids)} movies")


for year in range(START_YEAR, END_YEAR + 1):
    print(f"\n[INFO] Collecting year {year}")
    movies = discover_movies(year)
    print(f"[INFO] Found {len(movies)} movies")

    for movie in movies:
        movie_id = movie["id"]

        if movie_id in collected_ids:
            continue

        try:
            details = fetch_movie_details(movie_id)
            director, cast = fetch_credits(movie_id)
            keywords = fetch_keywords(movie_id)

            record = {
                "id": movie_id,
                "imdb_id": details.get("imdb_id"),
                "title": movie.get("title"),
                "original_title": movie.get("original_title"),
                "overview": movie.get("overview"),
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average"),
                "vote_count": movie.get("vote_count"),
                "popularity": movie.get("popularity"),
                "genres": ", ".join(
                    GENRE_MAP[g["id"]] for g in details.get("genres", [])
                ),
                "runtime": details.get("runtime"),
                "tagline": details.get("tagline"),
                "director": director,
                "main_cast": ", ".join(cast),
                "keywords": ", ".join(keywords),
                "poster_path": movie.get("poster_path")
            }

            records.append(record)
            collected_ids.add(movie_id)

            if len(records) % 50 == 0:
                pd.DataFrame(records).to_csv(CHECKPOINT_FILE, index=False)
                print(f"[CHECKPOINT] {len(records)} movies saved")

            time.sleep(REQUEST_DELAY)

        except Exception as e:
            print(f"[ERROR] Movie {movie_id} failed: {e}")
            time.sleep(1)


df = pd.DataFrame(records)
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
print(f"\n[DONE] Saved {len(df)} movies → {OUTPUT_FILE}")
