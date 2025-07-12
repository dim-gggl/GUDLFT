import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'something_special')
    JSON_CLUBS = BASE_DIR / os.environ.get('JSON_CLUBS', 'clubs.json')
    JSON_COMPETITIONS = BASE_DIR / os.environ.get('JSON_COMPETITIONS', 'competitions.json')
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
    RUN_PORT = os.environ.get('FLASK_RUN_PORT', '5000')
    TESTING = False

class TestConfig(Config):
    TESTING = True
    JSON_CLUBS = BASE_DIR / "tests" / "clubs.json"
    JSON_COMPETITIONS = BASE_DIR / "tests" / "competitions.json"

config = {
    'default': Config,
    "test": TestConfig
}