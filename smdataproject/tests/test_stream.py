
import unittest

import tabulator
from .. import parser

class StreamParserTestCase(unittest.TestCase):
    def test_stream(self):
        url="https://raw.githubusercontent.com/strets123/frictionless-pres/master/data/smdataset%3Fpage%5Bnumber%5D%3D0"
        with tabulator.Stream(
            url,
            format="json-api", 
            custom_parsers={"json-api": parser.JSONAPIParser}) as stream:
            for item in stream:
            	print(item)


