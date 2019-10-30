import json
import logging
import json_handler
from input_handler import InputHandler
from decimal import Decimal
import os


logging.basicConfig(
    filename=os.path.dirname(__file__) + "/cc.log",
    filemode="a",
    level=logging.INFO,
    format=f"%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)


def convert(amount: float, input_curr: str, output_curr: str = None):
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
        return convert_all_currencies(amount, input_curr)

    return convert_to_output(amount, input_curr, output_curr)


def convert_to_output(amount: float, input_curr: str, output_curr: str):
    ans = (
        Decimal(amount)
        / Decimal(rates[input_curr])
        * Decimal(rates[output_curr])
    )
    data = {
        "input": {"amount": amount, "currency": input_curr},
        "output": {output_curr: f"{ans:.2f}"},
    }
    return data


def convert_all_currencies(amount: float, input_curr: str):
    temp_data = {}
    currencies_list = input_handler.get_currencies_list()
    for currency in currencies_list:
        # skipping iteration of currency we don't need to calculate
        if input_curr == currency:
            continue
        ans = (
            Decimal(amount)
            / Decimal(rates[input_curr])
            * Decimal(rates[currency])
        )
        temp_data.update({currency: f"{ans:.2f}"})

    data = {
        "input": {"amount": amount, "currency": input_curr},
        "output": temp_data,
    }
    return data

    
def indent_and_print(data: dict):
    print(json.dumps(data, indent=4))


rates = json_handler.get_latest_rates()
input_handler = InputHandler()

if __name__ == "__main__":
    input_handler.args_parser()
    args = input_handler
    output_data = convert(args.amount, args.in_currency, args.out_currency)
    indent_and_print(output_data)
