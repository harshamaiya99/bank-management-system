import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

"""
Stateless helper functions for robust Selenium interactions.
Pass the 'driver' explicitly.
"""


def smart_click(driver, locator, timeout=10):
    """
    Robust click that handles ElementClickInterceptedException (toasts/sticky headers).
    """
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable(locator))

    try:
        element.click()
    except ElementClickInterceptedException:
        # Scroll to center to avoid sticky headers/footers
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except ElementClickInterceptedException:
            # Force click via JS as last resort
            driver.execute_script("arguments[0].click();", element)


def smart_fill(driver, locator, text, timeout=10):
    """
    Robust fill for React/Shadcn controlled inputs where standard .clear() often fails.
    """
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.visibility_of_element_located(locator))

    # Ensure element is focused/clickable
    smart_click(driver, locator, timeout)

    # 1. Try standard clear
    element.clear()

    # 2. React safeguard: If value persists, use Select All + Backspace
    if element.get_attribute("value"):
        cmd_ctrl = Keys.COMMAND if sys.platform == 'darwin' else Keys.CONTROL
        element.send_keys(cmd_ctrl + "a")
        element.send_keys(Keys.BACKSPACE)

    # 3. Type new text
    element.send_keys(str(text))


def smart_check(driver, locator, timeout=10):
    """
    Handles both standard <input type='checkbox'> and ARIA (role='checkbox').
    """
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable(locator))

    is_aria = element.get_attribute("role") == "checkbox"

    if is_aria:
        if element.get_attribute("aria-checked") != "true":
            smart_click(driver, locator, timeout)
    else:
        if not element.is_selected():
            smart_click(driver, locator, timeout)


def smart_uncheck(driver, locator, timeout=10):
    """
    Handles both standard <input type='checkbox'> and ARIA (role='checkbox').
    """
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable(locator))

    is_aria = element.get_attribute("role") == "checkbox"

    if is_aria:
        if element.get_attribute("aria-checked") == "true":
            smart_click(driver, locator, timeout)
    else:
        if element.is_selected():
            smart_click(driver, locator, timeout)


def get_text(driver, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located(locator)).text


def get_value(driver, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located(locator)).get_attribute("value")