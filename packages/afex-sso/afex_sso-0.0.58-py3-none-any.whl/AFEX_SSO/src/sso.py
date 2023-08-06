import time
import json
import requests
from django.conf import settings as app_settings
from django.utils import timezone

from .get_hash_key import get_hash_key

URL = app_settings.SSO_URL
API_KEY = app_settings.SSO_API_KEY
SECRET_KEY = app_settings.SSO_SECRET_KEY


# settings.configure()
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SSO.settings")


class SSO:
    """_summary_
    SSO CLASS
    """

    # def __init__(self, sp_api_key, sp_hash_key, session_key) -> None:
    #     self.api = sp_api_key
    #     self.hash = sp_hash_key
    #     self.session = session_key

    # def __call__(self):
    #     return self.check_credentials(self.api, self.hash, self.session)


    def check_credentials(self, session_key):
        try:
            HASH_KEY = get_hash_key(
                api_key=API_KEY,
                secret_key=SECRET_KEY,
                idempotency_key=session_key
            )
            headers = {
                "api-key": API_KEY,
                "hash-key":  HASH_KEY,
                "request-ts": session_key
            }
            response = requests.get(
                f"{URL}/v1/api/verify_sp/{session_key}", headers=headers)
            data = json.loads(response.text)
            return data

        except Exception as e:
            return f"Something went wrong, please confirm the credentials and try again: {e}"

    def sign_out(self, email: str):
        try:
            REQUEST_TS = timezone.now()
            HASH_KEY = get_hash_key(
                api_key=API_KEY,
                secret_key=SECRET_KEY,
                idempotency_key=REQUEST_TS
            )
            headers = {
                "api-key": API_KEY,
                "hash-key": HASH_KEY,
                "request-ts": REQUEST_TS
            }
            data = {
                "email": email
            }
            response = requests.post(
                f"{URL}/v1/api/signout", headers=headers, data=data)
            data = json.loads(response.text)
            return data

        except Exception as e:
            return f"Something went wrong, please confirm the credentials and try again: {e}"

