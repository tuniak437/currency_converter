from flask import Flask, request
from cc import CurrencyConverter
from input_handler import InputHandler
app = Flask(__name__)


@app.route("/currency_converter", methods=["GET"])
def currency_converter():
    amount = float(request.args.get("amount"))
    input_curr = str(request.args.get("input_currency"))
    output_curr = str(request.args.get("output_currency"))
    ih = InputHandler()
    inp = ih.find_currency(input_curr)
    out = ih.output_validator(output_curr)
    cc = CurrencyConverter()
    cc.currencies = ih.get_currencies_list()
    return cc.convert(amount, inp, output_curr)


if __name__ == "__main__":
    app.run()
