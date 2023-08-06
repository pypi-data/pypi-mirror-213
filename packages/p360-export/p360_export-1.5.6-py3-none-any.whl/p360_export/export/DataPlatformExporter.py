import os

from pyspark.sql import DataFrame
from pyspark.dbutils import DBUtils

from p360_export.export.ExporterInterface import ExporterInterface


class DataPlatformExporter(ExporterInterface):
    def __init__(self, config, dbutils: DBUtils):
        self.__config = config
        self.__dbutils = dbutils

    def export(self, df: DataFrame):
        config_id = self.__config.get("id")
        df.toPandas().to_csv("/dbfs/tmp/tmpxol6w4xe.csv")  # pyre-ignore[16]
        exports_base_path = self.__config["credentials"]["csv_exports_base_path"]
        self.__dbutils.fs.mv("dbfs:/tmp/tmpxol6w4xe.csv", os.path.join(exports_base_path, config_id + ".csv"))
