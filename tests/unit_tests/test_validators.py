import pytest
from datetime import datetime, timedelta

from validators import validate_competition_date, validate_places_required


########################################################
#           VALIDATE PLACES REQUIRED TESTS
########################################################


def test_valid_booking():
    """
    Test when the number of places required is valid.
    """
    club = {"points": "10"}
    competition = {"number_of_places": "15"}
    result = validate_places_required(5, club, competition)
    assert result is None

def test_more_places_than_available():
    """
    Test when the number of places required is greater 
    than the number of places available.
    """
    club = {"points": "20"}
    competition = {"number_of_places": "10"}
    result = validate_places_required(15, club, competition)
    assert result == "Not enough places available"

def test_more_places_than_club_points():
    """
    Test when the number of places required is greater 
    than the number of points the club has.
    """
    club = {"points": "5"}
    competition = {"number_of_places": "20"}
    result = validate_places_required(10, club, competition)
    assert result == "The club does not have enough points"

def test_more_than_12_places():
    """
    Test when the number of places required is greater 
    than 12.
    """
    club = {"points": "20"}
    competition = {"number_of_places": "20"}
    result = validate_places_required(13, club, competition)
    assert result == "You cannot book more than 12 places"

def test_exactly_12_places():
    """
    Test when the number of places required is exactly 12.
    """
    club = {"points": "15"}
    competition = {"number_of_places": "15"}
    result = validate_places_required(12, club, competition)
    assert result is None

def test_zero_places():
    """
    Test when the number of places required is 0.
    """
    club = {"points": "10"}
    competition = {"number_of_places": "10"}
    result = validate_places_required(0, club, competition)
    assert result is None

def test_negative_places():
    """
    Test when the number of places required is negative.
    """
    club = {"points": "10"}
    competition = {"number_of_places": "10"}
    result = validate_places_required(-1, club, competition)
    assert result is None


########################################################
#       VALIDATE COMPETITION DATE TESTS
########################################################


def test_future_competition():
    """
    Test when the competition date is in the future.
    """
    future_date = (datetime.now() + timedelta(days=1)).isoformat()
    competition = {"date": future_date}
    result = validate_competition_date(competition)
    assert result is None

def test_past_competition():
    """
    Test when the competition date is in the past.
    """
    past_date = (datetime.now() - timedelta(days=1)).isoformat()
    competition = {"date": past_date}
    result = validate_competition_date(competition)
    assert result == "This competition has already ended"

def test_current_competition():
    """
    Test when the competition date is today.
    """
    current_date = datetime.now().isoformat()
    competition = {"date": current_date}
    result = validate_competition_date(competition)
    assert result == "This competition has already ended"
