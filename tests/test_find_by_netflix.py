from time import sleep
from flerovium import Flerovium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import unittest


class TestFindByLabel(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_rect(width=1024, height=700)
        self.driver.get("https://www.webs.com")

    def tearDown(self):
        self.driver.close()

    def test_sign_in(self):

        fl = Flerovium(self.driver)
        fl.find_by_label("Sign In").click()
        # fl.find_by_label("Email Address").send_keys("sam.treweek@bjss.com")
        # fl.find_by_label("Continue").click()
