import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()
r = redis.from_url(os.environ["REDIS_URL"])
t = r.get("token")
print(t.decode("utf-8") if t else "No hay token")
