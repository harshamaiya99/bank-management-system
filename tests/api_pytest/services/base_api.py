import requests
from tests.api_pytest.utils.allure_logger import allure_attach
from tests.api_pytest.utils.logger import api_logger


class BaseAPI:

    @staticmethod
    def post(url, headers, payload):
        api_logger.info(f"POST Request -> {url}")
        api_logger.debug(f"Headers: {headers} | Payload: {payload}")

        response = requests.post(url, headers=headers, json=payload)

        api_logger.info(f"Response Status -> {response.status_code}")
        api_logger.debug(f"Response Body: {response.text}")
        allure_attach("POST", url, response, headers=headers, payload=payload)
        return response

    @staticmethod
    def get(url, headers):
        api_logger.info(f"GET Request -> {url}")
        api_logger.debug(f"Headers: {headers}")

        response = requests.get(url, headers=headers)

        api_logger.info(f"Response Status -> {response.status_code}")
        api_logger.debug(f"Response Body: {response.text}")
        allure_attach("GET", url, response, headers=headers)
        return response

    @staticmethod
    def put(url, headers, payload):
        api_logger.info(f"PUT Request -> {url}")
        api_logger.debug(f"Headers: {headers} | Payload: {payload}")

        response = requests.put(url, headers=headers, json=payload)

        api_logger.info(f"Response Status -> {response.status_code}")
        api_logger.debug(f"Response Body: {response.text}")
        allure_attach("PUT", url, response, headers=headers, payload=payload)
        return response

    @staticmethod
    def delete(url, headers):
        api_logger.info(f"DELETE Request -> {url}")
        api_logger.debug(f"Headers: {headers}")

        response = requests.delete(url, headers=headers)

        api_logger.info(f"Response Status -> {response.status_code}")
        api_logger.debug(f"Response Body: {response.text}")
        allure_attach("DELETE", url, response, headers=headers)
        return response