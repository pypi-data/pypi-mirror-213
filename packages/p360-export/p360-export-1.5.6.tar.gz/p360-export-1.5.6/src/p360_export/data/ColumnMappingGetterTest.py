import unittest

from p360_export.data.ColumnMappingGetter import ColumnMappingGetter


class ColumnMappingGetterTest(unittest.TestCase):
    def test_column_mapping_getter(self):
        config = {"params": {"mapping": {"email": "email_column"}}}
        self.assertEqual(ColumnMappingGetter(config).get(), {"email": "email_column"})


if __name__ == "__main__":
    unittest.main()
