from ast import arg
import os
import csv
import threading
import queue
import time
import argparse
from flerovium import Flerovium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--label", default="label")
parser.add_argument("--file", default="File")
parser.add_argument("--extract", default="Extract File")
parser.add_argument("--save_path", default="Save Path")


def _create_extract(extract):
    fle = Path(extract)
    fle.touch(exist_ok=True)


def _check(extract, url):
    with open(extract) as f:
        d = f.readlines()
        for line in d:
            if url in line:
                return True
        return False


def _extracted_list(extract, site):
    f = open(extract, "a")
    f.write(f"{site}\n")
    f.close()


def _get_file(file: str):
    if os.path.exists(file):
        with open(file, "r") as file:
            in_memory_file = file.read()
        return csv.DictReader(in_memory_file.splitlines())
    else:
        raise Exception("File cannot be found?")


def cli():
    args = parser.parse_args()
    label = args.label
    file = args.file
    extract = args.extract
    save_path = args.save_path

    size_of_threads_pool = 5
    q = queue.Queue()

    _create_extract(extract)

    def worker():
        while True:
            item = q.get()
            print(f"Extract {item}")
            _extracted_list(extract, item["url"])
            time.sleep(1)

            # find_by_label item['url']
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            url = f"https://www.{item['url']}"
            driver.get(url)

            fl = Flerovium(driver=driver)
            fl._cnn(label, item["url"], save_path)
            driver.close()

            q.task_done()

    threads = [
        threading.Thread(target=worker, daemon=True)
        for i in range(size_of_threads_pool)
    ]
    for t in threads:
        t.start()

    for item in _get_file(file):
        if _check(extract, item["url"]) is False:
            q.put(item)

    q.join()
    print("CNN Has completed")
