from flerovium import Flerovium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import unittest


class TestFindByLabel(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
        )

        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.bet365.com")

    def tearDown(self):
        self.driver.close()

    def test_login(self):
        fl = Flerovium(self.driver)
        fl.find_by_label("Log In").click()

        fl.find_by_label("Username")
        fl.send_keys("Sam")
        assert fl.element.get_attribute("value") == "Sam"
