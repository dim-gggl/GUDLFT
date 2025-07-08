class Competition:

    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.date = kwargs["date"]
        self.numberOfPlaces = int(kwargs["numberOfPlaces"])

    def add_number_of_places(self, places: int) -> None:
        self.numberOfPlaces += places

    def remove_number_of_places(self, places: int) -> None:
        self.numberOfPlaces -= places

    def to_dict(self):
        return {
            "name": self.name, 
            "date": self.date, 
            "numberOfPlaces": self.numberOfPlaces
        }

    def __str__(self):
        return f"Competition: {self.name}, Date: {self.date}, Number of Places: {self.numberOfPlaces}"


class CompetitionPlace:

    def __init__(self, **kwargs):
        self.competition = kwargs["competition"]


class Club:

    def __init__(self, **kwargs):
        self.name = kwargs["name"]
        self.email = kwargs["email"]
        self.points = int(kwargs["points"])
        self.competition_places = []

    def add_points(self, points: int) -> None:
        self.points += points

    def remove_points(self, points: int) -> None:
        self.points -= points

    def add_competition_place(self, competition_place: CompetitionPlace) -> None:
        self.competition_places.append(competition_place)

    def remove_competition_place(self, competition_place: CompetitionPlace) -> None:
        self.competition_places.remove(competition_place)

    def to_dict(self):
        return {
            "name": self.name, 
            "email": self.email, 
            "points": self.points
        }

    def __str__(self):
        return (
            f"Club: {self.name}, Email: {self.email}, "
            f"Points: {self.points}"
        )


