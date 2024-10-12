"""
When the app is refreshed it will scan the departures, find the one to staines at 7:37 and display information about that train.
"""
import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('Username')
pw = os.getenv('Password')


def call_api():
    url = 'https://api.rtt.io/api/v1/'
    return requests.get(url + 'json/search/VXH', auth=HTTPBasicAuth(user, pw))


if __name__ == "__main__":
    response = call_api()
    response_json = json.loads(response.text)
    print(response_json)