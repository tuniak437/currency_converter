import requests
import json
from _datetime import datetime
from requests import RequestException
import logging
import os


class JsonHandler:

    @staticmethod
    def get_latest_rates():
        """
        This method checks if our 'rates.json' file is up-to-date. If not,
        it tries to request new data from 'http://data.fixer.io'. If that
        fails, program will load the newest file possible as a backup.

        Getting rates in JSON format:
        {
          "success":true,
          "timestamp":1571165347,
          "base":"EUR",
          "date":"2019-10-15",
          "rates":{
            "AED":4.051446,
            "AFN":86.313569,
            .
            .
            .
            }
        }

        :return: only "rates" part of the JSON
        """
        with open(os.path.dirname(__file__) + "/rates.json") as json_file:
            json_file = json.load(json_file)

        # checking if our json file is up-to-date
        if str(json_file["date"]) == str(datetime.today().date()):
            return json_file["rates"]
        else:
            try:
                JsonHandler.request_and_save_data()
                with open(
                    os.path.dirname(__file__) + "/rates.json"
                ) as updated_json_file:
                    return json.load(updated_json_file)["rates"]

            except RequestException:
                logging.error("Unable to get latest rates from 'http://data.fixer.io'")
                with open(os.path.dirname(__file__) + "/rates.json") as json_file:
                    old_json_file = json.load(json_file)
                    print(
                        "Unable to get latest rates. Using rates from:",
                        old_json_file["date"],
                    )
                    return old_json_file["rates"]

    @staticmethod
    def request_and_save_data():
        response = requests.get(
            "http://data.fixer.io/api/latest?access_key=b46f14958a22f4d176398a04ed895296&format=1"
        )
        parse_json = response.json()

        with open(os.path.dirname(__file__) + "/rates.json", "w") as json_file:
            json.dump(parse_json, json_file)
        logging.info("New rates requested and saved successfully")

