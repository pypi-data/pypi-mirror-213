import unittest
from pyspark.sql import DataFrame

from p360_export.test.PySparkTestCase import PySparkTestCase
from p360_export.data.ColumnMappingGetter import ColumnMappingGetter

from p360_export.data.DataPicker import DataPicker
from p360_export.data.fix.DataPlatformDataFixer import DataPlatformDataFixer
from p360_export.data.fix.FacebookDataFixer import FacebookDataFixer
from p360_export.data.fix.GoogleAdsDataFixer import GoogleAdsDataFixer
from p360_export.data.fix.SFMCDataFixer import SFMCDataFixer
from p360_export.exceptions.data_picker import UserIdMappingMissingException
from p360_export.export.sfmc.FieldNameFixer import SFMCFieldNameFixer

TABLE_ID = "table_12345"
QUERY = f"SELECT email_col, gen_col, phone_col from {TABLE_ID}"

CONFIG = {"params": {"mapping": {"Email": "email_col", "Gender": "gen_col", "Phone": "phone_col"}}}

BASE_DF_DATA = [
    ["client_id1", "email1", "m", "unwanted", "phone1", "unwanted2"],
    ["client_id2", "email2", "f", "unwanted", "phone2", "unwanted2"],
    ["client_id3", "email3", "m", "unwanted", "phone3", "unwanted2"],
]
BASE_DF_SCHEMA = ["client_id", "email_col", "gen_col", "unwanted_col", "phone_col", "emailo_col"]

EXPECTED_DF_DATA = [
    ["email1", "m", "phone1"],
    ["email2", "f", "phone2"],
    ["email3", "m", "phone3"],
]
EXPECTED_LIST_BASED_SCHEMA = ["email_col", "gen_col", "phone_col"]
EXPECTED_MAPPING_BASED_SCHEMA = ["EMAIL", "GEN", "PHONE"]


class DataFixerTest(PySparkTestCase):
    @property
    def base_df(self) -> DataFrame:
        df = self.spark.createDataFrame(BASE_DF_DATA, BASE_DF_SCHEMA)

        data_picker = DataPicker(self.spark)
        return data_picker.pick(df, QUERY, TABLE_ID)

    def expected_df(self, schema: list) -> DataFrame:
        return self.spark.createDataFrame(EXPECTED_DF_DATA, schema)

    def test_data_platform_data_frame_builder(self):
        df = DataPlatformDataFixer().fix(df=self.base_df)
        self.compare_dataframes(df, self.expected_df(EXPECTED_LIST_BASED_SCHEMA), ["email_col"])

    def test_facebook_data_picker(self):
        df = FacebookDataFixer(ColumnMappingGetter(CONFIG)).fix(df=self.base_df)
        self.compare_dataframes(df, self.expected_df(EXPECTED_MAPPING_BASED_SCHEMA), ["EMAIL"])

    def test_google_ads_data_picker(self):
        google_ads_schema = ["user_id", "gen_col", "phone_col"]

        google_ads_config = {"params": {"mapping": {"user_id": "email_col", "Gender": "gen_col", "Phone": "phone_col"}}}

        df = GoogleAdsDataFixer(ColumnMappingGetter(google_ads_config)).fix(df=self.base_df)
        self.compare_dataframes(df, self.expected_df(google_ads_schema), ["user_id"])

    def test_sfmc_data_picker(self):
        long_column_name = "a" * 200
        expected_column_name = "a" * 128

        df = self.spark.createDataFrame([["value1"], ["value2"]], [long_column_name])
        expected_df = self.spark.createDataFrame([["value1"], ["value2"]], [expected_column_name])

        picked_df = SFMCDataFixer(SFMCFieldNameFixer()).fix(df)
        self.compare_dataframes(picked_df, expected_df, [expected_column_name])

    def test_google_ads_missing_user_id(self):
        with self.assertRaises(UserIdMappingMissingException):
            GoogleAdsDataFixer(ColumnMappingGetter(CONFIG)).fix(df=self.base_df)


if __name__ == "__main__":
    unittest.main()
