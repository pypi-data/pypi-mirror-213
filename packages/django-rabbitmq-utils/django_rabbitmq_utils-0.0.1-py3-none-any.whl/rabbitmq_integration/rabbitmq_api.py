import requests

class RabbitMQAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = (username, password)

    def get_queues(self):
        url = f"{self.base_url}/queues"
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error accessing RabbitMQ API: {response.text}")
