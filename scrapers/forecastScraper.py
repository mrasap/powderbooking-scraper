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
from sqlalchemy.engine import ResultProxy

from config import build_weatherunlocked_base_url
from database.queries import Queries
from scrapers.scraper import Scraper


class ForecastScraper(Scraper):
    @property
    def _url_base(self) -> str:
        return build_weatherunlocked_base_url()

    @property
    def _table_to_insert_into(self) -> str:
        return 'forecast'

    @property
    def _select_from_database(self) -> ResultProxy:
        # TODO: use a generator with fetchmany instead of fetchall to reduce memory load
        return self.db.execute(Queries.select_forecast_24h).fetchall()

    def _parse_request(self) -> None:
        req = self.current_request.json()

        # I am calculating the aggregate data here because it will be requested often
        # So I don't have to do an expensive query every time somebody requests the data
        snow_week = rain_week = 0
        for day in req['Days']:
            snow_week += day['snow_total_mm']
            rain_week += day['rain_total_mm']

        for day_number, day in enumerate(req['Days'], start=0):
            date_weatherunlocked = datetime.strptime(day['date'], "%d/%m/%Y")

            self.result += {'date_request': datetime.now(),
                            'date': date_weatherunlocked,
                            'timepoint': day_number,
                            'temperature_max_c': day['temp_max_c'],
                            'temperature_min_c': day['temp_min_c'],
                            'rain_total_mm': day['rain_total_mm'],
                            'rain_week_mm': rain_week,
                            'snow_total_mm': day['snow_total_mm'],
                            'snow_week_mm': snow_week,
                            'prob_precip_pct': day['prob_precip_pct'],
                            'wind_speed_max_kmh': day['windspd_max_kmh'],
                            'windgst_max_kmh': day['windgst_max_kmh'],
                            'resort_id': self.current_id
                            }
