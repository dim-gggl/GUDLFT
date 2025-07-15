from datetime import datetime


def validate_places_required(places_required, club, competition):
    """
    Check if the number of places required is valid based on 
    logical and specific rules.
    Returns a message if the number of places required is not valid, 
    otherwise returns None.
    """
    places_required = int(places_required)
    rules = [
        (places_required > int(competition["number_of_places"]), \
        "Not enough places available"),
        (places_required > int(club["points"]), \
        "The club does not have enough points"),
        (places_required > 12, \
        "You cannot book more than 12 places"),
    ]
    for condition, message in rules:
        if condition:
            return message
    return None

def validate_competition_date(competition):
    """
    Check if the competition date is in the past.
    Returns a message if the competition date is in the past, 
    otherwise returns None.
    """
    if competition["date"] < datetime.now().isoformat():
        return "You cannot book past competitions"
    return None