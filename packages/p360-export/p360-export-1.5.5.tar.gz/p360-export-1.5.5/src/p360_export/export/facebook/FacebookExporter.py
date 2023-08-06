from typing import Dict
from pyspark.sql import DataFrame
from pandas import DataFrame as pdDataFrame

from p360_export.export.ExporterInterface import ExporterInterface
from p360_export.export.facebook.CustomAudienceGetter import CustomAudienceGetter
from p360_export.export.facebook.FacebookParameters import FacebookParameters
from p360_export.utils.ColumnHasher import ColumnHasher
from p360_export.utils.secret_getters.SecretGetterInterface import SecretGetterInterface

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.api import FacebookAdsApi


class FacebookExporter(ExporterInterface):
    def __init__(
        self,
        credentials: Dict[str, str],
        secret_getter: SecretGetterInterface,
        column_hasher: ColumnHasher,
        custom_audience_getter: CustomAudienceGetter,
        facebook_parameters: FacebookParameters,
    ):
        self.__batch_size = 10000

        self.__credentials = credentials
        self.__secret_getter = secret_getter
        self.__column_hasher = column_hasher
        self.__custom_audience_getter = custom_audience_getter
        self.__facebook_parameters = facebook_parameters

    def __get_ad_account(self) -> AdAccount:
        access_token = self.__secret_getter.get(key=self.__credentials["access_token_key"])
        FacebookAdsApi.init(access_token=access_token)
        return AdAccount(self.__credentials["ad_account_id"])

    def __send_batches(self, df: pdDataFrame, df_size: int, schema: list):
        custom_audience = self.__custom_audience_getter.get(ad_account=self.__get_ad_account())

        parameters = self.__facebook_parameters.generate_parameters(df_size, schema)

        for start_idx in range(0, df_size, self.__batch_size):
            end_idx = start_idx + self.__batch_size
            batch = df[start_idx:end_idx]
            is_last_batch = end_idx >= df_size

            self.__facebook_parameters.update_parameters(parameters, batch, is_last_batch)
            custom_audience.create_users_replace(params=parameters)

    def export(self, df: DataFrame):
        schema = df.columns

        df = self.__column_hasher.hash(df=df, columns=schema, converter=self.__column_hasher.sha256)
        df = df.toPandas().values.tolist()  # pyre-ignore[16]

        self.__send_batches(df=df, df_size=len(df), schema=schema)
