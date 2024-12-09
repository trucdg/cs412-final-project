import requests


def fetch_game_data(event_name, season):
    """
    Fetch game data from the API.

    Args:
        event_name (str): The event name in the format "TeamA_vs_TeamB".
        season (str): The season year (e.g., "2024").

    Returns:
        dict: A dictionary containing the game date and scores.
    """
    url = f"https://www.thesportsdb.com/api/v1/json/3/searchevents.php"
    params = {"e": event_name, "s": season}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        if not data.get("event"):
            return None  # No event found

        # Extract relevant data from the first event
        event = data["event"][0]
        game_date = event["dateEvent"]
        score_team_a = event.get("intHomeScore")
        score_team_b = event.get("intAwayScore")

        return {
            "game_date": game_date,
            "score_team_a": score_team_a,
            "score_team_b": score_team_b,
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching game data: {e}")
        return None
