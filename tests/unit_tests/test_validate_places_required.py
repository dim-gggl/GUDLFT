from validators import validate_places_required


competition = {
    "numberOfPlaces": 10,
}

competition_with_more_places = {
    "numberOfPlaces": 15,
}

club_with_few_places = {
    "points": 5,
}

club = {
    "points": 17,
}


def test_valid_places_required():

    assert validate_places_required(
        1, 
        club, 
        competition
    ) is None


def test_validation_with_more_than_12_places():

    assert validate_places_required(
        13, 
        club, 
        competition_with_more_places
    ) == "You cannot book more than 12 places"


def test_validation_with_not_enough_places():

    assert validate_places_required(
        11, 
        club, 
        competition
    ) == "Not enough places available"


def test_validation_with_not_enough_points():

    assert validate_places_required(
        6, 
        club_with_few_places, 
        competition
    ) == "The club does not have enough points"