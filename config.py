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
import os


# The _delay between two API calls (in seconds)
DELAY_MIN = 0.4
DELAY_MAX = 1.0

# After how many API calls we will insert into the database
QUEUE_MAX = 20

# How many loops we will try out before giving up on google API
ITER_MAX = 5

# The amount of consecutive errors after the function is terminated
# Probably because we have throttled the API
CONSECUTIVE_ERRORS_MAX = 20


def build_weatherunlocked_base_url(localweathertype: str = 'forecast') -> str:
    """
    Build the base url for a weatherunlocked current_request.
    Credentials are built from environmental variables.

    :param localweathertype: 'forecast' or 'current'
    :return: base url string that needs lat and lng params inserted
    """
    app_id = os.environ.get('WEATHERUNLOCKED_APP_ID')
    app_key = os.environ.get('WEATHERUNLOCKED_APP_KEY')
    return f'http://api.weatherunlocked.com/api/{localweathertype}/{{lat}},{{lng}}?app_id={app_id}&app_key={app_key}'


def build_openweathermap_base_url() -> str:
    """
    Build the base url for an openweathermap current_request.
    Credentials are built from environmental variables.

    :return: base url string that needs lat and lng params inserted
    """
    app_id = os.environ.get('OPENWEATHERMAP_APP_ID')
    return f'https://api.openweathermap.org/data/2.5/weather?lat={{lat}}&lon={{lng}}&appid={app_id}&units=metric'


def build_database_url() -> str:
    """
    Build the database url.
    Credentials are built from environmental variables.

    :return: the database url
    """
    username = os.environ.get('POSTGRES_USERNAME', 'postgres')
    password = os.environ.get('POSTGRES_PASSWORD', 'password')
    host = os.environ.get('POSTGRES_HOST', 'localhost')
    port = os.environ.get('POSTGRES_PORT', '8001')
    database = os.environ.get('POSTGRES_DB', 'powderbooking')
    return f'postgresql://{username}:{password}@{host}:{port}/{database}'
