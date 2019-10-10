import requests
import json


class JsonHandler:
    def __init__(self):
        self.rates = JsonHandler.get_latest_rates()

    @classmethod
    def get_latest_rates(cls):
        with open(
            "C:\\Users\\Tuniak\\PycharmProjects\\currency_converter\\rates.json"
        ) as json_file:
            json_file_date = json.load(json_file)["date"]

        response = requests.get(
            "http://data.fixer.io/api/latest?access_key=b46f14958a22f4d176398a04ed895296&format=1"
        )
        parse_json = response.json()
        api_date = parse_json["date"]

        if json_file_date != api_date:
            with open("rates.json", "w") as json_file:
                json.dump(parse_json, json_file)

        return parse_json["rates"]

    def get_rates(self):
        return self.rates
