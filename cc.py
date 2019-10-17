import json
import logging
from json_handler import JsonHandler
from input_handler import InputHandler
from decimal import Decimal
import os

# TODO - refactor, refactor, refactor

logging.basicConfig(
    filename=os.path.dirname(__file__) + "/cc.log",
    filemode="a",
    level=logging.INFO,
    format=f"%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


class CurrencyConverter:
    def __init__(self):
        self.rates = JsonHandler().get_latest_rates()
        self.input_handler = InputHandler()

    def convert(self, amount, input_curr, output_curr=None):
        """
        Based on parameters provided, the convert method determines
        which method to call to convert entered currencies. If
        'output_curr' is not provided, method will convert 'input_curr'
        to every supported currency.

        :param amount: Entered amount of currency user wants to convert
        :param input_curr: Currency which is already in code format e.g."EUR"
        :param output_curr: same format as 'input_curr' if provided
        :return: calculated currencies in JSON format
        """
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
    print(cc.convert(args.amount, args.in_currency, args.out_currency))
