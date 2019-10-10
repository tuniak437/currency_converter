import json

from json_handler import JsonHandler
from input_handler import InputHandler

# TODO - split to files
# TODO - create classes
# TODO - realize what is happening first
# TODO - handle HTTP requests
# TODO - create full list of supported currencies
import json_handler

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
        self.rates = JsonHandler().rates
        self.inputs = InputHandler()

    def convert(self):
        ans = (
            self.inputs.get_amount()
            / self.rates[self.inputs.get_input()]
            * self.rates[self.inputs.get_output()]
        )
        data = {
            "input": {
                "amount": self.inputs.get_amount(),
                "currency": self.inputs.get_input(),
            },
            "output": {self.inputs.get_output(): f"{ans:.2f}"},
        }

        return json.dumps(data, indent=4)


def validate_inputs():
    pass


oh = InputHandler()
oh.args_parser()
JsonHandler().get_rates()
cc = CurrencyConverter()
print(cc.convert())





