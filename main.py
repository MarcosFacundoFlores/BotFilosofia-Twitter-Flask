import base64
import hashlib
import os
import re

from dotenv import load_dotenv
from flask import Flask, redirect, request, session
from requests_oauthlib import OAuth2Session

from tweet_utils import save_token

app = Flask(__name__)
app.secret_key = os.urandom(50)
load_dotenv()

client_id = os.environ["TWITTER_OAUTH2_CLIENT_ID"]
client_secret = os.environ["TWITTER_OAUTH2_CLIENT_ID_SECRET"]
redirect_uri = os.environ["REDIRECT_URI"]

auth_url = "https://twitter.com/i/oauth2/authorize"
token_url = "https://api.twitter.com/2/oauth2/token"

scopes = ["tweet.read", "users.read", "tweet.write", "offline.access"]

# Generar code verifier y challenge
code_verifier = re.sub(
    "[^a-zA-Z0-9]+", "", base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
)
code_challenge = (
    base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
    .decode()
    .replace("=", "")
)


def make_oauth_session():
    return OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scopes)


@app.route("/")
def home():
    twitter = make_oauth_session()
    authorization_url, state = twitter.authorization_url(
        auth_url, code_challenge=code_challenge, code_challenge_method="S256"
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def oauth_callback():
    twitter = make_oauth_session()
    code = request.args.get("code")
    token = twitter.fetch_token(
        token_url=token_url,
        client_secret=client_secret,
        code=code,
        code_verifier=code_verifier,
    )
    save_token(token)
    return "OAuth completado y token guardado en Redis"


if __name__ == "__main__":
    app.run(debug=True)
