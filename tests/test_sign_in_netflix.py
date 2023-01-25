from time import sleep
from flerovium import Flerovium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import unittest

from src.tag import Tag


class TestFindByLabel(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_rect(width=1024, height=700)
        self.driver.get("https://www.netflix.com")

        
    def tearDown(self):
        self.driver.close()

    def test_sign_in(self):
        fl = Flerovium(self.driver)
        fl.logging_mode = True
        fl.find_by_label("Accept").click()
        fl.find_by_cnn("Sign In").click()
        fl.find_by_label("Email or phone number").send_keys("sam@test.com")
        fl.find_by_label("Password").send_keys("pass")
        fl.find_by_cnn("Sign In").click()
        fl.screenshot()
        