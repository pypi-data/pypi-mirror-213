from typing import List

from pyspark.sql import DataFrame
from FuelSDK import ET_Delete, ET_Patch, ET_DataExtension_Column
from p360_export.export.sfmc.SFMCData import SFMCData
from p360_export.exceptions.utils import ColumnContainsNoValidExampleException

from p360_export.export.sfmc.DataExtensionFieldCreator import DataExtensionFieldCreator


class DataExtensionFieldUpdater:
    def __init__(self, sfmc_data: SFMCData, data_extension_field_creator: DataExtensionFieldCreator):
        self.__sfmc_data = sfmc_data
        self.__data_extension_field_creator = data_extension_field_creator

    def __get_data_extension_fields(self) -> List[dict]:
        data_extension_column = ET_DataExtension_Column()
        data_extension_column.auth_stub = self.__sfmc_data.client
        data_extension_column.props = ["Name", "CustomerKey", "ObjectID"]
        data_extension_column.search_filter = {
            "Property": "CustomerKey",
            "SimpleOperator": "like",
            "Value": self.__sfmc_data.export_id,
        }

        response = data_extension_column.get()

        return response.results

    def __get_removable_fields(self, existing_fields: List[dict]) -> List[dict]:
        removable_fields = []

        for field in existing_fields:
            if field["Name"] not in self.__sfmc_data.new_field_names:
                removable_fields.append({"Field": {"ObjectID": field["ObjectID"]}})

        return removable_fields

    def __remove_data_extension_fields(self, removable_fields: List[dict]):
        if removable_fields:
            props = {"CustomerKey": self.__sfmc_data.export_id, "Fields": removable_fields}
            ET_Delete(auth_stub=self.__sfmc_data.client, obj_type="DataExtension", props=props)

    def __get_addable_fields(self, df: DataFrame, existing_fields: List[dict]) -> List[dict]:
        addable_fields = []
        existing_field_names = [field["Name"] for field in existing_fields]

        for field_name in self.__sfmc_data.new_field_names:
            if field_name in existing_field_names:
                continue

            try:
                field_properties = self.__data_extension_field_creator.create(df=df, field_name=field_name)
                addable_fields.append({"Field": field_properties})
            except ColumnContainsNoValidExampleException:
                print(f"Skipping {field_name} because it contains only null values.")

        return addable_fields

    def __add_data_extension_fields(self, addable_fields: List[dict]):
        if addable_fields:
            props = {"CustomerKey": self.__sfmc_data.export_id, "Fields": addable_fields}
            ET_Patch(auth_stub=self.__sfmc_data.client, obj_type="DataExtension", props=props)

    def update(self, df: DataFrame):
        existing_fields = self.__get_data_extension_fields()

        addable_fields = self.__get_addable_fields(df, existing_fields)
        self.__add_data_extension_fields(addable_fields)

        removable_fields = self.__get_removable_fields(existing_fields)
        self.__remove_data_extension_fields(removable_fields)
