import json
from typing import Dict, Any
from requests import Session

from p360_export.utils.secret_getters.SecretGetterInterface import SecretGetterInterface


class GoogleAnalytics4Client:
    def __init__(self, secret_getter: SecretGetterInterface, credentials: Dict[str, Any]):
        self.__session = Session()
        self.__base_url = "https://www.google-analytics.com"
        self.__headers = {"Content-Type": "application/json"}
        self.__params = {
            "measurement_id": credentials["measurement_id"],
            "api_secret": secret_getter.get(credentials["api_secret_key"]),
        }

    def upload_event(self, event: Dict[str, Any]):
        self.__session.post(
            f"{self.__base_url}/mp/collect", data=json.dumps(event), headers=self.__headers, params=self.__params
        )
