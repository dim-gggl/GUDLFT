import json
from flask import current_app, Flask

from validators import validate_places_required, validate_competition_date

########################################################
# DATA & SERVICES FUNCTIONS
########################################################


def load_data(file_path: str, key: str):
    """Load JSON data from a club or competition file"""
    with open(file_path) as f:
        return json.load(f)[key]

CLUBS = load_data("clubs.json", "clubs")
COMPETITIONS = load_data("competitions.json", "competitions")


def save_json(file_path: str, data: list, key: str):
    """Save JSON data to a club or competition file"""
    with open(file_path, "w") as f:
        json.dump({key: data}, f, ensure_ascii=True, indent=4)


def update_clubs_and_competitions(club: dict, competition: dict):
    """Update clubs and competitions lists after booking"""
    clubs = [c for c in CLUBS if c["name"] != club["name"]]
    clubs.append(club)
    competitions = [
        comp for comp in COMPETITIONS if comp["name"] != competition["name"]
    ]
    competitions.append(competition)


def save_clubs_and_competitions(app_instance: Flask, 
                                clubs: list, 
                                competitions: list):
    """Save clubs and competitions to their respective files"""
    save_json(app_instance.config["JSON_CLUBS"], clubs, "clubs")
    save_json(
        app_instance.config["JSON_COMPETITIONS"], 
        competitions, 
        "competitions"
    )


def get_obj_by_field(key, value, list_of_dicts):
    return [item for item in list_of_dicts if item[key] == value][0]


def update_data_after_booking(competition: dict, 
                            club: dict, 
                            places_required: int) -> str | None:
    """
    Handles the logic for updating in-memory and file information
    after a booking.
    Returns an error message if the booking is not possible.
    """
    competition["number_of_places"] = int(competition["number_of_places"]) \
        - places_required
    club["points"] = int(club["points"]) - places_required
    # If, for any reason, the booking is not possible,
    # we get the error message and return it to the view.
    reservation_error = validate_places_required(
        places_required, club, competition
    )
    date_error = validate_competition_date(competition)
    if reservation_error or date_error:
        return reservation_error or date_error
    # If the booking is possible, we update the in-memory data
    # and save it to the files.
    update_clubs_and_competitions(club, competition)
    save_clubs_and_competitions(current_app, CLUBS, COMPETITIONS)
    return None