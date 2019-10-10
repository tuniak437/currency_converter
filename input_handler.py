import argparse


class InputHandler:
    def __init__(self):
        self.args = None
        self.amount = None
        self.input_currency = None
        self.output_currency = None
        self.supported_currency = {
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

        self.get_input()
        self.get_output()

    def input_validator(self):
        for currency in self.supported_currency.values():
            if len(currency) > 1:
                for country in currency:
                    if self.input_currency is country:
                        return self.input_currency
            else:
                if self.input_currency is currency[0]:
                    return self.input_currency
        else:
            print("currency not supported")

    def output_validator(self):
        for currency in self.supported_currency.values():
            if len(currency) > 1:
                for country in currency:
                    # print(country)
                    if self.output_currency is country:
                        return self.output_currency
            else:
                print(currency[0] is str(self.output_currency))
                if self.output_currency is currency[0]:
                    return self.output_currency
        else:
            print("currency not supported")

    def get_amount(self):
        return self.amount

    def get_input(self):
        self.input_validator()
        return self.input_currency

    def get_output(self):
        self.output_validator()
        return self.output_currency
