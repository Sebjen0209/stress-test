import time
from locust import User, task, between, run_single_user
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserBehavior(User):
    wait_time = between(1, 5)

    def on_start(self):
        self.driver = self.initialize_webdriver()
        self.driver.set_window_size(1400, 1000)
        self.driver.implicitly_wait(5)

    def on_stop(self):
        self.driver.quit()

    def initialize_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=Service(r'Chromedriver\chromedriver.exe'), options=chrome_options)
        return driver

    def add_cookies(self):
        self.driver.add_cookie({
            "name": "favorite_login_method",
            "value": "userpass",
            "path": "/",
            "secure": False,
        })
        self.driver.add_cookie({
            "name": "cookieconsent_status",
            "value": "dismiss",
            "path": "/",
            "secure": False
        })

    def perform_login(self):
        wait = WebDriverWait(self.driver, 10)
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ContentDiv > div:nth-child(3) > div > div.ng-isolate-scope > ul > li:nth-child(2) > a")))
        login_button.click()

        username_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#txt_Username")))
        password_field = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#txt_Password")))

        self.take_screenshot("PrøverAtFindeloginelementer.png")

        username_field.send_keys("smhj@ufm.dk")
        password_field.send_keys("Confirm92222")

        self.take_screenshot("ErDerINformationer.png")

    def check_login_success(self):
        wait = WebDriverWait(self.driver, 10)
        try:
            welcome_message = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Velkommen til e-grant.dk')]")))
            if welcome_message:
                print("Login successful")
            else:
                print("Login failed")
        except Exception as e:
            self.take_screenshot("welcome_message_error.png")
            print(f"Login failed: {e}")

    def take_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    @task
    def login(self):
        self.driver.get("https://login.e-grant.dk/?wa=wsignin1.0&wtrealm=urn%3aTilskudsPortal&wctx=https%3a%2f%2fwww.e-grant.dk%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3dhttps%3a%2f%2fwww.e-grant.dk%2f")

        self.add_cookies()
        time.sleep(3)  # Consider replacing with explicit waits if needed
        self.take_screenshot("Start_Picture.png")
        
        self.perform_login()


        self.check_login_success()

class WebsiteUser(User):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

if __name__ == "__main__":
    run_single_user(WebsiteUser)
