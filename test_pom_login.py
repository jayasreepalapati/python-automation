import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from login_page import loginpage

@pytest.fixture(scope="function")
def driver():
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_valid_login(driver):
    login_page = loginpage(driver)
    login_page.open()
    login_page.enter_username("student")
    login_page.enter_password("Password123")
    login_page.click_login()
    time.sleep(2)
    assert "logged-in-successfully" in login_page.get_current_url()
    print("✅ Valid login passed!")

def test_invalid_login(driver):
    login_page = loginpage(driver)
    login_page.open()
    login_page.enter_username("student")
    login_page.enter_password("wrongpassword")
    login_page.click_login()
    time.sleep(2)
    assert "logged-in-successfully" not in login_page.get_current_url()
    print("✅ Invalid login passed!")