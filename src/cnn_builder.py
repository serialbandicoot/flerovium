import argparse
import csv
import os
import queue
import threading
import time
import requests
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from flerovium import Flerovium

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
            domain = item["Domain"]
            print(f"Extract {domain}")
            _extracted_list(extract, item["Domain"])
            time.sleep(1)

            # find_by_label item['Domain']
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(options=options)
            options.add_argument(
                "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
            )
            url = f"http://www.{item['Domain']}"
            print(url)
            
            request = requests.get(url)
            if request.status_code == 200:
                driver.get(url)
                fl = Flerovium(driver=driver)
                fl._cnn(label, item["Domain"], save_path)
                driver.close()
            else:
                print(f"Invalid url {url}")

            q.task_done()

    threads = [
        threading.Thread(target=worker, daemon=True)
        for i in range(size_of_threads_pool)
    ]
    for t in threads:
        t.start()

    for item in _get_file(file):
        if _check(extract, item["Domain"]) is False:
            q.put(item)

    q.join()
    print("CNN Has completed")
