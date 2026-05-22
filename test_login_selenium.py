from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#open login page
driver.get("https://practicetestautomation.com/practice-test-login/")
print("page title",driver.title)
time.sleep(2)

#finding usernmae and password
username=driver.find_element(By.ID,"username")
password=driver.find_element(By.ID,"password")

#enter credentials
username.send_keys("student")
time.sleep(3)
password.send_keys("Password123")
time.sleep(3)

#click login button
login_btn=driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]")
print("Button found")
login_btn.click()
print("button clicked")
time.sleep(3)

#print result
print("after login",driver.title)
print("surrent url",driver.current_url)
time.sleep(3)

driver.quit()
print("browser closed")