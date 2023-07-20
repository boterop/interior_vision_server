from lib.cryptography import Cryptography
import datetime
import pytz
import requests


AUTH_SYSTEM_URL = "https://localhost:5001/{}"


class Auth:

    def gen_token(user, password):
        payload = {
            'user': user,
            'password': password,
            'exp_date': datetime.datetime.now(tz=pytz.timezone("UTC")) + datetime.timedelta(weeks=4)
        }
        return Cryptography.encode(payload)

    def validate_token(hash):
        data = Cryptography.decode(hash)

        if (data["exp_date"]):
            return False

        is_logged = requests.post(
            AUTH_SYSTEM_URL.format("login"), data)['content']

        return is_logged
