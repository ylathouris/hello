import logging

from chalice import AuthResponse, Chalice
from chalicelib.auth import authenticate

app = Chalice(app_name="hello")
app.log.setLevel(logging.DEBUG)


@app.authorizer(ttl_seconds=300)
def auth(auth_request):
    token = auth_request.token
    app.log.debug(token)
    data, authenticated = authenticate(token)
    app.log.info(str(data))
    app.log.info(str(authenticated))
    if not authenticated:
        # By specifying an empty list of routes,
        # we're saying this user is not authorized
        # for any URLs, which will result in an
        # Unauthorized response.
        app.log.error(data["error"])
        return AuthResponse(routes=[], principal_id="user")

    user_id = "user"  #data["sub"]
    app.log.info(f">>> User ID: {user_id}")
    response = AuthResponse(routes=["*"], principal_id=user_id)
    app.log.info(f">>> Response: {response.__dict__}")
    return response


@app.route("/", methods=["GET"], authorizer=auth)
def hello():
    app.log.debug("Running...")
    context = app.current_request.context
    return {"message": "Hello World"}
