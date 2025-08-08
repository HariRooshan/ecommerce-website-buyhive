from test_utils import get_driver, human_typing, BASE_URL
from selenium.webdriver.common.by import By
import time

def test_registration_valid():
    driver = get_driver()
    try:
        test_username = "testuser2"
        test_password = "Abcdefg1!"
        driver.get(BASE_URL + "register.php")
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "confirm_password").clear()
        human_typing(driver.find_element(By.NAME, "username"), test_username)
        human_typing(driver.find_element(By.NAME, "password"), test_password)
        human_typing(driver.find_element(By.NAME, "confirm_password"), test_password)
        driver.find_element(By.ID, "roleUser").click()
        driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()
        time.sleep(1)
        assert "Registration successful!" in driver.page_source
        print("Test: Registration valid - Passed")
    except Exception as e:
        print("Test: Registration valid - Failed")
        print("Exception:", e)
        print(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_registration_valid()