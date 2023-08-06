from typing import Dict, Any
from pyspark.sql import Row


class GoogleAnalytics4EventBuilder:
    def __init__(self, config: Dict[str, Any]):
        self.__config = config
        self.__default_params = {
            "event_name": "odap_export",
            "debug": False,
        }

    def build(self, row: Row) -> Dict[str, Any]:
        all_columns = row.asDict().keys()
        id_columns = {"client_id", "user_id"}
        attribute_columns = all_columns - id_columns

        event_name = self.__get_custom_param("event_name")
        debug_mode = self.__get_custom_param("debug")

        event = {
            "client_id": str(row.client_id),
            "user_id": str(row.user_id) if hasattr(row, "user_id") else None,
            "events": [{"name": event_name, "params": {}}],
            "user_properties": {attr: {"value": getattr(row, attr, None)} for attr in attribute_columns},
        }

        if debug_mode is True:
            event["events"][0]["params"]["debug_mode"] = True

        return event

    def __get_custom_param(self, param_name: str):
        param = self.__config.get("params").get("custom", {}).get(param_name)

        return param if param is not None else self.__default_params.get(param_name)
