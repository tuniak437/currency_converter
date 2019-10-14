from flask import Flask, request, jsonify
from cc import CurrencyConverter

app = Flask(__name__)


class BadRequest(Exception):
    def __init__(self, message, status=400, payload=None):
        self.message = message
        self.status = status
        self.payload = payload


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    payload = dict(error.payload or ())
    payload["error_message"] = error.message
    payload["status_code"] = error.status
    return jsonify(payload), 400


def error_handler():
    if not request.args.get("amount"):
        raise_error("amount")
    elif not request.args.get("input_currency"):
        raise_error("input_currency")


def raise_error(parameter):
    raise BadRequest(
        f"parameter '{parameter}' cannot be empty", 400, {"exit_code_number": 1}
    )


@app.route("/currency_converter", methods=["GET"])
def currency_converter():
    error_handler()
    amount = float(request.args.get("amount"))
    input_curr = str(request.args.get("input_currency"))
    output_curr = str(request.args.get("output_currency"))
    print(output_curr is "None")
    cc = CurrencyConverter()
    inp = cc.input_handler.find_currency(input_curr)
    out = cc.input_handler.output_validator(output_curr)
    return cc.convert(amount, inp, out)


if __name__ == "__main__":
    app.run()
