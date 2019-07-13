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


def request_weather_current_openweathermap():
    """ Get all the resorts from db and request the data from openweathermap """
    print('Starting API requests for the current weather')

    sql_insert = "INSERT INTO pwdr_weathercurrentopen (" \
                 "date_request, dt, date, timepoint, temperature_c, " \
                 "wind_speed_kmh, wind_direction_deg, visibility_km, clouds_pct, " \
                 "snow_3h_mm, rain_3h_mm, resort_id) " \
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql_select = "SELECT pr.id, lat, lng " \
                 "FROM pwdr_skiresort as pr " \
                 "LEFT JOIN (" \
                 "SELECT id, resort_id " \
                 "FROM pwdr_weathercurrentopen " \
                 "WHERE date_request > current_timestamp - 3 * interval '1 hour'" \
                 ") as pw on pr.id = pw.resort_id " \
                 "WHERE pw.id is NULL"
    url_base = 'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={appid}&units=metric'
    url_args = config(section='openweathermap')

    def req_handler_func(queue, req, _id):
        dt = datetime.fromtimestamp(req['dt']) if 'dt' in req else datetime.now()
        data = [
            datetime.now(),
            dt,
            dt.date(),
            floor(dt.hour / 3) if 'dt' in req else -1,
            req['main']['temp'] if 'main' in req and 'temp' in req['main'] else None,
            req['wind']['speed'] if 'wind' in req and 'speed' in req['wind'] else None,
            req['wind']['deg'] if 'wind' in req and 'deg' in req['wind'] else None,
            req['visibility'] if 'visibility' in req else None,
            req['clouds']['all'] if 'clouds' in req and 'all' in req['clouds'] else None,
            req['snow']['3h'] if 'snow' in req and '3h' in req['rain'] else None,
            req['rain']['3h'] if 'rain' in req and '3h' in req['rain'] else None,
            _id
        ]
        queue.put(data)

    request_weather_apis(sql_insert, sql_select, url_base, url_args, req_handler_func)
    print('finished API requests for the current weather')

