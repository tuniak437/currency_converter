import argparse

# todo - create route get methods
# todo - find a way to use args


class InputHandler:
    def __init__(self):
        self.args = None
        self.amount = None
        self.input_currency = None
        self.output_currency = None
        self.currencies_list = None
        self.supp_curr = {
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
            "R": ["ZAR"],
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
            help="currency code you want to get",
        )
        self.args = input_parser.parse_args()
        self.amount = self.args.amount

        self.input_validator()
        self.output_validator()

    def input_validator(self):
        if len(self.args.input) == 3:
            for currency in self.supp_curr.values():
                for country in range(len(currency)):
                    if self.args.input == currency[country]:
                        self.input_currency = self.args.input
        elif self.args.input in self.supp_curr.keys():
            if len(self.supp_curr[self.args.input]) > 1:
                self.input_currency = input(
                    f"more currencies under {self.args.input} available, pick one {list(self.supp_curr[self.args.input])}\n"
                )
            else:
                self.input_currency = self.supp_curr[self.args.input][0]
        else:
            print("currency is not supported")

    def output_validator(self):
        if self.args.output in self.get_currencies_list():
            self.output_currency = self.args.output
        elif self.args.output in self.supp_curr.keys():
            if len(self.supp_curr[self.args.output]) > 1:
                self.output_currency = input(
                    f"more currencies under {self.args.output} available, pick one {list(self.supp_curr[self.args.output])}\n"
                )
            else:
                self.output_currency = self.supp_curr[self.args.output][0]
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
        for currency in self.supp_curr.values():
            for country in range(len(currency)):
                currencies_list.append(currency[country])
        return currencies_list
