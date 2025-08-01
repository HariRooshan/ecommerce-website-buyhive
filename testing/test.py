# test_login.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://localhost/ecommerce-website/"
CHROMEDRIVER_PATH = ""  # Update if needed

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

def test_registration():
    driver.get(BASE_URL + "register.php")
    # Try invalid password
    driver.find_element(By.NAME, "username").send_keys("testuser1")
    driver.find_element(By.NAME, "password").send_keys("abc")
    driver.find_element(By.NAME, "confirm_password").send_keys("abc")
    driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()
    time.sleep(1)
    assert "Password must be at least 8 characters" in driver.page_source

    # Try mismatched passwords
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "confirm_password").clear()
    driver.find_element(By.NAME, "username").send_keys("testuser2")
    driver.find_element(By.NAME, "password").send_keys("Abcdefg1!")
    driver.find_element(By.NAME, "confirm_password").send_keys("Abcdefg2!")
    driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()
    time.sleep(1)
    assert "Passwords do not match" in driver.page_source

    # Register valid user
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "confirm_password").clear()
    driver.find_element(By.NAME, "username").send_keys("testuser3")
    driver.find_element(By.NAME, "password").send_keys("Abcdefg1!")
    driver.find_element(By.NAME, "confirm_password").send_keys("Abcdefg1!")
    driver.find_element(By.ID, "roleUser").click()
    driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()
    time.sleep(1)
    assert "Registration successful" in driver.page_source

def test_login():
    driver.get(BASE_URL + "login.php")
    # Invalid login
    driver.find_element(By.NAME, "username").send_keys("wronguser")
    driver.find_element(By.NAME, "password").send_keys("wrongpass")
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
    time.sleep(1)
    assert "Invalid username or password" in driver.page_source

    # Lockout test (try 5 times)
    for _ in range(5):
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "username").send_keys("wronguser")
        driver.find_element(By.NAME, "password").send_keys("wrongpass")
        driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
        time.sleep(0.5)
    assert "Too many failed attempts" in driver.page_source

    # Wait for lockout to expire
    time.sleep(65)
    driver.refresh()

    # Valid login
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "username").send_keys("testuser3")
    driver.find_element(By.NAME, "password").send_keys("Abcdefg1!")
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
    time.sleep(1)
    assert "Product Catalog" in driver.page_source

def test_catalog_and_cart():
    driver.get(BASE_URL + "index.php")
    # Add first available product to cart
    products = driver.find_elements(By.CSS_SELECTOR, ".card")
    for product in products:
        try:
            qty_input = product.find_element(By.NAME, "quantity")
            add_btn = product.find_element(By.CSS_SELECTOR, "button.btn-primary")
            if add_btn.is_enabled():
                qty_input.clear()
                qty_input.send_keys("2")
                add_btn.click()
                break
        except Exception:
            continue
    time.sleep(1)
    # Go to cart
    driver.find_element(By.LINK_TEXT, "View Cart").click()
    time.sleep(1)
    assert "Shopping Cart" in driver.page_source

def test_cart_update_and_remove():
    # Increase quantity
    plus_btn = driver.find_element(By.CSS_SELECTOR, "button.plus")
    plus_btn.click()
    time.sleep(1)
    # Remove item
    remove_btn = driver.find_element(By.CSS_SELECTOR, "button.remove-item")
    remove_btn.click()
    time.sleep(1)
    assert "Your cart is empty" in driver.page_source

def test_payment():
    # Add product again
    driver.get(BASE_URL + "index.php")
    products = driver.find_elements(By.CSS_SELECTOR, ".card")
    for product in products:
        try:
            qty_input = product.find_element(By.NAME, "quantity")
            add_btn = product.find_element(By.CSS_SELECTOR, "button.btn-primary")
            if add_btn.is_enabled():
                qty_input.clear()
                qty_input.send_keys("1")
                add_btn.click()
                break
        except Exception:
            continue
    time.sleep(1)
    # Go to cart and then payment
    driver.find_element(By.LINK_TEXT, "View Cart").click()
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Checkout").click()
    time.sleep(1)
    assert "Scan to Pay" in driver.page_source
    # Simulate payment
    driver.find_element(By.NAME, "pay").click()
    time.sleep(1)
    assert "Order Successful" in driver.page_source

def test_logout():
    driver.get(BASE_URL + "logout.php")
    time.sleep(1)
    assert "Login" in driver.page_source

if __name__ == "__main__":
    try:
        test_registration()
        test_login()
        test_catalog_and_cart()
        test_cart_update_and_remove()
        test_payment()
        test_logout()
        print("All tests passed!")
    except AssertionError as e:
        print("Test failed:", e)
    finally:
        driver.quit()