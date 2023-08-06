from abc import ABC, abstractmethod
from pyspark.sql import DataFrame


class ExporterInterface(ABC):
    @abstractmethod
    def export(self, df: DataFrame):
        pass
