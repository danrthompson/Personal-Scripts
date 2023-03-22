# create a flask server
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# create a function that handles an oauth callback
@app.route("/oauth_callback")
def oauth_callback():
    # get the code from the request
    code = request.args.get("code")
    # get the state from the request
    state = request.args.get("state")
    # get the redirect url from the request
    redirect_url = request.args.get("redirect_url")
    # get the client id from the request
    client_id = request.args.get("client_id")
    # get the client secret from the request
    client_secret = request.args.get("client_secret")
    # get the scope from the request
    scope = request.args.get("scope")
    # get the token url from the request
    token_url = request.args.get("token_url")
    # get the token type from the request
    token_type = request.args.get("token_type")
    # get the token from the request
    token = request.args.get("token")
    # get the token expiration from the request
    token_expiration = request.args.get("token_expiration")
    return render_template(
        "oauth_callback.html",
        code=code,
        state=state,
        redirect_url=redirect_url,
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        token_url=token_url,
        token_type=token_type,
        token=token,
        token_expiration=token_expiration,
    )


@app.route("/:id", methods=["post", "get"])
def index(id=None):
    if request.method == "POST":
        return "<h1>POST</h1>"
    else:
        return "<h1>GET</h1>"
