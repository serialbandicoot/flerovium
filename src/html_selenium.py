from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import JavascriptException, TimeoutException, ElementNotInteractableException, InvalidSelectorException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from src.tag import Tag


class HTMLSelenium:
    @staticmethod
    def get(driver: webdriver, tag: Tag):
        HTMLSelenium.release_driver_on_loaded(driver)
        return driver.find_elements(By.TAG_NAME, tag.value)

    @staticmethod
    def find_element_by_link(driver: webdriver, value: str, logging=False):
        HTMLSelenium.release_driver_on_loaded(driver)
        try:
            HTMLSelenium._wait(driver).until(
                EC.presence_of_element_located((By.LINK_TEXT, value))
            )
            HTMLSelenium.scroll_into_view(driver, driver.find_element(By.LINK_TEXT, value))
            return driver.find_element(By.LINK_TEXT, value)
        except (TimeoutException, ElementNotInteractableException):
            print("Timeout Exception - Continue")

        return None

    @staticmethod
    def find_element_by_name(driver: webdriver, value: str):
        HTMLSelenium.release_driver_on_loaded(driver)
        HTMLSelenium._wait(driver).until(
            EC.presence_of_element_located((By.NAME, value))
        )
        return driver.find_element(By.NAME, value)

    @staticmethod
    def find_element_by_id(driver: webdriver, value: str):
        HTMLSelenium.release_driver_on_loaded(driver)
        HTMLSelenium._wait(driver).until(EC.presence_of_element_located((By.ID, value)))
        return driver.find_element(By.ID, value)

    @staticmethod
    def find_element_by_class_name(driver: webdriver, value: str):
        if len(value.split()) > 0:
            value = "." + '.'.join(value.split())
            by = By.CSS_SELECTOR
        else:
            by = By.CLASS_NAME

        HTMLSelenium.release_driver_on_loaded(driver)
        try:
            HTMLSelenium._wait(driver).until(
                EC.presence_of_element_located((by, value))
            )
            HTMLSelenium.scroll_into_view(driver, driver.find_element(by, value))
            return driver.find_element(by, value)
        except (InvalidSelectorException, TimeoutException):
            print("Timeout Exception - Continue")

        return None

    @staticmethod
    def release_driver_on_loaded(driver: webdriver):
        wait = HTMLSelenium._wait(driver)
        jquery, document_ready = False, False
        try:
            wait.until(
                lambda driver: driver.execute_script("return jQuery.active == 0")
                == True
            )
        except JavascriptException as e:
            jquery = True
            pass

        try:
            wait.until(
                lambda driver: driver.execute_script("return document.readyState")
                == "complete"
            )
            sleep(0.1)  # Race condition!
            document_ready = True
        except Exception as e:
            e
            pass

        if jquery and document_ready:
            return

    @staticmethod
    def _wait(driver):
        return WebDriverWait(driver, 15)

    @staticmethod
    def scroll_into_view(driver, element):
        actions = ActionChains(driver)
        actions.move_to_element(element)
        actions.perform()

    @staticmethod
    def send_keys(driver: webdriver, element, value: str):
        driver.execute_script(f"arguments[0].value='{value}';", element)
