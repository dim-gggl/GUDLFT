from conftests import client
from models import Club, Competition, CompetitionPlace

from server import data_manager

# def test_club_points_not_updated_after_purchase(client):
#     club = {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
#     competition = {"name": "Spring Festival", "date": "2025-03-27 10:00:00", "numberOfPlaces": "25"}
#     response = client.post("/purchasePlaces", data={"name": club["name"], "competition": competition["name"], "places": "1"})
#     assert club["points"] == "13"
#     assert competition["numberOfPlaces"] == "25"


def test_club_points_updated_after_purchase(client):
    initial_clubs = data_manager.load_clubs()
    initial_club = next(club for club in initial_clubs if club.name == "Simply Lift")

    initial_competitions = data_manager.load_competitions()
    initial_competition = next(comp for comp in initial_competitions if comp.name == "Spring Festival")

    initial_points = initial_club.points
    initial_number_of_places = initial_competition.numberOfPlaces
    
    response = client.post(
        "/purchasePlaces",
        data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "1"
        }
    )
    updated_clubs = data_manager.load_clubs()
    updated_competitions = data_manager.load_competitions()
    updated_club = next(
        club for club in updated_clubs if club.name == "Simply Lift"
    )
    updated_competition = next(
        comp for comp in updated_competitions if comp.name == "Spring Festival"
    )
    
    assert updated_club.points == initial_points - 1
    assert updated_competition.numberOfPlaces == initial_number_of_places - 1

    data_manager.save_clubs(initial_clubs)
    data_manager.save_competitions(initial_competitions)


