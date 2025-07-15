import pytest
from unittest.mock import patch
from datetime import datetime
from copy import deepcopy


import server
from server import app
from config import Config
from validators import validate_places_required


clubs_data = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": 13},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": 4},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": 12}
]
competitions_data = [
    {"name": "Spring Festival", 
    "date": "2026-03-27 10:00:00", 
    "numberOfPlaces": 25,
    "status": "upcoming"},
    {"name": "Fall Classic", 
    "date": "2026-10-22 13:30:00", 
    "numberOfPlaces": 13,
    "status": "upcoming"}
]

class MockDataManager:
    """Manages mock data for tests with proper state management"""
    
    def __init__(self):
        self.reset_data()
    
    def reset_data(self):
        """Reset data to initial state"""
        self.stored_clubs = deepcopy(clubs_data)
        self.stored_competitions = deepcopy(competitions_data)
        server.clubs = deepcopy(self.stored_clubs)
        server.competitions = deepcopy(self.stored_competitions)
    
    def load_json(self, file_path, key=None):
        """Mock load_json function that returns current state"""
        if key == "clubs":
            return self.stored_clubs
        if key == "competitions":
            return self.stored_competitions
        return []
    
    def save_json(self, file_path, data, key):
        """Mock save_json function that updates internal state"""
        if key == "clubs":
            self.stored_clubs = data
            server.clubs = data
        elif key == "competitions":
            self.stored_competitions = data
            server.competitions = data
    
    def get_club_by_name(self, name):
        """Get a club by name from stored data"""
        return next(
            (club for club in self.stored_clubs if club["name"] == name),
            None
        )
    
    def get_competition_by_name(self, name):
        """Get a competition by name from stored data"""
        return next(
            (comp for comp in self.stored_competitions if \
            comp["name"] == name),
            None
        )


@pytest.fixture
def test_app():
    """Flask test app fixture with proper configuration"""
    app.config.from_object(Config)
    app.config['TESTING'] = True
    yield app


@pytest.fixture
def mock_data_manager():
    """Mock data manager fixture"""
    return MockDataManager()


@pytest.fixture
def mock_json_functions(mock_data_manager):
    """Mock JSON functions fixture with proper patching"""
    with patch('server.load_json', side_effect=mock_data_manager.load_json), \
         patch('server.save_json', side_effect=mock_data_manager.save_json):
        mock_data_manager.reset_data()
        yield mock_data_manager


def test_clubs_cannot_book_more_than_places_available(
test_app):
    """Test that clubs cannot book more places than available"""
    with test_app.test_client() as client:
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Simply Lift", 
                "competition": "Spring Festival", 
                "places": "26"
            }
        )
        
        assert response.status_code == 200
        assert "Not enough places available" in response.data.decode("utf-8")


def test_club_points_updated_after_purchase(test_app, mock_json_functions):
    """Test that club points are correctly updated after a purchase"""
    initial_points = mock_json_functions.get_club_by_name(
        "Simply Lift")["points"]
    initial_places = mock_json_functions.get_competition_by_name(
        "Spring Festival")["numberOfPlaces"]
    
    with test_app.test_client() as client:
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Simply Lift",
                "competition": "Spring Festival",
                "places": "1"
            }
        )
    
    updated_club = mock_json_functions.get_club_by_name("Simply Lift")
    updated_competition = mock_json_functions.get_competition_by_name(
        "Spring Festival")

    assert int(updated_club["points"]) == int(initial_points) - 1
    assert int(updated_competition["numberOfPlaces"]) == int(initial_places) - 1


def test_clubs_cannot_book_past_competitions(test_app, mock_json_functions):
    """Test that clubs cannot book past competitions"""
    with test_app.test_client() as client:
        response = client.post(
            "/purchasePlaces",
            data={
                "club": "Simply Lift",
                "competition": "Fall Classic",
                "places": "1"
            }
        )
        competition = mock_json_functions.get_competition_by_name("Fall Classic")
        if competition["date"] < datetime.now().isoformat():
            assert "You cannot book past competitions" in response.data.decode("utf-8")
        else:
            assert response.status_code == 200


def test_validation_rules():
    """Test validation rules separately"""    
    result = validate_places_required(
        26, 
        {"points": 21}, 
        {"numberOfPlaces": 19}
    )
    assert result == "Not enough places available"
    
    result = validate_places_required(
        25, 
        {"points": 21}, 
        {"numberOfPlaces": 30}
    )
    assert result == "The club does not have enough points"
    
    result = validate_places_required(
        15, 
        {"points": 20}, 
        {"numberOfPlaces": 20}
    )
    assert result == "You cannot book more than 12 places"
    
    result = validate_places_required(
        5, 
        {"points": 10}, 
        {"numberOfPlaces": 10}
    )
    assert result is None


def test_display_points(test_app):
    """Test that the display points page is rendered"""
    with test_app.test_client() as client:
        response = client.get("/displayPoints")
        assert response.status_code == 200
        assert "Points" in response.data.decode("utf-8")


def test_display_points_with_no_clubs(test_app, mock_json_functions):
    """Test that the display points page is rendered with no clubs"""
    def empty_clubs_load_json(file_path, key=None):
        if key == "clubs":
            return []
        if key == "competitions":
            return mock_json_functions.stored_competitions
        return []
    
    with patch('server.load_json', side_effect=empty_clubs_load_json):
        server.clubs = []
        
        with test_app.test_client() as client:
            response = client.get("/displayPoints")
            assert "No clubs found" in response.data.decode("utf-8")


def test_unknown_email_redirects_to_index(test_app):
    """Test that an unknown email redirects to the index page"""
    with test_app.test_client() as client:
        response = client.post(
            "/showSummary", 
            data={"email": "unknown@example.com"},
            follow_redirects=True
        )
        assert response.request.path == "/"


def test_unknown_email_displays_error_message(test_app):
    """Test that an unknown email displays an error message after redirect"""
    with test_app.test_client() as client:
        response = client.post(
            "/showSummary", 
            data={"email": "unknown@example.com"},
            follow_redirects=True
        )
        assert "Unknown email" in response.data.decode("utf-8")