from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

driver.get("https://www.python.org")
print("page title:",driver.title)
time.sleep(2)

search_box=driver.find_element(By.NAME,"q")
search_box.send_keys("python automation")
time.sleep(2)

search_box.send_keys(Keys.RETURN)
time.sleep(3)

print("after search",driver.title)
print("current url",driver.current_url)
time.sleep(2)

driver.quit()
print("browser closed")