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
import plac

from config import build_database_url
from powderbooking.database import DatabaseHandler
from scrapers.forecastScraper import ForecastScraper
from scrapers.weatherScraper import WeatherScraper


def main(api: 'The API to scrape, can be forecast or weather'):
    """
    Scrape either the weather or forecast API and insert the results into the database.
    """
    print('Creating database Handler')
    db = DatabaseHandler(database_url=build_database_url())
    print('Initiating scraping session for api', api)
    if api == 'forecast':
        ForecastScraper(db=db).scrape()
    elif api == 'weather':
        WeatherScraper(db=db).scrape()
    else:
        print('Invalid input for api, aborting..')
        exit(1)


if __name__ == '__main__':
    plac.call(main)
