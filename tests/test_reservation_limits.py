import pytest
from unittest.mock import patch

from server import app
from config import Config
from validators import validate_places_required


clubs_data = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": 13},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": 4},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": 12}
]
competitions_data = [
    {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": 25},
    {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": 13}
]

class MockDataManager:
    """Manages mock data for tests"""
    
    def __init__(self):
        self.stored_clubs = [club for club in clubs_data]
        self.stored_competitions = [comp for comp in competitions_data]
    
    def load_json(self, file_path, key):
        """Mock load_json function"""
        if key == "clubs":
            return [club for club in self.stored_clubs]
        if key == "competitions":
            return [comp for comp in self.stored_competitions]
        return []
    
    def save_json(self, file_path, data, key):
        """Mock save_json function"""
        if key == "clubs":
            self.stored_clubs.clear()
            self.stored_clubs.extend([item for item in data])
        elif key == "competitions":
            self.stored_competitions.clear()
            self.stored_competitions.extend([item for item in data])
    
    def get_club_by_name(self, name):
        """Get a club by name from stored data"""
        return next(
            club for club in self.stored_clubs if club["name"] == name
        )
    
    def get_competition_by_name(self, name):
        """Get a competition by name from stored data"""
        return next(
            comp for comp in self.stored_competitions if comp["name"] == name
        )
    
    def reset_data(self):
        """Reset data to initial state"""
        self.stored_clubs = [club for club in clubs_data]
        self.stored_competitions = [comp for comp in competitions_data]


@pytest.fixture
def test_app():
    """Flask test app fixture"""
    app.config.from_object(Config)
    yield app


@pytest.fixture
def mock_data_manager():
    """Mock data manager fixture"""
    return MockDataManager()


@pytest.fixture
def mock_json_functions(mock_data_manager):
    """Mock JSON functions fixture"""
    with patch('server.load_json', side_effect=mock_data_manager.load_json), \
         patch('server.save_json', side_effect=mock_data_manager.save_json):
        yield mock_data_manager


def test_clubs_cannot_book_more_than_places_available(test_app):
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
    initial_club = mock_json_functions.get_club_by_name("Simply Lift")
    initial_competition = mock_json_functions.get_competition_by_name(
        "Spring Festival"
    )
    
    initial_points = initial_club["points"]
    initial_places = initial_competition["numberOfPlaces"]
    
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
    
    updated_club = mock_json_functions.get_club_by_name("Simply Lift")
    updated_competition = mock_json_functions.get_competition_by_name(
        "Spring Festival"
    )
    
    assert updated_club is not None, (
        "Club 'Simply Lift' not found after purchase"
    )
    assert updated_competition is not None, (
        "Competition 'Spring Festival' not found after purchase"
    )
    assert int(updated_club["points"]) == int(initial_points) - 1
    assert int(
        updated_competition["numberOfPlaces"]
    ) == int(initial_places) - 1


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
