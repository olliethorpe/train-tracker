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


def find_service(response: dict):
    # Extract services
    if services := response.get("services"):
        print(f"Found {len(services)} services.")
    else:
        print("Could not find services in response.")

    # Validate service against model
    for s in services:
        service = Service(**s)  # Validating every service is quite cumbersome, should use a light-weight check first
        platform = service.location_detail.platform
        origin = service.location_detail.origin[0].description
        destination = service.location_detail.destination[0].description
        scheduled_arrival = service.location_detail.scheduled_arrival
        scheduled_departure = service.location_detail.scheduled_departure
        actual_arrival = service.location_detail.scheduled_arrival
        actual_departure = service.location_detail.actual_departure

        service_string = f"""
The service from {origin} to {destination} is departing Vauxhall at {actual_departure}.

Information
===================
It will arrive at Platform {platform} at {actual_arrival}.
It was scheduled to depart at {scheduled_departure}.
This train is {'LATE' if actual_departure != scheduled_departure else 'ON TIME'}.

"""
        print(service_string)
        break
    return


if __name__ == "__main__":
    response = call_api(mock=True, write_mock_data=False)
    result = find_service(response)
    print(result)
