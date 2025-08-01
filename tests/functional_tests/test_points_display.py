"""Tests fonctionnels pour l'affichage des points."""

from unittest.mock import patch


def test_display_points(test_app):
    """Test that the display points page is rendered"""
    with test_app.test_client() as client:
        response = client.get("/display_points")
        assert response.status_code == 200
        assert "Points" in response.data.decode("utf-8")


def test_display_points_with_no_clubs(test_app, mock_json_functions):
    """Test that the display points page is rendered with no clubs"""
    with patch('server.CLUBS', []):
        with test_app.test_client() as client:
            response = client.get("/display_points")
            assert "No clubs found" in response.data.decode("utf-8")
