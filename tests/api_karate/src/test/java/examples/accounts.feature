Feature: End-to-End Account Lifecycle

  Background:
    * url baseUrl

  # -------------------------------------------------------------------------
  # Scenario: Full CRUD (Create, Read, Update, Delete)
  # This flow mimics a real user life cycle:
  # 1. Open an account
  # 2. Check details
  # 3. Update details (e.g. change name or status)
  # 4. Close/Delete the account
  # 5. Verify it is gone
  # -------------------------------------------------------------------------
  Scenario Outline: E2E Lifecycle for <name>

    # =======================================================================
    # STEP 1: CREATE ACCOUNT
    # =======================================================================
    Given path 'accounts'
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
    # Capture the ID for subsequent steps
    And def accountId = response.account_id
    And print 'Created Account ID:', accountId

    # =======================================================================
    # STEP 2: VERIFY CREATION (GET)
    # =======================================================================
    Given path 'accounts', accountId
    When method get
    Then status 200
    And match response.account_holder_name == "<name>"
    And match response.balance == <balance>
    # Save the full object to use as a base for the update
    And def currentDetails = response

    # =======================================================================
    # STEP 3: UPDATE ACCOUNT (PUT)
    # =======================================================================
    # We modify the object we just fetched, rather than re-typing a generic JSON
    * set currentDetails.account_holder_name = currentDetails.account_holder_name + ' Updated'
    * set currentDetails.status = 'Inactive'
    * set currentDetails.balance = <balance> + 1000

    Given path 'accounts', accountId
    And request currentDetails
    When method put
    Then status 200
    And match response.message == "Account updated successfully"

    # =======================================================================
    # STEP 4: VERIFY UPDATE (GET)
    # =======================================================================
    Given path 'accounts', accountId
    When method get
    Then status 200
    # Assertions to prove the update happened
    And match response.account_holder_name contains 'Updated'
    And match response.status == 'Inactive'
    And match response.balance == <balance> + 1000

    # =======================================================================
    # STEP 5: DELETE ACCOUNT
    # =======================================================================
    Given path 'accounts', accountId
    When method delete
    Then status 200
    And match response.message == "Account deleted successfully"

    # =======================================================================
    # STEP 6: VERIFY DELETION (Expect 404)
    # =======================================================================
    Given path 'accounts', accountId
    When method get
    Then status 404
    And match response.detail == "Account not found"

    # =======================================================================
    # TEST DATA
    # =======================================================================
    Examples:
      | name           | dob        | gender | email                | phone      | type    | balance |
      | Karate Master  | 1980-01-01 | Male   | master@karate.io     | 1112223333 | Savings | 1000.00 |
      | Karate Student | 2005-06-15 | Female | student@karate.io    | 4445556666 | Current | 50.00   |