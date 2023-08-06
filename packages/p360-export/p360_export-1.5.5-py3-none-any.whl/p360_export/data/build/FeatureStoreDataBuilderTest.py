import unittest

from p360_export.data.build.FeatureStoreDataBuilder import FeatureStoreDataBuilder
from p360_export.test.PySparkTestCase import PySparkTestCase

CONFIG = {
    "params": {"export_columns": ["phone", "id"], "mapping": {"email": "mapped_email"}},
    "segments": [
        {
            "definition_segment": [
                {
                    "attributes": [
                        {"op": "BETWEEN", "id": "col_1", "value": [0.0, 14.0]},
                        {"op": "LESS THAN", "id": "col_2", "value": 0.0},
                    ],
                    "op": "AND",
                }
            ],
        }
    ],
    "featurestorebundle": {"db_name": "", "entities": {"a": ""}},
}


class FeatureStoreDataBuilderTest(PySparkTestCase):
    def test_data_getter_gets_correct_data(self):
        def get_latest(features):
            df_complete = self.spark.createDataFrame(
                [
                    ["123", 1, "a@b.c", 1, 1, 1],
                    ["456", 2, "b@c.d", 2, 2, 2],
                    ["789", 1, "c@d.e", 5, 3, 4],
                ],
                ["phone", "id", "mapped_email", "foo", "col_1", "col_2"],
            )

            return df_complete.select(features)

        df_expected = self.spark.createDataFrame(
            [
                ["123", 1, "a@b.c", 1, 1],
                ["456", 2, "b@c.d", 2, 2],
                ["789", 1, "c@d.e", 3, 4],
            ],
            ["phone", "id", "mapped_email", "col_1", "col_2"],
        )

        feature_store_data_builder = FeatureStoreDataBuilder(config=CONFIG, spark=None)
        feature_store_data_builder.get_latest = get_latest

        self.compare_dataframes(df_expected, feature_store_data_builder.build(), sort_keys=["id"])


if __name__ == "__main__":
    unittest.main()
