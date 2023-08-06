from dependency_injector import containers, providers
from p360_export.containers.Core import Core
from p360_export.data.fix.GoogleAdsDataFixer import GoogleAdsDataFixer
from p360_export.export.google.ads.GoogleAdsExporter import GoogleAdsExporter
from p360_export.export.google.ads.GoogleClient import GoogleClient
from p360_export.export.google.ads.UserDataJobCreator import UserDataJobCreator
from p360_export.export.google.ads.UserDataJobOperationGetter import UserDataJobOperationGetter
from p360_export.export.google.ads.UserDataJobOperationRequestGetter import UserDataJobOperationRequestGetter
from p360_export.export.google.ads.UserDataSender import UserDataSender
from p360_export.export.google.ads.UserListGetter import UserListGetter


class GoogleAdsContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    core: Core = providers.DependenciesContainer()  # pyre-ignore[8]

    client = providers.Singleton(GoogleClient, secret_getter=core.secret_getter, credentials=config.credentials)

    user_data_job_creator = providers.Singleton(UserDataJobCreator, client=client)
    user_data_job_operation_getter = providers.Singleton(UserDataJobOperationGetter, client=client)
    user_data_job_operation_request_getter = providers.Singleton(
        UserDataJobOperationRequestGetter, client=client, user_data_job_operation_getter=user_data_job_operation_getter
    )

    user_data_sender = providers.Singleton(
        UserDataSender,
        client=client,
        user_data_job_creator=user_data_job_creator,
        user_data_job_operation_request_getter=user_data_job_operation_request_getter,
    )

    user_list_getter = providers.Singleton(
        UserListGetter, config=config, client=client, audience_name_getter=core.audience_name_getter
    )

    data_fixer = providers.Singleton(GoogleAdsDataFixer, column_mapping_getter=core.column_mapping_getter)
    exporter = providers.Singleton(
        GoogleAdsExporter, user_data_sender=user_data_sender, user_list_getter=user_list_getter
    )
