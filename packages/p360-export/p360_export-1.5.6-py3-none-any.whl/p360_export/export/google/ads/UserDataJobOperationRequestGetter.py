from typing import Sequence

from google.ads.googleads.client import GoogleAdsClient
from p360_export.export.google.ads.UserDataJobOperationGetter import UserDataJobOperationGetter


class UserDataJobOperationRequestGetter:
    def __init__(self, client: GoogleAdsClient, user_data_job_operation_getter: UserDataJobOperationGetter):
        self.__client = client
        self.__max_amount_of_ids_in_operation = 20
        self.__user_data_job_operation_getter = user_data_job_operation_getter

    def get(self, user_data_job_resource_name: str, user_ids: Sequence[str]):
        request = self.__client.get_type(name="AddOfflineUserDataJobOperationsRequest")

        request.resource_name = user_data_job_resource_name
        request.enable_partial_failure = False

        for idx in range(0, len(user_ids), self.__max_amount_of_ids_in_operation):
            user_ids_subset = user_ids[idx : idx + self.__max_amount_of_ids_in_operation]
            request.operations.append(self.__user_data_job_operation_getter.get(user_ids=user_ids_subset))

        return request
