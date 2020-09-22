
import base64
from typing import Dict

import boto3
import jwt


def authenticate(token: str) -> Dict:
    ssm = boto3.client("ssm")
    name = "/hello/auth-key"
    param = ssm.get_parameter(Name=name, WithDecryption=True)
    secret = param["Parameter"]["Value"]
    secret = base64.b64decode(secret).decode("utf-8")

    payload = None
    authenticated = True
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.InvalidTokenError as err:
        authenticated = False
        payload = {"error": str(err)}

    return (payload, authenticated)
