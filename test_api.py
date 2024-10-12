"""
When the app is refreshed it will scan the departures, find the one to staines at 7:37 and display information about that train.
"""

# 3rd party
import requests
from requests.auth import HTTPBasicAuth
import json
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path

# Local
from service_model import Service

load_dotenv()

user = os.getenv("Username")
pw = os.getenv("Password")


# Morning train info
EXPECTED_TIME = datetime.strptime(os.getenv("expected_train_time"), "%H:%M")
EXPECTED_START_STN_CD = os.getenv("expected_start_station")
EXPECTED_END_STN_CD = os.getenv("expected_end_station")


def call_api(mock=True, write_mock_data=False) -> dict:
    """_summary_

    Args:
        mock (bool, optional): _description_. Defaults to True.
        write_mock_data (bool, optional): _description_. Defaults to False.

    Returns:
        dict: _description_
    """
    # Reduce api load by mocking response
    mock_data_path = "./example_response.json"
    if mock and Path(mock_data_path).exists():
        with open(mock_data_path) as f:
            res = json.load(f)
        print("Using mock data")
        return res

    url = "https://api.rtt.io/api/v1/"
    r = requests.get(url + "json/search/VXH", auth=HTTPBasicAuth(user, pw))
    response = r.text

    if write_mock_data:
        print("Writing mock data")
        with open(mock_data_path, "w") as f:
            f.write(response)

    return json.loads(response)


def parse_response(response: dict):
    # Extract services
    if services := response.get("services"):
        print(f"Found {len(services)} services.")
    else:
        print("Could not find services in response.")

    # Validate service against model
    for s in services:
        service = Service(**s)
        platform = service.location_detail.platform
        origin = service.location_detail.origin[0].description
        scheduled_arrival = service.location_detail.scheduled_arrival
        scheduled_departure = service.location_detail.scheduled_departure
        actual_departure = service.location_detail.actual_departure
        print(f"There is a train departing from Platform {platform} at {actual_departure}.")
        print(scheduled_arrival)
        print(actual_departure)
        break
    return {}


if __name__ == "__main__":
    response = call_api(mock=False, write_mock_data=True)
    result = parse_response(response)
    print(result)
