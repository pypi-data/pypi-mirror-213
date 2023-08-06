import unittest
import os

from nure.sync.postgre import PostgreSql
from nure.sync.suffix import ParameterSuffix


class PostgreTestCase(unittest.TestCase):
    def setUp(self) -> None:
        ttl = 10_800
        self.venture_code = 'tw'
        self.db = PostgreSql(
            'tests/credentials/pitbull.json',
            root_path='tests/data/postgre',
            suffix_func=ParameterSuffix({
                'sa_replace': ['venture_code']
            }), ttl=ttl)

    def test_require(self):
        fn = self.db.require('tests/sql/catalogue.sql', sa_replace={'venture_code': self.venture_code})
        self.assertEqual(fn, os.path.join(self.db.root_path, f'catalogue__{self.venture_code}.csv'))
