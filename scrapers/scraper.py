#  Copyright 2019 Michael Kemna.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from abc import ABC, abstractmethod

import time
from random import randint
from typing import List

import requests
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import DatabaseError

from config import *
from powderbooking.database import DatabaseHandler
from scrapers.errorHandler import ErrorHandler


class Scraper(ErrorHandler, ABC):
    """
    This class is used as a base for all other scrapers.
    It is an abstract class, as it requires the values for each specific api to function.

    The process can be described as follows:
    1 - Retrieve the records that need to be scraped
    2 - For each record, request the data and parse the results
    3 - Insert that data into the database in batches
    """
    db: DatabaseHandler
    results: List[dict]

    current_id: int  # the current id that we are handling

    def __init__(self, db: DatabaseHandler):
        super().__init__()
        self.db = db
        self.results = []

    @staticmethod
    def _delay() -> None:
        """
        Add a randomized delay between requests to avoid throttling / DNSing google.
        """
        time.sleep(randint(DELAY_MIN * 10, DELAY_MAX * 10) / 10)

    @property
    @abstractmethod
    def _url_base(self) -> str:
        """
        The base url of the api that we are scraping.
        """
        pass

    @property
    @abstractmethod
    def _table_to_insert_into(self) -> str:
        """
        The table that we are inserting into.
        """
        pass

    @property
    @abstractmethod
    def _select_from_database(self) -> ResultProxy:
        pass

    @abstractmethod
    def _parse_request(self) -> None:
        """
        Parse the request and add the outcome to the results so it is inserted into the database.
        """
        pass

    def _insert_into_database(self) -> None:
        if len(self.results) > 0:
            try:
                self.db.insert(table=self._table_to_insert_into, values=self.results)
            except DatabaseError:
                self.handle_database_error()

            self.results = []

    def scrape(self) -> None:
        """
        Scrape the data from the weather apis and add it to the database.
        """
        for self.current_id, lat, lng in self._select_from_database:
            self.current_request = requests.get(url=self._url_base.format(lat=lat, lng=lng),
                                                headers={'Accept': 'application/json'})

            # these are measures to avoid and handle throttling by the api that we are scraping
            if self.check_request_error():
                if self.is_throttled():
                    break
                else:
                    continue
            self._delay()

            self._parse_request()

            # insert into the database in a blockwise manner
            # to avoid opening the database for every single new record
            if len(self.results) >= QUEUE_MAX:
                self._insert_into_database()

        # insert the remaining items into the database
        self._insert_into_database()
        print(self.result())
