import json
from crime_api import get_hate_crime_trends, fetch_raw_response

if __name__ == "__main__":
    raw = fetch_raw_response("MA", 2000, 2010)
    print(json.dumps(raw, indent=2))
