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


def request_weather_forecast_weatherunlocked():
    """ Get all the resorts from db and request the data from weatherunlocked """
    print('Starting API requests for the weather forecast')

    # Arrange all the params
    sql_insert = "INSERT INTO pwdr_weatherforecast (" \
          "date_request, date, timepoint, temperature_max_c, temperature_min_c, " \
          "rain_total_mm, rain_week_mm, snow_total_mm, snow_week_mm, prob_precip_pct, " \
          "wind_speed_max_kmh, windgst_max_kmh, resort_id) " \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql_select = "SELECT pr.id, lat, lng " \
             "FROM pwdr_skiresort as pr " \
             "LEFT JOIN (" \
             "SELECT id, resort_id " \
             "FROM pwdr_weatherforecast " \
             "WHERE date = current_date " \
             "and timepoint = 0" \
             ") as pw on pr.id = pw.resort_id " \
             "WHERE pw.id is NULL"

    url_base = 'http://api.weatherunlocked.com/api/{localweathertype}/{lat},{lng}?app_id={app_id}&app_key={app_key}'
    url_args = config(section='weatherunlocked')
    url_args['localweathertype'] = 'forecast'

    def req_handler_func(queue, req, _id):
        # I am calculating the aggregate data here because it will be requested often
        # So I don't have to do an expensive query every time somebody requests the data
        snow_week = rain_week = 0
        for day in req['Days']:
            snow_week += day['snow_total_mm']
            rain_week += day['rain_total_mm']

        for j, day in enumerate(req['Days'], start=0):
            date_weatherunlocked = datetime.strptime(day['date'], "%d/%m/%Y")
            data = [
                datetime.now(),
                date_weatherunlocked,
                j,
                day['temp_max_c'],
                day['temp_min_c'],
                day['rain_total_mm'],
                rain_week,
                day['snow_total_mm'],
                snow_week,
                day['prob_precip_pct'],
                day['windspd_max_kmh'],
                day['windgst_max_kmh'],
                _id
            ]
            queue.put(data)

    # Start the requests
    request_weather_apis(sql_insert, sql_select, url_base, url_args, req_handler_func)
    print('Finished API requests for the weather forecast')