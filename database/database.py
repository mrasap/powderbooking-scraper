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
from contextlib import contextmanager
from typing import List, Dict

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine, Connection, ResultProxy

from config import build_database_url
from database.models import model_resort, model_weather, model_forecast


def build_postgres_engine(database_url: str = build_database_url()) -> Engine:
    return create_engine(database_url)


def build_postgres_database(engine=build_postgres_engine()) -> (Engine, MetaData):
    metadata = MetaData()

    model_resort(metadata)
    model_weather(metadata)
    model_forecast(metadata)

    metadata.create_all(engine)

    return engine, metadata


class DatabaseHandler:
    """
    Database handler to manage all database interactions in one place.

    inspired by: https://github.com/rshk/flask-sqlalchemy-core/
    """
    engine: Engine
    metadata: MetaData

    def __init__(self):
        self.engine, self.metadata = build_postgres_database()

    @contextmanager
    def connect(self) -> Connection:
        """
        Connect to the database, ensures that the connection is closed once all transactions have occurred.
        """
        with self.engine.connect() as conn:
            yield conn
            conn.close()

    def execute(self, *args, **kwargs) -> ResultProxy:
        """
        Execute the inserted args and kwargs onto the database and return the ResultProxy.
        """
        with self.connect() as conn:
            return conn.execute(*args, **kwargs)

    def insert(self, table: str, values: List[Dict[str]]) -> ResultProxy:
        """
        Insert the inserted list of values into the table that is given.
        Will raise a ValueError if the table is not inside the database.

        :param table: the name of the table that should be inserted into.
        :param values: a list of new rows that should be inserted.
        :return: the ResultProxy.
        """
        if table not in self.metadata.tables.keys:
            raise ValueError(f'{table} not in the tables of the database')
        return self.execute(self.metadata.tables[table].insert(), values)
