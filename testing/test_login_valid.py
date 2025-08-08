from test_utils import get_driver, human_typing, BASE_URL
from selenium.webdriver.common.by import By
import time

def test_login_valid():
    driver = get_driver()
    test_username = "testuser2"
    test_password = "Abcdefg1!"
    try:
        driver.get(BASE_URL + "login.php")
        human_typing(driver.find_element(By.NAME, "username"), test_username)
        human_typing(driver.find_element(By.NAME, "password"), test_password)
        driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
        time.sleep(1)
        assert "Product Catalog" in driver.page_source
        print("Test: Login valid - Passed")
    except Exception as e:
        print("Test: Login valid - Failed")
        print("Exception:", e)
        print(driver.page_source)
    finally:
        driver.quit()

if __name__ == "__main__":
    test_login_valid()