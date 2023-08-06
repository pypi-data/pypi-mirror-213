import os
import pprint

import pytest
from dotenv import find_dotenv, load_dotenv

from station.common.clients.central.central_client import CentralApiClient


@pytest.fixture
def central_client():
    load_dotenv(find_dotenv())
    url = os.getenv("CENTRAL_API_URL")
    client_id = os.getenv("STATION_ROBOT_ID")
    client_secret = os.getenv("STATION_ROBOT_SECRET")
    return CentralApiClient(url, client_id, client_secret)


def test_get_token(central_client):
    token = central_client._get_token()

    assert token is not None


def test_get_registry_credentials(central_client):
    registry_credentials = central_client.get_registry_credentials(
        os.getenv("STATION_ID")
    )
    pprint.pprint(registry_credentials)
    assert registry_credentials


def test_update_public_key(central_client):
    public_key = "test_public_key".encode("utf-8").hex()
    station_id = os.getenv("STATION_ID")
    response = central_client.update_public_key(station_id, public_key)
    print(response)


def test_get_trains_for_station(central_client):
    station_id = os.getenv("STATION_ID")
    response = central_client.get_trains(station_id)
    assert response
    print(response)
