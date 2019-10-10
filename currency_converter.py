import json
import argparse
import requests

# TODO - split to files
# TODO - create classes
# TODO - realize what is happening first
# TODO - handle HTTP requests
# TODO - create full list of supported currencies

supported_currencies = {
    "Kč": ["CZK"],
    "€": ["EUR"],
    "$": ["USD", "CAD", "AUD", "NZD", "SGD", "MXN", "CLP"],
    "£": ["GBP"],
    "SFr.": ["CHF"],
    "kr": ["SEK", "DKK", "NOK", "ISK"],
    "¥": ["JPY", "CNY"],
    "د.إ": ["AED"],
    "֏": ["AMD"],
    "BD": ["BHD"],
    "R$": ["BRL"],
    "Br": ["BYN"],
    "HK$": ["HKD"],
    "Ft": ["HUF"],
    "Rp": ["IDR"],
    "₪": ["ILS"],
    "₹": ["INR"],
}


class CurrencyConverter:
    def __init__(self):
        self.args = None
        self.amount = None
        self.input_currency = None
        self.output_currency = None
        self.rates = CurrencyConverter.get_latest_rates()

    def args_parser(self):
        input_parser = argparse.ArgumentParser(allow_abbrev=False)
        input_parser.add_argument(
            "--amount", type=float, required=True, help="amount you want to exchange"
        )
        input_parser.add_argument(
            "--input",
            "--input_currency",
            required=True,
            help="currency code you want to exchange",
        )
        input_parser.add_argument(
            "--output", "--output_currency", help="currency code you want to get"
        )
        self.args = input_parser.parse_args()
        self.amount = self.args.amount
        self.input_currency = self.args.input
        self.output_currency = self.args.output

    def convert(self):
        ans = (
            self.amount
            / self.rates[self.input_currency]
            * self.rates[self.output_currency]
        )
        data = {
            "input": {"amount": self.amount, "currency": self.input_currency},
            "output": {self.output_currency: f"{ans:.2f}"},
        }

        return json.dumps(data, indent=4)

    @staticmethod
    def get_latest_rates():
        with open(
            "C:\\Users\\Tuniak\\PycharmProjects\\currency_converter\\rates.json"
        ) as json_file:
            json_file_date = json.load(json_file)["date"]

        response = requests.get(
            "http://data.fixer.io/api/latest?access_key=b46f14958a22f4d176398a04ed895296&format=2"
        )
        parse_json = response.json()
        api_date = parse_json["date"]

        if json_file_date != api_date:
            with open("rates.json", "w") as json_file:
                json.dump(parse_json, json_file)

        return parse_json["rates"]


def validate_inputs():
    pass


us = CurrencyConverter()
us.args_parser()
print(us.convert())
