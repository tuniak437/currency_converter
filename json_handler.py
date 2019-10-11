import requests
import json
from _datetime import datetime


class JsonHandler:
    def __init__(self):
        self.rates = JsonHandler.get_latest_rates()

    # todo - fix class

    @classmethod
    def get_latest_rates(cls):
        with open(
            "C:\\Users\\Tuniak\\PycharmProjects\\currency_converter\\rates.json"
        ) as json_file:
            json_file = json.load(json_file)

        if str(json_file["date"]) == str(datetime.today().date()):
            return json_file["rates"]
        else:
            response = requests.get(
                "http://data.fixer.io/api/latest?access_key=b46f14958a22f4d176398a04ed895296&format=1"
            )
            parse_json = response.json()

            with open("rates.json", "w") as json_file:
                json.dump(parse_json, json_file)

            with open("C:\\Users\\Tuniak\\PycharmProjects\\currency_converter\\rates.json") as json_file:
                json_file = json.load(json_file)

            return json_file["rates"]

    def get_rates(self):
        return self.rates

