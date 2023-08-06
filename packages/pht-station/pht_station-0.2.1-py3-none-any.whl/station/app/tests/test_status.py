from dotenv import find_dotenv, load_dotenv
from fastapi.testclient import TestClient

from station.app.api.dependencies import get_db
from station.app.main import app

from .test_db import override_get_db

load_dotenv(find_dotenv())

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_station_status():
    resp = client.get("api/station/status")
    assert resp.status_code == 200
