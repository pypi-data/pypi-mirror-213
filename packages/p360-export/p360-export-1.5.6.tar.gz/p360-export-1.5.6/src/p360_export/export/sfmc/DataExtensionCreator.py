from typing import Dict, List
from FuelSDK import ET_DataExtension
from pyspark.sql import DataFrame

from p360_export.exceptions.exporter import UnableToCreateDataExtension
from p360_export.exceptions.utils import ColumnContainsNoValidExampleException
from p360_export.export.AudienceNameGetter import AudienceNameGetter
from p360_export.export.sfmc.DataExtensionFieldCreator import DataExtensionFieldCreator
from p360_export.export.sfmc.SFMCData import SFMCData


class DataExtensionCreator:
    def __init__(
        self,
        sfmc_data: SFMCData,
        data_extension_field_creator: DataExtensionFieldCreator,
        audience_name_getter: AudienceNameGetter,
    ):
        self.__sfmc_data = sfmc_data
        self.__audience_name_getter = audience_name_getter
        self.__data_extension_field_creator = data_extension_field_creator

    def __get_subscriber_key_field(self, df: DataFrame) -> Dict[str, str]:
        return self.__data_extension_field_creator.create_primary_key_field(
            df=df, field_name=self.__sfmc_data.subscriber_key
        )

    def __get_additional_fields(self, df: DataFrame) -> List[Dict[str, str]]:
        additional_fields = []

        for field_name in self.__sfmc_data.export_columns:
            try:
                additional_fields.append(self.__data_extension_field_creator.create(df=df, field_name=field_name))
            except ColumnContainsNoValidExampleException:
                print(f"Skipping {field_name} because it contains only null values.")

        return additional_fields

    def create(self, df: DataFrame) -> str:
        data_extension = ET_DataExtension()
        data_extension.auth_stub = self.__sfmc_data.client
        data_extension.props = {
            "Name": self.__audience_name_getter.get(),
            "CustomerKey": self.__sfmc_data.export_id,
            "IsSendable": True,
            "SendableDataExtensionField": {"Name": self.__sfmc_data.subscriber_key},
            "SendableSubscriberField": {"Name": "Subscriber Key"},
        }

        data_extension.columns = [self.__get_subscriber_key_field(df)]
        data_extension.columns.extend(self.__get_additional_fields(df))

        response = data_extension.post()

        if response.results[0]["StatusCode"] == "Error":
            raise UnableToCreateDataExtension(str(response.results))

        return response.results[0]["NewObjectID"]
