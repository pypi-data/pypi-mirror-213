from dependency_injector import containers, providers
from p360_export.containers.Core import Core
from p360_export.export.google.ga4.GoogleAnalytics4Client import GoogleAnalytics4Client
from p360_export.export.google.ga4.GoogleAnalytics4EventBuilder import GoogleAnalytics4EventBuilder
from p360_export.export.google.ga4.GoogleAnalytics4EventsUploader import GoogleAnalytics4EventsUploader
from p360_export.export.google.ga4.GoogleAnalytics4Exporter import GoogleAnalytics4Exporter
from p360_export.data.fix.GoogleAnalytics4DataFixer import GoogleAnalytics4DataFixer


class GoogleAnalytics4Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    core: Core = providers.DependenciesContainer()  # pyre-ignore[8]

    client = providers.Singleton(
        GoogleAnalytics4Client, secret_getter=core.secret_getter, credentials=config.credentials
    )

    event_builder = providers.Singleton(GoogleAnalytics4EventBuilder, config=config)

    events_uploader = providers.Singleton(GoogleAnalytics4EventsUploader, client=client, event_builder=event_builder)

    data_fixer = providers.Singleton(GoogleAnalytics4DataFixer, column_mapping_getter=core.column_mapping_getter)

    exporter = providers.Singleton(GoogleAnalytics4Exporter, events_uploader=events_uploader)
