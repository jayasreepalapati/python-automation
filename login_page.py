from selenium.webdriver.common.by import By

class loginpage:
    def __init__(self,driver):
        self.driver = driver
        self.url="https://practicetestautomation.com/practice-test-login/"
        self.username_field=(By.ID,"username")
        self.password_field=(By.ID,"password")
        self.login_btn=(By.XPATH, "//button[contains(text(),'Submit')]")
        
    def open(self):
        self.driver.get(self.url)
    
    def enter_username(self,username):
        self.driver.find_element(*self.username_field).send_keys(username)
    
    def enter_password(self,password):
        self.driver.find_element(*self.password_field).send_keys(password)
    
    
    def click_login(self):
        self.driver.find_element(*self.login_btn).click()
    
    def get_current_url(self):
        return self.driver.current_url
    