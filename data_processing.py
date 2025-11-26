def extract_yearly_count(api_json):
    """
    FBI API returns a list inside 'results'.
    We extract total incidents for that year.
    """
    if api_json is None or "results" not in api_json:
        return None

    results = api_json["results"]
    if len(results) == 0:
        return None

    # The "data_year" and "value" fields contain crime counts
    return {
        "year": results[0]["data_year"],
        "count": results[0]["value"]
    }
