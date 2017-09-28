import tabulator
from tabulator.loaders.remote import _WebStream

_WebStream.HEADERS["Accept"] = "application/json"
tabulator.config.PARSERS["json-api"] = 'normalising_parser.NormalisingJSONAPIParser'
from datapackage_pipelines.lib.stream_remote_resources import *

