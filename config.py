import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    """
    Configuration for the application, including JSON file paths 
    for clubs and competitions.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'something_special')
    JSON_CLUBS = BASE_DIR / os.environ.get('JSON_CLUBS', 'clubs.json')
    JSON_COMPETITIONS = BASE_DIR / os.environ.get(
        'JSON_COMPETITIONS', 
        'competitions.json'
    )
    DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
    RUN_PORT = os.environ.get('FLASK_RUN_PORT', '5000')
    TESTING = False

config = {"default": Config}