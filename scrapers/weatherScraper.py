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
from datetime import datetime

from math import floor
from typing import List

from sqlalchemy.engine import ResultProxy

from config import build_openweathermap_base_url
from powderbooking.query import Query
from scrapers.scraper import Scraper
from scrapers.utils import get_nested


class WeatherScraper(Scraper):
    @property
    def _url_base(self) -> str:
        return build_openweathermap_base_url()

    @property
    def _table_to_insert_into(self) -> List[str]:
        return ['weather']

    @property
    def _select_from_database(self) -> ResultProxy:
        # TODO: use a generator with fetchmany instead of fetchall to reduce memory load
        return self.db.execute_query(Query.select_weather_3h).fetchall()

    def _parse_request(self) -> None:
        req = self.current_request.json()

        dt = datetime.fromtimestamp(req['dt']) if 'dt' in req else datetime.now()

        record = {'date_request': datetime.now(),
                  'dt': dt,
                  'date': dt.date(),
                  'timepoint': floor(dt.hour / 3) if 'dt' in req else -1,
                  'temperature_c': get_nested(req, 'main.temp'),
                  'wind_speed_kmh': get_nested(req, 'wind.speed'),
                  'wind_direction_deg': get_nested(req, 'wind.deg'),
                  'visibility_km': get_nested(req, 'visibility'),
                  'clouds_pct': get_nested(req, 'clouds.all'),
                  'snow_3h_mm': get_nested(req, 'snow.3h'),
                  'rain_3h_mm': get_nested(req, 'rain.3h'),
                  'resort_id': self.current_id
                  }

        self.results[0].append(record)
