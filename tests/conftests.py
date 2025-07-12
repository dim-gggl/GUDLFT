import pytest

from server import create_app

@pytest.fixture
def client():
    app = create_app(conf="test")
    with app.test_client() as client:
        yield client



