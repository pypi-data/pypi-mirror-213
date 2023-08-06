from pyspark.sql import DataFrame
from p360_export.data.fix.DataFixerInterface import DataFixerInterface


class DataPlatformDataFixer(DataFixerInterface):
    def fix(self, df: DataFrame) -> DataFrame:
        return df
