import time, os
from locust import HttpUser, task, between, FastHttpUser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebsiteUser(FastHttpUser):  # Single user class for all behavior
    wait_time = between(1, 5)
    logged_in = False

    def on_start(self):
        self.driver = self.initialize_webdriver()
        self.driver.set_window_size(1400, 1000)
        self.set_zoom_level(0.1)
        self.driver.implicitly_wait(5)
        
    def on_stop(self):
        if self.driver:
            self.driver.quit()

    def initialize_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(service=Service(r'Chromedriver\chromedriverArb.exe'), options=chrome_options)
        return driver

    def switch_to_login(self):
        wait = WebDriverWait(self.driver, 5)
        login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ContentDiv > div:nth-child(3) > div > div.ng-isolate-scope > ul > li:nth-child(2) > a")))
        login_button.click()

    def perform_login(self):
        wait = WebDriverWait(self.driver, 5)
        username_input = wait.until(EC.presence_of_element_located((By.ID, 'txt_UserName')))
        username_input.send_keys('sebastianjensen0209@gmail.com')

        password_input = wait.until(EC.presence_of_element_located((By.ID, 'txt_Password')))
        password_input.send_keys('Sebber0209')

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        login_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_GotLoginUsernamePassword')))
        login_button.click()

    def check_login_success(self):
        wait = WebDriverWait(self.driver, 10)
        self.set_zoom_level(0.9)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.logged_in = True 
        
        time.sleep(2)
        self.take_screenshot("pic")

    def take_screenshot(self, filename):
        screenshot_folder = "Pics"
        unique_filename = os.path.join(screenshot_folder, f"{filename}_user_{id(self)}.png")
        self.driver.save_screenshot(unique_filename)

    def set_zoom_level(self, zoom_factor):
        self.driver.execute_script(f"document.body.style.zoom='{zoom_factor}'")

    @task
    def login(self):
        if not self.logged_in:
            self.driver.get("https://login.e-grant.dk/?wa=wsignin1.0&wtrealm=urn%3aTilskudsPortal&wctx=https%3a%2f%2fwww.e-grant.dk%2f_layouts%2f15%2fAuthenticate.aspx%3fSource%3dhttps%3a%2f%2fwww.e-grant.dk%2f")
            self.switch_to_login()
            self.perform_login()
            self.check_login_success()
            
        '''
        if self.logged_in:
            #response = self.client.get("/BrugerRestService.svc/HentBrugerInformation")
            response = self.client.get("/SagRestService.svc/Uddelinger?SprogKultur=en-uk")
            if response.status_code == 200:
                print("Successfully accessed authenticated endpoint")
            else:
                print("Failed to access authenticated endpoint")

        '''
        
if __name__ == "__main__":
    import os
    os.system("locust -f your_script.py --users 100 --spawn-rate 10")
