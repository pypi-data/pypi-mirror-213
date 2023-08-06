import json
from raga.validators.test_session_validation import TestSessionValidator
from raga.utils.http_client import HTTPClient
from raga.utils.raga_config_reader import read_raga_config, get_config_value

config_data = read_raga_config()

class Auth:
    def __init__(self):
        self.http_client = HTTPClient(get_config_value(config_data, 'default', 'api_host'))
        self.raga_access_key_id = get_config_value(config_data, 'default', 'raga_access_key_id')
        self.raga_secret_access_key = get_config_value(config_data, 'default', 'raga_secret_access_key')
        self.token = self.create_token()

    def create_token(self):
        """
        Creates an authentication token by sending a request to the Raga API.

        Returns:
            str: The authentication token.

        Raises:
            KeyError: If the response data does not contain a valid token.
        """
        res_data = self.http_client.post(
            "api/token",
            {"accessKey": self.raga_access_key_id, "secretKey": self.raga_secret_access_key},
        )
        token = res_data.get("data", {}).get("token")
        if not token:
            raise KeyError("Invalid response data. Token not found.")
        return token
