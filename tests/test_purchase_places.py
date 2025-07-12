import pytest
from server import load_json, save_clubs_and_competitions, app
from config import config

@pytest.fixture
def test_app():
    app.config.from_object(config['test'])
    yield app

def test_club_points_updated_after_purchase(test_app):
    initial_clubs = load_json(test_app.config["JSON_CLUBS"], "clubs")
    initial_club = next(club for club in initial_clubs if club["name"] == "Simply Lift")

    initial_competitions = load_json(test_app.config["JSON_COMPETITIONS"], "competitions")
    initial_competition = next(comp for comp in initial_competitions if comp["name"] == "Spring Festival")

    initial_points = initial_club["points"]
    initial_number_of_places = initial_competition["numberOfPlaces"]
    
    with test_app.test_client() as client:
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Simply Lift",
                "competition": "Spring Festival",
                "places": "1"
            }
        )
        assert response.status_code == 200
    
    updated_clubs = load_json(test_app.config["JSON_CLUBS"], "clubs")
    updated_competitions = load_json(test_app.config["JSON_COMPETITIONS"], "competitions")
    
    updated_club = next(
        club for club in updated_clubs if club["name"] == "Simply Lift"
    )
    updated_competition = next(
        comp for comp in updated_competitions if comp["name"] == "Spring Festival"
    )
    
    assert int(updated_club["points"]) == int(initial_points) - 1
    assert int(updated_competition["numberOfPlaces"]) == int(initial_number_of_places) - 1
    save_clubs_and_competitions(test_app, updated_clubs, updated_competitions)

