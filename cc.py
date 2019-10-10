import json

from json_handler import JsonHandler
from input_handler import InputHandler

# TODO - realize what is happening first
# TODO - handle HTTP requests
# TODO - create full list of supported currencies


class CurrencyConverter:
    def __init__(self):
        self.rates = JsonHandler().rates
        ih = InputHandler()
        ih.args_parser()
        self.amount = ih.get_amount()
        self.input = ih.get_input()
        self.output = ih.get_output()
        self.currencies = ih.get_currencies_list()

    def convert(self):
        if self.output is not None:
            ans = self.amount / self.rates[self.input] * self.rates[self.output]
            data = {
                "input": {"amount": self.amount, "currency": self.input},
                "output": {self.output: f"{ans:.2f}"},
            }
            return json.dumps(data, indent=4)
        else:
            temp_data = {}
            for country in self.currencies:
                ans = self.amount / self.rates[self.input] * self.rates[country]
                temp_data.update({country: f"{ans:.2f}"})
            data = {
                "input": {"amount": self.amount, "currency": self.input},
                "output": temp_data,
            }
            return json.dumps(data, indent=4)


if __name__ == "__main__":
    JsonHandler().get_rates()
    cc = CurrencyConverter()
    print(cc.convert())
