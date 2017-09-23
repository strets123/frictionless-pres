# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import ijson
import json
from tabulator.parsers.json import JSONParser
from tabulator import exceptions
from tabulator import helpers


# Module API

class JSONAPIParser(JSONParser):
    """Parser to parse JSON data format.
    """

    # Public

    def __iter_extended_rows(self):

        while True:
            path = 'item'
            if self.__property is not None:
                path = '%s.item' % self.__property
            items = ijson.items(self.__chars, path)
            for row_number, item in enumerate(items, start=1):
                if isinstance(item, (tuple, list)):
                    yield (row_number, None, list(item))
                elif isinstance(item, dict):
                    keys = []
                    values = []
                    for key in sorted(item.keys()):
                        keys.append(key)
                        values.append(item[key])
                    yield (row_number, list(keys), list(values))
                else:
                    if not self.__force_parse:
                        message = 'JSON item has to be list or dict'
                        raise exceptions.SourceError(message)
                    yield (row_number, None, [])
            data = json.loads(self.__chars)
            next_url = data["links"]["next"]
            if next_url is not None:
                print(next_url)
                self.open(next_url)
            else:
                break
