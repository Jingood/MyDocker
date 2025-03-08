import random
import string
from locust import HttpUser, TaskSet, task, between

def random_string(length=10):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))

class UserBehavior(TaskSet):

    def on_start(self):

        self.username = f"locust_{random_string(5)}"
        self.password = "1234abcd"

        signup_data = {
            "username": self.username, 
            "password": self.password
            }
        self.client.post("/accounts/api/signup/", json=signup_data)

        login_data = {
            "username": self.username, 
            "password": self.password
            }
        response = self.client.post("/accounts/api/login/", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access")
            if token:
                self.client.headers.update({"Authorization": "Bearer {token}"})

    @task
    def change_password(self):
        self.old_password = self.password
        self.new_password = "abcd1234"

        change_data = {
            "old_password": self.old_password, 
            "new_password1": self.new_password, 
            "new_password2": self.new_password
            }
        self.client.post("/accounts/api/profile/change_password/", json=change_data)
        self.password = self.new_password
    
    @task
    def create_post(self):
        title = f"{random_string(5)}"
        content = f"{random_string(20)}"

        post_data = {
            "title": title,
            "content": content
        }
        response = self.client.post("/posts/api/", json=post_data)
        self.post_id = response.json().get("id")

    @task
    def get_post_list(self):
        self.client.get("/posts/api/")
    
    @task
    def update_post(self):
        post_id = self.post_id
        title = f"{random_string(10)}"
        content = f"{random_string(15)}"

        upost_data = {
            "post_id": post_id,
            "title": title,
            "content": content
        }
        self.client.put(f"/posts/api/{post_id}/", json=upost_data)