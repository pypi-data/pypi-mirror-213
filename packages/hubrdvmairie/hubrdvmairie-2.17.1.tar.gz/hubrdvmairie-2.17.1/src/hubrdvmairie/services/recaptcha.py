import os

import requests


def verify_recaptcha(token: str) -> float:
    try:
        params = {
            "secret": os.environ.get("GOOGLE_SITE_VERIFICATION"),
            "response": token,
        }

        response = requests.get(
            url="https://www.google.com/recaptcha/api/siteverify",
            params=params,
            timeout=5,
        )
        response_json = response.json()

        return response_json["score"]
    except Exception as e:
        print(str(e))
        return 0
