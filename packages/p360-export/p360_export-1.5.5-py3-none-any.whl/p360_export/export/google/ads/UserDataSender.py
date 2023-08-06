from typing import Sequence

from google.ads.googleads.client import GoogleAdsClient
from p360_export.export.google.ads.UserDataJobCreator import UserDataJobCreator

from p360_export.export.google.ads.UserDataJobOperationRequestGetter import UserDataJobOperationRequestGetter


class UserDataSender:
    def __init__(
        self,
        client: GoogleAdsClient,
        user_data_job_creator: UserDataJobCreator,
        user_data_job_operation_request_getter: UserDataJobOperationRequestGetter,
    ):
        self.__client = client
        self.__user_data_job_creator = user_data_job_creator
        self.__user_data_job_operation_request_getter = user_data_job_operation_request_getter

    def send(self, user_list_resource_name: str, user_ids: Sequence[str]):
        user_data_service = self.__client.get_service(name="OfflineUserDataJobService")

        user_data_job_resource_name = self.__user_data_job_creator.create(
            user_data_service=user_data_service, user_list_resource_name=user_list_resource_name
        )

        request = self.__user_data_job_operation_request_getter.get(
            user_data_job_resource_name=user_data_job_resource_name, user_ids=user_ids
        )

        user_data_service.add_offline_user_data_job_operations(request=request)
        user_data_service.run_offline_user_data_job(resource_name=user_data_job_resource_name)
