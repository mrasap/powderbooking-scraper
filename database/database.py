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
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine

from config import build_database_url
from database.models import model_resort, model_weather, model_forecast


def _build_postgres_engine(database_url: str = build_database_url()) -> Engine:
    return create_engine(database_url)


def build_postgres_database(engine=_build_postgres_engine()) -> (Engine, MetaData):
    metadata = MetaData()

    model_resort(metadata)
    model_weather(metadata)
    model_forecast(metadata)

    metadata.create_all(engine)

    return engine, metadata
