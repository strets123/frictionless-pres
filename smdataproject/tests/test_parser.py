import unittest

import tabulator
from .. import parser


class JSONAPIParserTestCase(unittest.TestCase):
    def test_stream(self):
        """
        Given 2 remote pages of a JSON-API resource
        When I parse it with tabulator
        Then I get back a single item list with the full json in it
        """
        url="https://raw.githubusercontent.com/strets123/frictionless-pres/master/data/smdataset%3Fpage%5Bnumber%5D%3D0"
        with tabulator.Stream(
            url,
            format="json-api", 
            custom_parsers={"json-api": parser.JSONAPIParser},
            property='data',
            ) as stream:
            for index, item in enumerate(stream):
                self.assertTrue(isinstance(item[0], dict))
                self.assertIn("attributes", item[0])
                self.assertIn("id", item[0])
                self.assertIn("links", item[0])
                self.assertEqual(len(item), 1)