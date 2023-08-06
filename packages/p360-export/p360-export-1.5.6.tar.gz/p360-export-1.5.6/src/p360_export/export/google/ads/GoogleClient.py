from typing import Any, Dict
from google.ads.googleads.client import GoogleAdsClient

from p360_export.utils.secret_getters.SecretGetterInterface import SecretGetterInterface


class GoogleClient:
    def __new__(cls, secret_getter: SecretGetterInterface, credentials: Dict[str, Any]) -> GoogleAdsClient:
        config_dict = {
            "developer_token": secret_getter.get(credentials["developer_token_key"]),
            "refresh_token": secret_getter.get(credentials["refresh_token_key"]),
            "client_id": credentials["client_id"],
            "client_secret": secret_getter.get(credentials["client_secret_key"]),
            "login_customer_id": credentials["customer_id"],
            "use_proto_plus": True,
        }

        return GoogleAdsClient.load_from_dict(config_dict=config_dict)
