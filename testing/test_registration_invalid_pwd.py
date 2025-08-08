from test_utils import get_driver, human_typing, BASE_URL
from selenium.webdriver.common.by import By
import time

def test_registration_invalid_password():
    driver = get_driver()
    try:
        driver.get(BASE_URL + "register.php")
        human_typing(driver.find_element(By.NAME, "username"), "invaliduser")
        human_typing(driver.find_element(By.NAME, "password"), "abc")
        human_typing(driver.find_element(By.NAME, "confirm_password"), "abc")
        driver.find_element(By.ID, "roleUser").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()
        time.sleep(1)
        assert "Password must be at least 8 characters" in driver.page_source
        print("Test: Registration invalid password - Passed")
    except Exception as e:
        print("Test: Registration invalid password - Failed")
        print("Exception:", e)
        print(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_registration_invalid_password()