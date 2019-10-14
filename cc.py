import json

import pysnooper

from json_handler import JsonHandler
from input_handler import InputHandler
from decimal import *

# TODO - handle HTTP requests
# TODO - documentation
# TODO - refactor, refactor, refactor


class CurrencyConverter:
    def __init__(self):
        self.rates = JsonHandler().get_latest_rates()
        self.input_handler = InputHandler()
        self.currencies = self.input_handler.get_currencies_list()

    def convert(self, amount, input_curr, output_curr=None):
        if output_curr is None:
            return self.convert_all_currencies(amount, input_curr)
        else:
            return self.convert_to_output(amount, input_curr, output_curr)

    def convert_to_output(self, amount, input_curr, output_curr):
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
            # we don't need to calculate same currency in/out
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
    cc = CurrencyConverter()
    cc.input_handler.args_parser()
    print(cc.convert(cc.input_handler.amount, cc.input_handler.in_currency, cc.input_handler.out_currency))
