from random import sample, randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import tempfile
import string
import random
from selenium.common.exceptions import JavascriptException
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import shutil

class HelperCNN:
    
    class_name = []
    style = []
    html  = []
    
    def __init__(self, cnn_name: str, class_id: int, qty=2) -> None:
        self.cnn_name = cnn_name
        self.class_id = class_id
        self.qty = qty

    def button(self, 
               c  = "#ffffff", 
               bc = "#e50a14", 
               fs = "16px", 
               b  = "1px solid #e50a14",
               br = "5px",
               p  = "10px 130px 10px 130px",
               ls = "1px",
               tx = "Login"):
    
        for _ in range(self.qty):
            h1 = "%06x" % randint(0, 0xFFFFFF)
            h2 = "%06x" % randint(0, 0xFFFFFF)
            
            c  = f"#{h1}"
            bc = f"#{h2}"
            fs = f"{sample(list(range(10, 26)),1)[0]}px"

            class_name = h1+h2
            self.class_name.append(f"x_{class_name}")

            self.style.append({
                "color": c,
                "background-color": bc,
                "font-size": fs,
                "border": b,
                "border-radius": br,
                "padding": p,
                "letter-spacing": ls,
                "margin": "20px"
            }) 

            self.html.append(
                f"<button class=\"x_{class_name}\" type=\"button\">{tx}</button>"
            )

            self._get_css()

        return self

    def _get_css(self):

        def key_value(item):
            keys = item.keys()

            style = []
            for key in keys:
                style.append(
                    f"{key}: {item[key]};"
                )
            return ''.join(style)

        self.css = list(map(lambda row: key_value(row), self.style))

    def generate(self):
        if len(self.html) is None and len(self.style) == 0:
            raise Exception("Missing Object and Style")

        style = ""
        main = ""
        head = """
        <html><body>
        """
        style_start = "<style>"
        style_end = "</style>"
        foot = """
        </body></html>
        """
        for idx in range(self.qty):
            style = style + f"""
                    .{self.class_name[idx]} {{
                        {self.css[idx]}
                }}
            """
            main = main + f"""
                       {self.html[idx]}
            """

        doc = head + style_start + style + style_end + main + foot 
        f = open("cnn.html", "w")
        f.write(doc)
        f.close()

        return self

    def create_images(self):
        html_selenium = HTMLSelenium(self.cnn_name, self.class_id)
        html_selenium.create_images()

class HTMLSelenium:
    
    def __init__(self, prefix: str, class_id: int) -> None:
        self.prefix = prefix
        self.class_id = class_id

        options = Options()
        options.headless = True

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_rect(width=1024, height=700)
        self.driver.get("file:///Users/sam.treweek/Projects/flerovium/cnn.html")

    def release_driver_on_loaded(self):
        wait = WebDriverWait(self.driver, 15)
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

    def get(self, tag: str):
        self.release_driver_on_loaded()
        return self.driver.find_elements(By.TAG_NAME, tag)

    def random_string(self):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(10))

    def create_images(self):
        buttons = self.get("BUTTON")
        element_names = []

        #Clean Dir
        self._empty_tmp2()

        for element in buttons:
            file_name = f"{self.prefix.lower()}_{self.random_string()}.png"
            element_names.append(file_name)
            file = os.path.join(tempfile.gettempdir(), file_name)
            f = open(file, "wb")
            f.write(element.screenshot_as_png)
            f.close()
            shutil.move(file, os.path.join(self._get_tmp2_location(), file_name))

        self.create_labels_file(element_names)

    def create_labels_file(self, element_names):
        file = os.path.join(self._get_tmp2_location(), "labels-1.csv")
        f = open(file, "w")
        f.write("file,label\n")
        f.close()

        with open(file, "a") as myfile:
            for ln in element_names:
                line = f"{ln},{self.class_id}\n"
                myfile.write(line)
        
        return {
            "ok": True
        }

    def _empty_tmp2(self):
        dir = self._get_tmp2_location()
        if os.path.exists(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)

    def _get_tmp2_location(self):
        root = os.path.join(os.getcwd(), "keras_notebooks", "auth_data", "tmp2")
        return root
