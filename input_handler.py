import argparse
import logging


class InputHandler:
    def __init__(self):
        self.amount = None
        self.in_currency = None
        self.out_currency = None
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
        # todo - handle wrong inputs
        args = input_parser.parse_args()
        self.amount = args.amount
        self.in_currency = self.find_currency(args.input)
        self.out_currency = self.output_validator(args.output)

    def output_validator(self, arg):
        # if parsed argument is empty, API returns str="None"
        if arg is None or arg == "None":
            return None
        else:
            return self.find_currency(arg)

    def find_currency(self, arg):
        if arg in self.get_currencies_list():
            return arg
        elif arg in self.supp_curr.keys():
            if len(self.supp_curr[arg]) > 1:
                inp = input(
                    f"more currencies under {arg} available, pick one "
                    f"{list(self.supp_curr[arg])}\n"
                )
                return inp.upper()
            else:
                return self.supp_curr[arg][0]
        else:
            logging.error("ValueError - Entered currency is not supported.")
            raise ValueError("Entered currency is not supported.")

    def get_currencies_list(self):
        currencies_list = []
        for currency in self.supp_curr.values():
            for country in range(len(currency)):
                currencies_list.append(currency[country])
        return currencies_list
