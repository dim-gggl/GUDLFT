class Club:

    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = points

    def add_points(self, points):
        self.points += points

    def remove_points(self, points):
        self.points -= points

    def __str__(self):
        return f"Club: {self.name}, Email: {self.email}, Points: {self.points}"

class Competition:

    def __init__(self, name, date, numberOfPlaces):
        self.name = name
        self.date = date
        self.numberOfPlaces = numberOfPlaces

    def add_number_of_places(self, places):
        self.numberOfPlaces += places

    def remove_number_of_places(self, places):
        self.numberOfPlaces -= places

def __str__(self):
        return f"Competition: {self.name}, Date: {self.date}, Number of Places: {self.numberOfPlaces}"