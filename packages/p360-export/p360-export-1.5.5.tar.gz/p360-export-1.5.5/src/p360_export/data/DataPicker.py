from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession


class DataPicker:
    def __init__(self, spark: SparkSession):
        self.__spark = spark

    def pick(self, df: DataFrame, query: str, table_id: str) -> DataFrame:
        df.createOrReplaceTempView(table_id)

        return self.__spark.sql(query)
