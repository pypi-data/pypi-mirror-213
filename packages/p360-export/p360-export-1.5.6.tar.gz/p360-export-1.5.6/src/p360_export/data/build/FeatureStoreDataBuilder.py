from pyspark.sql import DataFrame, SparkSession, types as t, functions as f
from typing import List, Set

from p360_export.data.build.DataBuilderInterface import DataBuilderInterface


class FeatureStoreDataBuilder(DataBuilderInterface):
    def __init__(self, config, spark: SparkSession):
        self.__last_compute_date = "last_compute_date"
        self.__timestamp_column = "timestamp"

        self.__config = config
        self.__spark = spark

        self.__feature_store = config["featurestorebundle"]["db_name"]
        self.__entity = list(config["featurestorebundle"]["entities"].keys())[0]

    @property
    def data_location(self):
        return "feature_store"

    @property
    def metadata_table(self):
        return f"{self.__feature_store}.features_metadata"

    @property
    def features_table(self):
        return f"{self.__feature_store}.features_{self.__entity}"

    def build(self) -> DataFrame:
        attributes = self._get_required_attribute_names()

        return self.get_latest(features=attributes)

    def resolve_fsbundle_nulls(self, df):
        for field in df.schema.fields:
            if isinstance(field.dataType, t.MapType):
                df = df.withColumn(field.name, f.col(field.name).getItem(0))

        return df

    def get_latest(self, features: List[str]):
        last_compute_date = self.__spark.read.table(self.metadata_table).select(f.max(self.__last_compute_date)).collect()[0][0]

        df = self.__spark.read.table(self.features_table).filter(f.col(self.__timestamp_column) == last_compute_date)

        return self.resolve_fsbundle_nulls(df=df.select(features))

    def _get_required_attribute_names(self) -> List[str]:
        attributes_from_export_columns = set(self.__config["params"]["export_columns"])
        attributes_from_mapping = set(self.__config["params"]["mapping"].values())
        attributes_from_condition = self._get_attributes_from_segments()

        return list(attributes_from_export_columns | attributes_from_mapping | attributes_from_condition)

    def _get_attributes_from_segments(self) -> Set[str]:
        attributes = set()
        for segment in self.__config["segments"]:
            if segment:
                attributes.update(self._get_attributes_from_definition_segment(segment["definition_segment"]))

        return attributes

    def _get_attributes_from_definition_segment(self, definition_segment: List[dict]) -> Set[str]:
        attributes = set()
        for definition_part in definition_segment:
            attributes.update(self._get_attribute_ids(definition_part["attributes"]))

        return attributes

    def _get_attribute_ids(self, attributes: List[dict]) -> Set[str]:
        return {attribute["id"] for attribute in attributes}
