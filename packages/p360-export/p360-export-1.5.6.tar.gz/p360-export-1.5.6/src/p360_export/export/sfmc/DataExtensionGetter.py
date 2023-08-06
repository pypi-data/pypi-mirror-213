from pyspark.sql import DataFrame
from FuelSDK import ET_DataExtension

from p360_export.export.sfmc.DataExtensionCreator import DataExtensionCreator
from p360_export.export.sfmc.SFMCData import SFMCData
from p360_export.export.sfmc.DataExtensionFieldUpdater import DataExtensionFieldUpdater


class DataExtensionGetter:
    def __init__(
        self,
        sfmc_data: SFMCData,
        data_extension_field_updater: DataExtensionFieldUpdater,
        data_extension_creator: DataExtensionCreator,
    ):
        self.__sfmc_data = sfmc_data
        self.__data_extension_field_updater = data_extension_field_updater
        self.__data_extension_creator = data_extension_creator

    def __get_existing_data_extension(self) -> dict:
        data_extension = ET_DataExtension()
        data_extension.auth_stub = self.__sfmc_data.client
        data_extension.props = ["ObjectID"]
        data_extension.search_filter = {
            "Property": "CustomerKey",
            "SimpleOperator": "equals",
            "Value": self.__sfmc_data.export_id,
        }

        response = data_extension.get()
        if response.results:
            return response.results[0]

        return {}

    def get(self, df: DataFrame) -> str:
        data_extension = self.__get_existing_data_extension()
        if data_extension:
            self.__data_extension_field_updater.update(df)

            return data_extension["ObjectID"]

        return self.__data_extension_creator.create(df)
