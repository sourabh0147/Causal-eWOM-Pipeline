import requests
import time
import pandas as pd

def get_steam_reviews(appid, max_reviews=1000):
    url = f"https://store.steampowered.com/appreviews/{appid}"
    reviews_data = []
    cursor = '*'
    print(f"Fetching reviews and playtime telemetry for App ID: {appid}...")

    while len(reviews_data) < max_reviews:
        params = {
            'json': 1, 'filter': 'recent', 'language': 'english',
            'review_type': 'all', 'purchase_type': 'all',
            'num_per_page': 100, 'cursor': cursor
        }

        response = requests.get(url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code != 200: break

        data = response.json()
        batch = data.get('reviews', [])
        if not batch: break

        reviews_data.extend(batch)
        next_cursor = data.get('cursor')
        if not next_cursor or next_cursor == cursor: break
        cursor = next_cursor

        # Short delay to be polite to the public endpoint
        time.sleep(0.5)

    reviews_data = reviews_data[:max_reviews]
    df = pd.json_normalize(reviews_data)

    # Notice we can grab playtime_forever directly from the review author object
    columns_to_keep = {
        'recommendationid': 'review_id',
        'author.steamid': 'author_steamid',
        'author.num_games_owned': 'author_total_games',
        'author.playtime_at_review': 'playtime_at_review_mins',
        'author.playtime_forever': 'playtime_forever_mins',  # <-- Extracted in Stage 1
        'review': 'review_text',
        'voted_up': 'is_positive_valence',
        'timestamp_created': 'unix_timestamp'
    }

    df = df.rename(columns=columns_to_keep)
    return df[[col for col in columns_to_keep.values() if col in df.columns]]

# --- Execution Block ---
TARGET_APP_ID = 1091500  # Cyberpunk 2077
MAX_TO_FETCH = 2500

# 1. Get base reviews AND current lifetime playtime in one swift pass
df_final = get_steam_reviews(TARGET_APP_ID, max_reviews=MAX_TO_FETCH)

# 2. Calculate the dependent variables
df_final['subsequent_lifetime_playtime'] = df_final['playtime_forever_mins'] - df_final['playtime_at_review_mins']
df_final['subsequent_lifetime_playtime'] = df_final['subsequent_lifetime_playtime'].clip(lower=0)

# Calculate elapsed time proxy (Current Unix time minus review Unix time)
current_unix = int(time.time())
df_final['time_elapsed_since_pub'] = (current_unix - df_final['unix_timestamp']) / (60*60*24) # in days

# 3. Save the complete dataset
csv_filename = f"primary_steam_data_{TARGET_APP_ID}.csv"
df_final.to_csv(csv_filename, index=False)
print(f"\nReal telemetry secured without an API key! Final N = {len(df_final)}. Exported to {csv_filename}.")