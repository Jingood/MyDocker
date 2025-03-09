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
                self.client.headers.update({"Authorization": f"Bearer {token}"})

        self.old_password = self.password
        self.new_password = "abcd1234"

        change_data = {
            "old_password": self.old_password, 
            "new_password1": self.new_password, 
            "new_password2": self.new_password
            }
        with self.client.post("/accounts/api/profile/change_password/", json=change_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                self.password = self.new_password
            else:
                response.failure(f"비밀번호 변경 실패: {response.status_code}")
    
    @task
    def scenario_flow(self):
        title = f"{random_string(5)}"
        content = f"{random_string(20)}"

        post_data = {
            "title": title,
            "content": content
        }
        with self.client.post("/posts/api/", json=post_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                self.post_id = response.json().get("id")
            else:
                response.failure(f"게시물 생성 실패: {response.status_code}")

        with self.client.get("/posts/api/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"게시물 목록 조회 실패: {response.status_code}")

        post_id = self.post_id
        up_title = f"{random_string(10)}"
        up_content = f"{random_string(15)}"

        upost_data = {
            "title": up_title,
            "content": up_content
        }
        with self.client.put(f"/posts/api/{post_id}/", json=upost_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"게시물 수정 실패: {response.status_code}")

        p_like_data = {
            "post_id": post_id
        }
        with self.client.post(f"/posts/api/like/{post_id}/", json=p_like_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"게시물 좋아요 실패: {response.status_code}")
    
        c_content = f"{random_string(7)}"

        comment_data = {
            "content": c_content
        }
        with self.client.post(f"/posts/api/comment/{post_id}/", json=comment_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                self.comment_id = response.json().get("id")
            else:
                response.failure(f"댓글 생성 실패: {response.status_code}")
    
        comment_id = self.comment_id
        uc_content = f"{random_string(6)}"

        ucomment_data = {
            "content": uc_content
        }
        with self.client.put(f"/posts/api/detail/{comment_id}/", json=ucomment_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"댓글 수정 실패: {response.status_code}")
    
        parent_id = self.comment_id
        r_content = f"{random_string(11)}"

        reply_data = {
            "content": r_content
        }
        with self.client.post(f"/posts/api/reply/{post_id}/{parent_id}/", json=reply_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"대댓글 생성 실패: {response.status_code}")

        like_data = {
            "comment_id": comment_id
        }
        with self.client.post(f"/posts/api/comment/like/{comment_id}/", json=like_data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"대댓글 좋아요 실패: {response.status_code}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)