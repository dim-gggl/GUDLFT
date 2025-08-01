import pytest
from unittest.mock import patch, mock_open, MagicMock
import json
from copy import deepcopy
from flask import Flask

import data_manager
from data_manager import (
    load_data,
    save_json,
    get_obj_by_field,
    update_clubs_and_competitions,
    save_clubs_and_competitions,
    update_data_after_booking
)


########################################################
#               LOAD DATA TESTS
########################################################


def test_load_clubs_data():
    """
    Test when the clubs data is loaded from the file.
    """
    mock_data = {"clubs": [{"name": "Test Club", "email": "test@test.com"}]}
    
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = load_data("clubs.json", "clubs")
        assert result == mock_data["clubs"]

def test_load_competitions_data():
    """
    Test when the competitions data is loaded from the file.
    """
    mock_data = {
        "competitions": [
            {"name": "Test Comp", "date": "2024-01-01"}
        ]
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = load_data("competitions.json", "competitions")
        assert result == mock_data["competitions"]

def test_file_not_found():
    """
    Test when the file is not found.
    """
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            load_data("nonexistent.json", "clubs")


########################################################
#               SAVE JSON TESTS
########################################################


def test_save_clubs_data():
    """
    Test when the clubs data is saved to the file.
    """
    mock_data = [{"name": "Test Club", "email": "test@test.com"}]
    mock_file = mock_open()
    with patch("builtins.open", mock_file), \
        patch("json.dump") as mock_dump:
        save_json("clubs.json", mock_data, "clubs")

        mock_file.assert_called_once_with("clubs.json", "w")
        handle = mock_file()
        expected_data = {"clubs": mock_data}
        mock_dump.assert_called_once_with(
            expected_data, handle, ensure_ascii=True, indent=4
        )


def test_save_competitions_data():
    """
    Test when the competitions data is saved to the file.
    """
    mock_data = [{"name": "Test Comp", "date": "2024-01-01"}]
    mock_file = mock_open()
    with patch("builtins.open", mock_file), patch("json.dump") as mock_dump:
        save_json("competitions.json", mock_data, "competitions")

        mock_file.assert_called_once_with("competitions.json", "w")
        handle = mock_file()
        expected_data = {"competitions": mock_data}
        mock_dump.assert_called_once_with(
            expected_data, handle, ensure_ascii=True, indent=4
        )


########################################################
#           GET OBJECT BY FIELD TESTS
########################################################


def test_find_club_by_email():
    """
    Test when the club is found by email.
    """
    clubs = [{"name": "Test Club", "email": "test@test.com"}]
    result = get_obj_by_field("email", "test@test.com", clubs)
    assert result == clubs[0]

def test_find_club_by_unknown_email():
    """
    Test when the club is not found by email.
    """
    clubs = [{"name": "Test Club", "email": "test@test.com"},
             {"name": "Test Club 2", "email": "test2@test.com"}]
    result = get_obj_by_field("email", "test@test.com", clubs)
    assert result == {"name": "Test Club", "email": "test@test.com"}

def test_object_not_found():
    """
    Test when the object is not found.
    """
    clubs = [{"name": "Club A", "email": "a@test.com"}]
    with pytest.raises(IndexError):
        get_obj_by_field("name", "Unknown Club", clubs)


########################################################
#       UPDATE CLUBS AND COMPETITIONS TESTS
########################################################


def test_update_existing_club_and_competition():
    """
    Test when the club and competition are updated.
    """
    original_clubs = [{"name": "Club A", "points": "10"}]
    original_competitions = [{"name": "Competition A", "number_of_places": 20}]
    
    # Patch the global variables in the data_manager module
    with patch.object(data_manager, 'CLUBS', original_clubs), \
         patch.object(data_manager, 'COMPETITIONS', original_competitions):
        
        updated_club = {"name": "Club A", "points": 5}
        updated_competition = {"name": "Competition A", "number_of_places": 15}

        update_clubs_and_competitions(updated_club, updated_competition)
        
        # Since we're patching the global variables, they should be updated
        assert len(data_manager.CLUBS) == 1
        assert len(data_manager.COMPETITIONS) == 1
        assert data_manager.CLUBS[0]["points"] == 5
        assert data_manager.COMPETITIONS[0]["number_of_places"] == 15


def test_update_new_objects():
    """
    Test when new objects are added.
    """
    original_clubs = []
    original_competitions = []
    
    with patch.object(data_manager, 'CLUBS', original_clubs), \
         patch.object(data_manager, 'COMPETITIONS', original_competitions):
        
        updated_club = {"name": "New Club", "points": 10}
        updated_competition = {
            "name": "New Competition", 
            "number_of_places": 20
        }

        update_clubs_and_competitions(updated_club, updated_competition)

        assert len(data_manager.CLUBS) == 1
        assert len(data_manager.COMPETITIONS) == 1
        assert data_manager.CLUBS[0]["name"] == "New Club"
        assert data_manager.COMPETITIONS[0]["name"] == "New Competition"

########################################################
# SAVE CLUBS AND COMPETITIONS TESTS
########################################################

def test_save_clubs_and_competitions():
    """
    Test when the clubs and competitions are saved to the files.
    """
    mock_app = MagicMock()
    mock_app.config = {
        "JSON_CLUBS": "clubs.json",
        "JSON_COMPETITIONS": "competitions.json"
    }
    
    clubs = [{"name": "Club A"}]
    competitions = [{"name": "Comp A"}]
    
    with patch('data_manager.save_json') as mock_save:
        save_clubs_and_competitions(mock_app, clubs, competitions)
        
        assert mock_save.call_count == 2
        mock_save.assert_any_call("clubs.json", clubs, "clubs")
        mock_save.assert_any_call(
            "competitions.json", competitions, "competitions"
        )


########################################################
#           UPDATE DATA AFTER BOOKING TESTS
########################################################


@pytest.fixture
def app_context():
    """Create an application context for tests that need it"""
    from server import app
    with app.app_context():
        yield app

def test_successful_booking(app_context):
    """
    Test when the booking is successful.
    """
    competition = {
        "name": "Test Comp", 
        "number_of_places": "10", 
        "date": "2025-01-01 10:00:00"
    }
    club = {"name": "Test Club", "points": "15"}
    
    with patch('data_manager.validate_places_required', return_value=None), \
         patch('data_manager.validate_competition_date', return_value=None), \
         patch('data_manager.update_clubs_and_competitions') as mock_update, \
         patch('data_manager.save_clubs_and_competitions') as mock_save:
        
        result = update_data_after_booking(competition, club, 5)
        
        assert result is None
        assert competition["number_of_places"] == 5
        assert club["points"] == 10
        mock_update.assert_called_once_with(club, competition)
        mock_save.assert_called_once()

def test_booking_with_validation_error():
    """
    Test when the booking is not successful.
    """
    competition = {
        "name": "Test Comp", 
        "number_of_places": "10", 
        "date": "2025-01-01 10:00:00"
    }
    club = {"name": "Test Club", "points": "15"}
    
    with patch(
        'data_manager.validate_places_required', 
        return_value="Not enough places"), \
         patch(
        'data_manager.validate_competition_date', 
        return_value=None):
        
        result = update_data_after_booking(competition, club, 15)
        
        assert result == "Not enough places"
        assert competition["number_of_places"] == "10"
        assert club["points"] == "15"