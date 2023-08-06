from pyspark.sql import DataFrame
from p360_export.data.extra.FacebookData import FacebookData
from p360_export.data.fix.DataFixerInterface import DataFixerInterface
from p360_export.data.ColumnMappingGetter import ColumnMappingGetter
from p360_export.exceptions.data_picker import InvalidFacebookColumnException


class FacebookDataFixer(DataFixerInterface):
    def __init__(self, column_mapping_getter: ColumnMappingGetter):
        self.__column_mapping = column_mapping_getter.get()

    def fix(self, df: DataFrame) -> DataFrame:
        selectable_columns = set()

        for new_name, old_name in self.__column_mapping.items():
            mapped_name = FacebookData.column_map.get(new_name.lower())

            if not mapped_name:
                raise InvalidFacebookColumnException(f"Column {new_name} is not accepted by Facebook API.")

            df = df.withColumnRenamed(old_name, mapped_name)
            selectable_columns.add(mapped_name)

        return df.select(list(selectable_columns))
