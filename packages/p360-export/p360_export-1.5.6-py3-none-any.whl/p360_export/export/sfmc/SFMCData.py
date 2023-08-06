from typing import List
from FuelSDK import ET_Client

from p360_export.export.sfmc.FieldNameFixer import SFMCFieldNameFixer

from p360_export.utils.secret_getters.SecretGetterInterface import SecretGetterInterface


class SFMCData:
    def __init__(self, config, secret_getter: SecretGetterInterface, field_name_fixer: SFMCFieldNameFixer) -> None:
        self.__config = config
        self.__secret_getter = secret_getter
        self.__field_name_fixer = field_name_fixer
        self.client = self.__get_client()

    def __get_client(self):
        return ET_Client(
            params={
                "clientid": self.client_id,
                "clientsecret": self.client_secret,
                "authenticationurl": f"https://{self.tenant_url}.auth.marketingcloudapis.com/",
                "useOAuth2Authentication": "True",
                "accountId": self.account_id,
                "scope": "data_extensions_read data_extensions_write automations_write automations_read",
                "applicationType": "server",
            }
        )

    @property
    def client_id(self) -> str:
        return self.__config["credentials"]["client_id"]

    @property
    def tenant_url(self) -> str:
        return self.__config["credentials"]["tenant_url"]

    @property
    def account_id(self) -> str:
        return self.__config["credentials"]["account_id"]

    @property
    def file_location(self) -> str:
        return self.__config["credentials"]["file_location"]

    @property
    def ftp_username(self) -> str:
        return self.__config["credentials"]["ftp_username"]

    @property
    def subscriber_key(self) -> str:
        return self.__field_name_fixer.fix_name(self.__config["params"]["mapping"]["subscriber_key"])

    @property
    def export_columns(self) -> List[str]:
        fixed_columns = set(self.__field_name_fixer.fix_names(self.__config["params"]["export_columns"]))
        return list(fixed_columns - set([self.subscriber_key]))

    @property
    def export_id(self) -> str:
        return self.__config["export_id"]

    @property
    def new_field_names(self) -> List[str]:
        return self.export_columns + [self.subscriber_key]

    @property
    def client_secret(self) -> str:
        return self.__secret_getter.get(key=self.__config["credentials"]["client_secret_key"])

    @property
    def ftp_password(self) -> str:
        return self.__secret_getter.get(key=self.__config["credentials"]["ftp_password_key"])

    @property
    def ftp_relative_path(self) -> str:
        return self.__config["credentials"].get("ftp_relative_path", "/Import/")
