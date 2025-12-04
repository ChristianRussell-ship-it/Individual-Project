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

# --- NEW: get list of states for the dropdown --------------------
def get_state_choices():
    """
    Return a list of (abbr, name) for U.S. states.
    Tries FBI API first; if that fails, uses a local fallback list.
    """
    if not API_KEY:
        print("Warning: FBI_API_KEY missing, using local state list.")
    else:
        try:
            url = f"https://api.usa.gov/crime/fbi/cde/hate-crime/states?API_KEY={API_KEY}"
            data = fetch_with_retry(url)
            states = []
            # This part is defensive because we don't know the exact JSON layout
            for item in data.get("states", []):
                abbr = item.get("state_abbr") or item.get("abbr")
                name = item.get("state_name") or item.get("name")
                if abbr and name:
                    states.append((abbr, name))
            if states:
                # sort alphabetically by name
                return sorted(states, key=lambda x: x[1])
        except Exception as e:
            print("Could not fetch state list from FBI API, using fallback. Error:", e)

    # Fallback: full list of states + DC (works even with no internet)
    fallback_states = [
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming"),
        ("DC", "District of Columbia"),
    ]
    return sorted(fallback_states, key=lambda x: x[1])
