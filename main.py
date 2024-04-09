import requests
import selectorlib
import time
from datetime import datetime

URL = "http://programmer100.pythonanywhere.com/"


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
    with open("data.txt", "a") as file:
        file.write(extracted_local + "\n")


if __name__ == "__main__":
        while True:
            scraped = scrape(URL)
            extracted = extract(scraped)
            now = datetime.now()
            dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
            data_input = dt_string + "," + extracted
            store(data_input)
            print(data_input)
            time.sleep(2)
