import json

from models import Club, Competition
from config import CLUBS_FILE, COMPETITIONS_FILE


def load_data_from_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_data_to_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, ensure_ascii=True, indent=4)

class DataManager:

    def load_clubs(self):
        return [Club(**data) for data in load_data_from_json(CLUBS_FILE)["clubs"]]
    
    def load_club_by_email(self, email):
        return [club for club in self.load_clubs() if club.email == email][0]

    def get_club_by_name(self, name):
        return [club for club in self.load_clubs() if club.name == name][0]

    def load_competitions(self):
        return [Competition(**data) for data in load_data_from_json(COMPETITIONS_FILE)["competitions"]] 

    def get_competition_by_name(self, name):
        return [competition for competition in self.load_competitions() if competition.name == name][0]

    def save_clubs(self, clubs):
        save_data_to_json(
            CLUBS_FILE, 
            {"clubs": [club.to_dict() for club in clubs]}
        )

    def save_competitions(self, competitions):
        save_data_to_json(
            COMPETITIONS_FILE, 
            {"competitions": [competition.to_dict() for competition in competitions]}
        )