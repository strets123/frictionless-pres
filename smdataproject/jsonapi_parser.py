# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import ijson
from tabulator.parser import Parser
from tabulator import exceptions
from tabulator import helpers


# Module API


class JSONAPIParser(Parser):
    """Parser to parse JSON API data format.
    Note that subclassing the JSONParser was not trivial due to the
    __iter_extended_rows function being private and used outside
    """
    options = [
        'property',
    ]

    def __init__(self, loader, force_parse=False, property=None):
        self.__loader = loader
        self.__property = property
        self.__force_parse = force_parse
        self.__extended_rows = None
        self.__encoding = None
        self.__chars = None

    @property
    def closed(self):
        return self.__chars is None or self.__chars.closed

    def open(self, source, encoding=None):
        self.close()
        self.__chars = self.__loader.load(source, encoding=encoding)
        self.__encoding = getattr(self.__chars, 'encoding', encoding)
        if self.__encoding:
            self.__encoding.lower()
        self.reset()

    def close(self):
        if not self.closed:
            self.__chars.close()

    def reset(self):
        helpers.reset_stream(self.__chars)
        self.__extended_rows = self.__iter_extended_rows()

    @property
    def encoding(self):
        return self.__encoding

    @property
    def extended_rows(self):
        return self.__extended_rows

    def __iter_extended_rows(self):
        """Use a while True loop to paginate the JSON-API API.

        Use the next attribute to keep looping until
        there are no pages left
        """
        start_rownum = 1
        while True:
            path = 'item'
            if self.__property is not None:
                path = '%s.item' % self.__property
            items = ijson.items(self.__chars, path)
            for row_number, item in enumerate(items, start=start_rownum):
                if isinstance(item, dict):
                    yield (row_number, None, [item])
                else:
                    if not self.__force_parse:
                        message = 'JSON item has to be a dict'
                        raise exceptions.SourceError(message)
                    yield (row_number, None, [])
            start_rownum = row_number + start_rownum
            self.__chars.seek(0)
            json_obj = ijson.items(self.__chars,'')
            for k in json_obj:
                next_url = k["links"]["next"]
                break
            if next_url is not None:
                self.__chars = self.__loader.load(next_url, encoding=self.__encoding)
                self.__chars.seek(0)
            else:
                break
