from dependency_injector import containers, providers
from p360_export.containers.Core import Core
from p360_export.data.fix.SFMCDataFixer import SFMCDataFixer
from p360_export.data.type.resolve.SFMCTypeResolver import SFMCTypeResolver

from p360_export.export.sfmc.DataExtensionCreator import DataExtensionCreator
from p360_export.export.sfmc.DataExtensionFieldCreator import DataExtensionFieldCreator
from p360_export.export.sfmc.DataExtensionFieldUpdater import DataExtensionFieldUpdater
from p360_export.export.sfmc.DataExtensionGetter import DataExtensionGetter
from p360_export.export.sfmc.FieldNameFixer import SFMCFieldNameFixer
from p360_export.export.sfmc.ImportDefinitionExecutor import ImportDefinitionExecutor
from p360_export.export.sfmc.ImportDefinitionGetter import ImportDefinitionGetter
from p360_export.export.sfmc.SFMCData import SFMCData
from p360_export.export.sfmc.SFMCExporter import SFMCExporter
from p360_export.export.sfmc.SFTPUploader import SFTPUploader


class SFMCContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    core: Core = providers.DependenciesContainer()  # pyre-ignore[8]

    field_name_fixer = providers.Singleton(SFMCFieldNameFixer)
    sfmc_data = providers.Singleton(
        SFMCData, config=config, secret_getter=core.secret_getter, field_name_fixer=field_name_fixer
    )

    sftp_uploader = providers.Singleton(SFTPUploader, sfmc_data=sfmc_data)
    sfmc_type_resolver = providers.Singleton(
        SFMCTypeResolver,
        email_validator=core.email_validator,
        phone_number_validator=core.phone_number_validator,
        dataframe_type_resolver=core.dataframe_type_resolver,
        column_sample_getter=core.column_sample_getter,
    )

    data_extension_field_creator = providers.Singleton(
        DataExtensionFieldCreator, df_type_resolver=core.dataframe_type_resolver, type_resolver=sfmc_type_resolver
    )
    data_extension_creator = providers.Singleton(
        DataExtensionCreator,
        sfmc_data=sfmc_data,
        data_extension_field_creator=data_extension_field_creator,
        audience_name_getter=core.audience_name_getter,
    )
    data_extension_field_updater = providers.Singleton(
        DataExtensionFieldUpdater, sfmc_data=sfmc_data, data_extension_field_creator=data_extension_field_creator
    )
    data_extension_getter = providers.Singleton(
        DataExtensionGetter,
        sfmc_data=sfmc_data,
        data_extension_field_updater=data_extension_field_updater,
        data_extension_creator=data_extension_creator,
    )

    import_definition_executor = providers.Singleton(ImportDefinitionExecutor, sfmc_data=sfmc_data)
    import_definition_getter = providers.Singleton(
        ImportDefinitionGetter, sfmc_data=sfmc_data, audience_name_getter=core.audience_name_getter
    )

    data_fixer = providers.Singleton(SFMCDataFixer, field_name_fixer=field_name_fixer)
    exporter = providers.Singleton(
        SFMCExporter,
        sftp_uploader=sftp_uploader,
        data_extension_getter=data_extension_getter,
        import_definition_getter=import_definition_getter,
        import_definition_executor=import_definition_executor,
    )
