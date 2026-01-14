import time
from pathlib import Path

import undetected_chromedriver as uc

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

sleep = time.sleep
PROFILE_DIR = Path("chrome_profile").resolve()
print("PROFILE", PROFILE_DIR)


def wait_until_page_loaded(driver, timeout=30):
    start = time.monotonic()
    while True:
        state = driver.execute_script("return document.readyState")
        body_ok = driver.find_elements(By.CSS_SELECTOR, "body")
        if state in ("interactive", "complete") and body_ok:
            return True

        elapsed = int(time.monotonic() - start)
        print(f"waiting... {elapsed}s / {timeout}s")
        if elapsed >= timeout:
            raise TimeoutError(f"Page load timeout after {timeout}s")
        time.sleep(1)


def wait_until_found_by_xpath(driver, xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def input_text_by_xpath(driver, xpath, text, timeout=10, clear_first=True):
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    if clear_first:
        el.clear()
    el.send_keys(text)
    return el


def click_by_xpath(driver, xpath, timeout=10):
    start = time.monotonic()
    while True:
        try:
            el = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            el.click()
            print("clicked")
            return el
        except TimeoutException:
            elapsed = int(time.monotonic() - start)
            print(f"waiting... {elapsed}s / {timeout}s")
            if elapsed >= timeout:
                raise TimeoutException(f"Click timeout after {timeout}s for {xpath}")

def click_element(driver, element, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: element.is_displayed() and element.is_enabled()
    )
    element.click()
    return element


def main():
    # Configure Chrome options
    driver = None
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={PROFILE_DIR}")
    options.add_argument("--start-maximized")

    try:
        # Initialize the WebDriver with the configured options
        # Selenium Manager handles the driver path automatically in recent versions
        driver = uc.Chrome(headless=False, options=options, use_subprocess=True)

        # Maximize the browser window
        driver.maximize_window()
        print(f"Window size after maximizing: {driver.get_window_size()}")

        # Go to google.com
        driver.get("https://www.google.com")
        wait_until_page_loaded(driver)
        print(driver.title)

        # Go to example.com
        driver.get("https://www.example.com/login/email")
        time.sleep(1)
        wait_until_page_loaded(driver)
        print(driver.title)

        # Input Username
        input_text_by_xpath(driver, "//input[@name='username']", "hello")
        # Input Password
        input_text_by_xpath(driver, "//input[@type='password']", "password")
        # Click Log in
        el_login_btn = wait_until_found_by_xpath(driver, xpath="//div[@id='loginContainer']//button")
        click_element(driver, el_login_btn)

    finally:
        input("Press ENTER to close the browser...")
        driver.service.process = None
        driver.quit()


if __name__ == "__main__":
    main()
