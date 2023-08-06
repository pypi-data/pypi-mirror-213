from pyspark.sql import DataFrame

from p360_export.export.ExporterInterface import ExporterInterface
from p360_export.export.google.ga4.GoogleAnalytics4EventsUploader import GoogleAnalytics4EventsUploader


class GoogleAnalytics4Exporter(ExporterInterface):
    def __init__(self, events_uploader: GoogleAnalytics4EventsUploader):
        self.__events_uploader = events_uploader

    def export(self, df: DataFrame):
        self.__events_uploader.upload(df)
