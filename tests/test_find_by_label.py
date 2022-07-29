from flerovium import Flerovium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import unittest


class TestFindByLabel(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.python.org")

    def tearDown(self):
        self.driver.close()

    def test_find_by_label_about(self):
        fl = Flerovium(self.driver)
        fl.find_by_label("About").click()
        assert self.driver.title == "About Python™ | Python.org"

    def test_find_by_label_downloads(self):
        fl = Flerovium(self.driver)
        fl.find_by_label("Downloads").click()
        assert self.driver.title == "Download Python | Python.org"

    def test_find_by_label_community(self):
        fl = Flerovium(self.driver)
        fl.find_by_label("Community")
        fl.click()
        assert self.driver.title == "Community | Python.org"

    def test_find_by_label_search(self):
        fl = Flerovium(self.driver)
        fl.find_by_label("Search").send_keys("Arrays")
        fl.find_by_label("Go").click()
        assert (
            self.driver.current_url == "https://www.python.org/search/?q=Arrays&submit="
        )
