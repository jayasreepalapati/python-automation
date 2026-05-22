import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

@pytest.fixture
def driver():
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()
    
def test_valid_login(driver):
    driver.get("https://practicetestautomation.com/practice-test-login/")
    driver.find_element(By.ID,"username").send_keys("student")
    driver.find_element(By.ID,"password").send_keys("Password123")
    driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
    time.sleep(3)
    assert "logged-in-successfully" in driver.current_url
    print("login test passed")
    
def test_invalid_login(driver):
    driver.get("https://practicetestautomation.com/practice-test-login/")
    driver.find_element(By.ID,"username").send_keys("student")
    driver.find_element(By.ID,"password").send_keys("wrongpassword")
    driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()
    time.sleep(3)
    assert "logged-in-successfully" not in driver.current_url
    print("invalid login test passed")
    