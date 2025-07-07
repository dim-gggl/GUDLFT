from conftests import client


def test_club_points_not_updated_after_purchase(client):
    club = {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
    competition = {"name": "Spring Festival", "date": "2025-03-27 10:00:00", "numberOfPlaces": "25"}
    response = client.post("/purchasePlaces", data={"name": "Simply Lift", "competition": "Spring Festival", "places": "1"})
    assert club["points"] == "13"
    assert competition["numberOfPlaces"] == "25"