from google.ads.googleads.client import GoogleAdsClient

from p360_export.export.AudienceNameGetter import AudienceNameGetter


class UserListGetter:
    def __init__(self, config, client: GoogleAdsClient, audience_name_getter: AudienceNameGetter):
        self.__page_size = 10000
        self.__config = config
        self.__client = client
        self.__audience_name_getter = audience_name_getter

    def __get_existing_user_lists(self) -> list:
        request = self.__client.get_type(name="SearchGoogleAdsRequest")
        request.customer_id = self.__client.login_customer_id
        request.query = "SELECT user_list.id, user_list.integration_code FROM user_list"
        request.page_size = self.__page_size

        response = self.__client.get_service(name="GoogleAdsService").search(request=request)

        return response.results

    def __create_user_list(self) -> str:
        user_list_name = self.__audience_name_getter.get()

        user_list_service = self.__client.get_service(name="UserListService")
        user_list_operation = self.__client.get_type(name="UserListOperation")

        user_list = user_list_operation.create
        user_list.name = user_list_name
        user_list.integration_code = self.__config["export_id"]
        user_list.crm_based_user_list.upload_key_type = self.__client.enums.CustomerMatchUploadKeyTypeEnum.CRM_ID
        user_list.membership_life_span = 10

        response = user_list_service.mutate_user_lists(
            customer_id=self.__client.login_customer_id, operations=[user_list_operation]
        )

        return response.results[0].resource_name

    def get(self) -> str:
        for user_list in self.__get_existing_user_lists():
            if user_list.user_list.integration_code == self.__config["export_id"]:
                return user_list.user_list.resource_name

        return self.__create_user_list()
