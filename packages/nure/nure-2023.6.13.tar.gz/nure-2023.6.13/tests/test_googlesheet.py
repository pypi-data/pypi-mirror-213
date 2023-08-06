import os
import unittest

from nure.sync.googlesheet import GoogleSheet


class GoogleSheetTestCase(unittest.TestCase):
    def setUp(self) -> None:
        ttl = 10_800
        self.googlesheet = GoogleSheet(
            'tests/credentials/googlesheet_key.pickle',
            'tests/credentials/googlesheet_secret.json',
            root_path='tests/data/googlesheet',
            ttl=ttl)

    def test_require(self):
        key = {
            'spreadsheet_id': '1CjuMlcz2LT6FkxV21zXyITRfBFblSGVqEIB0_3mZX3E',
            'range': 'subcats_exclude!A2:C'
        }

        fn = self.googlesheet.require(key, header=['country', 'segment', 'sub_cat_type'])
        self.assertEqual(fn, os.path.join(self.googlesheet.root_path, key['spreadsheet_id'], f'{key["range"].split("!")[0]}.csv'))
