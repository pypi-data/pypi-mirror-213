from dependency_injector import containers, providers
from p360_export.containers.Core import Core
from p360_export.data.fix.FacebookDataFixer import FacebookDataFixer

from p360_export.export.facebook.CustomAudienceGetter import CustomAudienceGetter
from p360_export.export.facebook.FacebookExporter import FacebookExporter
from p360_export.export.facebook.FacebookParameters import FacebookParameters


class FacebookContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    core: Core = providers.DependenciesContainer()  # pyre-ignore[8]

    custom_audience_getter = providers.Singleton(CustomAudienceGetter, audience_name_getter=core.audience_name_getter)
    facebook_parameters = providers.Singleton(FacebookParameters)

    data_fixer = providers.Singleton(FacebookDataFixer, column_mapping_getter=core.column_mapping_getter)
    exporter = providers.Singleton(
        FacebookExporter,
        credentials=config.credentials,
        secret_getter=core.secret_getter,
        column_hasher=core.column_hasher,
        custom_audience_getter=custom_audience_getter,
        facebook_parameters=facebook_parameters,
    )
