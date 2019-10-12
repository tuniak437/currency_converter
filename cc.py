import json

from flask import request, Flask

from json_handler import JsonHandler
from input_handler import InputHandler
from decimal import *

# TODO - handle HTTP requests


class CurrencyConverter:
    def __init__(self):
        self.rates = JsonHandler().get_latest_rates()
        self.currencies = None

    def convert(self, amount, input_curr, output_curr=None):
        if output_curr is None:
            return self.convert_all_currencies(amount, input_curr)
        else:
            return self.convert_only_output(amount, input_curr, output_curr)

    def convert_only_output(self, amount, input_curr, output_curr):
        # todo - decimal not fixed
        ans = (
                Decimal(amount)
                / Decimal(self.rates[input_curr])
                * Decimal(self.rates[output_curr])
        )
        data = {
            "input": {"amount": amount, "currency": input_curr},
            "output": {output_curr: f"{ans:.2f}"},
        }
        return json.dumps(data, indent=4)

    def convert_all_currencies(self, amount, input_curr):
        temp_data = {}
        for country in self.currencies:
            if input_curr == country:
                continue
            ans = (
                    Decimal(amount)
                    / Decimal(self.rates[input_curr])
                    * Decimal(self.rates[country])
            )
            temp_data.update({country: f"{ans:.2f}"})

        data = {
            "input": {"amount": amount, "currency": input_curr},
            "output": temp_data,
        }
        return json.dumps(data, indent=4)


if __name__ == "__main__":
    ih = InputHandler()
    ih.args_parser()
    cc = CurrencyConverter()
    cc.currencies = ih.get_currencies_list()
    print(cc.convert(ih.amount, ih.input_currency, ih.output_currency))
