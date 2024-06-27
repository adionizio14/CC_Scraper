from selenium import webdriver
import time
import webbrowser

class Startup:

    def __init__(self) -> None:
        
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
        self.chrome_options.add_argument("--window-size=1920x1080")  # Set a larger window size
        self.chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        self.chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection
        self.chrome_options.add_argument("--log-level=3")  # Suppress logs

    def start_driver(self):
        
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get('https://login.cmdgroup.com/Account/Login?immediate=false')
        time.sleep(2)
        self.login()
        return self.driver

    def login(self):

        self.email = self.driver.find_element('id', 'txtUserName')
        self.email.send_keys("adionizio@specifiedbuilding.com")
        self.password = self.driver.find_element('id', 'txtPassword')
        self.password.send_keys("GHQjlm2023!")
        self.driver.find_element('id', 'btnLogon').click()


