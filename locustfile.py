from locust import HttpUser, task, between
import random

class TimelineUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def get_timeline(self):
        user_id = random.randint(1, 1000)
        self.client.get(
            f"/api/timeline?user=user{user_id}&limit=20",
            name="/api/timeline"
        )
