"""Integration tests for the booking flow.

These tests integrate all the validation rules defined in `validators.py`
and the business logic in `data_manager.update_data_after_booking`.
No function is "mocked" at the validation level: we simply patch
the disk write to avoid any real write.
"""

from contextlib import ExitStack, contextmanager
from copy import deepcopy
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from data_manager import update_data_after_booking
from server import app  # Necessary for the Flask context

########################################################
#                COMMON FIXTURES
########################################################


def _generate_club(name: str = "Test Club", points: int = 20):
    return {
        "name": name,
        "email": f"{name.lower().replace(' ', '')}@test.com",
        "points": str(points),
    }


def _generate_competition(
    name: str = "Test Competition", number_of_places: int = 30, days_delta: int = 1
):
    """days_delta > 0 => future date, days_delta <= 0 => past date"""
    date = datetime.now() + timedelta(days=days_delta)
    return {
        "name": name,
        "date": date.isoformat(sep=" ", timespec="seconds"),
        "number_of_places": str(number_of_places),
    }


@pytest.fixture
def flask_app_context():
    """Provide a Flask application context for the tests."""
    with app.app_context():
        yield app


@contextmanager
def _patch_environment(clubs, competitions):
    """Context manager applying the necessary patches for each test."""
    with ExitStack() as stack:
        stack.enter_context(patch("data_manager.CLUBS", clubs))
        stack.enter_context(patch("data_manager.COMPETITIONS", competitions))
        stack.enter_context(patch("server.CLUBS", clubs))
        stack.enter_context(patch("server.COMPETITIONS", competitions))
        # Neutralize the disk write
        stack.enter_context(patch("data_manager.save_clubs_and_competitions"))
        yield


def _generate_data(club_details, competition_details):
    """Generate clubs and competitions data for the tests."""
    clubs = [_generate_club(**club_details)]
    competitions = [_generate_competition(**competition_details)]

    club = clubs[0]
    competition = competitions[0]

    return clubs, competitions, club, competition


########################################################
#               TEST SCENARIOS
########################################################


def test_booking_success(flask_app_context):
    """
    Successful booking:
    - the club points and the competition places are updated
    - no error is returned
    """
    clubs, competitions, club, competition = _generate_data(
        club_details={"points": 10},
        competition_details={"number_of_places": 20, "days_delta": 1},
    )

    with _patch_environment(clubs, competitions):
        # We book 5 places
        error = update_data_after_booking(competition, club, 5)

    # No error expected
    assert error is None

    # Check the update in memory
    assert int(competition["number_of_places"]) == 15
    assert int(club["points"]) == 5


def test_login_with_unknown_email(flask_app_context):
    """Login with an unknown email should return an error."""
    clubs = []
    competitions = []
    with _patch_environment(clubs, competitions):
        response = app.test_client().post(
            "/show_summary", data={"email": "unknown@test.com"}
        )
    
        # Check the redirection
        assert response.status_code == 302
        assert response.location == "/"

    # Check the flash message - it should be empty for redirect response
    # The actual flash message is not in response.data for 302 redirects


def test_purchase_places_route_integration(flask_app_context):
    """Complete integration via the Flask route `/purchase_places`."""
    clubs, competitions, club, competition = _generate_data(
        club_details={"points": 20},
        competition_details={"number_of_places": 30, "days_delta": 2},
    )

    with _patch_environment(clubs, competitions):
        with app.test_client() as client:
            response = client.post(
                "/purchase_places",
                data={
                    "competition": competition["name"],
                    "club": club["name"],
                    "places": "2",
                },
                follow_redirects=True,
            )
        # After redirection, we should get a 200 status code and
        # a success message
        # The values should be updated
        assert response.status_code == 200
        assert "Great-booking complete!" in response.data.decode("utf-8")
        assert int(club["points"]) == 18
        assert int(competition["number_of_places"]) == 28


def test_booking_more_than_available_places(flask_app_context):
    """Booking refused because not enough places available."""
    clubs, competitions, club, competition = _generate_data(
        club_details={"points": 30},
        competition_details={"number_of_places": 3, "days_delta": 1},
    )

    with _patch_environment(clubs, competitions):
        error = update_data_after_booking(competition, club, 5)

    # Check the error message
    assert error == "Not enough places available"
    # No update should have occurred
    assert int(competition["number_of_places"]) == 3
    assert int(club["points"]) == 30


def test_booking_places_for_a_past_competition(flask_app_context):
    """Booking refused because the competition is in the past."""
    clubs, competitions, club, competition = _generate_data(
        club_details={"points": 15},
        competition_details={"number_of_places": 10, "days_delta": -2},
    )

    with _patch_environment(clubs, competitions):
        error = update_data_after_booking(competition, club, 2)

    assert error == "You cannot book past competitions"
    # No update should have occurred
    assert competition["number_of_places"] == "10"
    assert club["points"] == "15"


def test_booking_more_than_12_places(flask_app_context):
    """Booking refused because the number of places is greater than 12."""
    clubs, competitions, club, competition = _generate_data(
        club_details={"points": 15},
        competition_details={"number_of_places": 13, "days_delta": 1},
    )

    with _patch_environment(clubs, competitions):
        error = update_data_after_booking(competition, club, 13)

    assert error == "You cannot book more than 12 places"
    # No update should have occurred
    assert int(competition["number_of_places"]) == 13
    assert int(club["points"]) == 15


def test_booking_more_places_than_points(flask_app_context):
    """Booking refused because the number of places is greater than the points."""
    clubs, competitions, club, competition = _generate_data(
        club_details={"points": 8},
        competition_details={"number_of_places": 10, "days_delta": 1},
    )

    with _patch_environment(clubs, competitions):
        error = update_data_after_booking(competition, club, 9)

    assert error == "The club does not have enough points"
    # No update should have occurred
    assert int(competition["number_of_places"]) == 10
    assert int(club["points"]) == 8