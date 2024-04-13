import requests
import selectorlib
import time
from datetime import datetime
import sqlite3

URL = "http://programmer100.pythonanywhere.com/"

connection = sqlite3.connect("data.db")


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["temperature"]
    return value


def store(extracted_local):
    now_local = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temperatures VALUES(?,?)",
                   (now_local, extracted_local))
    connection.commit()


if __name__ == "__main__":
        while True:
            scraped = scrape(URL)
            extracted = extract(scraped)
            store(extracted)
            print(extracted)
            time.sleep(2)
