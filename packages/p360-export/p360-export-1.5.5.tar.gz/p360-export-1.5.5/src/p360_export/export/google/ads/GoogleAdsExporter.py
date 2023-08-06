from pyspark.sql import DataFrame

from p360_export.export.ExporterInterface import ExporterInterface
from p360_export.export.google.ads.UserDataSender import UserDataSender
from p360_export.export.google.ads.UserListGetter import UserListGetter


class GoogleAdsExporter(ExporterInterface):
    def __init__(
        self,
        user_data_sender: UserDataSender,
        user_list_getter: UserListGetter,
    ):
        self.__user_data_sender = user_data_sender
        self.__user_list_getter = user_list_getter

    def export(self, df: DataFrame):
        user_ids = list(df.select("user_id").toPandas()["user_id"])

        user_list_resource_name = self.__user_list_getter.get()

        self.__user_data_sender.send(user_list_resource_name, user_ids)
