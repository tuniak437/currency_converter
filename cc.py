import json
import logging
import pysnooper

from json_handler import JsonHandler
from input_handler import InputHandler
from decimal import *
from _datetime import datetime

# TODO - handle HTTP requests
# TODO - documentation
# TODO - refactor, refactor, refactor

# todo - better naming

logging.basicConfig(
    filename="C:\\Users\\Tuniak\\PycharmProjects\\currency_converter\\cc.log",
    filemode="w",
    level=logging.INFO,
    format=f"%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


class CurrencyConverter:
    def __init__(self):
        self.rates = JsonHandler().get_latest_rates()
        self.input_handler = InputHandler()

    def convert(self, amount, input_curr, output_curr=None):
        if output_curr is None or output_curr == "None":
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
        currencies_list = self.input_handler.get_currencies_list()
        for currency in currencies_list:
            # skipping iteration of currency we don't need to calculate
            if input_curr == currency:
                continue
            ans = (
                Decimal(amount)
                / Decimal(self.rates[input_curr])
                * Decimal(self.rates[currency])
            )
            temp_data.update({currency: f"{ans:.2f}"})

        data = {
            "input": {"amount": amount, "currency": input_curr},
            "output": temp_data,
        }
        return json.dumps(data, indent=4)


if __name__ == "__main__":
    cc = CurrencyConverter()
    cc.input_handler.args_parser()
    args = cc.input_handler
    # todo - figure print method only for CLI app
    print(cc.convert(args.amount, args.in_currency, args.out_currency))
