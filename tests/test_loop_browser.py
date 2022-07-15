from flerovium import Flerovium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import unittest


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.python.org")

    def tearDown(self):
        self.driver.close

    def test_find_by_label(self):
        flerovium = Flerovium(self.driver)
        e = flerovium.find_by_label("About")
        e.click()
        assert self.driver.title == "About Python™ | Python.org"
