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
        self.driver.get("https://www.ted.com")

    def tearDown(self):
        self.driver.close()

    def test_sign_in(self):
        fl = Flerovium(self.driver)
        fl.find_by_label("Sign In").click()
        fl.find_by_label("Email Address", Tag.INPUT).send_keys("hello")
        text = fl.find_by_label("Email Address").text()
        assert text == "hello"

    def test_sign_in_by_cnn(self):
        fl = Flerovium(self.driver)
        fl.find_by_cnn("Sign In").click()
