from typing import List, Sequence

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v10.common.types.offline_user_data import UserIdentifier


class UserDataJobOperationGetter:
    def __init__(self, client: GoogleAdsClient) -> None:
        self.__client = client

    def __prepare_google_user_ids(self, user_ids: Sequence[str]) -> List[UserIdentifier]:
        google_user_ids = []
        for user_id in user_ids:
            google_user_id = self.__client.get_type("UserIdentifier")
            google_user_id.third_party_user_id = user_id
            google_user_ids.append(google_user_id)

        return google_user_ids

    def get(self, user_ids: Sequence[str]):
        google_user_ids = self.__prepare_google_user_ids(user_ids)

        user_data_job_operation = self.__client.get_type(name="OfflineUserDataJobOperation")
        user_data_job_operation.remove_all = True
        user_data_job_operation.create.user_identifiers.extend(google_user_ids)

        return user_data_job_operation
