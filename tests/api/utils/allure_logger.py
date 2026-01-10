import allure
import json

from tests.api.utils.validators import Validator

def allure_attach(method, url, response, headers=None, payload=None):
    allure.attach(
        json.dumps(
            {
                "method": method,
                "url": url,
                "headers": headers,
                "payload": payload
            },
            indent=2
        ),
        name="API Request",
        attachment_type=allure.attachment_type.JSON
    )

    try:
        body = response.json()
    except ValueError:
        body = response.text

    allure.attach(
        json.dumps(
            {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": body
            },
            indent=2
        ),
        name="API Response",
        attachment_type=allure.attachment_type.JSON
    )


def assert_json_match(actual, expected):
    """
    Attaches Expected and Actual JSONs to the Allure report
    and performs the dictionary assertion.
    """

    # Custom serializer to handle the Any() class in JSON reports
    def json_serializer(obj):
        if isinstance(obj, Validator):
            return str(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

    # 1. Attach Expected Data
    allure.attach(
        json.dumps(expected, indent=2, sort_keys=True, default=json_serializer),
        name="Assertion - Expected",
        attachment_type=allure.attachment_type.JSON
    )

    # 2. Attach Actual Data
    allure.attach(
        json.dumps(actual, indent=2, sort_keys=True),
        name="Assertion - Actual",
        attachment_type=allure.attachment_type.JSON
    )

    # 3. Perform Assertion
    assert actual == expected