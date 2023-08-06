#  Copyright 2023 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from typing import Dict, Optional


class Page:
    def __init__(self, data: Dict):  # noqa
        """Page Constructor.

        Args:
            data (Dict): Page Data
        """
        self.data: dict = data
        self.book: str = data["id"]["book"]
        self.name: str = data["id"]["name"]
        self.comment: str = data["comment"]
        self.start_timestamp: Dict[str, int] = data["started"]  # eg. {'epochSeconds': 0, 'nano': 0}
        self.end_timestamp: Optional[Dict[str, int]] = data["ended"]
        self.updated = data["updated"]
        self.removed = data["removed"]

    def __str__(self):  # noqa
        return str(self.data)

    def __repr__(self):  # noqa
        return self.__str__()


class PageNotFound(Exception):
    def __init__(self, name: str, book: str):
        """Exception for the case when the page was not found in data source.

        Args:
            name: Page Name
            book: Book ID
        """
        self._name = name
        self._book = book

    def __str__(self):
        return f"Unable to find the page with name '{self._name}' in book '{self._book}'."
