
from unittest import mock

from chalice.test import Client
import pytest

from app import app


@pytest.fixture()
def client():
    with Client(app) as client:
        yield client


@pytest.fixture()
def auth():
    with mock.patch("app.authenticate") as mocked:
        yield mocked


@pytest.fixture()
def bad_auth(auth):
    auth.return_value = ({"error": "Bad Token"}, False)
    yield auth


@pytest.fixture()
def good_auth(auth):
    auth.return_value = ({"sub": "user123"}, True)
    yield auth


class TestHello:

    def test_returns_unauthorized_with_no_token(self, client):
        result = client.http.get("/")

        expected = {"message": "Unauthorized"}
        assert result.json_body == expected
        assert result.status_code == 401

    def test_returns_unauthorized_with_invalid_token(self, client, bad_auth):
        headers = {"Authorization": "bad-token"}
        result = client.http.get("/", headers=headers)

        expected = {"Message": "User is not authorized to access this resource"}
        assert result.json_body == expected
        assert result.status_code == 403

    def test_returns_expected_with_valid_token(self, client, good_auth):
        headers = {"Authorization": "good-token"}
        result = client.http.get("/", headers=headers)

        expected = {"message": "Hello World"}
        assert result.json_body == expected
        assert result.status_code == 200
