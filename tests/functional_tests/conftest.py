import pytest
import json
from unittest.mock import patch
from copy import deepcopy

from server import app
from config import Config


########################################################
#                   MOCK DATA
########################################################
clubs_data = []
competitions_data = []

with open("clubs.json", "r") as f:
    clubs_data.extend(json.load(f)["clubs"])

with open("competitions.json", "r") as f:
    competitions_data.extend(json.load(f)["competitions"])

# Changed the date to open it to booking
competitions_data[0]["date"] = "2026-03-27 10:00:00"
competitions_data[1]["date"] = "2026-10-22 13:30:00"

# An old version of the competition so 
# we"re still able to test a past one
competitions_data.append(
    {
        "name": "Fall Classics", 
        "date": "2024-10-22 13:30:00",
        "number_of_places": "13"
    }
)

########################################################
#           MOCK DATA MANAGER
########################################################


class MockDataManager:
    """Manages mock data for tests with proper state management"""
    
    def __init__(self):
        self.reset_data()
    
    def reset_data(self):
        """Reset data to initial state"""
        # Creating independent copies of the initial loaded data
        # (So we don"t modify the original data throughout the tests)
        self.stored_clubs = deepcopy(clubs_data)
        self.stored_competitions = deepcopy(competitions_data)
    
    def load_data(self, file_path, key=None):
        """Mock load_data function that returns current state"""
        if key == "clubs":
            return self.stored_clubs
        if key == "competitions":
            return self.stored_competitions
        return []
    
    def save_json(self, file_path, data, key):
        """Mock save_json function that updates internal state"""
        if key == "clubs":
            self.stored_clubs = data
        elif key == "competitions":
            self.stored_competitions = data
    
    def get_club_by_name(self, name):
        """Get a club by name from stored data"""
        return next(
            (club for club in self.stored_clubs if club["name"] == name),
            None
        )
    
    def get_competition_by_name(self, name):
        """Get a competition by name from stored data"""
        return next(
            (c for c in self.stored_competitions if c["name"] == name),
            None
        )


########################################################
#                   FIXTURES
########################################################


@pytest.fixture
def test_app():
    """Flask test app fixture with proper configuration"""
    app.config.from_object(Config)
    app.config["TESTING"] = True
    yield app


@pytest.fixture
def mock_data_manager():
    """Mock data manager fixture"""
    return MockDataManager()


@pytest.fixture
def mock_json_functions(mock_data_manager):
    """Mock JSON functions fixture with proper patching"""
    with patch("data_manager.load_data", 
                side_effect=mock_data_manager.load_data), \
         patch("data_manager.save_json", 
                side_effect=mock_data_manager.save_json), \
         patch("server.CLUBS", 
                mock_data_manager.stored_clubs), \
         patch("server.COMPETITIONS", 
                mock_data_manager.stored_competitions), \
         patch("data_manager.CLUBS", 
                mock_data_manager.stored_clubs), \
         patch("data_manager.COMPETITIONS", 
                mock_data_manager.stored_competitions):
        mock_data_manager.reset_data()
        yield mock_data_manager