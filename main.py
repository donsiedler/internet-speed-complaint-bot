import os
import time

from selenium import webdriver
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
        pass


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # Keeps the browser open!
chrome_options.add_argument("--start-maximized")
service = Service(ChromeDriverManager().install())

bot = InternetSpeedTwitterBot(options=chrome_options, service=service)
bot.get_internet_speed()
bot.tweet_at_provider()
