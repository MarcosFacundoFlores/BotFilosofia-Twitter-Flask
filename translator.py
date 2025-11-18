import os

import deepl
from dotenv import load_dotenv

load_dotenv()
auth_key = os.getenv("DEEPL_API_KEY")
assert auth_key is not None, "DEEPL_API_KEY is missing!"
deepl_client = deepl.DeepLClient(auth_key)


def translate_many(texts: list[str]) -> list[str]:
    result = deepl_client.translate_text(texts, source_lang="EN", target_lang="ES")

    # Normalize to list
    if not isinstance(result, list):
        result = [result]

    return [item.text for item in result]
