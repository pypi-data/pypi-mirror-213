from typing import Dict
from p360_export.exceptions.data_picker import EmptyColumnMappingException


class ColumnMappingGetter:
    def __init__(self, config):
        self.column_mapping = config["params"]["mapping"]

    def get(self) -> Dict[str, str]:
        if not self.column_mapping:
            raise EmptyColumnMappingException(
                "No column mapping specified. The params.mapping value in the configuration file is empty."
            )

        return self.column_mapping
