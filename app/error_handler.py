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

from app.config import *

class ErrorHandler:
    def __init__(self):
        self.requests = 0
        self.requestErrors = 0
        self.integrityErrors = 0
        self.i = 0

    def __call__(self, req):
        self.requests += 1
        if req.status_code is 200:
            return self.reset()
        else:
            print('ERROR in request:', req.url)
            print('Status code:', req.status_code)
            return self.requestError()

    def requestError(self):
        self.requestErrors += 1
        self.i += 1
        return True

    def integrityError(self):
        self.integrityErrors += 1

    def reset(self):
        self.i = 0
        return False

    def is_throttled(self):
        delay()
        if self.i >= CONSECUTIVE_ERRORS_MAX:
            print('Amount of consecutive errors exceeded', CONSECUTIVE_ERRORS_MAX)
            return True
        else:
            return False

    def result(self):
        return 'Total amount of requests processed: {} \n ' \
               'Total amount of request errors: {} \n ' \
               'Total amount of integrity errors: {}' \
            .format(self.requests, self.requestErrors, self.integrityErrors)
