from typing import Dict, Any
from pyspark.sql import DataFrame

from p360_export.containers.Container import init_container, set_skeleton_config


def export(config: Dict[str, Any]):
    container = init_container(export_config=config)

    set_skeleton_config(container)

    base_df = container.core.data_builder().build()

    query, table_id = container.core.query_builder().build()

    picked_df = container.core.data_picker().pick(df=base_df, query=query, table_id=table_id)

    final_df = container.manager().data_fixer.fix(picked_df)

    container.manager().exporter.export(final_df)


def odap_export(df: DataFrame, config: Dict[str, Any]):
    container = init_container(export_config=config)

    final_df = container.manager().data_fixer.fix(df)

    container.manager().exporter.export(final_df)
