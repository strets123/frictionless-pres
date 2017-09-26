import tabulator

tabulator.config.PARSERS["json-api"] = 'normalising_parser.NormalisingJSONAPIParser'
from datapackage_pipelines.lib.stream_remote_resources import *

