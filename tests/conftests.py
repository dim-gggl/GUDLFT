import pytest
import sys
import os

# Ajouter le répertoire parent au path Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

@pytest.fixture
def club():
    club = Club(name="Test Club", email="test@test.com", points=10)
    return club

@pytest.fixture
def competition():
    competition = Competition(name="Test Competition", date="2025-01-01", number_of_places=10)
    return competition

