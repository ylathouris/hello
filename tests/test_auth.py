
from unittest import mock

import jwt
import pytest

from chalicelib import auth


@pytest.fixture()
def ssm():
    ssm_ = mock.MagicMock()
    with mock.patch("chalicelib.auth.boto3.client") as mocked:
        mocked.return_value = ssm_
        yield ssm_


@pytest.fixture()
def secret(ssm):
    param = {"Parameter": {"Value": ""}}
    ssm.get_parameter.return_value = param
    yield ssm


@pytest.fixture()
def jwt_decode(secret):
    with mock.patch("chalicelib.auth.jwt.decode") as mocked:
        yield mocked


@pytest.fixture()
def good_token(jwt_decode):
    payload = {"sub": "user123"}
    jwt_decode.return_value = payload
    yield jwt_decode


@pytest.fixture()
def bad_token(jwt_decode):
    jwt_decode.side_effect = jwt.InvalidTokenError("Oops!")
    yield jwt_decode


class TestAuth:

    def test_returns_expected_for_valid_token(self, good_token):
        data, status = auth.authenticate("good-token")

        assert data == {"sub": "user123"}
        assert status is True

    def test_returns_expected_for_invalid_token(self, bad_token):
        data, status = auth.authenticate("good-token")

        assert data == {"error": "Oops!"}
        assert status is False

    def test_decodes_token(self, jwt_decode):
        auth.authenticate("token")

        jwt_decode.assert_called_once_with("token", "", algorithms=["HS256"])