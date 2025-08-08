from test_utils import get_driver, human_typing, BASE_URL
from selenium.webdriver.common.by import By
import time

def test_registration_mismatched_password():
    driver = get_driver()
    try:
        driver.get(BASE_URL + "register.php")
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "confirm_password").clear()
        human_typing(driver.find_element(By.NAME, "username"), "mismatchuser")
        human_typing(driver.find_element(By.NAME, "password"), "Abcdefg1!")
        human_typing(driver.find_element(By.NAME, "confirm_password"), "Abcdefg2!")
        driver.find_element(By.ID, "roleUser").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()
        time.sleep(1)
        assert "Passwords do not match" in driver.page_source
        print("Test: Registration mismatched password - Passed")
    except Exception as e:
        print("Test: Registration mismatched password - Failed")
        print("Exception:", e)
        print(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_registration_mismatched_password()