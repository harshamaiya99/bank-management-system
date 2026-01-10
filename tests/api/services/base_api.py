import requests
from tests.api.utils.allure_logger import allure_attach

class BaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, headers, payload):
        url = self.base_url + endpoint
        response = requests.post(url, headers=headers, json=payload)
        allure_attach("POST", url, response, headers=headers, payload=payload)
        return response

    def get(self, endpoint, headers):
        url = self.base_url + endpoint
        response = requests.get(url, headers=headers)
        allure_attach("GET", url, response, headers=headers)
        return response

    def put(self, endpoint, headers, payload):
        url = self.base_url + endpoint
        response = requests.put(url, headers=headers, json=payload)
        allure_attach("PUT", url, response, headers=headers, payload=payload)
        return response

    def delete(self, endpoint, headers):
        url = self.base_url + endpoint
        response = requests.delete(url, headers=headers)
        allure_attach("DELETE", url, response, headers=headers)
        return response
