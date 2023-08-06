import unittest
import os

from nure.sync.s3 import S3


class S3TestCase(unittest.TestCase):
    def setUp(self) -> None:
        ttl = 10_800
        self.s3 = S3(
            root_path='tests/data/s3',
            ttl=ttl
        )

    def test_require(self):
        fn = self.s3.require(R's3://zalora.ds-team/LochNess/sku_properties_all.csv')
        self.assertEqual(fn, os.path.join(self.s3.root_path, 'zalora.ds-team/LochNess/sku_properties_all.csv'))

    def test_exist(self):
        self.assertTrue(self.s3.exist(R's3://zalora.ds-team/LochNess/sku_properties_all.csv'))
        self.assertFalse(self.s3.exist(R's3://zalora.ds-team/abc.xyz'))
