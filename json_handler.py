import requests
import json
from datetime import datetime
from requests import RequestException
import logging
import redis


def get_latest_rates():
    """
    This function checks if rates in redis are up-to-date. If not,
    it tries to request new data from 'http://data.fixer.io'. If
    that fails, program will load the latest rates saved in redis.
    :return: only "rates" part of the JSON
    """
    rates_json = load_from_redis(r.get("rates"))
    if rates_json["date"] == str(datetime.today().date()):
        return rates_json["rates"]
    try:
        r.set("rates", save_to_redis())
        return load_from_redis(r.get("rates"))
    except RequestException:
        logging.error("Unable to get latest rates from 'http://data.fixer.io'")
        return rates_json["rates"]


def save_to_redis():
    response = requests.get(
        "http://data.fixer.io/api/latest?access_key=b46f14958a22f4d176398a04ed895296&format=1"
    )
    logging.info("New rates requested and saved successfully")
    return json.dumps(response.json())


def load_from_redis(rates: str):
    return json.loads(rates)


r = redis.Redis(decode_responses=True)
