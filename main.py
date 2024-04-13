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
    cursor = connection.cursor()
    cursor.execute("INSERT INTO temperatures VALUES(?,?)", extracted_local)
    connection.commit()


if __name__ == "__main__":
        while True:
            scraped = scrape(URL)
            extracted = extract(scraped)
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
            data_input = dt_string + "," + extracted
            data_input = data_input.split(",")
            store(data_input)
            print(data_input)
            time.sleep(2)
