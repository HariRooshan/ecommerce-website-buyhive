from test_utils import get_driver, human_typing, BASE_URL
from selenium.webdriver.common.by import By
import time

def test_login_invalid():
    driver = get_driver()
    try:
        driver.get(BASE_URL + "login.php")
        # Invalid login (first attempt)
        human_typing(driver.find_element(By.NAME, "username"), "wronguser")
        human_typing(driver.find_element(By.NAME, "password"), "wrongpass")
        driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
        time.sleep(1)
        assert "Invalid username or password" in driver.page_source

        # Lockout test (try 5 times total)
        for _ in range(5):
            driver.find_element(By.NAME, "username").clear()
            driver.find_element(By.NAME, "password").clear()
            human_typing(driver.find_element(By.NAME, "username"), "wronguser")
            human_typing(driver.find_element(By.NAME, "password"), "wrongpass")
            driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
            time.sleep(0.5)
        # After 5th attempt, lockout message should appear
        assert "Too many failed attempts" in driver.page_source

        # Wait for lockout to expire (your PHP sets 10 seconds, wait a bit more)
        time.sleep(12)
        driver.refresh()

        # Valid login
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "username").send_keys("testuser2")
        driver.find_element(By.NAME, "password").send_keys("Abcdefg1!")
        driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
        time.sleep(1)
        assert "Product Catalog" in driver.page_source
        print("Test: Login Invalid - Passed")
    except Exception as e:
        print("Test: Login Invalid - Failed")
        print("Exception:", e)
        print(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_login_invalid()