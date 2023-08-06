from FuelSDK import ET_Post, ET_Get

from p360_export.exceptions.exporter import UnableToCreateImportDefinition
from p360_export.export.AudienceNameGetter import AudienceNameGetter
from p360_export.export.sfmc.SFMCData import SFMCData


class ImportDefinitionGetter:
    def __init__(self, sfmc_data: SFMCData, audience_name_getter: AudienceNameGetter) -> None:
        self.__sfmc_data = sfmc_data
        self.__audience_name_getter = audience_name_getter

    def __create_import_definition_properties(self, data_extension_id: str) -> dict:
        return {
            "Name": self.__audience_name_getter.get(),
            "CustomerKey": self.__sfmc_data.export_id,
            "DestinationObject": {"ObjectID": data_extension_id},
            "RetrieveFileTransferLocation": {"CustomerKey": self.__sfmc_data.file_location},
            "AllowErrors": True,
            "UpdateType": "Overwrite",
            "FileSpec": f"{self.__sfmc_data.export_id}.csv",
            "FileType": "CSV",
            "FieldMappingType": "InferFromColumnHeadings",
        }

    def __create_import_definition(self, import_definition_properties: dict) -> str:
        response = ET_Post(
            auth_stub=self.__sfmc_data.client, obj_type="ImportDefinition", props=import_definition_properties
        )

        if response.results[0]["StatusCode"] == "Error":
            raise UnableToCreateImportDefinition(str(response.results))

        return response.results[0]["NewObjectID"]

    def get(self, data_extension_id: str) -> str:
        props = ["ObjectID"]
        search_filter = {"Property": "CustomerKey", "SimpleOperator": "equals", "Value": self.__sfmc_data.export_id}

        response = ET_Get(
            auth_stub=self.__sfmc_data.client, obj_type="ImportDefinition", props=props, search_filter=search_filter
        )
        if response.results:
            return response.results[0]["ObjectID"]

        import_definition_properties = self.__create_import_definition_properties(data_extension_id)

        return self.__create_import_definition(import_definition_properties)
