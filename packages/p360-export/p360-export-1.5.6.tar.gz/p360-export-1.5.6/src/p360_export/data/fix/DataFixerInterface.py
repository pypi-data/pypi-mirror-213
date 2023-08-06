from abc import ABC, abstractmethod
from pyspark.sql import DataFrame


class DataFixerInterface(ABC):
    @abstractmethod
    def fix(self, df: DataFrame) -> DataFrame:
        pass
