import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from server import create_app, app

########################################################
# MOCK JSON FUNCTIONS
########################################################

@pytest.fixture
def test_app():
    """Fixture for the Flask test app"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture
def mock_json_functions():
    """Fixture to mock the JSON functions"""
    clubs_data = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": 13},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": 4}
    ]
    competitions_data = [
        {"name": "Spring Festival", "date": "2026-03-27 10:00:00", "number_of_places": 25}
    ]
    
    with patch('server.CLUBS', clubs_data), \
         patch('server.COMPETITIONS', competitions_data):
        yield

########################################################
# CREATE APP TESTS
########################################################

class TestCreateApp:
    """Unit tests for the create_app function"""
    
    def test_create_app_returns_flask_app(self):
        """Test that create_app returns a Flask app"""
        test_app = create_app()
        assert isinstance(test_app, Flask)
    
    def test_create_app_has_secret_key(self):
        """Test that the created app has a secret key"""
        test_app = create_app()
        assert test_app.secret_key is not None
    
    def test_create_app_config_loaded(self):
        """Test that the configuration is loaded"""
        test_app = create_app()
        assert test_app.config is not None
    
########################################################
# INDEX ROUTE TESTS
########################################################

class TestIndexRoute:
    """Unit tests for the index route"""
    
    def test_index_route_returns_200(self, test_app):
        """Test that the index route returns 200"""
        with test_app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200
    
    def test_index_route_contains_welcome_message(self, test_app):
        """Test that the index route contains the welcome message"""
        with test_app.test_client() as client:
            response = client.get('/')
            assert b"Welcome to the GUDLFT Registration Portal" in response.data

########################################################
# SUMMARY ROUTE TESTS
########################################################

class TestSummaryRoute:
    """Unit tests for the summary route"""
    
    def test_show_summary_with_valid_email(self, test_app, mock_json_functions):
        """Test that show_summary returns 200 with a valid email"""
        with test_app.test_client() as client:
            response = client.post('/show_summary', data={'email': 'john@simplylift.co'})
            assert response.status_code == 200
            assert b"Welcome" in response.data
    
    def test_show_summary_with_invalid_email(self, test_app, mock_json_functions):
        """Test that show_summary returns 500 with an invalid email"""
        with test_app.test_client() as client:
            response = client.post('/show_summary', data={'email': 'invalid@email.com'})
            assert response.status_code == 500
    
    def test_show_summary_missing_email(self, test_app):
        """Test that show_summary returns 400 without an email"""
        with test_app.test_client() as client:
            response = client.post('/show_summary', data={})
            assert response.status_code == 400

########################################################
# BOOK ROUTE TESTS
########################################################

class TestBookRoute:
    """Unit tests for the book route"""
    
    def test_book_with_valid_competition_and_club(self, test_app, mock_json_functions):
        """Test that book returns 200 with a valid competition and club"""
        with test_app.test_client() as client:
            response = client.get('/book/Spring Festival/Simply Lift')
            assert response.status_code == 200
            assert b"Spring Festival" in response.data
    
    def test_book_with_invalid_competition(self, test_app, mock_json_functions):
        """Test that book returns 500 with an invalid competition"""
        with test_app.test_client() as client:
            response = client.get('/book/Invalid Competition/Simply Lift')
            assert response.status_code == 500
    
    def test_book_with_invalid_club(self, test_app, mock_json_functions):
        """Test that book returns 500 with an invalid club"""
        with test_app.test_client() as client:
            response = client.get('/book/Spring Festival/Invalid Club')
            assert response.status_code == 500

########################################################
# PURCHASE PLACES ROUTE TESTS
########################################################

class TestPurchasePlacesRoute:
    """Unit tests for the purchase_places route"""
    
    def test_purchase_places_success(self, test_app, mock_json_functions):
        """Test that purchase_places returns 200 with success"""
        with patch('server.update_data_after_booking', return_value=None):
            with test_app.test_client() as client:
                response = client.post('/purchase_places', data={
                    'club': 'Simply Lift',
                    'competition': 'Spring Festival',
                    'places': '1'
                })
                assert response.status_code == 200
                assert b"Great-booking complete" in response.data
    
    def test_purchase_places_with_error(self, test_app, mock_json_functions):
        """Test that purchase_places returns 200 with an error"""
        with patch('server.update_data_after_booking', 
        return_value="Error message"):
            with test_app.test_client() as client:
                response = client.post('/purchase_places', data={
                    'club': 'Simply Lift',
                    'competition': 'Spring Festival',
                    'places': '1'
                })
                assert response.status_code == 200
                assert b"Error message" in response.data
    
    def test_purchase_places_missing_data(self, test_app):
        """Test that purchase_places returns 400 with missing data"""
        with test_app.test_client() as client:
            response = client.post('/purchase_places', data={})
            assert response.status_code == 400

########################################################
# DISPLAY POINTS ROUTE TESTS
########################################################

class TestDisplayPointsRoute:
    """Unit tests for the display_points route"""
    
    def test_display_points_with_clubs(self, test_app, mock_json_functions):
        """Test that display_points returns 200 with clubs"""
        with test_app.test_client() as client:
            response = client.get('/display_points')
            assert response.status_code == 200
            assert b"Points" in response.data
    
    def test_display_points_without_clubs(self, test_app):
        """Test that display_points returns 200 without clubs"""
        with patch('server.CLUBS', []):
            with test_app.test_client() as client:
                response = client.get('/display_points')
                assert response.status_code == 200
                assert b"No clubs found" in response.data

########################################################
# LOGOUT ROUTE TESTS
########################################################

def test_logout_redirects_to_index(self, test_app):
    """Test that logout redirects to index"""
    with test_app.test_client() as client:
        response = client.get('/logout')
        assert response.status_code == 302  
        assert response.location.endswith('/')