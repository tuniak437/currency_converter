import json

from flask import request, Flask

from json_handler import JsonHandler
from input_handler import InputHandler
from decimal import *

# TODO - handle HTTP requests


class CurrencyConverter:
    def __init__(self):
        self.rates = JsonHandler().rates
        self.amount = ih.get_amount()
        self.input = ih.get_input()
        self.output = ih.get_output()
        self.currencies = ih.get_currencies_list()

    # @app.route("/", methods=["GET"])
    # def currency_converter(self):
    #     self.amount = request.form.get("amount")
    #     self.input = request.form.get("input_currency")
    #     self.output = request.form.get("output_currency")
    #     print(self.amount, self.input, self.output)

    def convert(self):
        if self.output is not None:
            ans = (
                Decimal(self.amount)
                / Decimal(self.rates[self.input])
                * Decimal(self.rates[self.output])
            )
            data = {
                "input": {"amount": self.amount, "currency": self.input},
                "output": {self.output: f"{ans:.2f}"},
            }
            return json.dumps(data, indent=4)
        else:
            temp_data = {}
            for country in self.currencies:
                ans = (
                    Decimal(self.amount)
                    / Decimal(self.rates[self.input])
                    * Decimal(self.rates[country])
                )
                temp_data.update({country: f"{ans:.2f}"})
            data = {
                "input": {"amount": self.amount, "currency": self.input},
                "output": temp_data,
            }
            return json.dumps(data, indent=4)


if __name__ == "__main__":
    # pass
    ih = InputHandler()
    ih.args_parser()
    app = Flask(__name__)
    JsonHandler().get_rates()
    cc = CurrencyConverter()
    print(cc.convert())
