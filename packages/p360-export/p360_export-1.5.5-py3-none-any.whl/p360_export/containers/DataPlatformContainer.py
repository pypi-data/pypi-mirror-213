from dependency_injector import containers, providers
from p360_export.containers.Core import Core
from p360_export.data.fix.DataPlatformDataFixer import DataPlatformDataFixer
from p360_export.export.DataPlatformExporter import DataPlatformExporter


class DataPlatformContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    core: Core = providers.DependenciesContainer()  # pyre-ignore[8]

    data_fixer = providers.Singleton(DataPlatformDataFixer)
    exporter = providers.Singleton(DataPlatformExporter, config=config, dbutils=core.dbutils)
