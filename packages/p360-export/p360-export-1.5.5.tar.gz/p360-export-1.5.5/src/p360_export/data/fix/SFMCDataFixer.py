from pyspark.sql import DataFrame
from p360_export.data.fix.DataFixerInterface import DataFixerInterface
from p360_export.export.sfmc.FieldNameFixer import SFMCFieldNameFixer


class SFMCDataFixer(DataFixerInterface):
    def __init__(self, field_name_fixer: SFMCFieldNameFixer):
        self.__field_name_fixer = field_name_fixer

    def fix(self, df: DataFrame) -> DataFrame:
        new_column_names = self.__field_name_fixer.fix_names(df.columns)

        return df.toDF(*new_column_names)
