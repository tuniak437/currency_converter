import logging
from flask import Flask, request, jsonify
import cc

app = Flask(__name__)


class BadRequest(Exception):
    def __init__(self, message, status, payload=None):
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
        raise_empty_parameter("amount")
    elif not request.args.get("input_currency"):
        raise_empty_parameter("input_currency")


def raise_empty_parameter(par):
    logging.error(f"Parameter '{par}' empty")
    raise BadRequest(f"parameter '{par}' cannot be empty", 400, {"exit_code_number": 1})


def raise_wrong_input():
    # No need to log this error. Method find_currency in input_handler
    # already logging ValueError exception.
    raise BadRequest("Invalid or not supported parameter", 400, {"exit_code_number": 1})


def raise_wrong_type(amount):
    logging.error(f"Invalid value for parameter 'amount'={amount}")
    raise BadRequest(f"parameter 'amount' cannot be '{amount}'", 400, {"exit_code_number": 1})


@app.route("/currency_converter", methods=["GET"])
def currency_converter():
    """
    This function calls error_handler() function to check if all required
    parameters are provided. Then the function checks if parameter
    'amount' can be casted into float type.

    :return: Calculated rates in JSON format
    """
    error_handler()
    amount = request.args.get("amount")
    try:
        amount = float(amount)
    except ValueError:
        raise_wrong_type(amount)
    input_curr = str(request.args.get("input_currency"))
    output_curr = str(request.args.get("output_currency"))

    try:
        return parse_parameters(amount, input_curr, output_curr)
    except ValueError:
        raise_wrong_input()


def parse_parameters(amount, input_curr, output_curr):
    inp = cc.input_handler.find_currency(input_curr)
    out = cc.input_handler.output_validator(output_curr)
    return cc.convert(amount, inp, out)


if __name__ == "__main__":
    app.run()
