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
        flerovium = Flerovium(self.driver)
        e = flerovium.find_by_label("About")
        e.click()
        assert self.driver.title == "About Python™ | Python.org"

    def test_find_by_label_downloads(self):
        flerovium = Flerovium(self.driver)
        e = flerovium.find_by_label("Downloads")
        e.click()
        assert self.driver.title == "Download Python | Python.org"

    def test_find_by_label_community(self):
        flerovium = Flerovium(self.driver)
        e = flerovium.find_by_label("Community")
        e.click()
        assert self.driver.title == "Community | Python.org"

    def test_find_by_label_search(self):
        flerovium = Flerovium(self.driver)
        search = flerovium.find_by_label("Search")
        search.send_keys("Arrays")
        go = flerovium.find_by_label("Go")
        go.click()
        assert (
            self.driver.current_url == "https://www.python.org/search/?q=Arrays&submit="
        )
