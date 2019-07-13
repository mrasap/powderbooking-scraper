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


# The delay between two API calls (in seconds)
DELAY_MIN = 0.4
DELAY_MAX = 1.0

# After how many API calls we will insert into the database
QUEUE_MAX = 20

# How many loops we will try out before giving up on google API
ITER_MAX = 5

# The amount of consecutive errors after the function is terminated
# Probably because we have throttled the API
CONSECUTIVE_ERRORS_MAX = 20
