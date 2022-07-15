from selenium import webdriver
from selenium.webdriver.common.by import By
from enum import Enum


class Tag(Enum):

    A = "a"


class HTML:
    @staticmethod
    def get(driver: webdriver, tag: Tag):
        return driver.find_elements(By.TAG_NAME, tag.value)
