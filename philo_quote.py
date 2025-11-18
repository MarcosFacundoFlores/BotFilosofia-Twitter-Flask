import base64
import os

import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session

from tweet_utils import (
    format_tweet,
    load_token,
    parse_philo_quote,
    post_tweet,
    save_token,
)

load_dotenv()
client_id = os.environ["TWITTER_OAUTH2_CLIENT_ID"]
client_secret = os.environ["TWITTER_OAUTH2_CLIENT_ID_SECRET"]
token_url = "https://api.twitter.com/2/oauth2/token"

t = load_token()
if not t:
    raise Exception("No hay token en Redis. Primero completa OAuth con main.py")

twitter = OAuth2Session(client_id, token=t)

# Refrescar token si es necesario
"""refreshed_token = twitter.refresh_token(
    token_url,
    client_id=client_id,
    client_secret=client_secret,
    refresh_token=t["refresh_token"],
)
save_token(refreshed_token) """

# Refrescar token manualmente usando Basic Auth
auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
headers = {"Authorization": f"Basic {auth_header}"}
data = {
    "grant_type": "refresh_token",
    "refresh_token": t["refresh_token"],
}

res = requests.post(token_url, headers=headers, data=data)
if not res.ok:
    raise Exception(f"Error refrescando token: {res.status_code} {res.text}")

refreshed_token = res.json()
save_token(refreshed_token)


# Obtener y formatear quote
philo_quote = parse_philo_quote()
tweet_text = format_tweet(philo_quote)
payload = {"text": tweet_text}

# Publicar
response = post_tweet(payload, refreshed_token)
print(response)
