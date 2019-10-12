import json

from flask import request, Flask

from json_handler import JsonHandler
from input_handler import InputHandler
from decimal import *

# TODO - handle HTTP requests


class CurrencyConverter:
    def __init__(self):
        self.rates = JsonHandler().get_latest_rates()
        self.amount = ih.amount
        self.input = ih.input_currency
        self.output = ih.output_currency
        self.currencies = ih.get_currencies_list

    # @app.route("/", methods=["GET"])
    # def currency_converter(self):
    #     self.amount = request.form.get("amount")
    #     self.input = request.form.get("input_currency")
    #     self.output = request.form.get("output_currency")
    #     print(self.amount, self.input, self.output)

    def convert(self):
        if self.output is None:
            return self.convert_all_currencies()
        else:
            return self.convert_only_output()

    def convert_only_output(self):
        # todo - decimal not fixed
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

    def convert_all_currencies(self):
        temp_data = {}
        for country in self.currencies:
            if self.input == country:
                continue
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
    # app = Flask(__name__)
    cc = CurrencyConverter()
    print(cc.convert())
