"""Tests fonctionnels pour l'affichage des points."""

from unittest.mock import patch

########################################################
#           DISPLAY POINTS PAGE TESTS
########################################################

def test_display_points(test_app):
    """Test that the display points page is rendered"""
    with test_app.test_client() as client:
        # Calling the display points page
        response = client.get("/display_points")

        # Check that the page is rendered
        assert response.status_code == 200
        # Check that the page contains the word "Points"
        assert "Points" in response.data.decode("utf-8")


def test_display_points_with_no_clubs(test_app):
    """Test that the display points page is rendered with no clubs"""
    # Patch the CLUBS variable to an empty list
    with patch('server.CLUBS', []):
        # Calling the display points page
        with test_app.test_client() as client:
            response = client.get("/display_points")
            
            # Check on the error message that is displayed
            assert "No clubs found" in response.data.decode("utf-8")
