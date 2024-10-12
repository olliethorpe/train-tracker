"""
When the app is refreshed it will scan the departures, find the one to staines at 7:37 and display information about that train.
"""

import json
import os
from datetime import time
from pathlib import Path

# 3rd party
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Local
from service_model import Service

load_dotenv()

user = os.getenv("Username")
pw = os.getenv("Password")


# Morning train info
exp_tt = os.getenv("expected_train_time", "12:00")
EXPECTED_DEPARTURE_TIME = time(int(exp_tt[:2]), int(exp_tt[3:]))
SERVICE_START_TIPLOC = os.getenv("expected_start_station")
SERVICE_END_TIPLOC = os.getenv("expected_end_station")
RT_TRAINS_URL = os.getenv('rttrains_url')

SERVICE_DESC = """
The service from {} to {} is departing Vauxhall at {}.

Information
===================
It will arrive at Platform {} at {}.
It was scheduled to depart at {}.
This train is {}.

"""


def get_station_departures(station_code: str, mock=True, write_mock_data=True) -> dict:
    """Get the next hour of scheduled departures for a given station from the real time trains api.

    Args:
        station_code (str): The station of interest.
        mock (bool, optional): For testing. Use a mock data set to avoid request spamming. Defaults to True.
        write_mock_data (bool, optional): Write api response to mock data set. Defaults to False.

    Returns:
        dict: Api response as a json object.
    """
    mock_data_path = "./example_response.json"
    if mock and Path(mock_data_path).exists():
        with open(mock_data_path) as f:
            res = json.load(f)
        print("Using mock data")
        return res

    r = requests.get(RT_TRAINS_URL + f"json/search/{station_code}", auth=HTTPBasicAuth(user, pw))
    response = r.text

    if write_mock_data:
        print("Writing mock data")
        with open(mock_data_path, "w") as f:
            f.write(response)

    return json.loads(response)


def find_service(data: dict, start_tiploc: str, end_tiploc: str, expected_departure: time) -> Service:
    """Return the service with matching start & end tiplocs (location codes) and expected departure time from the real \
    time trains api response.

    Args:
        data (dict): Dict containing service information for given platform.
        start_tiploc (str): Location code of starting station.
        end_tiploc (str): Location code of ending station.
        expected_departure (time): Expected departure time from traget station.

    Raises:
        ValueError: When a matching service cannot be found.
        Exception: When service information is not part of the input data set.

    Returns:
        Service: The service matching the inpout parameters.
    """
    if services := data.get("services"):
        for s in services:
            service = Service(**s)  # Cumbersome?
            if (
                service.location_detail.origin[0].tiploc == start_tiploc
                and service.location_detail.destination[0].tiploc == end_tiploc
                and service.location_detail.scheduled_departure == expected_departure
            ):
                return service

        raise ValueError(
            f"Cannot find service from {start_tiploc} to {end_tiploc} departing station at {expected_departure}"
        )
    raise Exception("Could not find services in response.")


if __name__ == "__main__":
    response = get_station_departures('VXH', mock=False)
    service = find_service(response, SERVICE_START_TIPLOC, SERVICE_END_TIPLOC, EXPECTED_DEPARTURE_TIME)

    platform = service.location_detail.platform
    origin = service.location_detail.origin[0].description
    destination = service.location_detail.destination[0].description
    scheduled_arrival = service.location_detail.scheduled_arrival
    scheduled_departure = service.location_detail.scheduled_departure
    actual_arrival = service.location_detail.scheduled_arrival
    actual_departure = service.location_detail.actual_departure

    punctuality = 'LATE' if actual_departure != scheduled_departure else 'ON TIME'

    print(
        SERVICE_DESC.format(
            origin,
            destination,
            actual_departure,
            platform,
            actual_arrival,
            scheduled_departure,
            punctuality,
        )
    )
