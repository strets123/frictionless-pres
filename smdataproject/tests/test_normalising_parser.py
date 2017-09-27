import sys
sys.path.append("..")

import unittest

import tabulator
from smdataproject import normalising_parser


class JSONAPIParserTestCase(unittest.TestCase):
    def test_stream(self):
        """
        Given 2 remote pages of a JSON-API resource
        When I parse it with tabulator
        Then I get back a single item list with the full json in it
        """
        url = "https://raw.githubusercontent.com/strets123/" \
              "frictionless-pres/master/data/smdataset%3Fpage" \
              "%5Bnumber%5D%3D0"
        with tabulator.Stream(
            url,
            format="json-api", 
            custom_parsers={"json-api": normalising_parser.NormalisingJSONAPIParser},
            property='data',
                ) as stream:
            for index, item in enumerate(stream):
                self.assertTrue(isinstance(item[0], dict))
                self.assertIn("attributes", item[0])
                self.assertIn("id", item[0])
                self.assertIn("links", item[0])
                self.assertEqual(len(item), 1)

    def test_stream_ijson_parser(self):
        """
        Given I pass in a schema of fields with their corresponding ijson prefixes
        When I call tabulator.Stream
        Then I can parse a remote dataset directly to the json format of my choice
        """
        url = "https://raw.githubusercontent.com/strets123/" \
            "frictionless-pres/master/data/smdataset%3F" \
            "page%5Bnumber%5D%3D0"
        schema_with_ijson = {
            "fields": [
                {"name": "id", "ijson_path": "data.item.attributes.identifier.item.value"},
                {"name": "name", "ijson_path": "data.item.attributes.title.item.value"},
                {"name": "earliest_date", "ijson_path":
                    "data.item.attributes.lifecycle.creation.item.date.item.earliest"},
                {"name": "latest_date", "ijson_path": "data.item.attributes.lifecycle.creation.item.date.item.latest"},
                {"name": "description", "ijson_path": "data.item.attributes.description.item.value"},
                {"name": "large_image_link", "ijson_path":
                    "data.item.attributes.multimedia.item.processed.large.location"},
                {"name": "large_thumbnail_link", "ijson_path":
                    "data.item.attributes.multimedia.item.processed.large_thumbnail.location"},
                {"name": "small_thumbnail_link", "ijson_path":
                    "data.item.attributes.multimedia.item.processed.small_thumbnail.location"},
                {"name": "makers", "ijson_path": "data.item.attributes.lifecycle.creation.item.maker.item.summary_title"},
                {"name": "maker_types", "ijson_path":
                    "data.item.attributes.lifecycle.creation.item.maker.item.@link.role.item.value"},

            ]
            }

        with tabulator.Stream(
            url,
            format="json-api", 
            custom_parsers={"json-api": normalising_parser.NormalisingJSONAPIParser},
            property='data',
            jsonpath_schema=schema_with_ijson,
                ) as stream:
            items = list(stream)
            self.assertEqual(
                items,
                [['1975-8386',
                  'Penarth, South Wales and other Picturesque '
                  'Resorts on  the Bristol Channel via the Taff Vale  Railway',
                  1914, 1914,
                  "Poster,  'Penarth, South Wales and other Picturesque"
                  " resorts on the Bristol Channel via the Taff Vale"
                  " Railway' and Bristol  Channel passenger service"
                  " and Edwards, Robertsons & Co.'s Saloon Steamers,"
                  " Lorna Doone, Bonnie Doone etc. About 1914."
                  "  Printed by Hudson & Kearns Limited. Published by Taff Vale Railway. Format, Quad  Royal.",
                  'I/2/2/large_DS100797.jpg',
                  'https://smgco-images.s3.amazonaws.com/media/I/2/2/large_thumbnail_DS100797.jpg',
                  'I/2/2/small_thumbnail_DS100797.jpg', 'Taff  Vale  Railway|Hudson  & Kearns  Limited',
                  'publisher|maker'],
                 ['1978-9721', 'BR  poster', '', '',
                  "BR poster. Inter-City 125. It's the  Changing "
                  "Shape of Rail - London to Bristol, Cardiff "
                  "and Swansea, 1976",
                  'I/2/2/large_DS091288.jpg',
                  'https://smgco-images.s3.amazonaws.com'
                  '/media/I/2/2/large_thumbnail_DS091288.jpg',
                  'I/2/2/small_thumbnail_DS091288.jpg', '', ''],
                 ['1991-7266', 'BR(WR&SR) notice', '', '',
                  'BR(WR&SR) notice. Consent to Withdrawal of Railway'
                  ' Passenger Services between Bristol Temple Meads '
                  'and Bournemouth West and between Highbridge and'
                  ' Evercreech Junction. Printed by Taylor & Sons,'
                  ' Minety, Wilts. 1010 x 640mm.',
                  'I/2/2/large_DS130092.jpg',
                  'https://smgco-images.s3.amazonaws.com/media'
                  '/I/2/2/large_thumbnail_DS130092.jpg',
                  'I/2/2/small_thumbnail_DS130092.jpg', '', ''],
                 ['1991-7265', 'BR(WR&SR) notice', '', '',
                  'BR(WR&SR) notice. Proposed Withdrawal of Railway'
                  ' Passenger Services between Bristol Temple Meads,'
                  ' Bath Green Park and Broadstone, also between '
                  'Highbridge and Evercreech Junction, from '
                  '30 September 1963. Printed by Waterlow & Sons '
                  'Ltd, London & Dunstable. 1010 x 640mm.',
                  'I/2/2/large_DS130093.jpg',
                  'https://smgco-images.s3.amazonaws.com/media'
                  '/I/2/2/large_thumbnail_DS130093.jpg',
                  'I/2/2/small_thumbnail_DS130093.jpg',
                  'Waterlow and Sons Limited', 'printer']]
                )
