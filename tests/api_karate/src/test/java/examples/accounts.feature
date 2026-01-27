@regression
Feature: End-to-End Account Lifecycle

  Background:
    * url baseUrl
    # -----------------------------------------------------------
    # APPLY AUTH HEADER GLOBALLY
    # This automatically adds "Authorization: Bearer <token>"
    # to every single request (POST, GET, PUT, DELETE) in this file.
    # -----------------------------------------------------------
    * configure headers = authHeader

  # -------------------------------------------------------------------------
  # Scenario: Full CRUD (Create, Read, Update, Delete)
  # -------------------------------------------------------------------------

  # Tag the scenario as smoke AND regression
  @smoke @regression
  Scenario Outline: E2E Lifecycle for <name>

    # =======================================================================
    # STEP 1: CREATE ACCOUNT
    # =======================================================================
    Given path 'accounts'
    And header Idempotency-Id = java.util.UUID.randomUUID().toString()
    And header X-Process-Id = java.util.UUID.randomUUID().toString()

    And request
    """
    {
      "account_holder_name": "<name>",
      "dob": "<dob>",
      "gender": "<gender>",
      "email": "<email>",
      "phone": "<phone>",
      "address": "123 Karate Way",
      "zip_code": "99999",
      "account_type": "<type>",
      "balance": <balance>,
      "status": "Active",
      "services": "Internet Banking",
      "marketing_opt_in": true,
      "agreed_to_terms": true
    }
    """
    When method post
    Then status 200
    And match response.message == "Account created successfully"
    And def accountId = response.account_id
    And print 'Created Account ID:', accountId

    # =======================================================================
    # STEP 2: VERIFY CREATION (GET)
    # =======================================================================
    Given path 'accounts', accountId
    And header X-Process-Id = java.util.UUID.randomUUID().toString()
    When method get
    Then status 200
    And match response.account_holder_name == "<name>"
    And match response.balance == <balance>
    And def currentDetails = response

    # =======================================================================
    # STEP 3: UPDATE ACCOUNT (PUT)
    # =======================================================================
    * set currentDetails.account_holder_name = currentDetails.account_holder_name + ' Updated'
    * set currentDetails.status = 'Inactive'
    * set currentDetails.balance = <balance> + 1000

    Given path 'accounts', accountId
    And header X-Process-Id = java.util.UUID.randomUUID().toString()
    And request currentDetails
    When method put
    Then status 200
    And match response.message == "Account updated successfully"

    # =======================================================================
    # STEP 4: VERIFY UPDATE (GET)
    # =======================================================================
    Given path 'accounts', accountId
    And header X-Process-Id = java.util.UUID.randomUUID().toString()
    When method get
    Then status 200
    And match response.account_holder_name contains 'Updated'
    And match response.status == 'Inactive'
    And match response.balance == <balance> + 1000

    # =======================================================================
    # STEP 5: DELETE ACCOUNT
    # =======================================================================
    Given path 'accounts', accountId
    And header X-Process-Id = java.util.UUID.randomUUID().toString()
    When method delete
    Then status 200
    And match response.message == "Account deleted successfully"

    # =======================================================================
    # STEP 6: VERIFY DELETION (Expect 404)
    # =======================================================================
    Given path 'accounts', accountId
    And header X-Process-Id = java.util.UUID.randomUUID().toString()
    When method get
    Then status 404
    And match response.detail == "Account not found"

    Examples:
      | name           | dob        | gender | email                | phone      | type    | balance |
      | Karate Master  | 1980-01-01 | Male   | master@karate.io     | 1112223333 | Savings | 1000.00 |
      | Karate Student | 2005-06-15 | Female | student@karate.io    | 4445556666 | Current | 50.00   |