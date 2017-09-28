# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import time
import ijson
from tabulator.parser import Parser
from tabulator import exceptions
from tabulator import helpers


# Module API


class NormalisingJSONAPIParser(Parser):
    """Parser to parse JSON API data format.
    Note that subclassing the JSONParser was not trivial due to the
    __iter_extended_rows function being private and used outside
    """

    options = [
        'property',
        'jsonpath_schema',
    ]

    def __init__(self, loader, force_parse=False, property=None, flatten_delimiter=None, jsonpath_schema=None):
        self.__loader = loader
        self.__property = property
        self.__force_parse = force_parse
        self.__extended_rows = None
        self.__encoding = None
        self.__chars = None
        self.__jsonpath_schema = jsonpath_schema
        self.__next_url = None

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

    def ijson_path_parse(self, start_rownum, path):
        data = ijson.parse(self.__chars)
        dtypes = ('boolean', 'number', 'string', 'null')
        column_names = [f["name"] for f in self.__jsonpath_schema["fields"]]
        pick_fields = tuple([f["ijson_path"] for f in self.__jsonpath_schema["fields"]])
        current_value = None
        for prefix, event, value in data:

            if prefix == "links.next":
                if event in ('null', 'string'):
                    self.__next_url = value
            if (prefix, event) == (path, 'start_map'):
                current_value = ["" for i in range(len(self.__jsonpath_schema["fields"]))]
            if (prefix, event) == (path, 'end_map'):
                start_rownum += 1
                yield start_rownum, column_names, current_value
            if current_value and event in dtypes:
                try:
                    ind = pick_fields.index(prefix)
                    if not current_value[ind]:
                        # handle lists by turning them to multivalue fields
                        current_value[ind] = value
                    else:
                        current_value[ind] = "{}|{}".format(current_value[ind], value)
                except ValueError:
                    pass

    def standard_parse(self, start_rownum, path):
        items = ijson.items(self.__chars, path)
        for row_number, item in enumerate(
            items, 
            start=start_rownum
            ):
            if isinstance(item, dict):
                
                yield (row_number, None, [item])
            else:
                if not self.__force_parse:
                    message = 'JSON item has to be a dict'
                    raise exceptions.SourceError(message)
                yield (row_number, None, [])

    def __iter_extended_rows(self):
        start_rownum = 1
        while True:
            if self.__property is not None:
                path = '%s.item' % self.__property
            else:
                raise Exception("Must set a list property in the json")
            if self.__jsonpath_schema is None:
                rows = self.standard_parse(start_rownum, path)
                
            else:
                rows = self.ijson_path_parse(start_rownum, path)

            for row in rows:
                start_rownum += 1
                yield row

            if self.__jsonpath_schema is None:
                # we have to parse it all to get the next out
                self.__chars.seek(0)
                json_obj = ijson.items(self.__chars,'')
                for k in json_obj:
                    self.__next_url = k["links"]["next"]
                    break
            if self.__next_url is not None:
                time.sleep(5)
                self.__chars = self.__loader.load(self.__next_url , encoding=self.__encoding)
                self.__chars.seek(0)
            else:
                break
