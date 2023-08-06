from pyspark.sql import DataFrame

from p360_export.export.ExporterInterface import ExporterInterface
from p360_export.export.sfmc.DataExtensionGetter import DataExtensionGetter
from p360_export.export.sfmc.SFTPUploader import SFTPUploader
from p360_export.export.sfmc.ImportDefinitionGetter import ImportDefinitionGetter
from p360_export.export.sfmc.ImportDefinitionExecutor import ImportDefinitionExecutor


class SFMCExporter(ExporterInterface):
    def __init__(
        self,
        sftp_uploader: SFTPUploader,
        data_extension_getter: DataExtensionGetter,
        import_definition_getter: ImportDefinitionGetter,
        import_definition_executor: ImportDefinitionExecutor,
    ):
        self.__sftp_uploader = sftp_uploader
        self.__data_extension_getter = data_extension_getter
        self.__import_definition_getter = import_definition_getter
        self.__import_definition_executor = import_definition_executor

    def export(self, df: DataFrame):
        self.__sftp_uploader.upload(df)

        data_extension_id = self.__data_extension_getter.get(df)

        import_definition_id = self.__import_definition_getter.get(data_extension_id)

        self.__import_definition_executor.execute(import_definition_id)
