@ignore
Feature: Authentication Helper

  Scenario: Get Manager Token
    Given url baseUrl
    And path 'token'
    # OAuth2 in FastAPI expects form fields, NOT json
    And form field username = 'manager'
    And form field password = 'manager123'
    When method post
    Then status 200
    # Return the token to the caller
    * def accessToken = response.access_token