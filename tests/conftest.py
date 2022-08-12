import json
import os

import pytest
from starlette.testclient import TestClient

from tests.reqover import create_build, upload_results
from src.main import app


@pytest.fixture(scope="session")
def client():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="session", autouse=True)
def upload_reqover_results(client):
    response = client.get("/openapi.json").json()
    file = save_file(response)
    project_token = "cpkoaj8qiwsw"
    data = {
        "name": os.getenv("BRANCH", "Master"),
        "serviceUrl": "http://testserver",
        "swaggerUrl": f"{client.base_url}/openapi.json",
    }
    results_url = create_build("https://reqover-io.herokuapp.com", data, project_token, file=file)
    yield
    upload_results(results_url)


def save_file(data):
    file_name = "/tmp/swagger.json"
    with open(file_name, "w") as outfile:
        json.dump(data, outfile)
    return file_name
