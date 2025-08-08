from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

BASE_URL = "http://localhost/ecommerce-website/"
driver = webdriver.Chrome()

def human_typing(element, text, delay=0.1):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def test_delete_cookies():
    driver.get(BASE_URL)
    driver.delete_all_cookies()
    # Optionally, verify cookies are deleted
    assert driver.get_cookies() == []

def test_registration_invalid_password():
    driver.get(BASE_URL + "register.php")
    human_typing(driver.find_element(By.NAME, "username"), "invaliduser")
    human_typing(driver.find_element(By.NAME, "password"), "abc")
    human_typing(driver.find_element(By.NAME, "confirm_password"), "abc")
    driver.find_element(By.ID, "roleUser").click()
    driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()
    time.sleep(1)
    assert "Password must be at least 8 characters" in driver.page_source

def test_registration_mismatched_password():
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

def test_registration_valid():
    global test_username, test_password
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

def test_login_invalid():
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



def test_login_valid():
    driver.get(BASE_URL + "login.php")
    human_typing(driver.find_element(By.NAME, "username"), test_username)
    human_typing(driver.find_element(By.NAME, "password"), test_password)
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
    time.sleep(1)
    assert "Product Catalog" in driver.page_source

def test_add_product_to_cart():
    driver.get(BASE_URL + "index.php")
    # Add first product to cart
    forms = driver.find_elements(By.TAG_NAME, "form")
    for form in forms:
        if form.find_elements(By.NAME, "product_id"):
            qty_input = form.find_element(By.NAME, "quantity")
            qty_input.clear()
            human_typing(qty_input, "2")
            form.find_element(By.XPATH, ".//button[contains(text(),'Add to Cart')]").click()
            break
    time.sleep(1)
    driver.find_element(By.PARTIAL_LINK_TEXT, "View Cart").click()
    time.sleep(1)
    assert "Shopping Cart" in driver.page_source

def test_remove_product_from_cart():
    # Remove product from cart
    remove_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]")
    remove_btn.click()
    time.sleep(1)
    assert "Your cart is empty" in driver.page_source

def test_add_product_and_update_quantity():
    driver.get(BASE_URL + "index.php")
    # Add product again
    forms = driver.find_elements(By.TAG_NAME, "form")
    for form in forms:
        if form.find_elements(By.NAME, "product_id"):
            qty_input = form.find_element(By.NAME, "quantity")
            qty_input.clear()
            human_typing(qty_input, "1")
            form.find_element(By.XPATH, ".//button[contains(text(),'Add to Cart')]").click()
            break
    time.sleep(1)
    driver.find_element(By.PARTIAL_LINK_TEXT, "View Cart").click()
    time.sleep(1)
    # Increase quantity
    plus_btn = driver.find_element(By.CSS_SELECTOR, "button.plus")
    plus_btn.click()
    time.sleep(1)
    # Decrease quantity
    minus_btn = driver.find_element(By.CSS_SELECTOR, "button.minus")
    minus_btn.click()
    time.sleep(1)
    # Remove to empty cart
    remove_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]")
    remove_btn.click()
    time.sleep(1)
    assert "Your cart is empty" in driver.page_source

def test_payment():
    # Ensure user is logged in and cart has at least one product
    driver.get(BASE_URL + "logout.php")
    driver.get(BASE_URL + "login.php")
    human_typing(driver.find_element(By.NAME, "username"), test_username)
    human_typing(driver.find_element(By.NAME, "password"), test_password)
    driver.find_element(By.ID, "roleUser").click()
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
    time.sleep(1)
    # Add a product to cart
    driver.get(BASE_URL + "index.php")
    forms = driver.find_elements(By.TAG_NAME, "form")
    for form in forms:
        if form.find_elements(By.NAME, "product_id"):
            qty_input = form.find_element(By.NAME, "quantity")
            qty_input.clear()
            human_typing(qty_input, "1")
            form.find_element(By.XPATH, ".//button[contains(text(),'Add to Cart')]").click()
            break
    time.sleep(1)
    driver.find_element(By.PARTIAL_LINK_TEXT, "View Cart").click()
    time.sleep(1)
    # Go to payment page
    driver.find_element(By.PARTIAL_LINK_TEXT, "Checkout").click()
    time.sleep(1)
    assert "Scan to Pay" in driver.page_source
    # Simulate payment
    driver.find_element(By.NAME, "pay").click()
    time.sleep(1)
    assert "Order Successful" in driver.page_source

def test_admin_login():
    driver.get(BASE_URL + "logout.php")
    driver.get(BASE_URL + "login.php")
    human_typing(driver.find_element(By.NAME, "username"), "hari")
    human_typing(driver.find_element(By.NAME, "password"), "123")
    driver.find_element(By.ID, "roleAdmin").click()
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
    time.sleep(1)
    assert "Admin: Manage Products" in driver.page_source

def test_admin_edit_product_quantity_over_1000():
    # Go to admin dashboard (assume already logged in as admin)
    driver.get(BASE_URL + "admin_products.php")
    # Click the first Edit button
    driver.find_element(By.CSS_SELECTOR, "button.edit-btn").click()
    time.sleep(1)
    qty_input = driver.find_element(By.ID, "edit-quantity")
    qty_input.clear()
    human_typing(qty_input, "1001")
    time.sleep(1)
    # Try to trigger the JS validation (simulate blur)
    # qty_input.send_keys(Keys.TAB)
    
    # The value should revert to previous (not 1001)
    try:
        alert = driver.switch_to.alert
        assert "Quantity cannot be greater than 1000" in alert.text
        alert.accept()
    except Exception as e:
        print("No alert present or error:", e)
    # The value should revert to previous (not 1001)
    time.sleep(1)
    assert int(qty_input.get_attribute("value")) <= 1000

def test_admin_edit_product_price():
    driver.get(BASE_URL + "admin_products.php")
    driver.find_element(By.CSS_SELECTOR, "button.edit-btn").click()
    time.sleep(1)
    price_input = driver.find_element(By.ID, "edit-price")
    price_input.clear()
    human_typing(price_input, "999")
    driver.find_element(By.XPATH, "//button[contains(text(),'Save Changes')]").click()
    time.sleep(1)
    # Check if the price is updated in the table
    assert "999" in driver.page_source

def test_admin_edit_product_quantity_low_stock():
    driver.get(BASE_URL + "admin_products.php")
    driver.find_element(By.CSS_SELECTOR, "button.edit-btn").click()
    time.sleep(1)
    qty_input = driver.find_element(By.ID, "edit-quantity")
    qty_input.clear()
    human_typing(qty_input, "3")
    driver.find_element(By.XPATH, "//button[contains(text(),'Save Changes')]").click()
    time.sleep(1)
    # Should show Low Stock label
    assert "Low Stock!" in driver.page_source

def test_admin_edit_product_quantity_out_of_stock():
    driver.get(BASE_URL + "admin_products.php")
    driver.find_element(By.CSS_SELECTOR, "button.edit-btn").click()
    time.sleep(1)
    qty_input = driver.find_element(By.ID, "edit-quantity")
    qty_input.clear()
    human_typing(qty_input, "0")
    driver.find_element(By.XPATH, "//button[contains(text(),'Save Changes')]").click()
    time.sleep(1)
    # Should show OUT OF STOCK label
    assert "OUT OF STOCK!" in driver.page_source

def test_print_session_for_user():
    driver.get(BASE_URL + "logout.php") 
    driver.get(BASE_URL + "login.php")
    human_typing(driver.find_element(By.NAME, "username"), test_username)
    human_typing(driver.find_element(By.NAME, "password"), test_password)
    driver.find_element(By.ID, "roleUser").click()
    driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
    time.sleep(1)
    print("Cookies after login for user:", test_username)
    for cookie in driver.get_cookies():
        print(cookie)

def test_set_window_size():
    driver.set_window_size(1200, 800)
    size = driver.get_window_size()
    assert size['width'] == 1200 and size['height'] == 800

def test_logo_on_homepage():
    driver.get(BASE_URL + "index.php")
    # Adjust selector as per your actual logo element
    logo = driver.find_elements(By.ID, "logo")
    assert len(logo) > 0 and logo[0].is_displayed()

def test_logout():
    driver.get(BASE_URL + "logout.php")
    time.sleep(1)
    assert "Login" in driver.page_source

if __name__ == "__main__":
    passed = []
    failed = []
    try:
        for func, desc in [
            (test_delete_cookies, "Delete cookies"),
            (test_registration_invalid_password, "Registration invalid password"),
            (test_registration_mismatched_password, "Registration mismatched password"),
            (test_registration_valid, "Registration valid"),
            (test_login_invalid, "Login invalid"),
            (test_login_valid, "Login valid"),
            (test_add_product_to_cart, "Add product to cart"),
            (test_remove_product_from_cart, "Remove product from cart"),
            (test_add_product_and_update_quantity, "Update product quantity and empty cart"),
            (test_payment, "Payment"),
            (test_admin_login, "Admin login"),
            (test_admin_edit_product_quantity_over_1000, "Admin edit product quantity > 1000"),
            (test_admin_edit_product_price, "Admin edit product price"),
            (test_admin_edit_product_quantity_low_stock, "Admin edit product quantity low stock"),
            (test_admin_edit_product_quantity_out_of_stock, "Admin edit product quantity out of stock"),
            (test_print_session_for_user, "Print session for user"),
            (test_set_window_size, "Set window size"),
            (test_logo_on_homepage, "Logo on homepage"),
            (test_logout, "Logout"),
        ]:
            try:
                func()
                print(f"Test: {desc} - Passed")
                passed.append(desc)
            except AssertionError as e:
                print(f"Test: {desc} - Failed")
                failed.append(desc)
                print("Test failed:", e)
                print(driver.page_source)
            except Exception as e:
                print(f"Test: {desc} - Failed (Exception)")
                failed.append(desc)
                print("Exception:", e)
                print(driver.page_source)
        print("\n--- TEST SUMMARY ---")
        print(f"Passed: {len(passed)}")
        for t in passed:
            print(f"  ✔ {t}")
        print(f"Failed: {len(failed)}")
        for t in failed:
            print(f"  ✖ {t}")
    finally:
        driver.quit()