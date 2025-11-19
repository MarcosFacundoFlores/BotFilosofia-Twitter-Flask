import base64
import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()
r = redis.from_url(os.environ["REDIS_URL"])

t = r.get("token")

if not t:
    print("No hay token en Redis")
    exit()

raw = t.decode("utf-8")
print("📌 Raw (tal cual está en Redis):")
print(raw)
print()

decoded_json = None

# Intentar decodificar como base64 → JSON
try:
    decoded = base64.b64decode(raw).decode("utf-8")
    decoded_json = json.loads(decoded)
    print("🟢 Interpretado como BASE64 → JSON decodificado:")
    print(json.dumps(decoded_json, indent=2))
    print()

except Exception:
    print("⚠️ No es base64 válido o no decodifica a JSON.")
    print()

# Si raw es JSON plano, intentar parsearlo
if decoded_json is None:
    try:
        decoded_json = json.loads(raw)
        print("🟢 Interpretado como JSON plano:")
        print(json.dumps(decoded_json, indent=2))
        print()
    except Exception:
        print("⚠️ No es JSON plano.")
        print()

# Convertir a base64 (ya sea desde JSON o desde raw)
print("📦 Base64 del contenido JSON:")
try:
    if decoded_json:
        # Re-encode JSON limpio
        json_clean = json.dumps(decoded_json)
        encoded = base64.b64encode(json_clean.encode()).decode()
        print(encoded)
    else:
        # fallback: encode raw
        encoded = base64.b64encode(raw.encode()).decode()
        print(encoded)
except Exception as e:
    print(f"Error convirtiendo a base64: {e}")
