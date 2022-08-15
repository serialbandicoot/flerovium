from cProfile import label
from dataclasses import dataclass
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@dataclass
class Button:
    id: str
    label: str
    background_color: str
    color: str
    padding: str
    text_align: str
    font_size: str
    font_family: str
    border: str


def remove(file_name: str):
    if os.path.exists(file_name):
        os.remove(file_name)


def create_file(file_name: str, content: str):
    remove(file_name)

    f = open(file_name, "a")
    f.write(content)
    f.close()


def random_color():
    c = "%06x" % random.randint(0, 0xFFFFFF)
    return f"#{c};"


def random_padding():
    x = random.randint(5, 30)
    y = random.randint(5, 50)
    return f"{x}px {y}px;"


def text_align():
    ta = random.choice(["center", "left", "right"])
    return f"{ta};"


def font_size():
    return f"{random.randint(6, 30)}px;"


def border():
    return f"{random.randint(0, 4)}px solid {random_color}"


def font_family():
    ff = random.choice(
        [
            "Arial (sans-serif)",
            "Verdana (sans-serif)",
            "Helvetica (sans-serif)",
            "Tahoma (sans-serif)",
            "Trebuchet MS (sans-serif)",
            "Times New Roman (serif)",
            "Georgia (serif)",
            "Garamond (serif)",
            "Courier New (monospace)",
            "Brush Script MT (cursive)",
        ]
    )
    return f"{ff};"


def label_case(label):
    rr = random.randint(0, 3)
    if rr == 0:
        return label.upper()
    elif rr == 1:
        return label.lower()
    elif rr == 2:
        return label.title()
    else:
        return label


def create_button(label: str):
    i = "".join(random.choices(string.ascii_uppercase, k=5))
    l = label_case(label)
    bc = random_color()
    c = random_color()
    p = random_padding()
    ta = text_align()
    fs = font_size()
    ff = font_family()
    b = border()
    return Button(i, l, bc, c, p, ta, fs, ff, b)


def create_button_html(label):
    button = create_button(label)
    html = f"""
          <STYLE>
            .button-{button.id} {{
              background-color: {button.background_color}
              color:  {button.color}
              padding: {button.padding}
              text-align: {button.text_align}
              font-size: {button.font_size}
              font-family: {button.font_family}
              border: {button.border}
            }}
          </STYLE>
          <input id=\"{button.id}\" type=\"button\" class=\"button-{button.id}\" value=\"{button.label}\">
      """
    return html


def create_html(file_name: str, label: str, no_buttons: int = 5):
    html = []
    for _ in range(0, no_buttons):
        html.append(create_button_html(label))
    create_file(file_name, "".join(html))


def create_image_from_element(file: str, element):
    f = open(f"temp_images/img_dir/{file}", "wb")
    f.write(element.screenshot_as_png)
    f.close()


def create_csv(file_name: str):
    remove(file_name)
    f = open(f"temp_images/{file_name}", "w")
    f.write("file,label\n")
    f.close()


def write_label_row(file_name: str, row):
    f = open(f"temp_images/{file_name}", "a")
    f.write(f"{row}\n")
    f.close()


def create_data(file_name: str):
    options = Options()
    options.headless = True
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(file_name)

    buttons = driver.find_elements(By.TAG_NAME, "input")
    # create_csv("labels.csv")
    for button in buttons:
        fi = f"Log-in-{button.id[0:8]}.png"
        write_label_row("labels.csv", f"{fi},1")
        create_image_from_element(fi, button)


f = "sign_up.html"
bf = "file:///Users/sam.treweek/Projects/flerovium/sign_up.html"
create_html(f, "Log in", 1000)
create_data(bf)
