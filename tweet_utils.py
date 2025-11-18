import json
import os
import random
from typing import Any, Dict, Optional

import redis
import requests

from translator import translate_many

r = redis.from_url(os.environ["REDIS_URL"])


def parse_philo_quote():
    """Obtiene una quote aleatoria y la traduce al español"""
    with open("uuids.json", "r") as f:
        uuids = json.load(f)

    uid = random.choice(uuids)

    res = requests.get(f"https://philosophersapi.com/api/quotes/{uid}")
    raw = res.json()

    quote_en = raw.get("quote", "")
    school_en = raw.get("philosopher", {}).get("school") or raw.get("school", "")

    quote_es, school_es = translate_many([quote_en, school_en])

    return {
        "quote": quote_es,
        "philosopher": raw.get("philosopher", {}).get("name")
        or raw.get("philosopher", {}).get("wikiTitle")
        or "Desconocido",
        "year": raw.get("year", ""),
        "school": school_es,
    }


def format_tweet(philo_quote: dict) -> str:
    quote = philo_quote.get("quote", "")
    philosopher = philo_quote.get("philosopher", "Desconocido")
    year = philo_quote.get("year", "")
    school = philo_quote.get("school", "")

    return f"{quote}\n\n--{philosopher}, {year}, {school}"


def post_tweet(payload: dict, token: dict) -> dict:
    """Publica el tweet usando el access_token"""
    headers = {
        "Authorization": f"Bearer {token['access_token']}",
        "Content-Type": "application/json",
    }
    response = requests.post(
        "https://api.twitter.com/2/tweets", json=payload, headers=headers
    )
    return response.json()


def save_token(token: dict):
    """Guarda el token en Redis"""
    r.set("token", json.dumps(token))


def load_token() -> Optional[Dict[str, Any]]:
    t = r.get("token")  # bytes o None
    if not t:
        return None
    return json.loads(t.decode("utf-8"))
