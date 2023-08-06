import time
from typing import List, Dict, Any
from threading import Thread, Semaphore
from pyspark.sql import DataFrame

from p360_export.export.google.ga4.GoogleAnalytics4EventBuilder import GoogleAnalytics4EventBuilder
from p360_export.export.google.ga4.GoogleAnalytics4Client import GoogleAnalytics4Client


class GoogleAnalytics4EventsUploader:
    def __init__(self, client: GoogleAnalytics4Client, event_builder: GoogleAnalytics4EventBuilder):
        self.__client = client
        self.__event_builder = event_builder
        self.__batch_size = 1000
        self.__requests_period = 0.5
        self.__num_requests_in_period = 25
        self.__semaphore = Semaphore(self.__num_requests_in_period)

    def upload(self, df: DataFrame):
        events = []

        for row in df.rdd.toLocalIterator():
            events.append(self.__event_builder.build(row))

            if len(events) == self.__batch_size:
                self.__upload_events(events)

        if len(events) > 0:
            self.__upload_events(events)

    def __upload_events(self, events: List[Dict[str, Any]]):
        threads = [Thread(target=self.__upload_event, args=(event,)) for event in events]
        _ = [thread.start() for thread in threads]
        _ = [thread.join() for thread in threads]
        events.clear()

    def __upload_event(self, event: Dict[str, Any]):
        with self.__semaphore:
            self.__client.upload_event(event)

            if self.__semaphore._value <= 0:  # noqa # pylint: disable=protected-access
                time.sleep(self.__requests_period)
