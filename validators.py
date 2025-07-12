def validate_places_required(places_required, club, competition):
    """
    Check if the number of places required is valid based on 
    logical and specific rules.
    Returns a message if the number of places required is not valid, 
    otherwise returns None.
    """
    places_required = int(places_required)
    rules = [
        (places_required > int(competition["numberOfPlaces"]), \
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
