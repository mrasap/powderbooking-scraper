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
import queue
import requests

from app.config import *
from app.error_handler import ErrorHandler


class Scraper:
    q: queue
    error_handler: ErrorHandler

    def __init__(self):
        self.q = queue.Queue()
        self.error_handler = ErrorHandler()

    def request_weather_apis(self, sql_insert, sql_select, url_base, url_args, req_handler_func):
        """ Core logic of requesting the API """
        """ 1 - Walk through all records (sql_select )"""
        """ 2 - Retrieve data (url_base and url_args)"""
        """ 3 - Handle the request (req_handler_func)"""
        """ 4 - Insert data into the database (sql_select)"""
        print('Amount of requests to be handled:', amount_db(sql_select))

        for i, (_id, lat, lng) in enumerate(select_db(sql_select), start=0):
            # print(i, ": ", _id, lat, lng)
            url_args['lat'] = lat
            url_args['lng'] = lng

            req = requests.get(url_base.format(**url_args), headers={'Accept': 'application/json'})

            # Stop if throttled, skip this record if there is an error in the current request
            if self.error_handler(req):
                if self.error_handler.is_throttled():
                    break
                else:
                    continue
            # Delay the script to avoid bombarding the API with too many requests
            delay()

            req = req.json()

            # The specific handling of the request is performed by the injected function
            req_handler_func(q, req, _id)

            # insert into the database in a blockwise manner
            # to avoid opening the database for every single new record
            if self.q.qsize() >= QUEUE_MAX:
                insert_db(sql_insert, self.error_handler, q)

        # insert the remaining items into the database
        insert_db(sql_insert, self.error_handler, q)
        print(self.error_handler.result())

