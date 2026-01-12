import allure
import json
import pytest


def normalize_services(services_str):
    """
    Splits a comma-separated string, strips whitespace, sorts items, and rejoins.
    Example: "SMS, Debit Card" -> "Debit Card,SMS"
    """
    if not services_str:
        return ""
    items = [s.strip() for s in str(services_str).split(",")]
    items.sort()
    return ",".join(items)


def assert_ui_match(actual: dict, expected: dict):
    """
    Asserts that the actual UI state matches the expected dictionary.
    Includes smart comparison for numbers and unsorted lists (services).
    """

    # [Attachments code remains the same as previous step...]
    allure.attach(
        json.dumps(expected, indent=2, sort_keys=True),
        name="UI Assertion - Expected",
        attachment_type=allure.attachment_type.JSON
    )
    allure.attach(
        json.dumps(actual, indent=2, sort_keys=True),
        name="UI Assertion - Actual",
        attachment_type=allure.attachment_type.JSON
    )

    mismatches = []

    for key, expected_val in expected.items():
        actual_val = actual.get(key)

        # --- SMART COMPARISON LOGIC ---
        is_match = False

        # 1. Special Handling for 'services' (Sort before compare)
        if key == "services":
            if normalize_services(actual_val) == normalize_services(expected_val):
                is_match = True

        # 2. Try direct string comparison
        elif str(actual_val) == str(expected_val):
            is_match = True

        # 3. Try numeric comparison
        else:
            try:
                if float(actual_val) == float(expected_val):
                    is_match = True
            except (ValueError, TypeError):
                pass

        if not is_match:
            mismatches.append(f"Field '{key}': Expected '{expected_val}' vs Actual '{actual_val}'")

    if mismatches:
        pytest.fail(f"UI State Verification Failed:\n" + "\n".join(mismatches))


def assert_message_match(actual: str, expected: str, context: str = "Validation Message"):
    """
    Asserts that a specific action message (e.g., Alert text) matches the expectation.
    Logs the result to Allure for visibility.
    """
    # with allure.step(f"Assert '{context}'"):
    allure.attach(
        f"Expected: {expected}\nActual:   {actual}",
        name=f"Assertion - {context}",
        attachment_type=allure.attachment_type.TEXT
    )

    assert actual == expected, f"{context} Mismatch! Expected '{expected}', but got '{actual}'"


def assert_message_contains(actual: str, expected_substring: str, context: str = "Validation Message"):
    """
    Asserts that the actual message contains the expected substring.
    Useful for dynamic alerts like 'Account Created! ID: 12345'.
    """
    allure.attach(
        f"Expected to contain: {expected_substring}\nActual:              {actual}",
        name=f"Assertion - {context}",
        attachment_type=allure.attachment_type.TEXT
    )

    assert expected_substring in actual, f"{context} Failed! Expected substring '{expected_substring}' not found in '{actual}'"