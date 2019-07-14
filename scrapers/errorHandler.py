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
from requests import Response

from config import *


class ErrorHandler:
    """
    This class is used as a base to handle all the errors during the scraping process.
    It is split from the scraper to split code into separate modules with their own responsibilities.

    The main responsibility of this class is to verify that we aren't being throttled.
    If we are, we should stop requesting to not overload the API that we are scraping.
    """
    requests_total: int
    requests_errors_total: int
    requests_errors_streak: int
    database_errors: int
    current_request: Response

    def __init__(self):
        self.requests_total = 0
        self.requests_errors_total = 0
        self.requests_errors_streak = 0
        self.database_errors = 0

    def check_request_error(self) -> bool:
        """
        Check if there is an error in the request.

        :return: true if there is an error, false otherwise
        """
        self.requests_total += 1
        if self.current_request.status_code is 200:
            self.reset_error_streak()
            return False
        else:
            self.handle_request_error()
            return True

    def handle_request_error(self) -> None:
        """
        Handle the error that was present in the request.
        """
        print('Error in current_request:', self.current_request.url)
        print('Status code:', self.current_request.status_code)
        self.requests_errors_total += 1
        self.requests_errors_streak += 1

    def handle_database_error(self) -> None:
        """
        Handle the error that was present in the database.
        """
        self.database_errors += 1

    def reset_error_streak(self) -> None:
        """
        If there was no error in the request, the streak is resolved and should be reset.
        """
        self.requests_errors_streak = 0

    def is_throttled(self) -> bool:
        """
        Check if the API is throttling us.

        :return: true if we have a large error streak, false otherwise
        """
        if self.requests_errors_streak >= CONSECUTIVE_ERRORS_MAX:
            print('Amount of consecutive errors exceeded', CONSECUTIVE_ERRORS_MAX)
            return True
        else:
            return False

    def result(self) -> str:
        """
        Return an overview of the results of the scraping process.
        """
        return f"""Total amount of requests processed: {self.requests_total}
               Total amount of requests errors: {self.requests_errors_total}
               Total amount of database errors: {self.database_errors}
               """
