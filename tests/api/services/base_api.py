import requests

class BaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, payload):
        return requests.post(self.base_url + endpoint, json=payload)

    def get(self, endpoint):
        return requests.get(self.base_url + endpoint)

    def put(self, endpoint, payload):
        return requests.put(self.base_url + endpoint, json=payload)

    def delete(self, endpoint):
        return requests.delete(self.base_url + endpoint)
