from locust import HttpUser, between, task
import random


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def index(self):
        charges = random.randrange(1, 100, 1)
        service_type = random.choice(["voice", "data"])
        payload = {
          "serviceType": service_type,
          "unit": charges
        }
        response = self.client.post("8ccffdqrya.execute-api.us-east-1.amazonaws.com/prod/charge-request-redis", json=payload)
        json_var = response.json()
        isAuthorized = bool(json_var['isAuthorized'])
        if not isAuthorized:
            self.client.post("8ccffdqrya.execute-api.us-east-1.amazonaws.com/prod/reset-redis", json=payload)
        response = self.client.post("r7wh1f1luh.execute-api.us-east-1.amazonaws.com/prod/charge-request-memcached",
                         json=payload)
        json_var = response.json()
        isAuthorized = bool(json_var['isAuthorized'])
        if not isAuthorized:
            self.client.post("r7wh1f1luh.execute-api.us-east-1.amazonaws.com/prod/reset-memcached", json=payload)
