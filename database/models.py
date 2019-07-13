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
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.engine import Engine

from config import generate_database_url


def build_postgres_engine() -> Engine:
    return create_engine(generate_database_url())


def setup_postgres_database(engine: Engine = build_postgres_engine()) -> None:
    metadata = MetaData()

    Table('users', metadata,
          Column('id', Integer, primary_key=True),
          Column('name', String),
          Column('fullname', String),
          )

    Table('addresses', metadata,
          Column('id', Integer, primary_key=True),
          Column('user_id', None, ForeignKey('users.id')),
          Column('email_address', String, nullable=False)
          )

    metadata.create_all(engine)
