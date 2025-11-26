import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("FBI_API_KEY")

BASE_URL = "https://api.usa.gov/crime/fbi/cde/hate-crime/state"


def fetch_with_retry(url, retries=3):
    """Try GET request with retries + timeout."""
    for i in range(retries):
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                return response.json()
            else:
                print("API response:", response.text)
        except requests.exceptions.Timeout:
            print(f"Timeout {i+1}/{retries} for URL:", url)
    raise RuntimeError("FBI API failed after retries / timeout.")

def get_hate_crime_trends(state, start_year, end_year):
    if not API_KEY:
        raise ValueError("Missing FBI API KEY")

    # Convert years to mm-yyyy
    start = f"01-{start_year}"
    end = f"01-{end_year}"

    url = (
        f"https://api.usa.gov/crime/fbi/cde/hate-crime/state/{state}"
        f"?type=counts&from={start}&to={end}&API_KEY={API_KEY}"
    )

    raw_json = fetch_with_retry(url)
    if "rates" not in raw_json:
        raise RuntimeError("Unexpected FBI API format")

    # Pick the correct category — category “01”
    state_key = list(raw_json["rates"].keys())[0]          # "Massachusetts Offenses"
    all_categories = raw_json["rates"][state_key]

    years = []
    state_rates = []

    for k, v in all_categories.items():
        category = k.split("-")[0]       # "01", "02", ...
        year = int(k.split("-")[1])      # 2000, 2001...

        if category == "01":             # KEEP ONLY main total category
            years.append(year)
            state_rates.append(v)

    return {
        "years": years,
        "state_rates": state_rates,
        "us_rates": [None] * len(years),
        "state_label": state,
    }




def fetch_raw_response(state, start_year, end_year):
    start = f"01-{start_year}"
    end = f"01-{end_year}"

    url = (
        f"https://api.usa.gov/crime/fbi/cde/hate-crime/state/{state}"
        f"?type=counts&from={start}&to={end}&API_KEY={API_KEY}"
    )
    return fetch_with_retry(url)
