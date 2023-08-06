from p360_export.export.sfmc.SFMCData import SFMCData


class ImportDefinitionExecutor:
    def __init__(self, sfmc_data: SFMCData) -> None:
        self.__sfmc_client = sfmc_data.client

    def execute(self, import_definition_id: str):
        request = self.__sfmc_client.soap_client.factory.create("PerformRequestMsg")
        definition = self.__sfmc_client.soap_client.factory.create("ImportDefinition")

        definition.ObjectID = import_definition_id

        request.Definitions = {"Definition": definition}
        request.Action = "start"

        self.__sfmc_client.soap_client.service.Perform(None, request)
