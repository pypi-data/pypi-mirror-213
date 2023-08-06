import json
import os
import unittest
from datetime import datetime, timedelta

from nure.sync.bigquery import BigQuery
from nure.sync.suffix import ParameterSuffix


class BigQeuryTestCase(unittest.TestCase):
    def setUp(self) -> None:
        ttl = 10_800
        self.venture_code = 'tw'
        meta_fn = 'tests/credentials/bigquery/metadata.json'
        with open(meta_fn) as fd:
            meta = json.load(fd)

        self.dataset_id = meta[self.venture_code]['dataset_id']
        self.db = BigQuery(
            f'tests/credentials/bigquery/{meta[self.venture_code]["project_id"]}.json',
            root_path='tests/data/bigquery',
            suffix_func=ParameterSuffix({
                're_replace': [R'\$\(date\)', R'\$\(venture_code\)'],
            }),
            ttl=ttl)

    def test_require(self):
        date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        fn = self.db.require('tests/sql/interaction.sql', re_replace={
            R'\$\(dataset_id\)': self.dataset_id,
            R'\$\(date\)': date,
            R'\$\(venture_code\)': self.venture_code
        })
        self.assertEqual(fn, os.path.join(self.db.root_path, f'interaction__{date}__{self.venture_code}.csv'))
