from locust import HttpUser, task, constant

class GudLFTUser(HttpUser):
    @task
    def basic_test(self):
        self.client.get("/")
        self.client.get("/display_points")
        self.client.post("/show_summary", data={"email": "admin@irontemple.com"})
