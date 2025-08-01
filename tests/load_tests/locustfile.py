import random
from locust import HttpUser, task, between


class GudLFTUser(HttpUser):
    """User class for the GUDLFT application"""

    wait_time = between(1, 3)

    def on_start(self):
        """Actions to perform when a user starts"""
        # Data to be loaded
        self.test_emails = [
            "john@simplylift.co",
            "admin@irontemple.com",
            "kate@shelifts.co.uk"
        ]
        self.test_clubs = [
            "Simply Lift",
            "Iron Temple",
            "She Lifts"
        ]
        self.test_competitions = [
            "Spring Festival",
            "Fall Classic"
        ]
        
    @task(3)
    def visit_homepage(self):
        self.client.get("/")

    @task(2)
    def visit_display_points(self):
        self.client.get("/display_points")
    
    @task(2)
    def login_with_email(self):
        email = random.choice(self.test_emails)
        self.client.post("/show_summary", data={"email": email})

    @task
    def book_places(self):
        club = random.choice(self.test_clubs)
        competition = random.choice(self.test_competitions)
        self.client.post(f"/book/{competition}/{club}")

    @task(1)
    def make_booking(self):
        club = random.choice(self.test_clubs)
        competition = random.choice(self.test_competitions)
        places = random.randint(1, 12)

        # First the user needs to login
        email = next(email for email in self.test_emails if email.split("@")[0] in club.lower())
        self.client.post("/show_summary", data={"email": email})

        # Then the user can book places
        self.client.post(f"/purchase_places", 
            data={"competition": competition, 
            "club": club, 
            "places": str(places)
        })

    @task(1)
    def logout(self):
        self.client.get("/logout")

class StressTestUser(HttpUser):
    """User class for stress testing"""

    wait_time = between(0.1, 0.5)
    weight = 2

    @task(10)
    def rapid_requests(self):
        self.client.get("/")
        self.client.get("/display_points")
        self.client.get("/logout")

    @task(5)
    def concurrent_bookings(self):
        self.client.post("/show_summary", data={"email": "john@simplylift.co"})
        self.client.post("/purchase_places", data={
            "club": "Simply Lift",
            "competition": "Spring Festival",
            "places": "1"
        })

    
class LoadTestConfig:

    @staticmethod
    def get_test_emails():
        """Returns the tests configurations"""
        return [
            "normal_load": {
                "users": 10,
                "spawn_rate": 2,
                "run_time": "2m"
            },
            "high_load": {
                "users": 50,
                "spawn_rate": 5,
                "run_time": "5m"
            },
            "stress_test": {
                "users": 100,
                "spawn_rate": 10,
                "run_time": "10m"
            }
        ]
