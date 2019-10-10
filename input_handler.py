import argparse


class InputHandler:
    def __init__(self):
        self.args = None
        self.amount = None
        self.input_currency = None
        self.output_currency = None
        self.currencies_list = None
        self.supported_currencies = {
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
            "JD": ["JOD"],
            "som": ["KGS", "UZS"],
            "₩": ["KRW"],
            "K.D.": ["KWD"],
            "₸": ["KZT"],
            "RM": ["MYR"],
            ".ر.ع": ["OMR"],
            "S/.": ["PEN"],
            "₱": ["PHP"],
            "zł": ["PLN"],
            "QR": ["QAR"],
            "lei": ["RON"],
            "din.": ["RSD"],
            "p.": ["RUB"],
            "SR": ["SAR"],
            "฿": ["THB"],
            "TL": ["TRY"],
            "NT$": ["TWD"],
            "﷼": ["YER"],
            "R": ["ZAR"]
        }

    def args_parser(self):
        input_parser = argparse.ArgumentParser(allow_abbrev=False)
        input_parser.add_argument(
            "--amount", type=float, required=True, help="amount you want to exchange"
        )
        input_parser.add_argument(
            "--input",
            "--input_currency",
            type=str,
            required=True,
            help="currency code you want to exchange",
        )
        input_parser.add_argument(
            "--output",
            "--output_currency",
            type=str,
            help="currency code you want to get"
        )
        self.args = input_parser.parse_args()
        self.amount = self.args.amount

        self.input_validator()
        self.output_validator()

    def print_inputs(self):
        print(self.args.amount)
        print(self.args.input == "EUR")
        print(self.args.output)

    def input_validator(self):
        if len(self.args.input) == 3:
            for currency in self.supported_currencies.values():
                for country in range(len(currency)):
                    if self.args.input == currency[country]:
                        self.input_currency = self.args.input
        elif self.args.input in self.supported_currencies.keys():
            self.input_currency = self.supported_currencies[self.args.input][0]
        else:
            print("currency not supported")

    def output_validator(self):
        for currency in self.supported_currencies.values():
            for country in range(len(currency)):
                if self.args.output == currency[country]:
                    self.output_currency = self.args.output
        if self.args.output in self.supported_currencies.keys():
            self.output_currency = self.supported_currencies[self.args.output][0]
        else:
            self.output_currency = None

    def get_amount(self):
        return self.amount

    def get_input(self):
        return self.input_currency

    def get_output(self):
        return self.output_currency

    def get_currencies_list(self):
        currencies_list = []
        for currency in self.supported_currencies.values():
            for country in range(len(currency)):
                currencies_list.append(currency[country])
        return currencies_list
