from locust import User, task, between
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Import Keys

class UserBehavior(User):
    wait_time = between(1, 5)

    def on_start(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(service=Service(r'Chromedriver\chromedriver.exe'), options=chrome_options)
        
    def on_stop(self):
        self.driver.quit()

    @task
    def login(self):
        self.driver.delete_all_cookies()
        self.driver.get("https://login.e-grant.dk/?wa=wsignin1.0&wtrealm=urn%3aTilskudsPortal&wctx=https%3a%2f%2fwww.e-grant.dk%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3dhttps%3a%2f%2fwww.e-grant.dk%2f")
        self.driver.execute_script("document.body.style.zoom='50%'")

        try:
            # Wait for the page to load completely
            wait = WebDriverWait(self.driver, 3)  # Increased the wait time to 20 seconds

            # Focus on the body element to start sending keys
            body = self.driver.find_element(By.TAG_NAME, 'body')

            # Press the Tab key 3 times and then Enter
            body.send_keys(Keys.TAB * 3)
            body.send_keys(Keys.ENTER)

        except Exception as e:
            self.driver.save_screenshot("keyboard_interaction_error.png")  # Capture screenshot
            print(f"Keyboard interaction failed: {e}")
            return  # Exit the method if keyboard interaction fails

        try:
            # Wait for username and password input fields
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "txt_Username")))
            password_field = wait.until(EC.presence_of_element_located((By.NAME, "txt_Password")))

            # Fill in username and password
            username_field.send_keys("smhj@ufm.dk")
            password_field.send_keys("Confirm92222")
        except Exception as e:
            self.driver.save_screenshot("input_fields_error.png")  # Capture screenshot
            print(f"Filling username and password failed: {e}")
            return  # Exit the method if we can't fill the login fields

        try:
            self.driver.implicitly_wait(6)
            welcome_message = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Velkommen til e-grant.dk')]")
            if welcome_message:
                print("Login successful")
            else:
                print("Login failed")
        except Exception as e:
            self.driver.save_screenshot("welcome_message_error.png")  # Capture screenshot
            print(f"Checking welcome message failed: {e}")

class WebsiteUser(User):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
