from selenium import webdriver
import time
import webbrowser
import auth

class Startup:

    def __init__(self) -> None:

        """
        Initalizes settings for the web browser to run in the background
        """
        
        self.keys = auth.Authentication()
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920x1080")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_argument("--log-level=3")

    def start_driver(self):

        """
        Method that starts the chrome web driver
        """
        
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get('https://login.cmdgroup.com/Account/Login?immediate=false')
        time.sleep(2)
        self.login()
        return self.driver

    def login(self):

        """
        Method that uses login credentials to access the CC account
        """

        self.email = self.driver.find_element('id', 'txtUserName')
        self.email.send_keys(self.keys.email)
        self.password = self.driver.find_element('id', 'txtPassword')
        self.password.send_keys(self.keys.password)
        self.driver.find_element('id', 'btnLogon').click()