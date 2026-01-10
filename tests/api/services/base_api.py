import requests
from tests.api.utils.allure_logger import attach_request, attach_response

class BaseAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, headers, payload):
        url = self.base_url + endpoint
        attach_request("POST", url, headers=headers, payload=payload)
        response = requests.post(url, headers=headers, json=payload)
        attach_response(response)
        return response

    def get(self, endpoint, headers):
        url = self.base_url + endpoint
        attach_request("GET", url, headers=headers)
        response = requests.get(url, headers=headers)
        attach_response(response)
        return response

    def put(self, endpoint, headers, payload):
        url = self.base_url + endpoint
        attach_request("PUT", url, headers=headers, payload=payload)
        response = requests.put(url, headers=headers, json=payload)
        attach_response(response)
        return response

    def delete(self, endpoint, headers):
        url = self.base_url + endpoint
        attach_request("DELETE", url, headers=headers)
        response = requests.delete(url, headers=headers)
        attach_response(response)
        return response
