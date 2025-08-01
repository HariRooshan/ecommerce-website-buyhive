from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

driver = webdriver.Chrome()
driver.get("http://localhost/ecommerce-website/login.php")
wait = WebDriverWait(driver, 10)

# Register a new user


username = f"testuser{random.randint(1000,9999)}"
email = f"{username}@example.com"
password = "testpassword"
time.sleep(1)
# wait.until(EC.visibility_of_element_located((By.ID, "register-form")))
# wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(username)
username = f"testuser{random.randint(1000,9999)}"
email = f"{username}@example.com"
password = "testpassword"

#

# Wait for redirect after registration
time.sleep(2)

# Log out if automatically logged in
# try:
#     logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'logout=1')]")))
#     logout_btn.click()
#     time.sleep(1)
# except:
#     pass

# Log in
wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.NAME, "login").click()
time.sleep(2)
wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys("bala")
driver.find_element(By.NAME, "password").send_keys("123")
driver.find_element(By.NAME, "login").click()

# Add first product to cart (if available)
try:
    add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@name,'add_to_cart')]")))
    add_to_cart_btn.click()
    time.sleep(1)
except:
    print("No product available to add to cart.")

# Open cart
try:
    cart_btn = driver.find_element(By.CSS_SELECTOR, ".cart-btn")
    cart_btn.click()
    time.sleep(1)
except:
    print("Cart button not found.")

# Proceed to checkout
try:
    checkout_btn = wait.until(EC.element_to_be_clickable((By.NAME, "checkout")))
    checkout_btn.click()
    time.sleep(2)
    WebDriverWait(driver, 10).until(EC.alert_is_present())

# Switch to alert and accept (click OK)
    alert = driver.switch_to.alert
    print("Alert text is:", alert.text)  # Optional: print alert message
    alert.accept()
except:
    print("Checkout button not found or cart is empty.")

# Log out
try:
    logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'logout=1')]")))
    logout_btn.click()
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.alert_is_present())

# Switch to alert and accept (click OK)
    alert = driver.switch_to.alert
    print("Alert text is:", alert.text)  # Optional: print alert message
    alert.accept()
    print("Logged out successfully.")


except:
    print("Logout button not found.")
time.sleep(5)
register_btn = wait.until(EC.element_to_be_clickable((By.NAME, "reg")))
register_btn.click()
# wait.until(EC.element_to_be_clickable((By.NAME, "username"))).send_keys(username)
driver.find_element(By.NAME, "username2").send_keys(username)
driver.find_element(By.NAME, "email").send_keys(email)
driver.find_element(By.NAME, "password2").send_keys(password)
driver.find_element(By.NAME, "register").click()

try:
    logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'logout=1')]")))
    logout_btn.click()
    time.sleep(1)
except:
    pass