import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    """
    Configuration for the application, including JSON file paths 
    for clubs and competitions.
    """
    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY', 'something_special')
        self.DEBUG = os.environ.get('FLASK_DEBUG', '1') == '1'
        self.RUN_PORT = os.environ.get('FLASK_RUN_PORT', '5000')
        self.TESTING = False
        self.JSON_CLUBS = "clubs.json"
        self.JSON_COMPETITIONS = "competitions.json"

config = {"default": Config()}
