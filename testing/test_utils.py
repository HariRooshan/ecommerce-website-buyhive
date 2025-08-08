from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

BASE_URL = "http://localhost/ecommerce-website/"

def get_driver():
    driver = webdriver.Chrome()
    return driver

def human_typing(element, text, delay=0.1):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)