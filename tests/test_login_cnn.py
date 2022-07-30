from flerovium import Flerovium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import unittest


class TestFindByLabel(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.close()

    def test_login_cnn(self):
        sites = [
            "http://en.wikipedia.org",
            "http://wordpress.org",
            "http://mozilla.org",
            "http://whatsapp.com",
            "https://www.educative.io",
            "https://www.adobe.com/uk/",
            "https://t.me/",
            "https://vimeo.com/",
            "https://vk.com/",
            "https://uol.com.br/",
            "https://facebook.com/",
            "https://github.com/",
            "https://amazon.com/"
        ]
        for site in sites:
            self.driver.get(site)
            fl = Flerovium(self.driver)
            fl.cnn("Log in", site)
