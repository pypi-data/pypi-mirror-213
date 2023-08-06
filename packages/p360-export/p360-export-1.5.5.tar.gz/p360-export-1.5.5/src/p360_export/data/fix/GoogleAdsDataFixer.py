from pyspark.sql import DataFrame
from p360_export.data.fix.DataFixerInterface import DataFixerInterface
from p360_export.data.ColumnMappingGetter import ColumnMappingGetter
from p360_export.exceptions.data_picker import UserIdMappingMissingException


class GoogleAdsDataFixer(DataFixerInterface):
    def __init__(self, column_mapping_getter: ColumnMappingGetter):
        self.__column_mapping = column_mapping_getter.get()

    def fix(self, df: DataFrame) -> DataFrame:
        if "user_id" not in self.__column_mapping:
            raise UserIdMappingMissingException("Mapping for user_id not specified.")

        for new_name, old_name in self.__column_mapping.items():
            df = df.withColumnRenamed(old_name, new_name)

        return df
