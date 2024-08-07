import time
from locust import User, task, between, run_single_user
from locust_plugins.users.webdriver import WebdriverUser
from locust_plugins.listeners import RescheduleTaskOnFail
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserBehavior(User):
    wait_time = between(1, 5)

    def on_start(self):
        self.driver = self.initialize_webdriver()
        self.driver.set_window_size(1400, 1000)
        self.set_zoom_level(0.1)
        self.driver.implicitly_wait(5)
        
    def on_stop(self):
        self.driver.quit()

    def initialize_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=Service(r'Chromedriver\chromedriverArb.exe'), options=chrome_options)
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
            "secure": False,
        })

    def switch_to_login(self):
        wait = WebDriverWait(self.driver, 5)
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ContentDiv > div:nth-child(3) > div > div.ng-isolate-scope > ul > li:nth-child(2) > a")))
        login_button.click()
        self.take_screenshot("1. LoginPane.png")

    def perform_login(self):
        wait = WebDriverWait(self.driver, 5)

        username_input = wait.until(EC.presence_of_element_located((By.ID, 'txt_UserName')))
        username_input.send_keys('sebastianjensen0209@gmail.com')

        password_input = wait.until(EC.presence_of_element_located((By.ID, 'txt_Password')))
        password_input.send_keys('Sebber0209')

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        self.take_screenshot("2. ErDerINformationer.png")
        
        #password_input.send_keys(Keys.RETURN)


        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.take_screenshot("3. blev der logget ind?.png")


        print("login button touch ting")
        #login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='btn_GotLoginUsernamePassword']")))
        login_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_GotLoginUsernamePassword')))
        
        print("find ting")
        login_button.click()
        print("fandt ting")
        self.take_screenshot("3. blev der logget ind?.png")

        
    def check_login_success(self):
        wait = WebDriverWait(self.driver, 10)
        self.set_zoom_level(0.9)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

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

    def set_zoom_level(self, zoom_factor):
        self.driver.execute_script(f"document.body.style.zoom='{zoom_factor}'")

    @task
    def login(self):
        self.driver.get("https://login.e-grant.dk/?wa=wsignin1.0&wtrealm=urn%3aTilskudsPortal&wctx=https%3a%2f%2fwww.e-grant.dk%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3dhttps%3a%2f%2fwww.e-grant.dk%2f")
        self.add_cookies()
        self.switch_to_login()
        self.perform_login()
        self.check_login_success()

class WebsiteUser(User):
    tasks = [UserBehavior]
    wait_time = between(1, 5)

if __name__ == "__main__":
    run_single_user(WebsiteUser)
