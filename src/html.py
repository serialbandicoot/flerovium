from selenium import webdriver
from selenium.webdriver.common.by import By
from enum import Enum


class Tag(Enum):

    A = "a"
    INPUT = "input"
    BUTTON = "button"


class HTML:
    @staticmethod
    def get(driver: webdriver, tag: Tag):
        return driver.find_elements(By.TAG_NAME, tag.value)

    @staticmethod
    def find_element_by_link(driver: webdriver, value: str):
        return driver.find_element(By.LINK_TEXT, value)

    @staticmethod
    def find_element_by_name(driver: webdriver, value: str):
        return driver.find_element(By.NAME, value)

    @staticmethod
    def find_element_by_id(driver: webdriver, value: str):
        return driver.find_element(By.ID, value)
