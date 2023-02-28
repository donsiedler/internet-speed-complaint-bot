import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

PROMISED_DOWNLOAD = 150
PROMISED_UPLOAD = 10

TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")


class InternetSpeedTwitterBot:
    def __init__(self, options, service):
        self.driver = webdriver.Chrome(service=service, options=options)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        # Opens and runs the speed test
        self.driver.get("https://www.speedtest.net/")
        accept_cookies = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_cookies.click()
        test_start = self.driver.find_element(By.CSS_SELECTOR, "div.start-button a")
        test_start.click()

        # Wait for test to finish
        time.sleep(45)

        # Get the test results
        self.down = self.driver.find_element(By.CSS_SELECTOR, "span.download-speed").text
        self.up = self.driver.find_element(By.CSS_SELECTOR, "span.upload-speed").text
        print(f"Download speed: {self.down} Mbps")
        print(f"Upload speed: {self.up} Mbps")

    def tweet_at_provider(self):
        # Open and sign in to Twitter
        self.driver.get("https://twitter.com/login/")
        time.sleep(4)  # Wait for Twitter login page to load
        username_input = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                            '2]/div/div/div[2]/div[2]/div/div/div/div['
                                                            '5]/label/div/div[2]/div/input')
        username_input.send_keys(TWITTER_EMAIL)
        next_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                         '2]/div/div/div[2]/div[2]/div/div/div/div[6]')
        next_button.click()
        time.sleep(2)  # Wait for next login page to load
        try:
            password_input = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                                '2]/div/div/div[2]/div[2]/div[1]/div/div/div['
                                                                '3]/div/label/div/div[2]/div[1]/input')
        except NoSuchElementException:  # Catch unusual activity modal
            username_input_2 = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div['
                                                                  '2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div['
                                                                  '2]/label/div/div[2]/div/input')
            username_input_2.send_keys("SiedlerApp")
            confirm_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                                '2]/div/div/div[2]/div[2]/div[2]/div/div/div/div')
            confirm_button.click()
            time.sleep(2)  # Wait for next login page to load

        password_input = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                                '2]/div/div/div[2]/div[2]/div[1]/div/div/div['
                                                                '3]/div/label/div/div[2]/div[1]/input')
        password_input.send_keys(TWITTER_PASSWORD)
        log_in_button = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div['
                                                           '2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div')
        log_in_button.click()


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # Keeps the browser open!
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())

bot = InternetSpeedTwitterBot(options=chrome_options, service=service)
# bot.get_internet_speed()
bot.tweet_at_provider()
