from p360_export.data.fix.DataFixerInterface import DataFixerInterface
from p360_export.exceptions.manager import ExportDestinationNotSetException, InvalidExportDestinationException
from p360_export.export.ExporterInterface import ExporterInterface


class ExportManager:
    def __init__(self, container):
        destination_type = container.config.get("destination_type")
        self.__export_container = self.__get_export_container(container, destination_type)

    def __get_export_container(self, container, export_destination):
        if not export_destination:
            raise ExportDestinationNotSetException("Export destination is not set.")

        if not hasattr(container, export_destination):
            raise InvalidExportDestinationException(f"No service with alias {export_destination} found.")

        return getattr(container, export_destination)

    @property
    def data_fixer(self) -> DataFixerInterface:
        if not hasattr(self.__export_container, "data_fixer"):
            raise NotImplementedError("Export container lacks 'data_fixer' singleton")

        return self.__export_container.data_fixer()

    @property
    def exporter(self) -> ExporterInterface:
        if not hasattr(self.__export_container, "exporter"):
            raise NotImplementedError("Export container lacks 'exporter' singleton")

        return self.__export_container.exporter()
