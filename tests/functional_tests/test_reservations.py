"""Tests fonctionnels pour les réservations de places."""

from datetime import datetime

########################################################
# BOOKING TESTS
########################################################

def test_clubs_cannot_book_more_than_places_available(test_app):
    """
    Test that clubs cannot book more places than available
    """
    
    with test_app.test_client() as client:
        response = client.post(
            "/purchase_places",
            data={
                "club": "Simply Lift", 
                "competition": "Spring Festival", 
                "places": "26"
            }
        )
        
        assert response.status_code == 200
        assert "Not enough places available" in response.data.decode("utf-8")


def test_club_points_updated_after_purchase(test_app, mock_json_functions):
    """
    Test that club points are correctly updated after a purchase
    """
    initial_points = mock_json_functions.get_club_by_name(
        "Simply Lift"
    )["points"]

    initial_places = mock_json_functions.get_competition_by_name(
        "Spring Festival"
    )["number_of_places"]
    
    with test_app.test_client() as client:
        client.post(
            "/purchase_places",
            data={
                "club": "Simply Lift",
                "competition": "Spring Festival",
                "places": "1"
            }
        )
    
    updated_club = mock_json_functions.get_club_by_name("Simply Lift")
    updated_competition = mock_json_functions.get_competition_by_name(
        "Spring Festival"
    )

    assert int(updated_club["points"]) == int(initial_points) - 1
    assert int(updated_competition["number_of_places"]) == int(initial_places) - 1


def test_clubs_cannot_book_past_competitions(test_app, 
                                            mock_json_functions):
    """Test that clubs cannot book past competitions"""

    with test_app.test_client() as client:
        response = client.post(
            "/purchase_places",
            data={
                "club": "Simply Lift",
                "competition": "Fall Classics",
                "places": "1"
            }
        )

        competition = mock_json_functions.get_competition_by_name("Fall Classics")
        assert competition["date"] < datetime.now().isoformat()
        assert "This competition has already ended" in response.data.decode("utf-8")

