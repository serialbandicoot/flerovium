from flerovium import Flerovium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import unittest

class TestCNN(unittest.TestCase):

    def test_cnn(self):

        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.python.org")

        fl = Flerovium(driver = self.driver)
        fl._cnn("About", "python.org")